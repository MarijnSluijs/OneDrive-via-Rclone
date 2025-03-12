Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c C:\Users\sluij\OneDrive\Documents\Projects\OneDrive via Rclone\Scripts\MountOneDrive.bat"
oShell.Run strArgs, 0, false
