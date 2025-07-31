# File System
mounted = False
mount_point = None
current_folder = '/'


def set_current_folder(folder):
    global current_folder
    if mounted:
        current_folder = folder
    else:
        raise Exception("File system is not mounted!")

def mount_fs(mp):
    if not mounted:
        with open('fs.config', 'w') as f:
            f.write("mounted=True\n")
            f.write("mount_point={}\n".format(mp))
        get_mount_info()  # Refresh mount info
        return {mounted: True, mount_point: mp}
    else:
        raise Exception("File system already mounted at {}".format(mount_point))

def unmount_fs():
    if mounted:
        with open('fs.config', 'w') as f:
            f.write("mounted=False\n")
            f.write("mount_point=None\n")
        get_mount_info()  # Refresh mount info
        return {mounted: False, mount_point: None}
    else:
        raise Exception("File system is not even mounted!")

def createFolder(folder_name):
    if mounted:
        set_current_folder(current_folder + folder_name + '/')
        return current_folder
    else:
        raise Exception("File system is not mounted!")

def getFolderContents():
    if mounted:
        with open('entries/Kernel/JellyBean/fs/storage.txt', 'r') as f:
            lines = f.readlines()
            folders = []
            files = []
            for line in lines:
                if line.startswith("folders="):
                    folders = line.split('=')[1].strip().split(',')
                elif line.startswith("files="):
                    files = line.split('=')[1].strip().split(',')
            return [folders, files]
    else:
        raise Exception("File system is not mounted!")


def changeDirectory(folder_name):
    if not mounted:
        raise Exception("File system is not mounted!")

    global current_folder

    if folder_name == '..':
        if current_folder != '/':
            set_current_folder('/'.join(current_folder.strip('/').split('/')[:-1]) + '/')
        return current_folder

    folders = getFolderContents()[0]
    current = current_folder.strip('/')

    # Generate full target path to match
    if current == '':
        full_path = folder_name.strip('/')
    else:
        full_path = current + '/' + folder_name.strip('/')

    matched = False
    for folder in folders:
        if folder.strip().strip('/') == full_path:
            matched = True
            break

    if matched:
        set_current_folder('/' + full_path + '/')
    else:
        print("Folder not found:", folder_name)

    return current_folder



def list_contents():
    if mounted:
        contents = getFolderContents()
        folders = contents[0]
        files = contents[1]
        return {
            'folders': [folder.strip() for folder in folders if folder.strip()],
            'files': [file.strip() for file in files if file.strip()]
        }
    else:
        raise Exception("File system is not mounted!")

# Code to get the Mount and Mount Point from fs.config
def get_mount_info():
    global mounted, mount_point
    try:
        with open('fs.config', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('mounted='):
                    mounted = line.split('=')[1].strip() == 'True'
                elif line.startswith('mount_point='):
                    mount_point = line.split('=')[1].strip()
    except FileNotFoundError:
        print("fs.config not found. Using default values.")
        mounted = False
        mount_point = None

get_mount_info()