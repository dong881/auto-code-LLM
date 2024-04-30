import re
import utils
import git_utils
import ollama

FP = "./target_file.py"
DEBUG = False

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

    while True:
        try:
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
                newMSG.append({"role": "user", "content": utils.read_file(FP) + "\nimpove current code, and give me fully code"})
                msg = git_utils.git_diff()
                msg += "Organize into git push commit text"
                commit_and_push_changes(msg)

        except Exception as e:
            print(e)
            newMSG = utils.RESET_ALL(topic_description)
            git_utils.git_reset_hard()

if __name__ == "__main__":
    main("write a greedy snake game, and make sure it can run and play.")
