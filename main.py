from GymRepository import GymRepository as gym, GymException
import sys
from datetime import datetime
from traceback import print_exception
from ArgumentParsers import commit_parser, branch_parser, tag_parser



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
                commit_args = commit_parser.parse_args()
                gym.commit(commit_args)
            case "reset":
                gym.reset(flags)
            case "help":
                gym.help(flags)
            case "branch":
                branch_args = branch_parser.parse_args()
                gym.branch(branch_args)
            case "tag":
                tag_args = tag_parser.parse_args()
                gym.tag(tag_args)
            case "--test":
                gym._test(flags)

    except GymException as e:
        print(e)


if __name__ == "__main__":
    main(sys.argv)
