import json
import subprocess
import re
import os
import tkinter as tk
from tkinter import filedialog, ttk
import ctypes
import sys

def authorize_onedrive_with_rclone():
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
    login_button["state"] = "disabled"
    finish_login_label.pack()
    finish_login_button.pack(pady=10)

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

def go_to_page2():
    # page1
    page1_label.pack_forget()
    status_label.pack_forget()
    login_button.pack_forget()
    finish_login_label.pack_forget()
    finish_login_button.pack_forget()
    # page 2
    page2_label.pack(pady=10)
    mount_label.pack()
    mount_path_label.pack()
    mount_path_button.pack(pady=10)
    finish_mount_label.pack()
    finish_mount_button.pack(pady=10)
    # page 3
    page3_label.pack_forget()
    terug_button.pack_forget()
    autostart_label.pack_forget()
    autostart_button.pack_forget()
    scriptslocation_label.pack_forget()
    quit_button.pack_forget()

def go_to_page3():
    # page 2
    page2_label.pack_forget()
    mount_label.pack_forget()
    mount_path_label.pack_forget()
    mount_path_button.pack_forget()
    finish_mount_label.pack_forget()
    finish_mount_button.pack_forget()
    # page 3
    page3_label.pack(pady=10)
    terug_button.pack(pady=10)
    autostart_button["state"] = "normal"
    autostart_label.pack()
    autostart_button.pack(pady=10)

def start_rclone_automatically():
    onedrive_path = str(mount_path.get()) + "\OneDrive via Rclone"
    # Use AppData folder for scripts_path
    scripts_path = os.path.expandvars("%APPDATA%") + "\OneDrive via Rclone"
    mountvbspath = str(scripts_path) + "\MountOneDrive.vbs"
    mountbatpath = str(scripts_path) + "\MountOneDrive.bat"
    if not os.path.exists(scripts_path):
        os.makedirs(scripts_path)

    if not os.path.exists(mountvbspath):
        open(mountvbspath, "w").close()
    if not os.path.exists(mountbatpath):
        open(mountbatpath, "w").close()

    # Create a .vbs file that runs MountOneDrive.bat silently
    with open(mountvbspath, "w") as f:
        f.write(f'''Set oShell = CreateObject ("Wscript.Shell") 
    Dim strArgs
    strArgs = "cmd /c ""{mountbatpath}"""
    oShell.Run strArgs, 0, false
    ''')

    # Create a .bat file that runs the script
    with open(mountbatpath, "w") as f:
        f.write(f"""@echo off
    rclone mount onedrive-rclone: "{onedrive_path}" --vfs-cache-mode full
    """)
        
    # Create a scheduled task to run wscript.exe with argument mountvbspath in the AppData folder
    subprocess.run([
        "schtasks", "/create", "/tn", "OneDrive via Rclone", "/tr", f'wscript "{mountvbspath}"',
        "/sc", "onlogon", "/rl", "highest", "/f"
    ], shell=True)
        
    autostart_button["state"] = "disabled"
    terug_button["state"] = "disabled"
    scriptslocation_label.pack()
    quit_button.pack(pady=10)

def change_mount_path():
    path = filedialog.askdirectory()
    if path:
        mount_path.set(path)
        global onedrive_path
        onedrive_path = path

root = tk.Tk()
root.title("OneDrive via Rclone configureren")
root.geometry("500x400")

# Pagina 1 (inloggen met OneDrive)
page1_label = tk.Label(root, text="Rclone toegang geven tot OneDrive", font=("Arial", 14))
page1_label.pack(pady=10)
status_label = tk.Label(root, text="Klik 'Inloggen met OneDrive' om Rclone toegang te geven tot uw OneDrive account.\nU moet inloggen met uw persoonlijke Microsoft Account.", font=("Arial", 10))
status_label.pack()
login_button = ttk.Button(root, text="Inloggen met OneDrive", command=authorize_onedrive_with_rclone)
login_button.pack(pady=20)
finish_login_label = tk.Label(root, text="Inloggen geslaagd.", font=("Arial", 10))
finish_login_button = ttk.Button(root, text="Volgende", command=go_to_page2)

# Pagina 2 (mountlocatie van OneDrive)
# Give the default mount location and a button to change the path
page2_label = tk.Label(root, text="Kies een locatie om OneDrive te mounten", font=("Arial", 14))
mount_label = tk.Label(root, text="Standaard wordt OneDrive gemount in uw gebruikersmap.\nWilt u een andere locatie kiezen, klik dan op Wijzigen.", font=("Arial", 10))
mount_path = tk.StringVar(value=os.path.expanduser("~"))
print("Mount path: " + str(mount_path.get()))
mount_path_label = tk.Label(root, textvariable=mount_path, font=("Arial", 10))
finish_mount_label = tk.Label(root, text="Op de gekozen locatie wordt een map aangemaakt genaamd 'OneDrive via Rclone',\nhierin komen uw OneDrive bestanden.", font=("Arial", 10))
mount_path_button = ttk.Button(root, text="Wijzigen", command=change_mount_path)
finish_mount_button = ttk.Button(root, text="Volgende", command=go_to_page3)

# Pagina 3 (OneDrive via Rclone automatisch opstarten)
page3_label = tk.Label(root, text="Rclone automatisch opstarten", font=("Arial", 14))
terug_button = ttk.Button(root, text="Terug", command=go_to_page2)
autostart_label = tk.Label(root, text="Klik op 'Volgende' om Rclone automatisch op te starten\nbij het starten van uw computer.", font=("Arial", 10))
autostart_button = ttk.Button(root, text="Volgende", command=start_rclone_automatically)
scriptslocation_label = tk.Label(root, text="Configuratie geslaagd! Start uw computer opnieuw op om OneDrive via Rclone\n te starten. De OneDrive folder kan na herstart worden gevonden op deze locatie:\n'" + str(mount_path.get()) + "\OneDrive via Rclone'", font=("Arial", 10))
quit_button = ttk.Button(root, text="Configuratie afsluiten", command=root.quit)

root.mainloop()