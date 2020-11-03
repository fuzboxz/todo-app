import sys
import os

FILENAME = "tasklist.csv"


def csvToDictionary(csv):
    tasks = {}
    csv.seek(0)
    raw = csv.readlines()
    for line in raw:
        fields = line.split(";")
        tasks[fields[0]] = fields[1].replace("\n", "")
    return tasks


def dbExists():
    directory = os.path.dirname(os.path.realpath(__file__))
    dbPath = os.sep.join([directory, FILENAME])
    if (os.path.isfile(dbPath)):
        return dbPath
    else:
        return False


def listTasks(**kwargs):
    output = []

    db = kwargs['db']
    tasks = csvToDictionary(db)

    for task in tasks:
        output.append("{0} - {1}".format(task, tasks[task]))
    print("\n".join(output))


def addTask(*args):
    print("Add task")


def removeTask(*args):
    print("Remove task")


def completeTask(*args):
    print("Complete task")


# Displays the command line information when no argument is specified
def showHelp():
    title = "Command Line Todo application"
    decor = "=" * len(title)

    # Construct argument list
    args = []
    for arg in functions.keys():
        args.append("\t{0}\t{1}".format(arg, str(functions[arg][0])))
    argstring = "\n".join(args)

    # Create final output string
    print("\n".join(["\n", title, decor, "\n", argstring]))


functions = {
    "-l": ["Lists all the tasks", listTasks],
    "-a": ["Adds a new task", addTask],
    "-r": ["Removes a task", removeTask],
    "-c": ["Completes a task", completeTask]
}

if __name__ == "__main__":
    # no arguments
    if len(sys.argv) == 1:
        showHelp()
        exit(0)
    else:
        option = sys.argv[1]
        if (dbPath := dbExists()):
            if (option in functions.keys()):
                try:
                    with open(dbPath, "r+") as db:
                        functions[option][1](db=db, args=sys.argv[2:])
                    exit(0)
                except IOError:
                    pass

        else:
            print("Error: tasklist.csv not accessible")
            exit(-1)
