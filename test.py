import git_utils
import ollama

# print(git_utils.git_diff())
msg = git_utils.git_diff()
msg += "write git push commit"

response = ollama.chat(model='llama3:latest', messages=[
  {
    'role': 'user',
    'content': msg,
  },
])
print(response['message']['content'])
