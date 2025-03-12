import subprocess
import os
import ctypes
import sys
import tkinter as tk
from tkinter import filedialog, ttk

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

def uninstall():
    # Remove winfsp
    subprocess.run(["winget", "uninstall", "WinFsp.WinFsp"])
    # Remove rclone onedrive mount
    subprocess.run(["rclone", "config", "delete", "onedrive-rclone"])
    # Remove rclone
    subprocess.run(["winget", "uninstall", "Rclone.Rclone"])
    # Remove task scheduler task
    os.system(f'schtasks /delete /tn "OneDrive via Rclone" /f')

    # Remove scripts in the AppData folder
    scripts_path = os.path.expandvars("%APPDATA%") + "\OneDrive via Rclone"
    os.system(f'rmdir /s /q "{scripts_path}"')
    remove_button["state"] = "disabled"
    finish_login_label.pack()
    finish_login_button.pack(pady=10)

root = tk.Tk()
root.title("OneDrive via Rclone verwijderen")
root.geometry("500x400")

# Pagina 1 (inloggen met OneDrive)
page1_label = tk.Label(root, text="OneDrive via Rclone verwijderen", font=("Arial", 14))
page1_label.pack(pady=10)
remove_label = tk.Label(root, text="Klik 'Verwijderen' om OneDrive via Rclone te verwijderen van uw computer.", font=("Arial", 10))
remove_label.pack()
remove_button = ttk.Button(root, text="Verwijderen", command=uninstall)
remove_button.pack(pady=20)
finish_login_label = tk.Label(root, text="OneDrive via Rclone is succesvol verwijderd.", font=("Arial", 10))
finish_login_button = ttk.Button(root, text="Sluiten", command=root.quit)

root.mainloop()