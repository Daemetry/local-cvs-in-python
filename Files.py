import os
import zlib
from hashlib import sha1


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
            if child == ".gym":
                continue
            files += match_files(os.path.join(path, child))
        return files


def write_tree(tree):
    tree_string = ""
    for key in tree:
        if isinstance(tree[key], str):
            tree_string += f'blob {tree[key]} {key}\n'
        else:
            subtree = write_tree(tree[key])
            tree_string += f'tree {subtree} {key}\n'
    return tree_string


def unflatten_tree(flat_tree):
    tree = {}
    for path in flat_tree:
        path_list = path.split("/")
        node_value = flat_tree[path]
        current_dict = tree

        for key in path_list[:-1]:
            if key not in current_dict:
                current_dict[key] = {}
            current_dict = current_dict[key]

        current_dict[path_list[-1]] = node_value

    return tree


def blobify(data, target_directory):
    """Creates a blob object from data, creates child directory
    in target_directory and a file in it, where in writes the data"""
    # создаем объектный хэш из данных
    obj_hash = sha1(data).hexdigest()

    # разбиваем хэш на каталоги и имя файла
    directory = obj_hash[:2]
    filename = obj_hash[2:]

    # создаем каталог, если он не существует
    object_directory = os.path.join(target_directory, directory)
    os.makedirs(object_directory, exist_ok=True)

    # создаем новый файл в объектном каталоге
    object_filename = os.path.join(object_directory, filename)
    with open(object_filename, 'wb') as f:
        # сжимаем данные zlib
        compressed_data = zlib.compress(data)
        # записываем заголовок объека
        header = f'blob {len(data)}\0'.encode()
        # записываем заголовок, данные и сжатый размер
        f.write(header)
        f.write(compressed_data)

    # возвращаем хэш созданного объекта
    return obj_hash


def unblobify(obj_hash, target_directory):
    """From a hash of the object gets the names of directory and file
    inside target_directory, where it searches for file and then
    creates a string from it"""

    # разбиваем хэш на каталоги и имя файла
    directory = obj_hash[:2]
    filename = obj_hash[2:]

    # находим путь к файлу объекта
    object_filename = os.path.join(target_directory, directory, filename)

    # считываем данные из файла объекта
    with open(object_filename, 'rb') as f:
        header, compressed_data = f.read().split(b"\x00", 1)

    header = header.strip().decode()

    # распаковываем сжатые данные
    data = zlib.decompress(compressed_data)

    # проверяем, что распакованные данные имеют нужный размер
    expected_size = int(header.split()[1])
    if len(data) != expected_size:
        raise ValueError(f'Error: expected {expected_size} bytes, got {len(data)} bytes')

    return data
