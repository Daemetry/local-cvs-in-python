import argparse
import os
import sys
import unittest
import shutil
from io import StringIO
from collections import namedtuple

from Commit import Commit
from GymException import GymException
from GymRepository import GymRepository


output_here = StringIO()
sys.stdout = output_here


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


if __name__ == "__main__":
    unittest.main()