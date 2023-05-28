import os

from Files import *
import argparse


class GymException(Exception):
    _message: str

    def __init__(self, message):
        self._message = message

    def __str__(self):
        return self._message


class GymRepository:
    _repository_directory = ".gym"
    _repository_structure = {
        "HEAD": "ref: refs/branch/boss",
        "objects": {},
        "backups": {},
        "refs": {
            "branch": {"boss": "hash: none"},
            "tag": {}
        },
        "index": "",
        "error.log": "",
        ".commits": ""
    }

    _available_commands = ["init", "add", "commit", "reset",
                           "checkout", "branch", "tag", "log", "help"]

    _commits = _repository_directory + "/.commits"
    index = _repository_directory + "/index"
    backup_index = _repository_directory + "/backups/index"
    head = _repository_directory + "/HEAD"
    log_file = _repository_directory + "/error.log"
    objects = _repository_directory + "/objects"

    @staticmethod
    def get_ref(name):
        if not name.startswith('refs'):
            name = "refs/" + name
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
        with open(GymRepository.index, 'r') as index:
            index_content = index.read()
            if not index_content:
                raise GymException("Nothing to commit")

            flat_tree = {entry[0]: entry[1] for entry in
                         [entry.strip().split() for entry in index_content.split('\n')]}

        nested_tree = unflatten_tree(flat_tree)

        return write_tree(nested_tree)

    @staticmethod
    def _index() -> str:
        with open(GymRepository.index, 'r') as index:
            return index.read()

    @staticmethod
    def _index_b() -> bytes:
        return GymRepository._index().encode(encoding)

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
        print(unblobify(args[0], GymRepository.objects).decode(encoding))
        # GymRepository._ensure_index()
        # print(GymRepository._index_to_tree())

    @staticmethod
    def _restore(filename, filehash):
        filedata = unblobify(filehash, GymRepository.objects)
        with open(filename, 'wb') as f:
            f.write(filedata)

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
                blobify(f.read(), GymRepository.objects)

    @staticmethod
    def _update_index(path):
        """"""

        GymRepository.assert_repo()

        # Прервать, если path является директорией
        if os.path.isdir(path):
            return

        GymRepository._ensure_index()

        with open(GymRepository.index, 'r') as f:
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
        with open(GymRepository.index, 'w') as index:
            index.write(index_content)

        os.makedirs(GymRepository._repository_directory + "/backups", exist_ok=True)
        with open(GymRepository.backup_index, 'w') as backup:
            backup.write(index_content)

    @staticmethod
    def _ensure_index():
        if os.path.exists(GymRepository.index):
            return

        if os.path.exists(GymRepository.backup_index):
            with open(GymRepository.backup_index, 'r') as backup:
                index = open(GymRepository.index, 'w')
                index.write(backup.read())
                index.close()
            return

        print("Looks like your index has been deleted externally.\n"
              "As well as backup. Your index data is lost.\n"
              "Please index everything necessary once more.")
        open(GymRepository.index, 'w').close()

    @staticmethod
    def _get_previous_commit_hash():
        with open(GymRepository.head, 'r') as head:
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
    def _is_branch(name: str) -> bool:
        path1 = GymRepository._repository_directory + f"/refs/branch/{name}"
        path2 = GymRepository._repository_directory + f"/refs/{name}"
        return os.path.exists(path1) or \
               (name.startswith("branch") and os.path.exists(path2))

    @staticmethod
    def _is_tag(name: str) -> bool:
        path1 = GymRepository._repository_directory + f"/refs/tag/{name}"
        path2 = GymRepository._repository_directory + f"/refs/{name}"
        return os.path.exists(path1) or \
               (name.startswith("tag") and os.path.exists(path2))

    @staticmethod
    def commit(args: argparse.Namespace):
        """Creates a new commit and clears the commit index"""
        GymRepository.assert_repo()

        message = args.message

        prev_commit_hash = GymRepository._get_previous_commit_hash()

        # as side effect, blobify creates the file in the objects system
        tree_hash = blobify(
            GymRepository._index_b(), GymRepository.objects
        )

        if prev_commit_hash != "none":
            prev_commit = unblobify(prev_commit_hash, GymRepository.objects).decode(encoding)
            (_, prev_tree_hash, _) = GymRepository.serialize_commit(prev_commit)
            if prev_tree_hash == tree_hash:
                raise GymException("Nothing to commit, aborting")

        new_commit = GymRepository.get_commit(message, tree_hash, prev_commit_hash)

        # as the last time, blobify creates a blob object in the objects directory
        new_commit_hash = blobify(new_commit.encode(encoding), GymRepository.objects)

        with open(GymRepository.head, 'r') as head:
            curr_head = head.read().split(": ")
        if curr_head[0] == "hash":
            with open(GymRepository.head, 'w') as index:
                index.write(f"hash: {new_commit_hash}")
        elif curr_head[0] == "ref":
            with open(GymRepository.get_ref(curr_head[1]), 'w') as ref:
                ref.write(f"hash: {new_commit_hash}")

        with open(GymRepository._commits, 'a') as commits:
            commits.write(f"hash: {new_commit_hash}\n")
            commits.write(new_commit)
            commits.write('\n' + '-' * 20 + '\n')

        print(f"Commit created: {new_commit_hash}")

    @staticmethod
    def branch(args: argparse.Namespace):
        """Creates a new branch"""
        GymRepository.assert_repo()

        pch = GymRepository._get_previous_commit_hash()
        GymRepository._create_ref(f"branch/{args.name}", pch)
        print(f"Created branch {args.name} on commit {pch}")

    @staticmethod
    def tag(args: argparse.Namespace):
        """Creates a tag on the current commit"""
        GymRepository.assert_repo()

        pch = GymRepository._get_previous_commit_hash()
        GymRepository._create_ref(f"tag/{args.name}", pch)
        print(f"Tagged {pch} with {args.name}")

    @staticmethod
    def checkout(args: argparse.Namespace):
        """Checks out on the commit (if hash given) or branch/tag (if name given)"""
        GymRepository.assert_repo()

        pch = GymRepository._get_previous_commit_hash()
        prev_commit = unblobify(pch, GymRepository.objects).decode(encoding)
        (_, prev_commit_index_hash, _) = GymRepository.serialize_commit(prev_commit)
        prev_commit_index = unblobify(prev_commit_index_hash, GymRepository.objects).decode(encoding)

        # if there are uncommitted changes and no --force is present,
        # discard
        if prev_commit_index != GymRepository._index() and not args.force:
            raise GymException("Uncommitted changes found, aborting.\n"
                               "In order to checkout regardless, use "
                               "\"gym checkout -f/--force [name/hash]\"")

        # if for some reason there are branch and tag with the same name,
        # clarifications needed, so discard
        mode = "hash"
        if GymRepository._is_branch(args.target):
            mode = "branch"
        if GymRepository._is_tag(args.target):
            if mode == "branch":
                raise GymException(f"Ambiguous referencing:\n"
                                   f"{args.target} is both a name of a tag and a branch.\n"
                                   f"Specify using \"branch/{args.target}\" or \"tag/{args.target}\"")
            mode = "tag"

        match mode:
            # when checkouting a commit, using its hash,
            # try to unblobify the commit,
            # notifing the user as they are entering DETACHED HEAD state
            case "hash":
                try:
                    target_commit = unblobify(args.target, GymRepository.objects).decode(encoding)
                except FileNotFoundError:
                    raise GymException("No such commit, aborting")

                print("Entering DETACHED HEAD state:\n"
                      "any commits made will be lost upon checkouting elsewhere,\n"
                      "unless tagged or branched.")
                with open(GymRepository.head, 'w') as head:
                    head.write(f"hash: {args.target}")

            # when checkouting a tag, open the tag file, extract the commit hash,
            # then unblobify the commit and update head,
            # notifing the user as they are entering DETACHED HEAD state
            case "tag":
                try:
                    tag_file = GymRepository.get_ref(
                        args.target if args.target.startswith("tag")
                        else f"tag/{args.target}")
                    print(tag_file)
                    with open(tag_file, 'r') as tag:
                        target_commit_hash = tag.read().split(": ")[1]
                except FileNotFoundError:
                    raise GymException("No such tag, aborting")

                target_commit = unblobify(target_commit_hash, GymRepository.objects).decode(encoding)

                print("Entering DETACHED HEAD state:\n"
                      "any commits made will be lost upon checkouting elsewhere,\n"
                      "unless tagged or branched.")
                with open(GymRepository.head, 'w') as head:
                    head.write(f"hash: {target_commit_hash}")

            # when checkouting a branch, open the branch file, extract commit hash,
            # then unblobify the commit and update head
            case "branch":
                try:
                    branch_file = GymRepository.get_ref(
                        args.target if args.target.starts_with("branch/") else f"branch/{args.target}")
                    with open(branch_file, 'r') as branch:
                        target_commit_hash = branch.read().split(": ")[1]
                except FileNotFoundError:
                    raise GymException("No such branch, aborting")

                target_commit = unblobify(target_commit_hash, GymRepository.objects).decode(encoding)
                with open(GymRepository.head, 'w') as head:
                    head.write(f"ref: {branch_file}")

        # noinspection PyUnboundLocalVariable
        (_, target_index_hash, _) = GymRepository.serialize_commit(target_commit)
        target_index = unblobify(target_index_hash, GymRepository.objects).decode(encoding)

        for file in prev_commit_index.split('\n'):
            os.remove(file.split(' ')[0])

        for file in target_index.split('\n'):
            filename, filehash = file.split(' ')
            GymRepository._restore(filename, filehash)

        print(f"Checked out on {args.target} successfully")

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
