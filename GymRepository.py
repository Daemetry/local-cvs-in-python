import os
from hashlib import sha1
from Files import create_file_tree, match_files


class GymRepository:
    _repository_directory = ".gym"
    _repository_structure = {
        "HEAD": "ref: refs/heads/boss",
        # "config": config.objToStr({ "core": { "": { "bare": opts.get("bare") == True } } }),
        "objects": {},
        "refs": {
            "heads": {},
            "tags": {}
        },
        "index": ""
    }

    _available_commands = ["init", "add", "commit", "reset",
                           "checkout", "branch", "log", "help"]

    @staticmethod
    def init(args):
        """Initiates a gym repository in the current directory"""

        if len(args) != 0:
            print("Hol' up, mate. You're not supposed to do this.\n"
                  "Creating a repository doesn't require any arguments.\n"
                  "Perhaps you meant something else?")
            return

        if GymRepository.repo_exists():
            return

        os.makedirs(GymRepository._repository_directory)
        create_file_tree(GymRepository._repository_structure,
                               GymRepository._repository_directory)
        # TODO: вывод информации на консоль

    @staticmethod
    def add(args):
        """Adds the current changes to the commit index"""

        if not GymRepository.repo_exists():
            print("This directory is not a gym repository")
            return

        if len(args) != 1:
            print("Too many arguments! Use only the name to search for")
            return

        files_to_add = match_files(args[0])
        for file in files_to_add:
            GymRepository._update_index(file)
        # TODO: вывод информации на консоль

    @staticmethod
    def _update_index(path):
        """"""
        if not GymRepository.repo_exists():
            print("This directory is not a gym repository")
            return

        # Прервать, если path является директорией
        if os.path.isdir(path):
            return

        with open(GymRepository._repository_directory + "/index", 'r') as f:
            index = f.readlines()

        new_index = []
        for entry in index:
            if not entry.startswith(path):
                new_index.append(entry)

        with open(path, 'r') as f:
            new_index.append(f"{path} {sha1(f.read().encode()).hexdigest()}")

        with open(GymRepository._repository_directory + "/index", 'w') as index:
            for entry in new_index:
                index.write(f"{entry}\n")

        # TODO: вывод информации на консоль

    @staticmethod
    def commit(args):
        """Creates a new commit and clears the commit index"""
        pass

    @staticmethod
    def branch(args):
        """Creates a new branch"""
        pass

    @staticmethod
    def tag(args):
        """Creates a tag on the current commit"""
        pass

    @staticmethod
    def reset(args):
        """Resets to the previous commit"""
        pass

    @staticmethod
    def log(args):
        """Prints the log of actions upon repository"""
        pass

    @staticmethod
    def help(args):
        """Use this command in case you need to get to know other ones better"""
        if len(args) != 1:
            print(f"Available commands: {str.join(', ', GymRepository._available_commands)}")
            print("Use \"gym help [command]\" in order to get usage of the command")
            return

        if args[0] not in GymRepository._available_commands:
            print(f"{args[0]} is not a valid command. If you want to see "
                  "the list of available commands, use 'gym help'")
            return

        # TODO: выводить информацию о команде


    @staticmethod
    def repo_exists():
        return os.path.exists(GymRepository._repository_directory)


if __name__ == '__main__':
    pass
