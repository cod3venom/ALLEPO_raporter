import subprocess, os, sys,time

electron = None
tamper = None
try:
    if sys.argv[1] is not None:
        comm = sys.argv[1]
        
       
    if comm == "screen":
        electron = subprocess.Popen('npm start', shell=True)
        electron_pid = electron.pid
        time.sleep(3)
        tamper = subprocess.Popen('python3 Store_tamper.py analysis screenshot', shell=True, stdout=subprocess.PIPE)
        tamper_pid = tamper.pid
    if comm == "noscreen":
        os.system('python3 Store_tamper.py analysis noscreen')
        
except KeyboardInterrupt:
    if electron is not None or tamper is not None:
        electron.terminate()
        tamper.terminate()