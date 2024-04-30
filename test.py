import git_utils
import ollama

# print(git_utils.git_diff())
msg = git_utils.git_diff()
msg += "Organize into git push commit text"

response = ollama.chat(model='llama3:latest', messages=[
{
    'role': 'user',
    'content': msg,
},
])
print(type(response['message']['content']))
print(git_utils.git_commit_and_push(response['message']['content']))
