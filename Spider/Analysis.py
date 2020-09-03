import subprocess, os, time

electron_pid = 0
tamper_pid = 0
try:
    electron = subprocess.Popen('npm start', shell=True)
    electron_pid = electron.pid
    time.sleep(3)
    tamper = subprocess.Popen('python3 Store_tamper.py analysis', shell=True)
    tamper_pid = tamper.pid
except KeyboardInterrupt:
    os.system('pkill python3')
    os.system('pkill electron')