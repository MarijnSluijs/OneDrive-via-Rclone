import subprocess
import os
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

# Remove winfsp
print("Removing WinFSP...")
subprocess.run(["winget", "uninstall", "WinFsp.WinFsp"])
# Remove rclone onedrive mount
print("Removing rclone mount...")
subprocess.run(["rclone", "config", "delete", "onedrive-rclone"])
# Remove rclone
print("Removing rclone...")
subprocess.run(["winget", "uninstall", "Rclone.Rclone"])
# Remove task scheduler task
print("Removing task scheduler task...")
os.system("schtasks /delete /tn OneDriveRclone /f")
input("Druk op Enter om af te sluiten...")