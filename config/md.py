# -*- coding: utf-8 -*-
import json, os, sys, random

class SetModule:
    __tools_ph = "config/tools.json"
    # Set a CLI color
    GR = "\033[32m" # green color
    RD = "\033[31m" # red color
    RS = "\033[m" # Reset color
    
    tools_menu = {
        "Home":{
            1:"Show my tools",
            2:"Upate Repository tools",
            3:"Add new Repository",
            4:"Remove Repository",
            5:"Uninstall",
            6:"About",
            7:"Exit",
        }
    }

    @classmethod
    def checkAllOK(self):
        status_complete = 0;
        with open("config/complete.json","rb") as cm:
            cm = json.loads(cm.read().decode("utf-8"))
            for key,value in cm.items():
                for i in cm[key]:
                    if not os.path.isfile(i):
                        Show().Message("e","File '{}' Not found...".format(i))
                        status_complete = 1
        if status_complete != 0:
            Show().Message("e","{} File not found detected. reinstall this tool to fix this broblem".format(status_complete))
            return 0

        return 1

class Show(SetModule):

    @classmethod
    def Message(cls,condition,text):
        if condition in ["error","eror","err","e"]:
            print("\n[{} x {}] {}".format(
                cls.RD,
                cls.RS,
                text
            ))
            return 0
        if condition in ["input","i"]:
            return ("\n[{} ?{} ] {}".format(
                cls.GR,
                cls.RS,
                text
            ))
        if condition in ["nor","normal"]:
            print("[{} + {}] {}".format(
                cls.GR,
                cls.RS,
                text
            ))
            return 0

        print("\n[{} ✓{} ] {}".format(
            cls.GR,
            cls.RS,
            text
        ))
    
    @classmethod
    def keyExceptions(cls):
        while(True):
            try:
                whatExit = input(Show().Message("i","Do you Want to exit? [y/n]: "))
            except (KeyboardInterrupt,Exception):
                continue
            else:
                if whatExit in ["N","n","NO","No","no"]:
                    if os.path.isdir("/usr/bin/"):
                        os.system("python3 main.py")
                    elif os.path.isdir("/data/data/com.termux/"):
                        os.system("python main.py")
                    else:
                        pass
                    break
                elif whatExit in ["y","Y","yes","Yes","YES"]:
                    sys.exit(0)
                else:
                    continue

        return 0