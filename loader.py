import os, os.path, sys, json, pexpect

# TODO: install python dependency automaticly to MCP Server Venv

print("@ Init")

cwd = os.getcwd()
print("Please make sure working directory is correct.")
print(cwd)

toolsPath   = cwd + "/tools"
runtimePath = cwd + "/mainSys/runtime.py"

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


print("\n@ Path Summary")
print("toolsPath  : {}".format(toolsPath))
print("runtimePath: {}".format(runtimePath))





print("\n\n@ Search For Tools")

toolPathList: list[str] = []

def searchForTools(currentWorkingRelativePath:str = "",init:bool = True) -> None:
    if(not init): print("")
    print("Search for: .{}".format(currentWorkingRelativePath))
    for fileOrDir in os.listdir("{}/{}".format(toolsPath,currentWorkingRelativePath)):
        absolutePath = "{}/{}/{}".format(toolsPath,currentWorkingRelativePath,fileOrDir).replace("//","/")
        print("Working with: {}".format(absolutePath))
        if(
            os.path.isfile(absolutePath) and
            ".py" in absolutePath
            ):
            target = "{}.{}".format(currentWorkingRelativePath,fileOrDir)
            target = target.replace("//","/")
            target = target.replace("/",".")
            target = target.replace("..",".")
            target = target.replace(".py","")
            print("Register target: {}",format(target))
            toolPathList.append(target)
        elif(not os.path.isfile(absolutePath) and not "__pycache__" in absolutePath):
            searchForTools("{}/{}".format(currentWorkingRelativePath,fileOrDir),False)

searchForTools()

print(toolPathList)





print("\n\n@ Generate runtime")
runtimeString = """
# include tools path
import sys
if(not '{}' in sys.path):
    sys.path.append('{}')


""".format(toolsPath,toolsPath)

for tools in toolPathList:
    importString = ""
    if(tools.split(".").__len__() <= 2):
        importName      = tools.split(".")[1]
        importString    = "import {}\n".format(importName)
    else:
        importName      = tools.split(".")[-1]
        importPath      = ".".join(tools.split(".")[:-1])
        importString    = "from {} import {}\n".format(importPath,importName)
    
    if("from ." in importString):
        importString = importString.replace("from .","from ")
    print(importString)
    runtimeString += importString

with open(runtimePath,"w") as runtime:
    runtime.write(runtimeString)



print("@ Loading finished ---------------")
print("@ Loading finished ---------------")
print("@ Loading finished ---------------")
print("@ Loading finished ---------------")