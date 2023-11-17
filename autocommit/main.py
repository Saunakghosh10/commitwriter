from autocommit.generate_commit_message import generate_commit_message
from autocommit.generate_docstring import generate_docstring
import subprocess
import os


# def add_documentation(file_path):
#     # Call the Python script to generate documentation
#     try:
#         docstring = subprocess.check_output(
#             ["python", "generate_docstring.py", file_path], text=True
#         )
#     except subprocess.CalledProcessError as e:
#         print(f"Error generating docstring for {file_path}: {e}")
#         return False

#     # Prepend documentation to the file if docstring is generated
#     if docstring:
#         with open(file_path, "r+") as file:
#             content = file.read()
#             file.seek(0, 0)
#             file.write(f'"""\n{docstring}\n"""\n{content}')
#         return True
#     return False


# def generate_commit_message(diffs):
# try:
#     commit_message = subprocess.check_output(
#         ["python", "generate_commit_message.py", diffs], text=True
#     )
#     return commit_message
# except subprocess.CalledProcessError as e:
#     print(f"Error generating commit message: {e}")
#     return None

from autohooks.api import ok, fail
from autohooks.api.git import get_staged_status, stash_unstaged_changes
from autohooks.api.path import match

DEFAULT_INCLUDE = "*.py"


def get_include(config):
    if not config:
        return DEFAULT_INCLUDE

    config = config.get("tool", "autohooks", "plugins", "foo")
    return config.get_value("include", DEFAULT_INCLUDE)


def precommit(config=None, report_progress=None, **kwargs):
    include = get_include(config)

    files = [f for f in get_staged_status() if match(f.path, include)]

    if not files:
        # no files to fix
        return 0

    if report_progress:  # to support autohooks < 22.8.0
        report_progress.init(len(files))

    with stash_unstaged_changes(files):
        for file_path in files:
            if file_path.endswith(".py"):
                try:
                    line_count = int(
                        subprocess.check_output(["wc", "-l", file_path]).split()[0]
                    )
                except subprocess.CalledProcessError as e:
                    print(f"Error counting lines in {file_path}: {e}")

                if line_count > 10:
                    generate_docstring(file_path)

            if report_progress:
                report_progress.update()

    # Generate diffs for staged files
    try:
        diffs = subprocess.check_output(["git", "diff", "--cached"], text=True)
    except subprocess.CalledProcessError as e:
        print(f"Error generating diffs: {e}")

    # Generate a commit message
    commit_message = generate_commit_message(diffs)
    if commit_message:
        try:
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error during commit: {e}")
    else:
        print("No commit message was generated.")

    return 0


# def main():
#     # Get a list of staged Python files with more than 10 lines
#     staged_files = subprocess.check_output(
#         ["git", "diff", "--cached", "--name-only"], text=True
#     )
#     for file_path in staged_files.strip().split("\n"):
#         if file_path.endswith(".py"):
#             line_count = int(
#                 subprocess.check_output(["wc", "-l", file_path]).split()[0]
#             )
#             if line_count > 10:
#                 if not add_documentation(file_path):
#                     exit(1)
#                 subprocess.run(["git", "add", file_path])

#     # Generate diffs for staged files
#     diffs = subprocess.check_output(["git", "diff", "--cached"], text=True)

#     # Generate a commit message
#     commit_message = generate_commit_message(diffs)
#     if commit_message:
#         subprocess.run(["git", "commit", "-m", commit_message])
#     else:
#         print("No commit message was generated. Exiting...")
#         exit(1)


# if __name__ == "__main__":
#     main()
