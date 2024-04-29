FP = "./target_file.py"
# execute_times = 10
DEBUG = False
# topic_description = "query the current time and print it out."
topic_description = """""   
query the current time and print it out.
"""

topic_description += ", don't use API key and Only give me the fully source code without any symbol, and don't give any other text. I need to execute right now."
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

# newMSG = [
#             {
#                 "role": "system",
#                 "content": "only give me the code without any symbol, and don't give any other text. I need to execute right now."
#             },
#             {
#                 "role": "user",
#                 "content": "get the current web https://www.ntust.edu.tw/home.php news"
#             },
#             {
#                 "role": "assistant",
#                 "content": "import requests\nimport json\nimport datetime\n\nurl = \"https://www.ntust.edu.tw/home.php\"\nresponse = requests.get(url)\nsoup = BeautifulSoup(response.text, 'html.parser')\nnews = soup.find_all('div', {'class': 'content-wrap'})\n\nfor news_i in news:\n    title = news_i.find('h2').text\n    content = news_i.find('p').text\n    publishdate = news_i.find('span', {'class': 'date'}).text\n    print(f\"{title}\\n{content}\\n{publishdate}\\n\")"
#             },
#             {
#                 "role": "user",
#                 "content": "Traceback (most recent call last):\n  File \"/home/azureuser/target_file.py\", line 7, in <module>\n    soup = BeautifulSoup(response.text, 'html.parser')\n           ^^^^^^^^^^^^^\nNameError: name 'BeautifulSoup' is not defined"
#             },
#             {
#                 "role": "assistant",
#                 "content": "from bs4 import BeautifulSoup\nimport requests\nimport json\nimport datetime\n\nurl = \"https://www.ntust.edu.tw/home.php\"\nresponse = requests.get(url)\nsoup = BeautifulSoup(response.text, 'html.parser')\nnews = soup.find_all('div', {'class': 'content-wrap'})\n\nfor news_i in news:\n    title = news_i.find('h2').text\n    content = news_i.find('p').text\n    publishdate = news_i.find('span', {'class': 'date'}).text\n    print(f\"{title}\\n{content}\\n{publishdate}\\n\")"
#             },
#             {
#                 "role": "user",
#                 "content": "Traceback (most recent call last):\n  File \"/home/azureuser/target_file.py\", line 4, in <module>\n    from bs4 import BeautifulSoup\nModuleNotFoundError: No module named 'bs4'"
#             },
#             {
#                 "role": "assistant",
#                 "content": "pip install beautifulsoup4"
#             },
#             {
#                 "role": "user",
#                 "content": "Great. Follow the above rules. Next, please help me write a query using python to "+topic_description
#             },
#         ]

newMSG_content = ""
with open("system_message.txt", "r") as file:
    newMSG_content = file.read()

newMSG = eval(newMSG_content)  
newMSG += topic_description

import os
import ollama
import re
import git_utils


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
                git_reset_hard()
                newMSG = eval(newMSG_content)  
                newMSG += topic_description
            else:
                print(f"Successfully executed the auto LLM script in {i} times.")
                msg = git_utils.git_diff()
                msg += "write git push commit"

                response = ollama.chat(model='llama3:latest', messages=[
                {
                    'role': 'user',
                    'content': msg,
                },
                ])
                git_commit_and_push(response)
            

    except e:
        print(e)
