FP = "./target_file.py"
execute_times = 3
# topic_description = "query the current time and print it out."
topic_description = "don't use API and query the current stock price of TSLA and print it out."


topic_description += "Only give me the code without any symbol, and don't give any other text. I need to execute right now."
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
        process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
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

newMSG = [
            {
                "role": "system",
                "content": "only give me the code without any symbol, and don't give any other text. I need to execute right now."
            },
            {
                "role": "user",
                "content": "get the current web https://www.ntust.edu.tw/home.php news"
            },
            {
                "role": "assistant",
                "content": "import requests\nimport json\nimport datetime\n\nurl = \"https://www.ntust.edu.tw/home.php\"\nresponse = requests.get(url)\nsoup = BeautifulSoup(response.text, 'html.parser')\nnews = soup.find_all('div', {'class': 'content-wrap'})\n\nfor news_i in news:\n    title = news_i.find('h2').text\n    content = news_i.find('p').text\n    publishdate = news_i.find('span', {'class': 'date'}).text\n    print(f\"{title}\\n{content}\\n{publishdate}\\n\")"
            },
            {
                "role": "user",
                "content": "Traceback (most recent call last):\n  File \"/home/azureuser/target_file.py\", line 7, in <module>\n    soup = BeautifulSoup(response.text, 'html.parser')\n           ^^^^^^^^^^^^^\nNameError: name 'BeautifulSoup' is not defined"
            },
            {
                "role": "assistant",
                "content": "from bs4 import BeautifulSoup\nimport requests\nimport json\nimport datetime\n\nurl = \"https://www.ntust.edu.tw/home.php\"\nresponse = requests.get(url)\nsoup = BeautifulSoup(response.text, 'html.parser')\nnews = soup.find_all('div', {'class': 'content-wrap'})\n\nfor news_i in news:\n    title = news_i.find('h2').text\n    content = news_i.find('p').text\n    publishdate = news_i.find('span', {'class': 'date'}).text\n    print(f\"{title}\\n{content}\\n{publishdate}\\n\")"
            },
            {
                "role": "user",
                "content": "Traceback (most recent call last):\n  File \"/home/azureuser/target_file.py\", line 4, in <module>\n    from bs4 import BeautifulSoup\nModuleNotFoundError: No module named 'bs4'"
            },
            {
                "role": "assistant",
                "content": "pip install beautifulsoup4"
            },
            {
                "role": "user",
                "content": "Great. Follow the above rules. Next, please help me write a query using python to "+topic_description
            },
        ]

import os
from groq import Groq
import re

def get_api_key(file_path):
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
        return api_key
    except Exception as e:
        print(f"Error occurred while reading API key from file '{file_path}': {e}")
        return None

api_key_file_path = "api_key.txt"
api_key = get_api_key(api_key_file_path)

if api_key:
    client = Groq(api_key=os.environ.get(api_key))

    for i in range(execute_times):
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages= newMSG,
            # temperature=1,
            # max_tokens=1024,
            # top_p=1,
            # stream=True,
            # stop=None,
        )

        response = ""
        response = completion.choices[0].message.content
        # print(response)
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
        # print(stderr)
        newMSG.append({"role": "user", "content": stderr})
        if not stderr:
            print("Successfully executed the auto LLM script.")
            break
else:
    print("API key is not available.")
