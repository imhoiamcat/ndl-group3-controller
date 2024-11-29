import subprocess
ans = subprocess.call("pwd", shell=True)
if ans == 0:
   print("Command executed.")
else:
   print("Command failed.")
