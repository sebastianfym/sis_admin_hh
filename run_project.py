import os
import subprocess
import sys
import platform

folder_name = "venv/bin/"
current_os = platform.system()

current_directory = os.path.dirname(os.path.abspath(__file__))
two_steps_up_directory = os.path.abspath(os.path.join(current_directory, '../../'))
folder_name = "venv/bin/" if current_os != "Windows" else "venv/Scripts/"
venv_path = os.path.join(two_steps_up_directory, folder_name)
print(two_steps_up_directory, 'two_steps_up_directory')
if current_os == "Windows":
    activate_script = os.path.join(venv_path, "activate.bat")
    activate_command = f"call {activate_script}"
else:
    activate_script = os.path.join(venv_path, "activate")
    print(activate_script, 'activate_script')
    activate_command = f"source {activate_script}"

subprocess.run(activate_command, shell=True)

os.chdir(current_directory)

subprocess.call(["python", "manage.py", "runserver"])