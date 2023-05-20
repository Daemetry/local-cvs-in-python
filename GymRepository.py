import os
from hashlib import sha1
from Files import *


class GymException(Exception):
    _message: str

    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


class GymRepository:
    _repository_directory = ".gym"
    _repository_structure = {
        "HEAD": "ref: refs/heads/boss",
        "objects": {},
        "backups": {},
        "refs": {
            "heads": {},
            "tags": {}
        },
        "index": ""
    }

    _available_commands = ["init", "add", "commit", "reset",
                           "checkout", "branch", "log", "help"]

    @staticmethod
    def get_index():
        return GymRepository._repository_directory + "/index"

    @staticmethod
    def get_backup_index():
        return GymRepository._repository_directory + "/backups/index"

    @staticmethod
    def get_log():
        return GymRepository._repository_directory + "/.log"

    @staticmethod
    def _test(args):
        filename = args[0]
        with open(GymRepository.get_index(), 'r') as f:
            index = {x.split()[0]: x.split()[1] for x in f.readlines()}

        filehash = index[filename]

        filedata = unblobify(filehash, GymRepository._repository_directory + "/objects")

        with open(GymRepository._repository_directory + filename, 'wb') as f:
            f.write(filedata)

        print("File has been successfully recreated")

    @staticmethod
    def init(args):
        """Initiates a gym repository in the current directory"""

        if args:
            raise GymException("init does not accept any parameters.")

        if GymRepository.repo_exists():
            raise GymException("Already a gym repository.")

        os.makedirs(GymRepository._repository_directory)
        create_file_tree(GymRepository._repository_structure,
                         GymRepository._repository_directory)

        print(f"Created a repository in {os.getcwd()}")

    @staticmethod
    def add(args):
        """Adds the current changes to the commit index"""

        GymRepository.assert_repo()

        if len(args) != 1:
            raise GymException("\"gym add\" accepts only one argument "
                               "being the name of the file or directory")

        files_to_add = match_files(args[0])
        if not files_to_add:
            raise GymException(f"Error: {args[0]} matched no files")

        for file in files_to_add:
            GymRepository._update_index(file)
            with open(file, "rb") as f:
                blobify(f.read(),
                        GymRepository._repository_directory + "/objects")

    @staticmethod
    def _update_index(path):
        """"""

        GymRepository.assert_repo()

        # Прервать, если path является директорией
        if os.path.isdir(path):
            return

        if os.path.exists(GymRepository.get_index()):
            with open(GymRepository.get_index(), 'r') as f:
                index = f.readlines()

        elif os.path.exists(GymRepository.get_backup_index()):
            with open(GymRepository.get_backup_index()) as backup:
                index = backup.readlines()

        else:
            print("Looks like your index has been deleted externally.\n"
                  "As well as backup. Your index data is lost.\n"
                  "Please index everything necessary once more.")
            open(GymRepository.get_index(), 'w').close()
            index = []

        new_index = []
        for entry in index:
            if not entry.startswith(path):
                new_index.append(entry)

        with open(path, 'rb') as f:
            entry = f"{path} {sha1(f.read()).hexdigest()}"
            new_index.append(entry)
            print(f"Added: {entry}")

        index_content = str.join("\n", new_index)
        with open(GymRepository.get_index(), 'w') as index:
            index.write(index_content)

        os.makedirs(GymRepository._repository_directory + "/backups", exist_ok=True)
        with open(GymRepository.get_backup_index(), 'w') as backup:
            backup.write(index_content)

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
            raise GymException(f"{args[0]} is not a valid command. If you want to see "
                  "the list of available commands, use 'gym help'")

        # TODO: выводить информацию о команде

    @staticmethod
    def repo_exists():
        return os.path.exists(GymRepository._repository_directory)

    @staticmethod
    def assert_repo():
        if not GymRepository.repo_exists():
            raise GymException("This directory is not a gym repository.")


if __name__ == '__main__':
    pass
