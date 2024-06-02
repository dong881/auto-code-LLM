import re
import utils
import git_utils
import ollama
import json

FP = "./target_file.py"
DEBUG = True
success_time = 0

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
    global success_time
    try:
        stdout, stderr = utils.execute_python_script(FP, timeout=60)  # Set timeout to 60 seconds
        print(stdout)
        if stderr:
            if DEBUG:   print(stderr)
            descript = stderr + "\nhow to fix?"
            newMSG = RESET_MSG(descript)
            if success_time>0: git_utils.git_reset_hard()
            return False
        return True
    except TimeoutError as e:
        print(f"Error: {e}")
        return False

def commit_and_push_changes(msg):
    response = ollama.chat(model='llama3:latest', messages=[{"role": "user", "content": msg}])
    print(git_utils.git_commit_and_push(response['message']['content']))

def RESET_MSG(msg):
    topic_description = utils.read_file(FP) + "\n\n" + msg
    return utils.RESET_ALL(topic_description)

def main(topicInput):
    global success_time
    topic_description = topicInput
    topic_description += ", Only give me the fully source code without any symbol, and don't give any other text. I need full source code to execute right now."
    newMSG = RESET_MSG(topic_description)
    if DEBUG: print(newMSG)
    if DEBUG: print(topic_description)
    
    MAX_MSG_SIZE = 15000
    while True:
        try:
            if DEBUG: print(len(json.dumps(newMSG)))

            if len(json.dumps(newMSG)) > MAX_MSG_SIZE:
                newMSG.append({"role": "user", "content": "Please consolidate the current progress, including identified issues, potential improvements, and areas for enhancement."})
                response = ollama.chat(model='llama3:latest', messages=newMSG)
                new_prompt = response['message']['content']
                print(new_prompt)
                newMSG = [{"role": "user", "content": new_prompt}]
            output = ollama.chat(model='llama3:latest', messages=newMSG)
            response = output['message']['content']
            print(response)
            response_list = utils.extract_code_blocks(response)
            if not response_list:
                print("Warning: No code blocks found in the response.")
            for res in response_list:
                install_packages(res)
                if DEBUG: print(res)
                if not utils.modify_file(FP, res):
                    newMSG = utils.RESET_ALL(topic_description)
                    newMSG.append({"role": "user", "content": response + "\nOnly give me the fully code without any symbol. I need to execute right now."})
                    continue
                newMSG.append({"role": "assistant", "content": res})
                if not execute_code():
                    if DEBUG: print("execute_code error")
                    continue
                print("Successfully executed the auto LLM script, then continue to improve the code")
                # if success_time > 5: return True
                success_time += 1
                newMSG = RESET_MSG("impove current code, and  Only give me the fully source code without any symbol, and don't give any other text. I need to execute right now.")
                msg = git_utils.git_diff()
                msg += "Organize into a simple and clear bulleted list with titles: git commit text"
                commit_and_push_changes(msg)

        except Exception as e:
            print(e)
            newMSG = utils.RESET_ALL(topic_description)
            git_utils.git_reset_hard()


if __name__ == "__main__":
    main("""
Provide a comprehensive, step-by-step guide along with all the essential functions needed to implement a code for the classic game of Tetris. This guide should cover everything from creating the game grid, handling the falling pieces, detecting collisions, rotating pieces, clearing completed lines, scoring, and any other necessary functions to fully implement the game.
    """)

# if __name__ == "__main__":
#     main("""
# Create a precise step-by-step guide for writing code that generates a 4x4 integer 2D array (matrix) where the sum of each row, each column, and both diagonals equals 33. Include the necessary basic functions required to implement this code.   
# """)
