SET mypath=%~dp0
SET path_to_index=%mypath:~0,-1%\..\index.html
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %path_to_index%  --args -allow-file-access-from-files