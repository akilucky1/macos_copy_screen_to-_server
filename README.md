# For MacOS sending screenshots to a server using SFTP
## This script will upload any new file in certain directory to a server
Then it will craate link, that will be inserted into a clipboard.

Notification will be shown. 

Original screenshot will be deleted after the upload. 

## Please don't forget to install the modules from PIP
I have automated it through AUTOMATOR app by running this script on startup 
-------------------------------------
AUTOMATOR Steps:

Create a New Automator Application:

Open Automator from the Applications folder.
Choose New Document.
Select Application as the document type.
Add a “Run Shell Script” Action:

In the left pane of Automator, search for Run Shell Script.
Drag the Run Shell Script action to the workflow area.
Configure the Script:

In the Run Shell Script box, type the following:
bash

/usr/bin/python3 /path/to/your/script/copyToServer.py

Replace /path/to/your/script/copyToServer.py with the actual path to your Python script. You can drag the Python file from Finder into the Automator window to get the full path.

Save the Automator Application:

Go to File → Save.
Choose a name for your application, like copyToServer.app, and save it in a location such as Applications or ~/Applications (for easy access).

Add the Application to Login Items:

Open System Preferences → Users & Groups.
Select your user account.
Go to the Login Items tab.
Click the + button and navigate to the Automator application you just created.
Add the application to the list.
Test the Script:
Now, when you restart your Mac or log in, your Python script should run automatically.


Libraries
--------------------------
```pip3 install paramiko pyperclip watchdog pync```

This will install:

paramiko: For SSH functionality (secure file transfers, executing commands over SSH, etc.)

pyperclip: For clipboard manipulation (copying and pasting)

watchdog: For monitoring file system events (like file changes)

pync: For sending macOS desktop notifications

