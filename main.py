import argparse, pexpect, os.path, os, json, sys, time
from common import pexpectExecuteCommand,executeCommand,pexpectForceUpdate,waitForever


parse = argparse.ArgumentParser()
parse.add_argument("--loadScript",action='store_true')
parse.add_argument("--startServer",action='store_true')








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





toolsPath   = cwd + "/tools"
if(not os.path.exists("./settings.json")):
    print("There is no settings file.")
    sys.exit(1)

Settings: None | dict = None
with open("./settings.json","rt") as setting:
    Settings = json.loads(setting.read())

if(Settings == None):
    print("This is invaild settings.")
    sys.exit(1)

if(Settings["useDefaultToolPath"]):
    print("'useDefaultToolPath' is enabled, plase check the path shown below.")
    print(toolsPath)
else:
    toolsPath = Settings["toolsPath"]
    print("'useDefaultToolPath' is disabled, plase check the path shown below.")
    print(toolsPath)

toolsPythonDependencyPath = toolsPath + "/requirements.txt"
if(os.path.exists(toolsPythonDependencyPath)):
    pexpectExecuteCommand(MCPserverSession,"pip install -r '{}'; pip list".format(toolsPythonDependencyPath),expect="-------------------------")
else:
    print("There is no requirements.txt for tools dependency.")








result = parse.parse_args()

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

