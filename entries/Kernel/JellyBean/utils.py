# this file would contain utility functions for the JellyBean kernel
# such as logging, error handling, and other helper functions

def log(message):
    with open("jellybean.log", "a") as log_file:
        log_file.write(message + "\n")