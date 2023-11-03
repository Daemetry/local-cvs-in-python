from Files import blobify, unblobify, encoding
from difflib import unified_diff

class Commit:
    _commit_directory: str

    def __init__(self, message: str, tree: str, previous_commits: list):
        self._message = message
        self._tree_hash = tree
        self._previous_commits = previous_commits

    @property
    def message(self):
        return self._message

    @property
    def tree_hash(self):
        return self._tree_hash

    @property
    def tree(self):
        return unblobify(self._tree_hash, Commit._commit_directory).decode(encoding)

    @property
    def pchs(self):
        return self._previous_commits

    def __str__(self):
        return f"message: {self._message}\n" \
               f"tree: {self._tree_hash}\n" \
               f"previous commits: {self._previous_commits}"

    def __repr__(self):
        return f"Commit({self._message}, {self._tree_hash}, {self._previous_commits})"

    def encode(self):
        return str(self).encode(encoding)

    def blobify(self):
        return blobify(self.encode(), Commit._commit_directory)

    @staticmethod
    def set_commit_directory(directory: str):
        if not isinstance(directory, str):
            raise TypeError("Expected directory to be a string. "
                            "That's just what happens sometimes :P")

        Commit._commit_directory = directory

    @staticmethod
    def serialize(commit: str):
        if not isinstance(commit, str):
            raise TypeError("Expected commit to be a string. "
                            "That's just what happens sometimes :P")

        try:
            message, tree, pch = [e.split(': ')[1] for e in commit.split('\n')]
            return message, tree, pch
        except IndexError or ValueError:
            return None

    @staticmethod
    def unhash(commit_hash: str):
        if not isinstance(commit_hash, str):
            raise TypeError("Expected commit hash to be a string. "
                            "That's just what happens sometimes :P")

        if commit_hash == "none":
            return None
        supposedly_commit = unblobify(commit_hash, Commit._commit_directory).decode(encoding)
        serialised = Commit.serialize(supposedly_commit)
        return Commit(serialised[0], serialised[1], eval(serialised[2])) if serialised else None

    @staticmethod
    def diff(from_commit_hash: str, to_commit_hash: str):
        """Computes difference between 'from' commit and 'to' commit,
        with assumption that 'from' is the starting point, and 'to' is the destination"""
        if not from_commit_hash or not to_commit_hash:
            raise GymException("")

        # commit trees in form of strings
        from_commit_tree = Commit.unhash(from_commit_hash).tree
        to_commit_tree = Commit.unhash(to_commit_hash).tree

        # converting to dictionaries of form { filename: filehash, ... }
        from_commit_tree = {filename: filehash for filename, filehash in map(str.split, from_commit_tree.split('\n'))}
        to_commit_tree = {filename: filehash for filename, filehash in map(str.split, to_commit_tree.split('\n'))}

        difference = []
        for filename in from_commit_tree.keys():
            if filename not in to_commit_tree.keys():
                difference.append(f"Deleted: {filename} {from_commit_tree[filename]}")
                continue

            if from_commit_tree[filename] != to_commit_tree[filename]:
                file_diff = Commit.file_diff_by_hash(from_commit_tree[filename], to_commit_tree[filename])
                file_diff = [f"At {pos}: {change}" for pos, change in file_diff]
                difference.append(f"Changed: {filename} {from_commit_tree[filename][:5]}... "
                                  f"-> {to_commit_tree[filename][:5]}...\n"
                                  + '\n'.join(file_diff))

        for filename in to_commit_tree.keys():
            if filename not in from_commit_tree.keys():
                difference.append(f"Added: {filename} {to_commit_tree[filename]}")

        return str.join('\n', sorted(difference))

    @staticmethod
    def file_diff_by_hash(from_file_hash: str, to_file_hash: str):
        from_file = unblobify(from_file_hash, Commit._commit_directory).decode(encoding)
        to_file = unblobify(to_file_hash, Commit._commit_directory).decode(encoding)

        diff = unified_diff(from_file.split('\n'), to_file.split('\n'))
        diff = list(diff)[2:] # Skip the first two lines
        # since its just file names (empty because none were given to the function)
        enumerated_diff = []
        deletions_counter = 0
        for i, diff_line in enumerate(diff):
            if diff_line.startswith('-') or diff_line.startswith('+'):
                enumerated_diff.append((i - deletions_counter, diff_line))
                deletions_counter += 1 if diff_line.startswith('-') else 0

        # enumerated_diff = list(filter(lambda x: x[1].startswith('+') or x[1].startswith('-'), enumerated_diff))

        return enumerated_diff
