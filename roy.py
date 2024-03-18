# Roy: A Simple Version Control System

import os
import tempfile
import shutil

BASE_DIR = ".roy/cache" # Data will reside in project specific directory

# Each commit will be a singly linked list node
class Commit:
    def __init__(self, commit_message, files, timestamp):
        self.commit_message = commit_message
        self.files = files  # Each commit, files will be updated
        self.timestamp = timestamp
        self.next = None

# Version Control Instance
# stores a reference to the head of commits
class VC:
    def __init__(self, basedir="", root=None, head_ref=None):
        self.basedir = os.path.realpath(basedir)
        self.tempdir = os.path.join(self.basedir, "tmp")
        os.makedirs(self.tempdir, exist_ok=True)

        print(self.basedir)
        print(self.tempdir)

        self.root = root

        self.head_ref = head_ref
        print(head_ref)


# Commands
def setup():
    pass

def diff(root):
    pass

def add(root):
    pass

def send(root):
    pass


### === Driver === ###
def main():
    vc = VC(BASE_DIR)

if __name__ == "__main__":
    main()