import os.path

from GymRepository import *
import sys
from datetime import datetime
from traceback import print_exception
from ArgumentParsers import *


def log_exception(exc_type, exc_value, exc_traceback):
    with open(GymRepository.log_file, 'r') as f:
        logs = f.read()
    with open(GymRepository.log_file, 'w') as f:
        time = datetime.now().strftime("%Y-%m-%D %H:%M:%S")
        f.write(f"[{time}]\n\n")
        print_exception(exc_type, exc_value, exc_traceback, file=f)
        f.write('-' * 30 + '\n')
        f.write(logs)
        print("\nAn error has occurred! "
              "\nWe as the developer team have already "
              "\nbeen notified and work on fixing it.")


sys.excepthook = log_exception


def main(args):
    if len(args) == 1:
        print("Welcome to the gym!")
        print("Time to show 'em commits who's the boss, right?")
        print("To see the list of available commands, you can use \"gym help\"")
        return

    command = args[1]
    flags = args[2:]
    match command:
        case "add":
            GymRepository.add(flags)

        case "branch":
            branch_args = branch_parser.parse_args()
            GymRepository.branch(branch_args)

        case "checkout":
            checkout_args = checkout_parser.parse_args()
            GymRepository.checkout(checkout_args)

        case "commit":
            commit_args = commit_parser.parse_args()
            GymRepository.commit(commit_args)

        case "help":
            GymRepository.help(flags)

        case "init":
            GymRepository.init(flags)

        case "log":
            raise NotImplementedError

        case "merge":
            merge_args = merge_parser.parse_args()
            GymRepository.merge(merge_args)

        case "reset":
            raise NotImplementedError
            # GymRepository.reset(flags)

        case "tag":
            tag_args = tag_parser.parse_args()
            GymRepository.tag(tag_args)

        # dev tools :)
        case "--test":
            GymRepository._test(flags)

        case "--htt":
            GymRepository._htt(flags)

        case "--test-error":
            GymRepository._test_runtime()


if __name__ == "__main__":
    try:
        main(sys.argv)
    except GymException as e:
        print(e)
