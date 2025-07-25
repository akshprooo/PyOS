# this will be how the JellyBean kernel interacts with the user for now,
# we will implement a shell like cmd or maybe a more advanced shell later
# for now, we will just print messages to the console and log them
# and we will use the utils module for logging and other utility functions

from os import system, name

from termcolor import cprint

def Shell():
    print("Welcome to the JellyBean Kernel Shell!")
    print("Type 'help' for a list of commands.")

    while True:
        command = input("JellyBean $> ")
        if command == "help":
            print("Available commands:")
            print("cls - Clear the screen")
            print("help - Show this help message")
            print("exit - Exit the shell")

        elif command == "exit":
            cprint("Exiting the JellyBean Kernel Shell. Goodbye!", 'red')
            break
        
        elif command == 'cls':
            if name == 'nt':
                system('cls')
            else:
                system('clear')
        
        else:
            print("Unknown command:", command)