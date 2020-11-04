# TODO app by Jozsef Ottucsak

## Requirements

* Python 3 (tested on Python 3.8.6 64-bit)
* Tested on Windows 10 (should work on all OSs)
* Only Python 3 built-in modules were used

## Installation

Clone or download the zip file to get started. If you have multiple python versions installed replace the python command with the executable name that you usually use to execute Python 3 code.

```
git clone https://github.com/green-fox-academy/fuzboxz-todo-app.git
cd fuzboxz-todo-app
python app.py
```

## Running unit tests

Basic functionality tests are provided to help with further development. To execute the test cases run the following commands. The first command can be ignored if *pytest* is installed.
```
pip install pytest
pytest unittests.py
```

## Usage

TODO app is a command-line interface application which uses command line switches to achieve it's functionality. The following functions are currently supported. 

- Start the application without any command line switch to show help
- **-l** to list the tasks
- **-a *"My Brand New Task"*** to add a new task
- **-r *task-id*** to remove a task
- **-c *task-id*** to complete a task

A *tasklist.csv* was provided as the default "database". It is a plaintext file that uses semicolons to separate columns. The first column is the ID of the given task, the second is the status of the task (if it contains any values that means it's completed) and the third column is description of the task.

If you want to restart from a clean state, delete the **tasklist.csv** file and create a new empty one. The file **must** reside in the same directory as the *app.py* executable. A different name can also be used, in this case the *FILENAME* constant of the *app.py* file must be modified.