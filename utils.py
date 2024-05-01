
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

import re
def extract_code_blocks(text):
    code_blocks = re.findall(r'```(.*?)```', text, re.DOTALL)
    if not code_blocks:
        code_blocks.append(text)
    return '\n'.join(code_blocks)

def RESET_ALL(topic_description):
    newMSG_content = ""
    with open("system_message.txt", "r") as file:
        newMSG_content = file.read()
    newMSG = eval(newMSG_content)
    newMSG[-1]["content"] += topic_description
    return newMSG
