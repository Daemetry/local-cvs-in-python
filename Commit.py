from Files import blobify, unblobify, encoding


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

    # @property
    # def tree(self):
    #     pass

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
    def set_commit_directory(directory):
        if not isinstance(directory, str):
            raise TypeError("Expected directory to be a string. "
                            "That's just what happens sometimes :P")
        Commit._commit_directory = directory

    @staticmethod
    def serialize(commit):
        if not isinstance(commit, str):
            raise TypeError("Expected commit to be a string. "
                            "That's just what happens sometimes :P")
        try:
            message, tree, pch = [e.split(': ')[1] for e in commit.split('\n')]
            return message, tree, pch
        except IndexError or ValueError:
            return None

    @staticmethod
    def unhash(commit_hash):
        if not isinstance(commit_hash, str):
            raise TypeError("Expected commit hash to be a string. "
                            "That's just what happens sometimes :P")
        if commit_hash == "none":
            return Commit(None, None, None)
        supposedly_commit = unblobify(commit_hash, Commit._commit_directory).decode(encoding)
        serialised = Commit.serialize(supposedly_commit)
        return Commit(serialised[0], serialised[1], eval(serialised[2])) if serialised else None
