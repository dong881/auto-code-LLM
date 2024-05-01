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
    stdout, stderr = utils.execute_python_script(FP)
    print(stdout)
    if stderr:
        if DEBUG: print(stderr)
        git_utils.git_reset_hard()
        return False
    return True

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
                utils.modify_file(FP, response)
                if not execute_code():
                    continue
                print("Successfully executed the auto LLM script in times.")
                newMSG.append({"role": "user", "content": utils.read_file(FP) + "\nimpove current code, and  Only give me the fully source code without any symbol, and don't give any other text. I need to execute right now."})
                msg = git_utils.git_diff()
                msg += "Organize into a simple and clear bulleted list with titles: git push commit text"
                commit_and_push_changes(msg)

        except Exception as e:
            print(e)
            newMSG = utils.RESET_ALL(topic_description)
            git_utils.git_reset_hard()


if __name__ == "__main__":
    main("""
    Sure! Here's a detailed description of the rules and gameplay for a Python Snake game, along with some features that could enhance the user experience:

### Rules:
1. **Objective**: The player controls a snake that moves around the screen, eating food pellets to grow larger. The goal is to eat as much food as possible without colliding with the snake's own body or the walls of the game area.
  
2. **Controls**: The player can control the direction of the snake using arrow keys (up, down, left, right) or WASD keys.

3. **Game Over Conditions**:
   - If the snake collides with its own body, the game ends.
   - If the snake collides with the wall, the game ends.
   - The game can also end after a certain time limit or after the player reaches a specific score.

4. **Scoring**: Each time the snake eats a food pellet, the player earns points. The longer the snake grows, the more points are earned per food pellet.

### Gameplay Features:
1. **Random Food Generation**: Food pellets should appear at random locations on the screen after the snake eats the previous one.

2. **Increasing Difficulty**: As the game progresses, the snake's speed should increase, making it more challenging for the player to control.

3. **Power-Ups**: Introduce special food items that grant temporary bonuses such as increased speed, longer snake length, or invincibility.

4. **Obstacles**: Include obstacles or barriers on the game board that the snake must navigate around, adding an additional layer of challenge.

5. **High Score Tracking**: Keep track of the player's highest score across multiple game sessions and display it on the game screen.

6. **Customization Options**: Allow players to customize aspects of the game such as the snake's appearance, the background theme, or the difficulty level.

7. **Sound Effects and Music**: Incorporate sound effects for actions like eating food, collision, and background music to enhance the gaming experience.

8. **Pause and Resume Functionality**: Implement a pause feature that allows players to temporarily halt the game and resume later without losing progress.

9. **Game Over Screen**: Display a game over screen with the player's final score and options to restart the game or return to the main menu.

### User Interface:
1. **Graphics**: Design visually appealing graphics for the snake, food pellets, obstacles, and game background.
  
2. **Responsive Controls**: Ensure that the controls are smooth and responsive, providing a seamless experience for the player.

3. **UI Elements**: Include informative UI elements such as score display, remaining lives (if applicable), and any active power-ups.

4. **Animations**: Incorporate animations for actions like snake movement, food consumption, and collision effects to make the game more engaging.

5. **Menu System**: Create an intuitive menu system with options for starting the game, adjusting settings, viewing high scores, and exiting the game.

By implementing these rules, gameplay features, and user interface elements, you can create a captivating and enjoyable Python Snake game with a rich user experience.
    """)
