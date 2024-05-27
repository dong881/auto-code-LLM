import git_utils
import utils
import ollama

# print(git_utils.git_diff())
# msg = git_utils.git_diff()
# msg += "Organize into git push commit text"
# msg = "Why is the sky blue?"

# response = ollama.chat(model='llama3:latest', messages=[
# {
#     'role': 'user',
#     'content': msg,
# },
# ])
# print(type(response['message']['content']))
# res = response['message']['content']
# print(response['message']['content'])
# print(res)
# print(git_utils.git_commit_and_push(response['message']['content']))

newMSG = "Why is the sky blue?"
stream = ollama.chat(model='llama3:latest', messages=[{'role': 'user', 'content': 'Why is the sky blue?'}],stream=True)
response = ""
for chunk in stream:
    response += chunk['message']['content'].rstrip('\n')
print(response)