import argparse, pexpect, os.path, os, subprocess, sys, time

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
        while True:
            session.flush()
            session.read_nonblocking(size=100,timeout=None)
            # pexpectForceUpdate(session)
            time.sleep(0.2) 
    except KeyboardInterrupt:
        print("The MCPServer will shutdown.")
        sys.exit(0)
    except pexpect.exceptions.TIMEOUT:
        print("This is bug. Please start this server again")
        pass