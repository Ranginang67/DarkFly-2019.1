"""
    DarkFly tools 2019.1
    ------------

    Developer/Author    : Ms.ambari (Muslim ambari)
    Supported platform  : all Linux distro and termux(android)
    Company             : MahesaSystem
    Email               : ambari.developer@gmail.com
    YouTube             : Ms.ambari
    Github              : /Ranginang67
    Termux Tested on    : Samsung galaxy J5 prime 8.0
    Linux Tested on     : Ubuntu Gnome 16.04 LTS

    ------------
    DarkFly tools 2019.1 is a open source, free, and automatic tools.
"""

banner_list = [
    """
       .---.        .-----------
      /     \  __  /    ------
     / /     \(  )/    -----
    //////   ' \/ `   ---
   //// / // :    : ---
  // /   /  /`    '--
 //          //..\\
        ====UU====UU====
        |   '//||\\`   |
        |     ''``    |
====================================
    """,
    # """
    # add costum banner here...
    # """,
]

import re
import os
import sys
import platform
import socket
import urllib.request
import json, random
import config.md as md
from time import sleep
import install

if not md.Show().checkAllOK():
    sys.exit(0)

network_status = 0

class MainModule:
    __tools_list = "config/tools.json"
    __home_directory = os.environ["HOME"]
    __tools_tmp = {}
    __users_tmp = {}
    __dell_tmp = {}

    @classmethod
    def getTools(cls,msg,RepoUrl):
        with open(MainModule.__tools_list,"r+") as TS:
            data = json.loads(TS.read())
            try:
                md.Show().Message("normal","{}: {}".format(msg,RepoUrl))
                r = urllib.request.urlopen(RepoUrl+"?tab=repositories")
                html = r.read().decode("utf8")
                regx = re.findall(r"itemprop=\"name.codeR[\D]*\".>\n*(.*?)<\/a>",html)
                getname = re.findall(r"-hidden\".itemprop=\"name\">(.*?)<\/span>",html)
                if regx:
                    data[RepoUrl]["name"] = getname[0]
                    for i in regx:
                        i = i.replace(" ","");
                        if not i in data[RepoUrl]["tools"]:
                            data[RepoUrl]["tools"].append(i)
                    TS.seek(0)
                    TS.write(json.dumps(data))
                    TS.truncate()
                else:
                    pass
            except Exception as e:
                md.Show().Message("e","ERROR: "+str(e))
    @classmethod
    def sysMain(cls,command):
        for c in command:
            os.system(c)
    @classmethod
    def exec(cls):
        if os.path.isdir("/usr/bin/"):
            os.system("python3 %s"%sys.argv[0])
            return 0
        if os.path.isdir("/data/data/com.termux/"):
            os.system("python %s"%sys.argv[0])
        return 0

    @classmethod
    def networkCheck(cls):
        ok_network = 1
        try:
            socket.gethostbyname("www.google.com")
        except:
            ok_network = 0

        return int(ok_network)

    @classmethod
    def UpdateRepository(cls):
        if not cls.networkCheck():
            md.Show().Message("e","Upate failed, Check your connection and try again\n")
            sys.exit(0)
        with open(cls.__tools_list,"r+") as ch:
            jsonRead = json.loads(ch.read())
            for us in jsonRead:
                try:
                    cls.getTools("Updating Repository from",us)
                except KeyboardInterrupt:
                    sys.exit(0)
        md.Show().Message("OK","Done!"); sleep(1.5)
        MainModule().exec()

    @staticmethod
    def toolsInstall(toolsName,toolsUrl,usersName):
        # if not MainModule.networkCheck(): # only works on fast Network connection
        #     sys.exit(md.Show().Message("e","Install failed, check your connection."))
        MainModule().sysMain(["clear","printf \"\a\""])
        if os.path.isdir("{}/{}".format(MainModule.__home_directory,toolsName)):
            md.Show().Message("e","Download Failed, tools '{}' exists".format(toolsName)); sleep(2)
            MainModule().exec()
            return 0
        md.Show().Message("normal","Downloading repo{}: {}".format("".rjust(1),toolsName))
        md.Show().Message("normal","From{}: {}".format("".rjust(13),usersName))
        MainModule().sysMain(["git clone -q {}/{} {}/{}".format(toolsUrl,toolsName,MainModule.__home_directory,toolsName)])

        if not os.path.isdir("{}/{}".format(MainModule.__home_directory,toolsName)):
            md.Show().Message("e","Download failed")
            return 0

        md.Show().Message("OK","Download success")
        md.Show().keyExceptions();

    @staticmethod
    def addRepository(repoUrl=None):
        if not MainModule().networkCheck():
            md.Show().Message("e","Failed to adding new users, Please check your connection and try again\n")
            sys.exit(0)
        MainModule().sysMain(["clear","printf \"\a\""])
        if not repoUrl:
            try:
                while True:
                    repoUrl = str(input(md.Show().Message("i","Input new github users [ EX: https://github.com/users ]: ")))
                    if repoUrl[0:19] != "https://github.com/":
                        md.Show().Message("e","Error: Invalid URL")
                        continue
                    try:
                        md.Show().Message("normal","Checking Valid URL.")
                        chk = urllib.request.urlopen(repoUrl)
                    except KeyboardInterrupt:
                        sys.exit(0)
                    except urllib.request.HTTPError:
                        md.Show().Message("e","Invalid URL.")
                        continue
                    else:
                        break
            except(KeyboardInterrupt):
                md.Show().keyExceptions()
                return 0
            except(Exception):
                sys.exit("\n")
        
        try:
            with open(MainModule.__tools_list,"r+") as addR:
                data = json.loads(addR.read())
                
                if repoUrl in data:
                    md.Show().Message("e","Github users '"+repoUrl+"' exists")
                    return 0
                data[repoUrl] = {"name":"0","tools":[]}

                addR.seek(0)
                addR.write(json.dumps(data))
                addR.truncate()

                try:
                    json.loads(open(MainModule.__tools_list,"r+").read())[repoUrl]
                except KeyError:
                    md.Show().Message("e","Failed to adding github users.")
                    sys.exit(0)
                md.Show().Message("ok","github user Successfully added")
                
                MainModule().getTools("Fetching repository from",repoUrl)
                md.Show().Message("OK","Done!"); sleep(1.5)
                MainModule().exec()
        except KeyboardInterrupt:
            sys.exit("\n")
    
    @classmethod
    def showTools(cls):
        global_reader = open(cls.__tools_list,"r+").read()
        users_repository_selection = 0
        MainModule().sysMain(["clear","printf \"\a\""])
        myItems = [
            "return",
            "exit"
        ]
        with open(cls.__tools_list,"rb") as LT:
            results = json.loads(LT.read().decode("utf8"))
            for cn,i in enumerate(results):
                cls.__users_tmp[cn+1] = i
                cls.__tools_tmp[i] = []
                for c,x in enumerate(set(results[i]["tools"])):
                    cls.__tools_tmp[i].append({c+1:x})
            for my in myItems:
                if not my in cls.__users_tmp.values():
                    cls.__users_tmp[list(cls.__users_tmp.keys())[-1]+1] = my

            for key,value in cls.__users_tmp.items():
                print("[ "+md.SetModule().GR+str(key)+md.SetModule().RS+" ] "+value)
            
            try:
                users_repository_selection = int(input(md.Show().Message("i","Choose: ")))
            except (KeyboardInterrupt):
                md.Show().keyExceptions()
                return 0
            except Exception:
                return 0
            
            try:
                if cls.__users_tmp[users_repository_selection] in ["exit","quit"]:
                    sys.exit(0)
                elif cls.__users_tmp[users_repository_selection] in ["return"]:
                    cls.exec()
                    return 0
            except KeyError:
                md.Show().Message("e","out of range\n")
                sleep(1)
                MainModule().showTools()
                return 0

            if not users_repository_selection:
                return 0

            getName = json.loads((open(cls.__tools_list,"r+").read()))[cls.__users_tmp[users_repository_selection]]["name"]

        MainModule().sysMain(["clear","printf \"\a\""])
        md.Show().Message("normal","Repository from: {}\n".format(getName))

        for addItems in myItems:
            cls.__tools_tmp[cls.__users_tmp[users_repository_selection]].append({list(cls.__tools_tmp[cls.__users_tmp[users_repository_selection]][-1])[0]+1:addItems})

        for cc,displayItems in enumerate(cls.__tools_tmp[cls.__users_tmp[users_repository_selection]]):
            print("[ {}{}{} ] {}".format(
                md.SetModule().GR,
                (cc+1),
                md.SetModule().RS,
                displayItems[cc+1]
            ))
        try:
            ts_select = int(input(md.Show().Message("i","Download from '{}' : ".format(getName))))
        except KeyboardInterrupt:
            md.Show().keyExceptions()
            return 0
        except Exception:
            sys.exit("\n")
        
        try:
            itemIfexitOrReturn = cls.__tools_tmp[cls.__users_tmp[users_repository_selection]][ts_select -1][list(cls.__tools_tmp[cls.__users_tmp[users_repository_selection]][ts_select -1])[0]]
            if itemIfexitOrReturn in ["exit","quit"]:
                sys.exit(0)
            elif itemIfexitOrReturn in ["return"]:
                MainModule().showTools()
            else:
                cls.toolsInstall(
                    cls.__tools_tmp[cls.__users_tmp[users_repository_selection]][ts_select -1][ts_select],
                    cls.__users_tmp[users_repository_selection],
                    getName
                )
        except (KeyError,IndexError):
            md.Show().Message("e","out of range\n")
            sleep(1)
            MainModule().showTools()
            return 0
        return 0
    @classmethod
    def removeRepository(cls):
        while True:
            MainModule().sysMain(["clear","printf \"\a\""])
            with open(cls.__tools_list,"r+") as delrep:
                ed = json.loads(delrep.read())
                for numb,i in enumerate(ed):
                    cls.__dell_tmp[numb+1] = i
                for kd,vd in cls.__dell_tmp.items():
                    print("[ {}{}{} ] {}".format(
                        md.SetModule().GR,
                        kd,
                        md.SetModule().RS,
                        vd
                    ))
                try:
                    whatDel = int(input(md.Show().Message("i","Select github users you want to delete: ")))
                except ValueError:
                    md.Show().Message("e","Type must be integer.")
                    sleep(1)
                    continue
                except KeyboardInterrupt:
                    md.Show().keyExceptions()
                    break
                
                if not whatDel in cls.__dell_tmp:
                    continue
                
                del ed[cls.__dell_tmp[whatDel]]

                delrep.seek(0)
                delrep.write(json.dumps(ed))
                delrep.truncate()

                md.Show().Message("OK","Users '{}' removed.".format(cls.__dell_tmp[whatDel]))
                sleep(1.5)
                MainModule().exec()
                break
        return 0

MainModule().sysMain(["clear","printf \"\a\""])
print(banner_list[random.randint(0,len(banner_list) -1)])
for key,val in md.SetModule().tools_menu.items():
    for x in val:
        print("[ "+md.SetModule().GR+str(x)+md.SetModule().RS+" ] "+val[x])
try:
    users_input = int(input("\n"+md.Show().Message("input","Choose: ")))
except (ValueError,KeyboardInterrupt):
    sys.exit("\n")

if users_input == 1:
    MainModule().showTools()
elif users_input == 2:
    MainModule().UpdateRepository()
elif users_input == 3:
    MainModule().addRepository()
elif users_input == 4:
    MainModule().removeRepository()
elif users_input == 5:
    install.Uninstall().uninstall()
elif users_input == 6:
    MainModule().sysMain(["clear","printf \"\a\" && cat config/about.txt"])
    md.Show().keyExceptions()
elif users_input == 7:
    sys.exit(0)
else:
    MainModule().exec()
