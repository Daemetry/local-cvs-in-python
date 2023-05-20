from GymRepository import GymRepository as gym, GymException
import sys
from datetime import datetime
from traceback import print_exception


def log_exception(exc_type, exc_value, exc_traceback):
    with open(gym.get_log(), 'a') as f:
        time = datetime.now().strftime("%Y-%m-%D %H:%M:%S")
        f.write(f"[{time}]\n\n")
        print_exception(exc_type, exc_value, exc_traceback, file=f)
        f.write('-' * 30 + '\n')
        print("\nAn error has occurred! "
              "\nWe as the developer team have already "
              "\nbeen notified and work on fixing it.")


sys.excepthook = log_exception


def main(args):
    try:
        if len(args) == 1:
            print("Welcome to the gym!")
            print("Time to show 'em commits who's the boss, right?")
            print("To see the list of available commands, you can use \"gym help\"")
            return

        command = args[1]
        flags = args[2:]
        match command:
            case "init":
                gym.init(flags)
            case "add":
                gym.add(flags)
            case "commit":
                gym.commit(flags)
            case "reset":
                gym.reset(flags)
            case "help":
                gym.help(flags)
            case "branch":
                gym.branch(flags)
            case "tag":
                gym.tag(flags)
            case "--test":
                gym._test(flags)

    except GymException as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)
