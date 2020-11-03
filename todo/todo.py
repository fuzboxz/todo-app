from todo.io import csvToDictionary, dictionaryToCSV

# Contains all the task related functionality for the todo app
# Helper functions for file I/O are in the io namespace


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
    tasks[id] = {"checked": False, "desc": args[0].replace("\n", "")}

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
