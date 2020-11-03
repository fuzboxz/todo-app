import sys
import os

FILENAME = "tasklist.csv"


# Import text to dictionary
def csvToDictionary(fp):
    tasks = {}
    raw = fp.readlines()

    for line in raw:
        fields = line.split(";")
        tasks[fields[0]] = {'checked': fields[1], 'desc': fields[2].replace("\n", "")}

    return tasks


# Export dictionary to CSV
def dictionaryToCSV(fp, tasks):
    # Return to beginning of the file
    fp.truncate(0)
    fp.seek(0)
    for i in tasks:
        checked = "True" if tasks[i]['checked'] else ""
        fp.write("{0};{1};{2}\n".format(i, checked, tasks[i]['desc']))


# Check if db exists
def dbExists():
    directory = os.path.dirname(os.path.realpath(__file__))
    dbPath = os.sep.join([directory, FILENAME])
    if (os.path.isfile(dbPath)):
        return dbPath
    else:
        return False


# List all the tasks
def listTasks(**kwargs):
    output = []

    db = kwargs['db']
    tasks = csvToDictionary(db)

    # Iterate through tasklist and format output
    if len(tasks) != 0:
        for i in tasks:
            checkbox = "[x]" if tasks[i]['checked'] else "[ ]"

            output.append("{0} - {1} {2}".format(i, checkbox, tasks[i]["desc"]))
        print("\n".join(output))
    else:
        print("No todos for today! :)")


# Add a task to the tasklist
def addTask(**kwargs):
    args = kwargs['args']
    if (len(args) == 0):
        print("Unable to add: no task provided")
        exit(-1)

    # Load tasks first, so we can continue the index numbering
    db = kwargs['db']
    tasks = csvToDictionary(db)

    # Indexing in the CSV starts at 1
    id = len(tasks) + 1
    tasks[id] = {"checked": False, "desc": args[0]}

    dictionaryToCSV(db, tasks)
    print("New task added: {0} - {1}".format(id, tasks[id]["desc"]))


# Remove a task from the tasklist
def removeTask(**kwargs):
    args = kwargs['args']

    # Check index
    if (len(args) == 0):
        print("Unable to check: no index provided")
        exit(-1)

    if not args[0].isnumeric():
        print("Unable to check: index is not a number")
        exit(-1)

    # Load tasks
    db = kwargs['db']
    tasks = csvToDictionary(db)

    i = args[0]
    if int(i) > len(tasks) or int(i) < 1:
        print("Unable to check: index is out of bound")
        exit(-1)

    print("Task deleted: {0} - {1}".format(args[0], tasks[i]['desc']))
    del tasks[i]
    dictionaryToCSV(db, tasks)


# Mark a task as complete in tasklist
def checkTask(**kwargs):
    args = kwargs['args']

    # Check index
    if (len(args) == 0):
        print("Unable to check: no index provided")
        exit(-1)

    if not args[0].isnumeric():
        print("Unable to check: index is not a number")
        exit(-1)

    # Load tasks
    db = kwargs['db']
    tasks = csvToDictionary(db)

    i = args[0]
    if int(i) > len(tasks) or int(i) < 1:
        print("Unable to check: index is out of bound")
        exit(-1)

    tasks[i]['checked'] = True
    dictionaryToCSV(db, tasks)
    print("Task checked: {0} - {1}".format(args[0], tasks[i]['desc']))


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
    "-c": ["Completes a task", checkTask]
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
                print("Unsupported argument")
                showHelp()
                exit(-1)

        else:
            print("Error: tasklist.csv not accessible")
            exit(-1)
