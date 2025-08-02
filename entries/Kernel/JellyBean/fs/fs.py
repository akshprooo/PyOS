import json
import os

mounted = False
mount_point = None
current_folder = '/'
storage_file = 'entries/Kernel/JellyBean/fs/storage.json'
config_file = 'fs.config'

def load_config():
    global mounted, mount_point
    try:
        with open(config_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('mounted='):
                    mounted = line.split('=')[1].strip() == 'True'
                elif line.startswith('mount_point='):
                    mount_point = line.split('=')[1].strip()
                    if mount_point == 'None':
                        mount_point = None
    except FileNotFoundError:
        mounted = False
        mount_point = None

def save_config():
    with open(config_file, 'w') as f:
        f.write(f"mounted={mounted}\n")
        f.write(f"mount_point={mount_point}\n")

def load_storage():
    try:
        with open(storage_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'folders': [], 'files': {}}

def save_storage(data):
    os.makedirs(os.path.dirname(storage_file), exist_ok=True)
    with open(storage_file, 'w') as f:
        json.dump(data, f, indent=2)

def normalize_path(path):
    return '/' + path.strip('/') if path.strip('/') else '/'

def mount_fs(mp):
    global mounted, mount_point
    if not mounted:
        mounted = True
        mount_point = mp
        save_config()
        return {'mounted': True, 'mount_point': mp}
    else:
        raise Exception(f"File system already mounted at {mount_point}")

def unmount_fs():
    global mounted, mount_point
    if mounted:
        mounted = False
        mount_point = None
        save_config()
        return {'mounted': False, 'mount_point': None}
    else:
        raise Exception("File system is not even mounted!")

def set_current_folder(folder):
    global current_folder
    if mounted:
        current_folder = folder
    else:
        raise Exception("File system is not mounted!")

def createFolder(folder_name):
    global current_folder
    if not mounted:
        raise Exception("File system is not mounted!")
    
    data = load_storage()
    
    if current_folder == '/':
        new_path = '/' + folder_name.strip('/')
    else:
        new_path = current_folder.rstrip('/') + '/' + folder_name.strip('/')
    
    new_path = normalize_path(new_path)
    
    if new_path not in data['folders']:
        data['folders'].append(new_path)
        save_storage(data)
    
    return new_path

def createFile(file_name, content=''):
    if not mounted:
        raise Exception("File system is not mounted!")
    
    data = load_storage()
    
    if current_folder == '/':
        file_path = '/' + file_name.strip('/')
    else:
        file_path = current_folder.rstrip('/') + '/' + file_name.strip('/')
    
    file_path = normalize_path(file_path)
    data['files'][file_path] = content
    save_storage(data)
    return file_path

def readFile(file_name):
    if not mounted:
        raise Exception("File system is not mounted!")
    
    data = load_storage()
    
    if current_folder == '/':
        file_path = '/' + file_name.strip('/')
    else:
        file_path = current_folder.rstrip('/') + '/' + file_name.strip('/')
    
    file_path = normalize_path(file_path)
    
    if file_path in data['files']:
        return data['files'][file_path]
    else:
        raise Exception(f"File not found: {file_name}")

def writeFile(file_name, content):
    if not mounted:
        raise Exception("File system is not mounted!")
    
    data = load_storage()
    
    if current_folder == '/':
        file_path = '/' + file_name.strip('/')
    else:
        file_path = current_folder.rstrip('/') + '/' + file_name.strip('/')
    
    file_path = normalize_path(file_path)
    data['files'][file_path] = content
    save_storage(data)

def changeDirectory(folder_name):
    global current_folder
    if not mounted:
        raise Exception("File system is not mounted!")

    if folder_name == '..':
        if current_folder != '/':
            parts = current_folder.strip('/').split('/')
            if len(parts) > 1:
                current_folder = '/' + '/'.join(parts[:-1])
            else:
                current_folder = '/'
        return current_folder

    if folder_name == '/':
        current_folder = '/'
        return current_folder

    data = load_storage()

    if current_folder == '/':
        target_path = '/' + folder_name.strip('/')
    else:
        target_path = current_folder.rstrip('/') + '/' + folder_name.strip('/')
    
    target_path = normalize_path(target_path)

    if target_path in data['folders'] or target_path == '/':
        current_folder = target_path
    else:
        raise Exception(f"Folder not found: {folder_name}")

    return current_folder

def list_contents():
    if not mounted:
        raise Exception("File system is not mounted!")

    data = load_storage()
    current_folders = []
    current_files = []

    for folder in data['folders']:
        if folder.startswith(current_folder) and folder != current_folder:
            relative_path = folder[len(current_folder):].strip('/')
            if relative_path and '/' not in relative_path:
                current_folders.append(relative_path)

    for file_path in data['files'].keys():
        if file_path.startswith(current_folder):
            relative_path = file_path[len(current_folder):].strip('/')
            if relative_path and '/' not in relative_path:
                current_files.append(relative_path)

    return {'folders': sorted(current_folders), 'files': sorted(current_files)}

def removeFolder(folder_name):
    if not mounted:
        raise Exception("File system is not mounted!")
    
    data = load_storage()
    
    if current_folder == '/':
        target_path = '/' + folder_name.strip('/')
    else:
        target_path = current_folder.rstrip('/') + '/' + folder_name.strip('/')
    
    target_path = normalize_path(target_path)
    
    if target_path in data['folders']:
        folders_to_remove = [f for f in data['folders'] if f.startswith(target_path)]
        files_to_remove = [f for f in data['files'].keys() if f.startswith(target_path)]
        
        for folder in folders_to_remove:
            data['folders'].remove(folder)
        
        for file_path in files_to_remove:
            del data['files'][file_path]
        
        save_storage(data)
    else:
        raise Exception(f"Folder not found: {folder_name}")

def removeFile(file_name):
    if not mounted:
        raise Exception("File system is not mounted!")
    
    data = load_storage()
    
    if current_folder == '/':
        file_path = '/' + file_name.strip('/')
    else:
        file_path = current_folder.rstrip('/') + '/' + file_name.strip('/')
    
    file_path = normalize_path(file_path)
    
    if file_path in data['files']:
        del data['files'][file_path]
        save_storage(data)
    else:
        raise Exception(f"File not found: {file_name}")

def getFolderContents():
    if not mounted:
        raise Exception("File system is not mounted!")
    
    data = load_storage()
    folders = data.get('folders', [])
    files = list(data.get('files', {}).keys())
    return [folders, files]

def get_mount_info():
    load_config()

get_mount_info()