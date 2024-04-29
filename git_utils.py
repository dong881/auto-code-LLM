import subprocess

def git_diff():
    try:
        # 使用 subprocess 模組執行 git diff 命令
        diff_output = subprocess.check_output(['git', 'diff'], stderr=subprocess.STDOUT)
        # 解碼 byte 為 string
        diff_output = diff_output.decode('utf-8')
        return diff_output
    except subprocess.CalledProcessError as e:
        # 如果命令執行失敗，輸出錯誤信息
        return f"Error executing command: {e.output.decode('utf-8')}"

def git_commit_and_push(commit_message):
    try:
        # 執行 git add .
        subprocess.run(['git', 'add', '.'])
        # 執行 git commit
        subprocess.run(['git', 'commit', '-m', commit_message])
        # 執行 git push
        subprocess.run(['git', 'push'])
        return "Commit and push successful."
    except subprocess.CalledProcessError as e:
        # 如果命令執行失敗，輸出錯誤信息
        return f"Error executing command: {e.output.decode('utf-8')}"

def git_reset_hard():
    try:
        # 執行 git reset --hard
        subprocess.run(['git', 'reset', '--hard'])
        return "All changes discarded successfully."
    except subprocess.CalledProcessError as e:
        # 如果命令執行失敗，輸出錯誤信息
        return f"Error executing command: {e.output.decode('utf-8')}"

def git_status():
    try:
        # 執行 git status
        status_output = subprocess.check_output(['git', 'status'], stderr=subprocess.STDOUT)
        # 解碼 byte 為 string
        status_output = status_output.decode('utf-8')
        return status_output
    except subprocess.CalledProcessError as e:
        # 如果命令執行失敗，輸出錯誤信息
        return f"Error executing command: {e.output.decode('utf-8')}"

def git_log():
    try:
        # 執行 git log
        log_output = subprocess.check_output(['git', 'log'], stderr=subprocess.STDOUT)
        # 解碼 byte 為 string
        log_output = log_output.decode('utf-8')
        return log_output
    except subprocess.CalledProcessError as e:
        # 如果命令執行失敗，輸出錯誤信息
        return f"Error executing command: {e.output.decode('utf-8')}"

# 其他 Git 功能可以類似的添加在這裡
