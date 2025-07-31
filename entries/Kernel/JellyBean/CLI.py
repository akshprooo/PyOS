# this will be how the JellyBean kernel interacts with the user for now,
# we will implement a shell like cmd or maybe a more advanced shell later
# for now, we will just print messages to the console and log them
# and we will use the utils module for logging and other utility functions

from os import system, name
from fs import fs

def Shell():
    print("Welcome to the JellyBean Kernel Shell!")
    print("Type 'help' for a list of commands.")

    while True:
        command = input("JellyBean $> " + fs.current_folder + " > ").strip()
        if command == "help":
            print("Available commands:")
            print("cls - Clear the screen")
            print("help - Show this help message")
            print("exit - Exit the shell")

        elif command == "exit":
            print("Exiting the JellyBean Kernel Shell. Goodbye!")
            break
        
        elif command == 'cls':
            if name == 'nt':
                system('cls')
            else:
                system('clear')
        elif command.startswith('mkdir '):
            folder_name = command.split(' ', 1)[1]
            fs.createFolder(folder_name)
        elif command.startswith('cd '):
            folder_name = command.split(' ', 1)[1]
            try:
                fs.changeDirectory(folder_name)
            except Exception as e:
                print(e)
        elif command == 'ls':
            contents = fs.list_contents()
            current = fs.current_folder.strip('/')

            print("Folders:")
            for folder in contents['folders']:
                # Only show folders in the current path
                if current == '' or folder.startswith(current + '/'):
                    # Show only immediate subfolder
                    parts = folder.strip().split('/')
                    if len(parts) == 1 and current == '':
                        print(" -", parts[0])
                    elif len(parts) == 2 and parts[0] == current:
                        print(" -", parts[1])

            print("Files:")
            for file in contents['files']:
                # Only show files in the current folder
                if current == '' or file.startswith(current + '/'):
                    parts = file.strip().split('/')
                    if len(parts) == 1 and current == '':
                        print(" -", parts[0])
                    elif len(parts) == 2 and parts[0] == current:
                        print(" -", parts[1])
        else:
            print("Unknown command:", command)