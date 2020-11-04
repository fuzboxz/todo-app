import os

# Contains all the file io related functionality for the todo app


# Checks if the given file exists and returns the path to it, otherwise returns false
def dbExists(filename):
    directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    dbPath = os.sep.join([directory, filename])
    if (os.path.isfile(dbPath)):
        return dbPath
    else:
        return False


# Import raw text from file to dictionary
def csvToDictionary(fp):
    tasks = {}
    fp.seek(0)
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
