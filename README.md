# book-room-Chalmers
Script that books specified rooms at a wanted time given an user, e.g. room 1215B at 10:00 to 13:00

This script needs your Chalmers login information to be used since to book a room, you need to be logged in. To not have your username and password in plain code, some security measurements have been implemented such that the passwords are encrypted with a key that is saved in windows credentials. Someone with enough knowledge could potentially get the key from the credential manager but it requires more work than if it was in plain text in the code.

# Step 1: Generate key

Locate generate_password.py in helper directory. Enter your Chalmers password as a string to the variable password. Run the file and:

- Copy encrypted password and paste it in the grupprum_executable.py file in the users list together with your cid mail (just as in "helper\grupprum_executable_example.py")
- Copy the generated key as this is needed to decrypt your password. 

# Step 2: Save key in the Credential manager

1. open "Credential magager"
2. click "Windows Credentials"
3. click "Add a generic credential"
4. Write "Fernet" to the "Internet or network address" field
5. User name: "key"
6. Paste your copied key to the password field.
7. Done, close credential manager

Your key is now saved on your system. This means that if someone gets ahold of your code, they wont be able to decrypt your password since they don't have the decrypt key that is located on your system.

# Step 3: Fill all the fields in grupprum_executable.py

In grupprum_executable.py there are several variables that needs to be specified. In the helper directory there exists an example of this file and how to specify the variables.

# Step 4: Update the .bat file (Optional)

In the .bat file there are two paths that need to be specified. One is to your python.exe file which either can be in a venv or in your global python directory. The other path is to grupprum_executable.py. In the bat file there is an example on how this is done.

The .bat file is needed if you want the script to run automatically, otherwise it is fine to just run the grupprum_executable.py when needed.

# Step 4: Create a task in Task Scheduler (Optional)

Open Task Scheduler and click "Create basic task". Name it what you like and set the trigger to daily set the time at eg. 01:00, set the action to start a program and paste the full path to the .bat file. To make it run as soon as you logg in to the computer, find the task in the library, select it and click properties. Thereon you need to go to the settings tab and click the box "Run as soon as possible after a scheduled start is missed"
