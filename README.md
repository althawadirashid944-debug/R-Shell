# R-Shell
# R

> A hybrid shell environment that combines custom Python commands with existing Linux shell commands.

> **Status:** Early development / Heavy WIP

## Overview

R is an experimental shell-like environment written in Python.

Instead of replacing your existing Linux tools, R extends them. It provides built-in Python commands for common file operations while allowing you to execute normal system commands seamlessly.



## Current Features

* Custom Python command system
* Linux command fallback (`subprocess`)
* File management commands
* Command history
* Tab autocomplete
* Current working directory tracking
* Clipboard system (Copy/Cut/Paste)
* Safe trash instead of permanent deletion
* ZIP archive creation
* Open files using the default application (`xdg-open`)

## Built-in Commands

| Command         | Description                               |
| --------------- | ----------------------------------------- |
| `ls`            | List files in the current directory       |
| `pwd`           | Show current directory                    |
| `cd <dir>`      | Change directory                          |
| `cd..`          | Move to the parent directory              |
| `touch <file>`  | Create file(s)                            |
| `mkdir <dir>`   | Create directory(ies)                     |
| `copy <file>`   | Copy file(s)                              |
| `cut <file>`    | Cut file(s)                               |
| `paste`         | Paste copied/cut items                    |
| `delete <file>` | Move file(s) to the Trash                 |
| `zip <folder>`  | Create a ZIP archive                      |
| `open <file>`   | Open a file using the default application |
| `empty_trash`   | Empty the user's Trash                    |
| `exit`          | Exit R                                    |

If a command is not built into R, it is executed as a normal Linux command whenever possible.

Example:

```text
> fastfetch
> git status
> python script.py
> echo Hello
```

## Installation

Clone the repository:

```bash
git clone  https://github.com/althawadirashid944-debug/R-Shell.git 
cd R-Shell
```

Run:

```bash
python file_ops.py
```
OR you could install it as a global command (still in works ) :
```bash 
cd R-Shell
cd r_shell
pip install .

If `r-shell` is not found, add ~/.local/bin to your PATH:
export PATH="$HOME/.local/bin:$PATH" 

```

## Philosophy

R is not trying to replace Linux tools.

Instead, it aims to provide a customizable environment where Python and existing shell commands work together, allowing users to build workflows that fit their needs.

## License

MIT License

