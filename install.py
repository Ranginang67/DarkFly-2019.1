# -*- coding: utf-8 -*-
from os import path, system, getuid
import time, sys

TERMUX      = "/data/data/com.termux/files/usr/bin/"
LINUX       = "/usr/bin/"
DARKFLYEXEC = "DarkFly."
COMMAND = {
    "termux":{1:"cd "+TERMUX+"DarkFly-2019.1",2:"python {}/{}".format(TERMUX,"DarkFly-2019.1/main.py")},
    "linux":{1:"cd "+LINUX+"DarkFly-2019.1",2:"python3 {}/{}".format(LINUX,"DarkFly-2019.1/main.py")}
}

class Install:
    @staticmethod
    def environmentExists(ph):
        if not path.exists(ph):
            return 0
        return 1

    def installLinux(self):
        if getuid():
            sys.exit("Your must be run this tool as superuser")
        execd = open(LINUX+DARKFLYEXEC,"w")
        if not self.environmentExists(LINUX+"python3"):
            system("apt-get install python3 -y")
        execd.write(("#!/bin/bash\n"+COMMAND["linux"][1]+"\n"+COMMAND["linux"][2]))
        system("mv ../DarkFly-2019.1 %s && chmod +x %s/%s && chmod 777 -R %s"%(LINUX,LINUX,DARKFLYEXEC,LINUX+"/DarkFly-2019.1"))
        # check if install is success
        if not self.environmentExists(LINUX+DARKFLYEXEC) or not self.environmentExists(LINUX+"DarkFly-2019.1"):
            sys.exit("Install failed.")
        sys.exit("[ ✓ ] Install Success. run: \"DarkFly.\"")
        execd.close()

    def installTermux(self):
        exect = open(TERMUX+DARKFLYEXEC,"w")
        if not self.environmentExists(TERMUX+"python3"):
            system("pkg install python -y")
        exect.write(("#!/bin/bash\n"+COMMAND["termux"][1]+"\n"+COMMAND["termux"][2]))
        system("mv ../DarkFly-2019.1 %s && chmod +x %s/%s && chmod 777 -R %s"%(TERMUX,TERMUX,DARKFLYEXEC,TERMUX+"/DarkFly-2019.1"))
        if not self.environmentExists(TERMUX+DARKFLYEXEC) or not self.environmentExists(TERMUX+"DarkFly-2019.1"):
            sys.exit("Install failed.")
        sys.exit("[ ✓ ] Install Success, run: \"DarkFly.\"")
        exect.close()
    
    def install(self):
        system_check = self.installTermux() if path.isdir(TERMUX) else self.installLinux()
        return 0

class Uninstall(Install):
    def uninstall(self):
        if self.environmentExists(LINUX):
            system("sudo rm -rf {}/DarkFly-2019.1 && sudo rm -rf {}/{}".format(
                LINUX,LINUX,DARKFLYEXEC
            ))
        elif self.environmentExists(TERMUX):
            system("rm -rf {}/DarkFly-2019.1 && rm -rf {}/{}".format(
                TERMUX,TERMUX,DARKFLYEXEC
            ))
        else:
            sys.exit(0)

if len(sys.argv) == 2:
    if sys.argv[1] == "install":
        Install().install()
        sys.exit(0)