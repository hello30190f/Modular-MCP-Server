import argparse, pexpect, os.path, os, subprocess, sys, time
parse = argparse.ArgumentParser()
parse.add_argument("--loadScript",action='store_true')
parse.add_argument("--startServer",action='store_true')



def executeCommand(command:str) -> None:
    response = subprocess.run([command,],shell=True,capture_output=True)
    print(response.stdout.decode())
    print("Exit: {}".format(response.returncode))

def pexpectExecuteCommand(session:pexpect.spawn,command:str,timeout = 1,expect:str=".+") -> None:
    session.sendline(command)
    # Give the command time to get executed
    time.sleep(timeout)
    session.expect(expect)

## create update func for pexpect. without LF
def pexpectForceUpdate(session:pexpect.spawn) -> None:
    session.send("")
    time.sleep(0.1)
    session.expect(".+")
    session.send("")
    time.sleep(0.1)
    session.expect(".*")

def waitForever(session:pexpect.spawn) -> None:
    try:
        session.wait()
        # while True:
        #     pexpectForceUpdate(session)
        #     # time.sleep(0.2) 
    except KeyboardInterrupt:
        print("The MCPServer will shutdown.")
        sys.exit(0)



result = parse.parse_args()

cwd = os.getcwd()
print("Please make sure working directory is correct.")
print(cwd)

pythonVenvPath      = cwd + "/MCPvenv"
pythonVenvActivate  = cwd + "/MCPvenv/bin/activate"
mainSystemPath      = cwd + "/mainSys"
print("Python venv path: {}".format(pythonVenvPath))

# create pyton venv to prevent from messing the raw python environemnt
print("\n@ Init python venv")
if(not os.path.exists(pythonVenvPath)):
    print("Create Venv because it does not exist.")
    executeCommand("cd {}; python -m venv MCPvenv".format(cwd))

MCPserverSession            = pexpect.spawn("/bin/bash", timeout=5, encoding='utf-8')
MCPserverSession.timeout    = 3600 # infinaite hour
MCPserverSession.logfile    = sys.stdout
pexpectExecuteCommand(MCPserverSession,"source {}".format(pythonVenvActivate))
pexpectExecuteCommand(MCPserverSession,"cd {}".format(cwd))
pexpectExecuteCommand(MCPserverSession,"pip install -r requirements.txt; pip list",expect="-------------------------")

if result.loadScript and result.startServer:
    print("Please do not specify mutiple option at once.")
    sys.exit(1)

if result.loadScript:
    # print("When loader says '@ Loading finished ---------------', plase exit this scirpt by pressing 'Ctrl+C'")
    pexpectExecuteCommand(MCPserverSession,"cd {}".format(cwd))
    pexpectExecuteCommand(MCPserverSession,"python -u loader.py",expect="@ Loading finished ---------------")
elif result.startServer:
    MCPserverSession.timeout = 5
    pexpectExecuteCommand(MCPserverSession,"cd {}".format(mainSystemPath))
    pexpectExecuteCommand(MCPserverSession,"python -u main.py", expect="Starting MCP server")
    waitForever(MCPserverSession)
else: 
    print("Please specify --loadScript or --startServer")

