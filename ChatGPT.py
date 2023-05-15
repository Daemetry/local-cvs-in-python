import os


# Initialize the repository
def init():
    if not os.path.isdir('.cvs'):
        os.makedirs('.cvs')
        with open('.cvs/files.txt', 'w') as f:
            f.write('')


# Add a file to the repository
def add(filename):
    with open('.cvs/files.txt', 'a') as f:
        f.write(filename + '\n')
        with open(filename, 'r') as fl:
            contents = fl.read()
            with open(os.path.join('.cvs', filename), 'w') as cvs_file:
                cvs_file.write('1\n' + contents)


# Commit changes to the repository
def commit():
    with open('.cvs/files.txt', 'r') as f:
        files = f.read().split('\n')[:-1]
        for file in files:
            with open(os.path.join('.cvs', file), 'r') as cvs_file:
                version = int(cvs_file.readline()) + 1
                contents = cvs_file.read()
                with open(os.path.join('.cvs', file), 'w') as new_cvs_file:
                    new_cvs_file.write(str(version) + '\n' + contents)


# Check out a file from the repository
def checkout(filename):
    with open(os.path.join('.cvs', filename), 'r') as f:
        version = f.readline()
        contents = f.read()
        with open(filename, 'w') as file:
            file.write(contents)


# View the log of changes to a file
def log(filename):
    with open(os.path.join('.cvs', filename), 'r') as f:
        lines = f.readlines()
        print('File: {}'.format(filename))
        for i in range(1, len(lines)):
            print('Version: {}'.format(i))
            print(lines[i])


# Sample usage
init()
add('test.txt')
commit()
checkout('test.txt')
log('test.txt')
