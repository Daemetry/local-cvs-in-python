import commands as c


def main(*args):
    """a"""
    if len(args) == 0:
        print("Try using a command. To see the list of available commands, you can use 'gym help'")
        return

    command = args[0]
    flags = args[1:]
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
    main()
