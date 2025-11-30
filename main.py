from nbt import nbt
import os
import uuid
import logging
from datetime import datetime
import shutil

origincwd = os.getcwd()

logFile = f"./logs/{datetime.strftime(datetime.now(), '%Y_%m_%dT%H_%M_%SZ%z')}.log"
try:
    os.chdir("./logs/")
except FileNotFoundError:
    os.mkdir("logs")
os.chdir(origincwd)
LOG_LEVEL = logging.DEBUG
logging.basicConfig(format="[%(filename)s %(asctime)s %(levelname)s] %(message)s", level=LOG_LEVEL, handlers=[logging.StreamHandler(), logging.FileHandler(logFile)])
logging.debug("Logging initialized")

defaults = {
    "directory": "./playerdata",
    "outputdir": "./new_playerdata",
    "convertAdvancements": False,
    "advancementsDir": "./advancements",
    "outputAdvDir": "./new_advancements"
}

inputs = {
    "directory": input("Input playerdata directory: "),
    "outputdir": input("Output playerdata directory: "),
    "convertAdvancements": bool(input("Should I convert advancements (T/F): "))
}

inputs.update({
    "advancementsDir": input("Input advancements directory: ") if inputs["convertAdvancements"] else "",
    "outputAdvDir": input("Output advancements directory: ") if inputs["convertAdvancements"] else ""
})

for val in inputs:
    if inputs[val] == "":
        inputs[val] = defaults[val]

try:
    os.chdir(inputs["advancementsDir"])
except FileNotFoundError:
    for d in inputs["advancementsDir"].split("/"):
        try:
            os.chdir(d)
        except FileNotFoundError:
            os.mkdir(d)
            os.chdir(d)
os.chdir(origincwd)
try:
    os.chdir(inputs["directory"])
except FileNotFoundError:
    for d in inputs["directory"].split("/"):
        try:
            os.chdir(d)
        except FileNotFoundError:
            os.mkdir(d)
            os.chdir(d)

files = os.listdir(".")
playerdata = []
for f in files:
    if f[-4:] == ".dat":
        logging.debug(f"found valid playerdata {f}")
        playerdata.append(f)

os.chdir(origincwd)

try:
    os.chdir(inputs["outputdir"])
except FileNotFoundError:
    for d in inputs["outputdir"].split("/"):
        try:
            os.chdir(d)
        except FileNotFoundError:
            os.mkdir(d)
            os.chdir(d)
os.chdir(origincwd)
try:
    os.chdir(inputs["outputAdvDir"])
except FileNotFoundError:
    for d in inputs["outputAdvDir"].split("/"):
        try:
            os.chdir(d)
        except FileNotFoundError:
            os.mkdir(d)
            os.chdir(d)

os.chdir(origincwd)

class NULL_NAMESPACE:
    bytes = b''

for f in playerdata:
    try:
        currentPD = nbt.NBTFile(f"./{inputs["directory"]}/{f}", "rb")
    except Exception as e:
        logging.error(f"Unable to open ./{inputs["directory"]}/{f}")
        logging.debug(e)
    try:
        name = currentPD["bukkit"]["lastKnownName"].value
    except Exception as e:
        logging.error(f"Unable to access ['bukkit']['lastKnownName'] of ./{inputs["directory"]}/{f}. You probably aren't on Bukkit or one of its forks.")
        logging.debug(e)
    offlineUUID = uuid.uuid3(NULL_NAMESPACE, f"OfflinePlayer:{name}")
    currentPD.write_file(f"./{inputs["outputdir"]}/{offlineUUID}.dat")
    logging.debug(f"created converted playerdata for '{name}' with offline uuid '{offlineUUID}'")
    if inputs["convertAdvancements"]:
        try:
            shutil.copyfile(f"./{inputs["advancementsDir"]}/{f[:-4]}.json", f"./{inputs["outputAdvDir"]}/{offlineUUID}.json")
        except Exception as e:
            logging.error(f"Unable to copy ./{inputs["advancementsDir"]}/{f[:-4]}.json to ./{inputs["outputAdvDir"]}/{offlineUUID}.json")
            logging.debug(e)
