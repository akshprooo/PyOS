# ToDo: Implement the main functionality of the JellyBean kernel

from os import system, name
import CLI
from termcolor import colored, cprint

def main():
    system("clear" if name != 'nt' else "cls")
    cprint("Starting JellyBean Kernel...", 'green')
    CLI.Shell()

if __name__ == "__main__":
    main()