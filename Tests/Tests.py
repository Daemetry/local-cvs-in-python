import argparse
import os
import unittest
import shutil
from collections import namedtuple

from Commit import Commit
from GymException import GymException
from GymRepository import GymRepository


class InitTests(unittest.TestCase):
    """Tests for command init"""

    def test_init_create_repository(self):
        args = []
        if os.path.exists(GymRepository._repository_directory):
            shutil.rmtree(GymRepository._repository_directory)
        GymRepository.init(args)
        assert os.path.exists(GymRepository._repository_directory) == True

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
        self.file_path = os.getcwd() + r"\file.txt"
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


    """Tests for command commit"""

class CommitTests(unittest.TestCase):

    def setUp(self):
        # Создание временной директории для тестов
        self.temp_dir = os.path.join(os.getcwd(), 'temp_dir')
        os.makedirs(self.temp_dir, exist_ok=True)

        # Создание файла в директории
        self.file_path = os.path.join(self.temp_dir, 'file.txt')
        with open(self.file_path, 'w') as file:
            file.write('Test file')

        # Создание аргументов командной строки для тестового вызова commit
        self.args = argparse.Namespace()
        self.args.message = 'Test commit'

    def tearDown(self):
        # Удаление временной директории и ее содержимого
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(self.temp_dir)

    def test_commit(self):
        prev_commit_hash = GymRepository._get_previous_commit_hash()

        # Вызов метода commit с данными тестового файла и сообщения
        GymRepository.commit(self.args)

        # Проверка, что новый коммит создан
        commits_file = GymRepository._commits
        with open(commits_file, 'r') as file:
            commits = file.read()
        self.assertIn('Test commit', commits)

        # Проверка, что изменения в коммите различаются от предыдущего коммита
        cur_commit_hash = GymRepository._get_previous_commit_hash()
        diff = Commit.diff(prev_commit_hash, cur_commit_hash)
        self.assertIsNot(diff, "")



if __name__ == "__main__":
    unittest.main()