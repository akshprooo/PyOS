import os
import subprocess
import py_cui

BOOT_DIR = "./entries"

selected_script = None
menu_widget = None

def get_boot_entries():
    return [f for f in os.listdir(BOOT_DIR) if f.endswith(".pyboot")]

def select_script(root):
    global selected_script, menu_widget
    selected_script = menu_widget.get()
    root.stop()

def exit_program(root):
    global selected_script
    selected_script = None
    root.stop()

def start_tui():
    global menu_widget

    scripts = get_boot_entries()

    root = py_cui.PyCUI(4, 2)
    root.set_title("Python Boot Manager")

    menu_widget = root.add_scroll_menu("Available Boot Scripts", 0, 0, row_span=4, column_span=2)
    menu_widget.add_item_list(scripts)

    menu_widget.add_key_command(py_cui.keys.KEY_ENTER, lambda: select_script(root))
    root.add_key_command(py_cui.keys.KEY_Q_LOWER, lambda: exit_program(root))

    root.start()

def main():
    start_tui()

    if selected_script:
        with open(os.path.join(BOOT_DIR, selected_script), 'r') as script_file:
            script_content = script_file.readlines()
            for line in script_content:
                line = line.strip().split(':')
                global kernel_path, os_name, os_ver
                if line[0] == "kernel":
                    kernel_path = line[1].strip()
                elif line[0] == "NAME":
                    os_name = line[1].strip()
                elif line[0] == "VER":
                    os_ver = line[1].strip()
    
    print(f"Selected OS: {os_name} Version: {os_ver}, kernel: {kernel_path}")
    print("Booting into the selected OS...")

    if kernel_path:
        global main_file
        with open(f'{BOOT_DIR}/{kernel_path}/config.pyos', 'r') as config_file:
            config_content = config_file.readlines()
            for line in config_content:
                if line.startswith("main_file:"):
                    main_file = line.split(':')[1].strip()
                    break
            else:
                main_file = "main.py"
            
            try:
                subprocess.run(['python', f'{BOOT_DIR}/{kernel_path}/{main_file}'])
            except FileNotFoundError:
                print("Main file not found.")
            except Exception as e:
                print(f"Error running the main file: {e}")


if __name__ == "__main__":
    main()