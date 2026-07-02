' Launch_Dashboard.vbs
' Silently runs Run_Dashboard.bat in the background without showing a terminal window.
' Double-click THIS file for the cleanest experience.

Set objShell = CreateObject("WScript.Shell")
strPath = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
objShell.CurrentDirectory = strPath
objShell.Run "cmd /c """ & strPath & "\Run_Dashboard.bat""", 0, False
