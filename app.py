import sys
from todo.todo import listTasks, addTask, removeTask, checkTask
from todo.io import dbExists

# Const filename
FILENAME = "tasklist.csv"

# Contains app functionality, key is the command line switch, first element of the list is the description, second is the Python function
functions = {
    "-l": ["Lists all the tasks", listTasks],
    "-a": ["Adds a new task", addTask],
    "-r": ["Removes a task", removeTask],
    "-c": ["Completes a task", checkTask]
}


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


if __name__ == "__main__":
    # No arguments specified
    if len(sys.argv) == 1:
        showHelp()
        exit(0)
    else:
        # At least one argument was given by the user
        option = sys.argv[1]

        # DB file exists
        if (dbPath := dbExists(FILENAME)):

            # Commandline switch is a key in the function dictionary
            if (option in functions.keys()):

                try:
                    # Create file object
                    with open(dbPath, "r+") as db:
                        # Call the Python method that's associated with the chosen commandline switch
                        # Pass the file object as a parameter for file manipulation and the rest of the
                        # commandline arguments as a kwarg
                        functions[option][1](db=db, args=sys.argv[2:])

                    exit(0)
                except IOError:
                    print("Some kind of error occured. Ouch.")
            else:
                print("Unsupported argument")
                showHelp()
                exit(-1)

        else:
            print("Error: tasklist.csv not accessible")
            exit(-1)
