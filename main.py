from nbt import nbt
import os
import uuid

directory = "./playerdata"
outputdir = "./new_playerdata"

origincwd = os.getcwd()

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
    if f[-4:-1] == ".dat":
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
