import argparse
import os
import unittest
import shutil
from collections import namedtuple

from Commit import Commit
from GymException import GymException
from GymRepository import GymRepository


class GitTest(unittest.TestCase):
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

    """Tests for command add"""

    "!"
    def test_add_file_index_exist(self):
        file = os.getcwd() + r"\file.txt"
        open(file, 'w').close()

        args = [file]
        GymRepository.add(args)
        assert os.path.exists(GymRepository.index) == True
        os.remove(file)

    def test_add_with_wrong_args(self):
        args = ["a", "b"]
        try:
            GymRepository.add(args)
        except Exception as e:
            self.assertIsInstance(e, GymException, "The exception is not handled in the program")

    "!"
    def test_add_with_file_added_to_index(self):
        file = os.getcwd() + r"\file.txt"
        open(file, 'w').close()
        args = [file]
        GymRepository.add(args)
        os.remove(file)
        file = os.getcwd() + r"\file.txt"
        open(file, 'w').close()
        try:
            GymRepository.add(args)
        except Exception as e:
            self.assertIsInstance(e, GymException, "The exception is not handled in the program")
        os.remove(file)

    """Tests for command commit"""

"""
    def test_commit(self):
        file = os.getcwd() + r"\file.txt"
        commit = namedtuple("commit", ["message"])
        commit.message = "message"
        open(file, 'w').close()
        args = [file]
        GymRepository.add(args)
        GymRepository.commit(commit)
        assert os.path.exists(GymRepository._commits) == True
"""