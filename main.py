import sys

functions = {
    "-l": "Lists all the tasks",
    "-a": "Adds a new task",
    "-r": "Removes a task",
    "-c": "Completes a task"
}


# Displays the command line information when no argument is specified
def showHelp():
    title = "Command Line Todo application"
    decor = "=" * len(title)
    
    # Construct argument list
    args = []
    for arg in functions.keys():
        args.append("\t{0}\t{1}".format(arg, str(functions[arg])))
    argstring = "\n".join(args)

    # Create final output string
    print("\n".join(["\n", title, decor, "\n", argstring]))


if __name__ == "__main__":
    
    # no arguments
    if len(sys.argv) == 1:
        showHelp()
        exit(0)