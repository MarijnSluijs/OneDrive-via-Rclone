import json
import subprocess
import re
import os
import tkinter as tk
from tkinter import filedialog
import time
import shutil
import ctypes
import sys

# Check if script is running as admin
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
    
if not is_admin():
    # Relaunch as admin
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Download winfsp with winget
print("\nWinFSP downloaden...")
subprocess.run(["winget", "install", "-e", "--id", "WinFsp.WinFsp"])

# Download rclone with winget
print("\nRclone downloaden...")
subprocess.run(["winget", "install", "-e", "--id", "Rclone.Rclone"])

# Run rclone authorize command, result will be access & refresh token
print("\nOneDrive authorizeren met Rclone (Browser wordt geopend)...")
result = subprocess.run(["rclone", "authorize", "onedrive"], capture_output=True, text=True)

# Extract JSON from output data using regex
match = re.search(r'(\{.*\})', result.stdout, re.DOTALL)

if match:
    token_json = match.group(1)  # Extract only the JSON part
    try:
        token_data = json.loads(token_json)  # Parse JSON
        access_token = token_data.get("access_token", "")
        refresh_token = token_data.get("refresh_token", "")
        expiry = token_data.get("expiry", "")

        print("Authorization successful")
    except json.JSONDecodeError:
        print("Failed to parse token JSON")
else:
    print("Could not find JSON in rclone output")

# Configure rclone with the token
print("\nRclone configureren met OneDrive (Browser wordt geopend)...")
subprocess.run(["rclone", "config", "create", "onedrive-rclone", "onedrive", "token", token_json])

# Ask the user where rclone should mount onedrive using tkinter askdirectory
root = tk.Tk()
root.withdraw()
print("\nSelecteer de folder waar Rclone OneDrive moet komen te staan...")
onedrive_path = filedialog.askdirectory(title="Selecteer de folder waar Rclone OneDrive moet komen te staan")

# Add /OneDriveRclone to the path
onedrive_path = onedrive_path + "/OneDriveRclone"

# Get absolute paths
runvbspath = os.path.abspath("Scripts/RunVbs.bat")
mountvbspath = os.path.abspath("Scripts/MountOneDrive.vbs")
mountbatpath = os.path.abspath("Scripts/MountOneDrive.bat")

# Create a .bat file that runs MountOneDrive.vbs via Task scheduler
with open("Scripts/RunVbs.bat", "w") as f:
    f.write(f"""@echo off
start "" "{mountvbspath}"
""")
    
# Create a .vbs file that runs MountOneDrive.bat silently
with open("Scripts/MountOneDrive.vbs", "w") as f:
    f.write(f"""Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c {mountbatpath}"
oShell.Run strArgs, 0, false
""")

# Create a .bat file that runs the script
with open("Scripts/MountOneDrive.bat", "w") as f:
    f.write(f"""@echo off
rclone mount onedrive-rclone: "{onedrive_path}" --vfs-cache-mode full
""")
    
# Create a scheduled task to run silently at startup
subprocess.run([
    "schtasks", "/create", "/tn", "OneDriveRclone", "/tr", f'"{runvbspath}"',
    "/sc", "onlogon", "/rl", "highest", "/f"
], shell=True)

print("\nOneDrive Rclone wordt nu gestart bij het opstarten van de computer.")

print(f"Herstart de computer om OneDrive automatisch te mounten op {onedrive_path}")
print("Verwijder de bestanden in de folder Scripts NIET, deze zijn nodig om OneDrive met Rclone te starten")
print("Klaar!")
input("Druk op Enter om af te sluiten...")