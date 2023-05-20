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
            "heads": {"boss": "hash: none"},
            "tags": {}
        },
        "index": ""
    }

    _available_commands = ["init", "add", "commit", "reset",
                           "checkout", "branch", "tag", "log", "help"]

    @staticmethod
    def get_index():
        return GymRepository._repository_directory + "/index"

    @staticmethod
    def get_backup_index():
        return GymRepository._repository_directory + "/backups/index"

    @staticmethod
    def get_head():
        return GymRepository._repository_directory + "/HEAD"

    @staticmethod
    def get_log():
        return GymRepository._repository_directory + "/.log"

    @staticmethod
    def get_objects():
        return GymRepository._repository_directory + '/' + "objects"

    @staticmethod
    def get_ref(name):
        return GymRepository._repository_directory + '/' + name

    @staticmethod
    def get_commit(message, tree_hash, previous_commit_hash):
        return f"message: {message}\n" \
               f"tree: {tree_hash}\n" \
               f"previous commit: {previous_commit_hash}"

    @staticmethod
    def serialize_commit(commit: str):
        return [prop.split(": ")[1] for prop in commit.split('\n')]

    @staticmethod
    def _index_to_tree():
        GymRepository._ensure_index()
        with open(GymRepository.get_index(), 'r') as index:
            index_content = index.read()
            if not index_content:
                raise GymException("Nothing to commit")

            flat_tree = {entry[0]: entry[1] for entry in
                         [entry.strip().split() for entry in index_content.split('\n')]}

        nested_tree = unflatten_tree(flat_tree)

        return write_tree(nested_tree)

    @staticmethod
    def _test(args):
        # filename = args[0]
        # with open(GymRepository.get_index(), 'r') as f:
        #     index = {x.split()[0]: x.split()[1] for x in f.readlines()}
        #
        # filehash = index[filename]
        #
        # filedata = unblobify(filehash, GymRepository._repository_directory + "/objects")
        #
        # with open(GymRepository._repository_directory + filename, 'wb') as f:
        #     f.write(filedata)
        #
        # print("File has been successfully recreated")
        print(unblobify(args[0], GymRepository.get_objects()).decode())
        # GymRepository._ensure_index()
        # print(GymRepository._index_to_tree())

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
                blobify(f.read(), GymRepository.get_objects())

    @staticmethod
    def _update_index(path):
        """"""

        GymRepository.assert_repo()

        # Прервать, если path является директорией
        if os.path.isdir(path):
            return

        GymRepository._ensure_index()

        with open(GymRepository.get_index(), 'r') as f:
            index = f.readlines()

        new_index = []
        for entry in index:
            if not entry.startswith(path):
                new_index.append(entry.strip())

        with open(path, 'rb') as f:
            entry = f"{path} {sha1(f.read()).hexdigest()}"
        new_index.append(entry)
        print(f"Added: {entry}")
        new_index.sort()

        index_content = str.join("\n", new_index)
        with open(GymRepository.get_index(), 'w') as index:
            index.write(index_content)

        os.makedirs(GymRepository._repository_directory + "/backups", exist_ok=True)
        with open(GymRepository.get_backup_index(), 'w') as backup:
            backup.write(index_content)

    @staticmethod
    def _ensure_index():
        if os.path.exists(GymRepository.get_index()):
            return

        if os.path.exists(GymRepository.get_backup_index()):
            with open(GymRepository.get_backup_index(), 'r') as backup:
                index = open(GymRepository.get_index(), 'w')
                index.write(backup.read())
                index.close()
            return

        print("Looks like your index has been deleted externally.\n"
              "As well as backup. Your index data is lost.\n"
              "Please index everything necessary once more.")
        open(GymRepository.get_index(), 'w').close()

    @staticmethod
    def _get_previous_commit_hash():
        with open(GymRepository.get_head(), 'r') as head:
            curr_head = head.read().split(": ")
            if curr_head[0] == "ref":
                with open(GymRepository.get_ref(curr_head[1]), 'r') as branch_head:
                    prev_commit_hash = branch_head.read().split(": ")[1]

            elif curr_head[0] == "hash":
                prev_commit_hash = curr_head[1]
        return prev_commit_hash

    @staticmethod
    def _create_ref(ref, commit_hash):
        with open(GymRepository._repository_directory + "/refs/" + ref, 'w') as f:
            f.write(f"hash: {commit_hash}")

    @staticmethod
    def commit(args):
        """Creates a new commit and clears the commit index"""
        GymRepository.assert_repo()

        message = "# message be here"  # TODO: use argparse to pass the message

        prev_commit_hash = GymRepository._get_previous_commit_hash()

        # as side effect, blobify creates the file in the objects system
        tree_hash = blobify(
            GymRepository._index_to_tree().encode(), GymRepository.get_objects()
        )

        if prev_commit_hash != "none":
            prev_commit = unblobify(prev_commit_hash, GymRepository.get_objects())
            (_, prev_tree_hash, _) = GymRepository.serialize_commit(prev_commit.decode())
            if prev_tree_hash == tree_hash:
                raise GymException("Nothing to commit, aborting")

        new_commit = GymRepository.get_commit(message, tree_hash, prev_commit_hash)

        # as the last time, blobify creates a blob object in the objects directory
        new_commit_hash = blobify(new_commit.encode(), GymRepository.get_objects())

        with open(GymRepository.get_head(), 'r') as head:
            curr_head = head.read().split(": ")
        if curr_head[0] == "hash":
            with open(GymRepository.get_head(), 'w') as index:
                index.write(f"hash: {new_commit_hash}")
        elif curr_head[0] == "ref":
            with open(GymRepository.get_ref(curr_head[1]), 'w') as ref:
                ref.write(f"hash: {new_commit_hash}")

        print(f"Commit created: {new_commit_hash}")

    @staticmethod
    def branch(args):
        """Creates a new branch"""
        pass

    @staticmethod
    def tag(args):
        """Creates a tag on the current commit"""
        GymRepository.assert_repo()

        if len(args) != 1:
            raise GymException("Too many arguments. Pass down only the name of the tag.")

        pch = GymRepository._get_previous_commit_hash()
        GymRepository._create_ref(f"tags/{args[0]}", pch)
        print(f"Tagged: {pch} with {args[0]}")


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
