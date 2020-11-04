import os
import re

from io import StringIO
import unittest
from unittest.mock import patch

from todo.io import csvToDictionary, dictionaryToCSV, dbExists
from todo.todo import listTasks, addTask, checkTask, removeTask
from app import showHelp


class TodoTests(unittest.TestCase):

    testDic = {
        "1": {"checked": '', "desc": "Walk the dog"},
        "2": {"checked": 'True', "desc": "Buy milk"},
        "3": {"checked": '', "desc": "Do homework"}}

    testUsgStr = """\
    Command Line Todo application
    =============================
    -l      Lists all the tasks
    -a      Adds a new task
    -r      Removes a task
    -c      Completes a task
    """
    testStr = "1 - [ ] Walk the dog\n2 - [x] Buy milk\n3 - [ ] Do homework\n"

    # Test usage
    def testUsage(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            showHelp()
            self.assertEqual(re.sub(r"\s+", "", fake_out.getvalue()), re.sub(r"\s+", "", TodoTests.testUsgStr))

    # Tests for todo.io

    # Non-existing file should return false
    def testNoFile(self):
        self.assertFalse(dbExists("this is not a legit file"))

    # The dbExists should return with the path to tasklist.csv
    def testFileExists(self):
        self.assertTrue("tasklist.csv" in dbExists("tasklist.csv"))

    # The dictionary read from the tasklist.csv file should match the testDic variable
    def testcsvToDictionary(self):
        with open(dbExists("tasklist.csv"), "r") as db:
            self.assertEqual(csvToDictionary(db), TodoTests.testDic)

    # The csv read from the file and written back to the file should match
    def testdictionaryToCsv(self):
        with open(dbExists("tasklist.csv"), "r+") as db:
            # Read original file
            original = db.readlines()

            # Convert the original file to dictionary and write it back to file
            db.seek(0)
            testdic = csvToDictionary(db)
            dictionaryToCSV(db, testdic)

            # Check if the output file matches the original
            db.seek(0)
            new = db.readlines()

            self.assertEqual(original, new)

    # Tests for todo.todo

    # List task - empty list
    def testEmptyList(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with open("testfile.csv", "a+") as db:
                listTasks(db=db)
            os.remove("testfile.csv")
            self.assertEqual(fake_out.getvalue(), "No todos for today! :)\n")

    # List task - default tasks
    def testDefaultTasks(self):
        with patch("sys.stdout", new=StringIO()) as fake_out:
            with open(db := dbExists("tasklist.csv"), "r") as db:
                listTasks(db=db)
            self.assertEqual(fake_out.getvalue(), TodoTests.testStr)

    # Add task - Intended functionality
    def testAddTask(self):
        with open(db := dbExists("tasklist.csv"), "r+") as db:
            addTask(db=db, args=["test"])
            db.seek(0)
            self.assertTrue(db.readlines()[3].replace("\n", '') == "4;;test")
            removeTask(db=db, args=["4"])

    # Remove task - Intended functionality
    def testRemoveTask(self):
        with open(db := dbExists("tasklist.csv"), "r+") as db:
            addTask(db=db, args=["test"])
            removeTask(db=db, args=["4"])
            with patch("sys.stdout", new=StringIO()) as fake_out:
                listTasks(db=db)
                self.assertEqual(fake_out.getvalue(), TodoTests.testStr)

    # Check task - Intended functionality
    def testCheckTask(self):
        with open(db := dbExists("tasklist.csv"), "r+") as db:
            addTask(db=db, args=["test"])
            checkTask(db=db, args=["4"])
            db.seek(0)
            self.assertTrue(db.readlines()[3].replace("\n", '') == "4;True;test")
            removeTask(db=db, args=["4"])


if __name__ == "__main__":
    unittest.main()
