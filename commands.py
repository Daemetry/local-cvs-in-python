commands = { "init", "add", "commit", "reset", "log", "help" }


def init(*args):
    """Initiates a gym repository in the current directory"""
    pass


def add(*args):
    """Adds the current changes to the commit index"""
    pass


def commit(*args):
    """Creates a new commit and clears the commit index"""
    pass


def reset(*args):
    """Resets to the previous commit"""
    pass


def log(*args):
    """Prints the log of recent actions upon repository"""
    pass


def help(*args):
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
