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
logging.getLogger().addHandler(logging.StreamHandler())
logging.debug("Logging initialized")

directory = "./playerdata"
outputdir = "./new_playerdata"
convertAdvancements = True
advancementsDir = "./advancements"
outputAdvDir = "./new_advancements"

try:
    os.chdir(directory)
except FileNotFoundError:
    for d in directory.split("/"):
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
    os.chdir(outputdir)
except FileNotFoundError:
    for d in outputdir.split("/"):
        try:
            os.chdir(d)
        except FileNotFoundError:
            os.mkdir(d)
            os.chdir(d)

os.chdir(origincwd)

class NULL_NAMESPACE:
    bytes = b''

for f in playerdata:
    currentPD = nbt.NBTFile(f"./{directory}/{f}", "rb")
    name = currentPD["bukkit"]["lastKnownName"].value
    offlineUUID = uuid.uuid3(NULL_NAMESPACE, f"OfflinePlayer:{name}")
    currentPD.write_file(f"./{outputdir}/{offlineUUID}.dat")
    logging.debug(f"created converted playerdata for '{name}' with offline uuid '{offlineUUID}'")
    if convertAdvancements:
        shutil.copyfile(f"./{advancementsDir}/{f[:-4]}.json", f"./{outputAdvDir}/{offlineUUID}.json")
