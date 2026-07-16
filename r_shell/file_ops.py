import os 
import shlex 
from pathlib import Path
import shutil 
import sys 
import subprocess 
from autocomplete import setup_autocomplete
from history import setup_history, save_history 
from loader import load_plugins 
from script_loader import find_script
RED = "\033[1;31m"
RESET = "\033[0m"

big_r = """
RRRRRRRRRRRRRRR   
R::::::::::::::::R  
R::::::RRRRRR:::::R 
RR:::::R     R:::::R
  R::::R     R:::::R
  R::::R     R:::::R
  R::::RRRRRR:::::R 
  R:::::::::::::RR  
  R::::RRRRRR:::::R 
  R::::R     R:::::R
  R::::R     R:::::R
  R::::R     R:::::R
RR:::::R     R:::::R
R::::::R     R:::::R
R::::::::    ::::::::R
RRRRRRRR    RRRRRRRR
"""





clipboard = {
    "mode":None, # copy or paste mode
    "items": [] 
}
def copy_item(*args):
    global clipboard

    if not args:
        print("Usage: copy <file>")
        return

    clipboard["mode"] = "copy"
    clipboard["items"] = [current_dir / item for item in args]

    print("Copied:", args) 

def cut_item(*args):
    global clipboard

    if not args:
        print("Usage: cut <file>")
        return

    clipboard["mode"] = "cut"
    clipboard["items"] = [current_dir / item for item in args]

    print("Cut:", args) 
def paste_item(*args):
    global clipboard

    if not clipboard["items"]:
        print("Clipboard empty")
        return

    for item in clipboard["items"]:
        target = current_dir / item.name

        if clipboard["mode"] == "copy":
            if item.is_dir():
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                shutil.copy2(item, target, exist_ok=True)

        elif clipboard["mode"] == "cut":
            shutil.move(str(item), str(target))

    print("Pasted")
    clipboard["items"] = []
    clipboard["mode"] = None 
def resolve_conflict(path):
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    counter = 1

    while True:
        new_name = f"{stem} ({counter}){suffix}"
        new_path = parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1 
def zip_item(*args):
    if not args:
        print("Usage: zip <folder>")
        return

    for item in args:
        path = current_dir / item

        if path.exists() and path.is_dir():
            shutil.make_archive(str(path), "zip", str(path))
            print("Zipped:", item)

def resolve_trash_conflict(path):
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    counter = 1

    while True:
        new_name = f"{stem} ({counter}){suffix}"
        new_path = parent / new_name

        if not new_path.exists():
            return new_path

        counter += 1   








def get_current_dir():
    return current_dir


current_dir= Path.home() 
def welcome_text():
    print("welcome to R a hybrid shell like environment that combines simple python commands with bash (type 'help' for a list of commands and their use)") 
def show_banner():
    print(RED + big_r + RESET)
def exit_program():
   save_history() 
   sys.exit() 


    
def show_location():
    print(f"You are here: {current_dir}") 
def list_files():
    for item in current_dir.iterdir():
        print(item.name) 
from pathlib import Path

def change_dir(*args):
    global current_dir

    if not args:
        current_dir = Path.home()
        return

    folder = args[0]

    if folder == "~":
        current_dir = Path.home()
        return

    path = Path(folder)

    # absolute path check (CORRECT)
    if path.is_absolute():
        new_path = path
    else:
        new_path = current_dir / path

    new_path = new_path.resolve()

    if new_path.exists() and new_path.is_dir():
        current_dir = new_path
    else:
        print("Folder NOT found:", new_path)
def move_back():
    global current_dir
    current_dir = current_dir.parent 
def go_home():
    global current_dir
    current_dir=Path.home() 
def open_item(*args):
    if not args:
        print("Usage: open <file>")
        return

    path = current_dir / args[0]

    if path.exists():
        subprocess.run(["xdg-open", str(path)])
    else:
        print("Not found") 
def delete_item(*args):
    trash = Path.home() / ".local/share/Trash/files"

    if not args:
        print("usage: delete <file>")
        return

    trash.mkdir(parents=True, exist_ok=True)

    for item in args:
        path = current_dir / item

        if path.exists():
            target = trash / path.name
            target = resolve_trash_conflict(target)

            shutil.move(str(path), str(target))
            print("Moved to trash:", path.name)

        else:
            print("Not found:", path)
def create_dir(*args):
    if not args :
        print("Usage: mkdir <file>")
        return
    path=current_dir / args[0] 
    for item in args:
     path = current_dir / item
     path.mkdir(exist_ok=True)
     print("Created directory:", path) 
def create_file(*args):
    if not args:
        print("Usage:touch <file>")
        return
    path=current_dir / args[0]
    for item in args :
        path=current_dir / item 
        path.touch(exist_ok=True)
        print("created file(s)", path)
def empty_trash():
    trash=Path.home() / ".local/share/Trash/files"
    if not trash.exists():
        print("Trash has no contents")
        return

    confirmation= input ("Empty Trash bin ? Y/n")
    if confirmation.lower().strip() == "y":
        for item in trash.iterdir():
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            except Exception as e :
                print(f"failed to delete {item}:{e}")
        print("Trash emptied")
    else:
        print("user gave no confirmation did nothing")

    
    
        



    



commands= {"pwd":show_location,
 "show_banner":show_banner,
"exit":exit_program,
 "list_files":list_files,
 "cd":change_dir,
 "ls":list_files,
 "cd..":move_back,
 "cd ~":go_home,
 "open":open_item,
 "delete":delete_item,
 "touch":create_file,
 "mkdir":create_dir,
 "copy":copy_item,
 "cut": cut_item,
 "paste": paste_item,
 "zip":zip_item,
 "empty_trash":empty_trash,
}
show_banner() 
welcome_text() 
load_plugins(commands) 
 

setup_history() 
setup_autocomplete(commands,get_current_dir) 
try:
    while True:
        parts = shlex.split(input(f"{current_dir} > ").strip())

        if not parts:
            continue

        cmd = parts[0]
        args = parts[1:]

        if cmd in commands:
            commands[cmd](*args)

        else:
            script = find_script(cmd)

            if script:
                subprocess.run([str(script), *args]) 

            else:
                try:
                    subprocess.run(parts)

                except FileNotFoundError:
                    print("Unknown command")

except KeyboardInterrupt:
    print("\nUse 'exit' to quit R")

except EOFError:
    save_history()
    sys.exit() 


