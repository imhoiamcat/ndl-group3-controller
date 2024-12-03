import subprocess
try:
	command = "mosquitto_sub -h localhost -t \"mqtt/pimylifeup\""
	command1 = "pwd"
	ans = subprocess.call(command, shell=True)
	out = input()
	print("out", out)
except subprocess.CalledProcessError as e:
	print(f"Command failed with return code {e.returncode}")
