import subprocess
import os
import re

leading_4_spaces = re.compile('^    ')

# command = f"cd {repo_path} && git log"

# if repo path doesn't have .git -> add it

repo_path = os.path.join("/home/jinho/Projects/openvino", ".git")


# command = "git log"
# command = "ls"

def get_commits(command):
    print(f'command: {command}')
    # lines = subprocess.check_output(
    #     command.split(), stderr=subprocess.STDOUT
    # ).decode("utf-8").split("\n")
    # print(lines)

    # temp2 = subprocess.run(command.split(), capture_output=True, text=True, stderr=subprocess.STDOUT).stdout
    # temp2 = subprocess.run(["ls", "-al"], capture_output=True).stdout.decode("utf-8")
    # lines = subprocess.check_output(
    #     command.split(), stderr=subprocess.STDOUT
    # ).split('\n')
    lines = subprocess.run(command.split(), capture_output=True, text=True).stdout.split("\n")
    indices = [idx for idx, l in enumerate(lines) if l.startswith("commit")]
    # print(indices)

    commits = []
    if len(indices) > 1:

        last_idx = indices[0]
        for idx in indices[1:]:
            commits.append(lines[last_idx:idx+1])
            last_idx = idx
        commits.append(lines[last_idx:])

    return commits

def main():
    num_logs = 4

    command = f"git --no-pager --git-dir={repo_path} log"
    if num_logs:
        command += f" -{num_logs}"
    commits = get_commits(command)

    print(len(commits))
    [print(commit) for commit in commits[:3]]

def test_commit_separation():
    import sys
    import traceback

    for num_logs in range(0, 10):
        command = f"git --no-pager --git-dir={repo_path} log"
        if num_logs:
            command += f" -{num_logs}"

        try:
            assert len(get_commits(command)) == num_logs
        except AssertionError:
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb) # Fixed format
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]

            commit_len = len(get_commits(command))
            print(f'error num_logs: {num_logs}, commit_len: {commit_len}')






if __name__ == '__main__':
    # test_commit_separation()
    main()
