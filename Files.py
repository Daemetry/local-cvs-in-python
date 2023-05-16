import os


def create_file_tree(tree, prefix):
    for name in tree:
        path = os.path.join(prefix, name)
        if isinstance(tree[name], str):
            with open(path, "w") as f:
                f.write(tree[name])
        else:
            if not os.path.exists(path):
                os.makedirs(path)
            create_file_tree(tree[name], path)


def match_files(path):
    if not os.path.exists(path):
        return []

    elif os.path.isfile(path):
        return [path]

    elif os.path.isdir(path):
        files = []
        for child in os.listdir(path):
            files += match_files(os.path.join(path, child))
        return files
