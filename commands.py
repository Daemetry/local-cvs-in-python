import os
import ctypes

repo = u".gym"  # the repository folder
commits = repo + u"/commits"
index = repo + u"/index"
head = repo + u"/HEAD"
tags = repo + u"/tags"
log = repo + u"/log.txt"

commands = {"init", "add", "commit", "reset", "log", "help"}  # supported commands for a gym repository


def init(args):
    """Initiates a gym repository in the current directory"""
    print(args)
    if len(args) != 0:
        print("Hol' up, mate. You're not supposed to do this.\n"
              "Creating a repository doesn't require any arguments.\n"
              "Perhaps you meant something else?")
        return

    if os.path.exists(".gym"):
        print("Already a gym in here! Can't fit another one.")
        return

    os.makedirs(".gym")
    # 0x02 is flag for a hidden file/directory
    ret = ctypes.windll.kernel32.SetFileAttributesW(".gym", 2)


def add(args):
    """Adds the current changes to the commit index"""
    pass


def commit(args):
    """Creates a new commit and clears the commit index"""
    pass


def branch(args):
    """Creates a new branch"""
    pass


def tag(args):
    """Creates a tag on the current commit"""
    pass


def reset(args):
    """Resets to the previous commit"""
    pass


def log(args):
    """Prints the log of actions upon repository"""
    pass


def help(args):
    """Use this command in case you need to get to know other ones better"""
    if len(args) == 0:
        print(f"Available commands: {str.join(', ', commands)}")
        return

    elif len(args) == 1:
        if args[0] not in commands:
            print(f"{args[0]} is not a valid command. If you want to see "
                  "the list of available commands, use 'gym help'")
            return


if __name__ == '__main__':
    pass
