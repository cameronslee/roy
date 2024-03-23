# Roy: A Simple Version Control System

import os
import sys 
import tempfile
import shutil
import hashlib
from datetime import datetime

### Hardcoded Config ###
USR = "foo"
### Hardcoded Config END ###

# Denotes an initial commit
NULL_SHA1 = 0000000000000000000000000000000000000000 

BASE_DIR = ".roy/" # Data will reside in project specific directory
MASTER_VOLUME = ".roy/master" 

def perror(msg):
    print("error: " + msg)

# Each commit will be a singly linked list node
class Commit:
    def __init__(self, commit_id, author, commit_message, files, timestamp):
        self.commit_id = commit_id
        self.commit_message = commit_message
        self.author = author
        self.files = files  # Each commit, files will be updated
        self.timestamp = timestamp
        self.next = None

# Version Control Instance
# stores a reference to the head of commits
class VC:
    def __init__(self, basedir=BASE_DIR, head_ref=None):
        self.basedir = os.path.realpath(basedir)
        self.tempdir = os.path.join(self.basedir, "tmp/")
        os.makedirs(self.tempdir, exist_ok=True)
        self.head_ref = head_ref

# Build a linked list 
# Reads master volume log, builds linked of each and returns a VC object
# with the head_ref set
def build_vc_instance():
    pass

def create_hash(name, timestamp, commit_msg):
    m = hashlib.sha1()

    m.update(str(name).encode('utf-8'))
    m.update(str(timestamp).encode('utf-8'))
    m.update(str(commit_msg).encode('utf-8'))

    print(m.hexdigest())

    return m

def touch(path):
    with open(path, 'a') as f:
        os.utime(path, None) # set access and modified times
        f.close()

# Commands
def setup():
    # already exists, exit setup
    if os.path.exists(BASE_DIR):
        perror("roy version control system already set up")
        return
    
    touch(MASTER_VOLUME)

def diff(head_node):
    # Open cache
    # Compare differences
    # Print to Screen
    pass

def add(head_node, commit_log):
    # Write to cache
    with open(MASTER_VOLUME, 'a') as f:
        # create log
        # if volume empty, pass null id to indicate start

        f.write(commit_log)
        f.close()

def log(root):
    pass

def send(root):
    pass


usage_string = """
usage: roy [-h | --help] <command> [<args>] 

commands:
start a VCS 
   setup    Setup directory for version control system
show changes
   diff     Show current changes to files that were made
stage changes
   add      Stage current changes
sync changes
   sync     Sync changes to main
"""


### === Driver === ###
def usage(msg=""):
    print(usage_string)

    if msg != "":
        print(msg)

def main():
    if len(sys.argv) < 2:
        usage()
        exit(1)

    cmd = sys.argv[1]

    match cmd:
        case "-h":
            usage()
        case "--help":
            usage()
        # Test: create hash
        case "-ch":
            create_hash("foo test", str(datetime.now()), "test commit") 

if __name__ == "__main__":
    main()
