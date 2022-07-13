import subprocess


files = ["config.py", "verification_mod.py", "choose_language_mod.py"]
for file in files:
    subprocess.Popen(args=["start", "python", file], shell=True, stdout=subprocess.PIPE)