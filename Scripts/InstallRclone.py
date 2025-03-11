import subprocess

# Download winfsp with winget
print("\nWinFSP downloaden...")
subprocess.run(["winget", "install", "-e", "--id", "WinFsp.WinFsp", "--accept-source-agreements", "--accept-package-agreements"])

# Download rclone with winget
print("\nRclone downloaden...")
subprocess.run(["winget", "install", "-e", "--id", "Rclone.Rclone", "--accept-source-agreements", "--accept-package-agreements"])