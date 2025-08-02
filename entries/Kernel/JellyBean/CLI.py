from os import system, name
import fs.fs as fs

def Shell():
    print("Welcome to the JellyBean Kernel Shell!")
    print("Type 'help' for a list of commands.")

    while True:
        try:
            command = input("JellyBean $> " + fs.current_folder + " > ").strip()
            
            if not command:
                continue
                
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd == "help":
                print("Available commands:")
                print("  help          - Show this help message")
                print("  exit          - Exit the shell")
                print("  cls/clear     - Clear the screen")
                print("  mount <path>  - Mount the filesystem")
                print("  unmount       - Unmount the filesystem")
                print("  mkdir <name>  - Create a directory")
                print("  cd <path>     - Change directory")
                print("  ls/dir        - List directory contents")
                print("  pwd           - Print working directory")
                print("  touch <file>  - Create an empty file")
                print("  cat <file>    - Display file contents")
                print("  echo <text>   - Print text or redirect to file with >")
                print("  rm <file>     - Remove a file")
                print("  rmdir <dir>   - Remove a directory")

            elif cmd == "exit":
                print("Exiting the JellyBean Kernel Shell. Goodbye!")
                break
                
            elif cmd == 'cls' or cmd == 'clear':
                if name == 'nt':
                    system('cls')
                else:
                    system('clear')
                    
            elif cmd == 'mount':
                if len(parts) > 1:
                    try:
                        result = fs.mount_fs(parts[1])
                        print(f"Mounted filesystem at {parts[1]}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Usage: mount <mount_point>")
                    
            elif cmd == 'unmount':
                try:
                    fs.unmount_fs()
                    print("Filesystem unmounted")
                except Exception as e:
                    print(f"Error: {e}")
                    
            elif cmd == 'mkdir':
                if len(parts) > 1:
                    try:
                        fs.createFolder(parts[1])
                        print(f"Created folder: {parts[1]}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Usage: mkdir <folder_name>")
                    
            elif cmd == 'cd':
                if len(parts) > 1:
                    try:
                        fs.changeDirectory(parts[1])
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Usage: cd <folder_name>")
                    
            elif cmd == 'ls' or cmd == 'dir':
                try:
                    contents = fs.list_contents()
                    current = fs.current_folder.strip('/')

                    if contents['folders']:
                        print("Folders:")
                        for folder in contents['folders']:
                            print(f"  {folder}/")
                            
                    if contents['files']:
                        print("Files:")
                        for file in contents['files']:
                            print(f"  {file}")
                            
                    if not contents['folders'] and not contents['files']:
                        print("Directory is empty")
                except Exception as e:
                    print(f"Error: {e}")
                    
            elif cmd == 'pwd':
                print(fs.current_folder)
                
            elif cmd == 'touch':
                if len(parts) > 1:
                    try:
                        fs.createFile(parts[1])
                        print(f"Created file: {parts[1]}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Usage: touch <file_name>")
                    
            elif cmd == 'cat':
                if len(parts) > 1:
                    try:
                        content = fs.readFile(parts[1])
                        print(content)
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Usage: cat <file_name>")
                    
            elif cmd == 'echo':
                if len(parts) > 2 and '>' in command:
                    try:
                        content_and_redirect = ' '.join(parts[1:])
                        if '>' in content_and_redirect:
                            content, file_part = content_and_redirect.split('>', 1)
                            file_name = file_part.strip()
                            content = content.strip().strip('"\'')
                            fs.writeFile(file_name, content)
                            print(f"Written to {file_name}")
                        else:
                            print(' '.join(parts[1:]))
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    if len(parts) > 1:
                        print(' '.join(parts[1:]))
                    else:
                        print()
                        
            elif cmd == 'rm':
                if len(parts) > 1:
                    try:
                        fs.removeFile(parts[1])
                        print(f"Removed file: {parts[1]}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Usage: rm <file_name>")
                    
            elif cmd == 'rmdir':
                if len(parts) > 1:
                    try:
                        fs.removeFolder(parts[1])
                        print(f"Removed folder: {parts[1]}")
                    except Exception as e:
                        print(f"Error: {e}")
                else:
                    print("Usage: rmdir <folder_name>")
                    
            else:
                print("Unknown command:", command)

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit the shell.")
        except EOFError:
            print("\nExiting the JellyBean Kernel Shell. Goodbye!")
            break

if __name__ == "__main__":
    Shell()