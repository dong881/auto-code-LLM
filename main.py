import re
import utils
import git_utils
import ollama
import json

FP = "./target_file.py"
DEBUG = True

def install_packages(response):
    if "pip install" in response:
        package_name_match = re.search(r'pip install\s+(\S+)', response)
        if package_name_match:
            package_name = package_name_match.group(1)
            stdout, stderr = utils.pip_install(package_name)
            if not stderr:
                print(f"Package {package_name} installed successfully.")
            else:
                print(f"Error occurred while installing package: {stderr}")

def execute_code():
    try:
        stdout, stderr = utils.execute_python_script(FP, timeout=60)  # Set timeout to 60 seconds
        print(stdout)
        if stderr:
            if DEBUG:   print(stderr)
            git_utils.git_reset_hard()
            return False
        return True
    except TimeoutError as e:
        print(f"Error: {e}")
        return False

def commit_and_push_changes(msg):
    response = ollama.chat(model='llama3:latest', messages=[{"role": "user", "content": msg}])
    print(git_utils.git_commit_and_push(response['message']['content']))

def main(topicInput):
    topic_description = utils.read_file(FP) + "\n\n" + topicInput
    topic_description += ", Only give me the fully source code without any symbol, and don't give any other text. I need to execute right now."
    newMSG = utils.RESET_ALL(topic_description)
    if DEBUG: print(newMSG)
    if DEBUG: print(topic_description)
    
    max_msg_size = 15000
    while True:
        try:
            if DEBUG: print(len(json.dumps(newMSG)))
            if len(json.dumps(newMSG)) > max_msg_size:
                newMSG.append({"role": "user", "content": "Please consolidate the current progress, including identified issues, potential improvements, and areas for enhancement."})
                response = ollama.chat(model='llama3:latest', messages=newMSG)
                new_prompt = response['message']['content']
                print(new_prompt)
                newMSG = [{"role": "user", "content": new_prompt}]
            
            stream = ollama.chat(model='llama3:latest', messages=newMSG, stream=True)

            response = ""
            for chunk in stream:
                response += chunk['message']['content']

            response_list = utils.extract_code_blocks(response)
            if not response_list:
                print("Warning: No code blocks found in the response.")
            for response in response_list:
                install_packages(response)
                newMSG.append({"role": "assistant", "content": response})
                if not utils.modify_file(FP, response):
                    newMSG = utils.RESET_ALL(topic_description)
                    newMSG.append({"role": "user", "content": response + "\nOnly give me the fully code without any symbol. I need to execute right now."})
                    continue
                if not execute_code():
                    continue
                print("Successfully executed the auto LLM script in times.")
                newMSG.append({"role": "user", "content": utils.read_file(FP) + "\nimpove current code, and  Only give me the fully source code without any symbol, and don't give any other text. I need to execute right now."})
                msg = git_utils.git_diff()
                msg += "Organize into a simple and clear bulleted list with titles: git commit text"
                commit_and_push_changes(msg)

        except Exception as e:
            print(e)
            newMSG = utils.RESET_ALL(topic_description)
            git_utils.git_reset_hard()


if __name__ == "__main__":
    main("""
Certainly! Here's a condensed and precise guide on how to write code for a Python Snake game, broken down into step-by-step instructions along with the necessary basic functions to implement. Additionally, I'll suggest some creative extra features to enhance the game. 

**Step-by-Step Guide:**

1. **Setup the Game Environment:**
   - Set up the game window and screen dimensions.
   - Import necessary libraries (e.g., pygame for graphics).
   - Define constants such as the size of the snake, speed, and screen dimensions.

2. **Create the Snake:**
   - Define a Snake class with attributes like position, length, and direction.
   - Implement functions for snake movement, growth, and collision detection.

3. **Generate Food:**
   - Create a function to generate random food pellets on the screen.
   - Ensure that food does not appear on the snake's body.

4. **Handle User Input:**
   - Capture user input for controlling the snake's direction (arrow keys or WASD).

5. **Game Loop:**
   - Set up the main game loop to continuously update the game state.
   - Update snake position, check for collisions, and handle user input within the loop.

6. **Scoring:**
   - Keep track of the player's score based on the number of food pellets eaten.
   - Update the score display accordingly.

7. **Game Over Conditions:**
   - Implement conditions for game over such as snake collision with itself or the walls.
   - Display a game over screen with the final score.

8. **Additional Features:**
   - **Increasing Difficulty:** Gradually increase the snake's speed as the game progresses.
   - **Power-Ups:** Add special food items granting temporary bonuses.
   - **Obstacles:** Introduce obstacles or barriers on the game board.
   - **High Score Tracking:** Store and display the player's highest score across sessions.
   - **Customization Options:** Allow players to customize the game's appearance and difficulty.
   - **Sound Effects and Music:** Include sound effects and background music for a more immersive experience.
   - **Pause and Resume Functionality:** Allow players to pause and resume the game at any time.
   - **Animations:** Add animations for snake movement, food consumption, and collision effects.

**Basic Functions to Implement:**

1. `initialize_game()`
2. `create_snake()`
3. `move_snake()`
4. `generate_food()`
5. `handle_input()`
6. `update_score()`
7. `check_collisions()`
8. `game_over()`

By following these steps and implementing the suggested functions, along with the additional features, you can create a comprehensive Python Snake game with a rich user experience.
please let snake  move automaticly continuously, and display apple.when snake eats apple, it will extand its body length. 
""")
