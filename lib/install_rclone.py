import tkinter as tk
from tkinter import ttk
import subprocess

def install_rclone():
    install_button["state"] = "disabled"
    progress.pack(pady=10)
    root.update_idletasks()

    subprocess.run(["winget", "install", "-e", "--id", "WinFsp.WinFsp", "--accept-source-agreements", "--accept-package-agreements"])
    progress["value"] = 50
    root.update_idletasks()

    subprocess.run(["winget", "install", "-e", "--id", "Rclone.Rclone", "--accept-source-agreements", "--accept-package-agreements"])
    progress["value"] = 100
    finish_label.pack()
    config_label.pack()
    finish_button.pack(pady=10)
    root.update_idletasks()

root = tk.Tk()
root.title("Rclone Installer")
root.geometry("500x400")

tk.Label(root, text="Rclone & WinFsp installeren", font=("Arial", 14)).pack(pady=10)
status_label = tk.Label(root, text="Klik 'Start installatie' om de installatie van Rclone en WinFsp te starten. \nWinFsp is nodig om Rclone te laten werken op Windows.", font=("Arial", 10))
status_label.pack()
install_button = ttk.Button(root, text="Start installatie", command=install_rclone)
install_button.pack(pady=20)
progress = ttk.Progressbar(root, length=300, mode="determinate")
finish_label = tk.Label(root, text="Installatie geslaagd.", font=("Arial", 10))
config_label = tk.Label(root, text="Start 'OneDrive via Rclone configureren.exe' om OneDrive via Rclone te configureren.", font=("Arial", 10))
finish_button = ttk.Button(root, text="Sluiten", command=root.quit)

root.mainloop()