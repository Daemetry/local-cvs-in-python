import commands as c
from sys import argv


def main(args):
    if len(args) == 0:
        print("Welcome to the gym!")
        print("Time to show 'em commits who's the boss, right?")
        print("Try using a command. To see the list of available commands, you can use 'gym help'")
        print("Nah kidding. Don't be a pussy, real men don't need help in the gym!")
        return
    command = args[1]
    flags = args[2:]
    match command:
        case "init":
            c.init(flags)
        case "add":
            c.add(flags)
        case "commit":
            c.commit(flags)
        case "reset":
            c.reset(flags)
        case "help":
            c.help(flags)


if __name__ == "__main__":
    main(argv)
