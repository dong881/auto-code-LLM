FP = "./target_file.py"
# execute_times = 10
DEBUG = False
# topic_description = "query the current time and print it out."
topic_description = "write a greedy snake game, and make sure it can run and play."

topic_description += ", Only give me the fully source code without any symbol, and don't give any other text. I need to execute right now."
if DEBUG: print(topic_description)

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error occurred while reading file '{file_path}': {e}")
        return None


def modify_file(file_path, modified_content):
    try:
        with open(file_path, 'w') as file:
            file.write(modified_content)
        # print(f"File '{file_path}' modified successfully.")
    except Exception as e:
        print(f"Error occurred while modifying file '{file_path}': {e}")


import subprocess

def execute_python_script(script_path):
    try:
        process = subprocess.Popen(['python3', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        return stdout, stderr
        
    except Exception as e:
        print(f"Error occurred while executing the script: {e}")
        return None, None

def pip_install(package):
    try:
        process = subprocess.Popen(['pip', 'install', package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()
        return stdout, stderr
    except Exception as e:
        print(f"Error occurred while installing package '{package}': {e}")
        return None, None

def extract_code_blocks(text):
    code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks.append(text)
    return code_blocks


import git_utils

def RESET_ALL():
    newMSG_content = ""
    with open("system_message.txt", "r") as file:
        newMSG_content = file.read()
    newMSG = eval(newMSG_content)
    newMSG[-1]["content"] += topic_description
    return newMSG

newMSG = RESET_ALL()
import os
import ollama
import re

print(newMSG)
while True:
    try:
        stream = ollama.chat(
            model='llama3:latest',
            messages=newMSG,
            stream=True,
        )

        response = ""
        for chunk in stream:
            response += chunk['message']['content']
        
        response_list = extract_code_blocks(response)
        if DEBUG: print(response_list)
        for response in response_list:
            if DEBUG: print(response)
            if "pip install" in response:
                package_name_match = re.search(r'pip install\s+(\S+)', response)
                if package_name_match:
                    package_name = package_name_match.group(1)
                    stdout, stderr = pip_install(package_name)
                    if not stderr:
                        print(f"Package {package_name} installed successfully.")
                    else:
                        print(f"Error occurred while installing package: {stderr}")
            newMSG.append({"role": "assistant", "content": response})
            modify_file(FP, response)
            stdout, stderr = execute_python_script(FP)
            print(stdout)
            if DEBUG: print(stderr)
            newMSG.append({"role": "user", "content": stderr})
            if stderr:
                newMSG = RESET_ALL()
                git_utils.git_reset_hard()
            else:
                print(f"Successfully executed the auto LLM script in times.")
                msg = git_utils.git_diff()
                msg += "write git push commit"

                response = ollama.chat(model='llama3:latest', messages=[
                {
                    'role': 'user',
                    'content': msg,
                },
                ])
                print(git_utils.git_commit_and_push(response))
            

    except Exception as e:
        print(e)
        newMSG = RESET_ALL()
        git_utils.git_reset_hard()


