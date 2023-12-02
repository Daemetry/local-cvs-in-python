import argparse
import os
import sys
import unittest
import shutil

from io import StringIO

from Commit import Commit
from GymException import GymException
from GymRepository import GymRepository
from Files import blobify, encoding, add_to_filename


class InitTests(unittest.TestCase):
    """Tests for command init"""

    def test_init_create_repository(self):
        args = []
        if os.path.exists(GymRepository._repository_directory):
            shutil.rmtree(GymRepository._repository_directory)
        GymRepository.init(args)
        assert os.path.exists(GymRepository._repository_directory)

    def test_init_repository_exists(self):
        args = []
        try:
            GymRepository.init(args)
        except Exception as e:
            self.assertIsInstance(e, GymException, "The exception is not handled in the program")

    def test_init_with_wrong_args(self):
        args = ["a"]
        try:
            GymRepository.init(args)
        except Exception as e:
            self.assertIsInstance(e, GymException, "The exception is not handled in the program")


class AddTests(unittest.TestCase):
    """Tests for command add"""

    def setUp(self):
        self.file_path = os.path.join(os.getcwd(), "file.txt")
        open(self.file_path, 'w').close()

    def tearDown(self):
        os.remove(self.file_path)

    def test_add_file_index_exist(self):
        args = [self.file_path]
        GymRepository.add(args)
        self.assertTrue(os.path.exists(GymRepository.index))

    def test_add_with_wrong_args(self):
        args = ["a", "b"]
        with self.assertRaises(GymException):
            GymRepository.add(args)


class CommitTests(unittest.TestCase):
    """Tests for command commit"""
    def setUp(self):
        # Создание файла в директории
        self.file_path = os.path.join(os.getcwd(), 'file.txt')
        with open(self.file_path, 'w') as file:
            file.write('Test file')

        # Создание аргументов командной строки для тестового вызова commit
        self.args = argparse.Namespace()
        self.args.message = 'Test commit'

    def tearDown(self):
        os.remove(self.file_path)
        with open(GymRepository.head, 'w') as head:
            head.write("hash: none")
        open(GymRepository.index, 'w').close()

    def test_commit_in_empty_repo(self):
        prev_commit_hash = GymRepository._get_current_commit_hash()

        # Вызов метода commit с данными тестового файла и сообщения
        GymRepository.add([self.file_path])
        GymRepository.commit(self.args)

        # Проверка, что новый коммит создан
        commits_file = GymRepository._commits
        with open(commits_file, 'r') as file:
            commits = file.read()
        self.assertIn('Test commit', commits)

        # Проверка, что изменения в коммите различаются от предыдущего коммита
        cur_commit_hash = GymRepository._get_current_commit_hash()
        diff = Commit.diff(prev_commit_hash, cur_commit_hash)
        self.assertIsNot(diff, "")

    def test_commit_in_not_empty_repo(self):
        GymRepository.add([self.file_path])
        GymRepository.commit(self.args)

        prev_commit_hash = GymRepository._get_current_commit_hash()

        new_file_name = "new_file.txt"
        open(new_file_name, 'w').close()
        GymRepository.add([new_file_name])

        self.args.message = "New commit"
        GymRepository.commit(self.args)

        # Проверка, что новый коммит создан
        commits_file = GymRepository._commits
        with open(commits_file, 'r') as file:
            commits = file.read()
        self.assertIn('New commit', commits)

        # Проверка, что изменения в коммите различаются от предыдущего коммита
        cur_commit_hash = GymRepository._get_current_commit_hash()
        diff = Commit.diff(prev_commit_hash, cur_commit_hash)
        self.assertIsNot(diff, "")


class TagAndBranchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.file_path = os.path.join(os.getcwd(), 'file.txt')
        with open(self.file_path, 'w') as file:
            file.write('Test file')

        GymRepository.add([self.file_path])

        args = argparse.Namespace()
        args.message = "Empty commit"
        GymRepository.commit(args)

    def tearDown(self):
        os.remove(self.file_path)
        with open(GymRepository.head, 'w') as head:
            head.write("hash: none")
        open(GymRepository.index, 'w').close()

    def test_tag(self):
        args = argparse.Namespace()
        args.name = "empty"
        GymRepository.tag(args)

        assert os.path.exists(".gym/refs/tag/empty")
        with open(".gym/refs/tag/empty", 'r') as file:
            current_commit_hash = GymRepository._get_current_commit_hash()
            assert file.read().split(': ')[1] == current_commit_hash

    def test_branch(self):
        args = argparse.Namespace()
        args.name = "new"
        GymRepository.branch(args)

        assert os.path.exists(".gym/refs/branch/new")
        with open(".gym/refs/branch/new", 'r') as file:
            current_commit_hash = GymRepository._get_current_commit_hash()
            assert file.read().split(': ')[1] == current_commit_hash


class CheckoutTests(unittest.TestCase):
    def setUp(self):
        initial_file = "initial.txt"
        open(initial_file, 'w').close()
        GymRepository.add([initial_file])

        args = argparse.Namespace()

        args.message = "Initial commit"
        GymRepository.commit(args)
        self.initial_hash = GymRepository._get_current_commit_hash()
        initial_index = GymRepository._index()

        self.tag = "initial"
        args.name = self.tag
        GymRepository.tag(args)

        self.boss_file = "boss.txt"
        open(self.boss_file, 'w').close()
        GymRepository.add([self.boss_file])

        args.message = "Boss commit"
        GymRepository.commit(args)

        self.other_file = "other.txt"
        obf_hash = blobify("".encode(encoding), GymRepository.objects)
        initial_index += f"\n{self.other_file} {obf_hash}"
        index_hash = blobify(initial_index.encode(encoding), GymRepository.objects)
        commit = Commit("Other commit", index_hash, [self.initial_hash])
        new_commit_hash = commit.blobify()
        self.branch = GymRepository.get_ref("other", reftype="branch")
        with open(self.branch, 'w') as branch:
            branch.write(f"hash: {new_commit_hash}")


    def tearDown(self):
        with open(GymRepository.head, 'w') as head:
            head.write("hash: none")
        open(GymRepository.index, 'w').close()

    def test_checkout_with_hash(self):
        args = argparse.Namespace()
        args.target = self.initial_hash
        GymRepository.checkout(args)

        with open(GymRepository.head, 'r') as head:
            head_content = head.read()

        assert head_content.startswith("hash: ")
        assert head_content.endswith(self.initial_hash)

        assert not os.path.exists(self.boss_file)


    def test_checkout_with_tag(self):
        args = argparse.Namespace()
        args.target = self.tag
        GymRepository.checkout(args)

        with open(GymRepository.head, 'r') as head:
            head_content = head.read()

        assert head_content.startswith("hash: ")
        assert head_content.endswith(self.initial_hash)

        assert not os.path.exists(self.boss_file)

    def test_checkout_with_branch(self):
        args = argparse.Namespace()
        args.target = self.branch.split('/', 2)[-1]
        GymRepository.checkout(args)

        with open(GymRepository.head, 'r') as head:
            head_content = head.read()

        assert head_content.startswith("ref: ")
        assert head_content.endswith(self.branch.split('/', 1)[-1])

        assert not os.path.exists(self.boss_file)
        assert os.path.exists(self.other_file)


class MergeTests(unittest.TestCase):

    def setUp(self):
        self.output = StringIO()
        sys.stdout = self.output

        initial_file = "initial.txt"
        open(initial_file, 'w').close()
        GymRepository.add([initial_file])

        args = argparse.Namespace()

        args.message = "Initial commit"
        GymRepository.commit(args)

        tag = "initial"
        args.name = tag
        GymRepository.tag(args)

        self.boss_file = "boss.txt"
        open(self.boss_file, 'w').close()
        GymRepository.add([self.boss_file])

        args.message = "Boss commit"
        GymRepository.commit(args)

        args.target = tag
        GymRepository.checkout(args)

        self.other_file = "other.txt"
        open(self.other_file, 'w').close()
        GymRepository.add([self.other_file])

        args.message = "Other commit"
        GymRepository.commit(args)

        args.name = "other"
        GymRepository.branch(args)
        args.target = "boss"
        GymRepository.checkout(args)

    def tearDown(self):
        with open(GymRepository.head, 'w') as head:
            head.write("hash: none")
        open(GymRepository.index, 'w').close()

    def test_merge_with_no_conflicts(self):
        args = argparse.Namespace()
        args.branch = "other"
        GymRepository.merge(args)
        merge_commit = Commit.unhash(GymRepository._get_current_commit_hash())
        assert merge_commit.message.startswith("# Merged")
        assert os.path.exists(self.boss_file)
        assert os.path.exists(self.other_file)

    def test_merge_with_conflicts(self):
        with open(self.other_file, 'w') as impostor:
            impostor.write("I am an impostor and I will create merge conflicts!")
        GymRepository.add([self.other_file])

        args = argparse.Namespace()
        args.message = "This commit shall create conflicts"
        GymRepository.commit(args)

        args.branch = "other"
        GymRepository.merge(args)
        actually_not_merge_commit = Commit.unhash(GymRepository._get_current_commit_hash())
        assert actually_not_merge_commit.message == args.message
        assert os.path.exists(self.boss_file)
        assert not os.path.exists(self.other_file)
        assert os.path.exists(add_to_filename(self.other_file, "_current"))
        assert os.path.exists(add_to_filename(self.other_file, "_incoming"))


if __name__ == "__main__":
    unittest.main()