# Roy: A Simple Version Control System

import os
import sys 
import tempfile
import shutil
import hashlib
from datetime import datetime
import difflib

# Denotes an initial commit
NULL_SHA1 = 0000000000000000000000000000000000000000 

### PATHS ####
BASE_DIR = ".roy/" # base dir for Roy instance
MASTER_VOLUME = ".roy/master/" 
CACHE_VOLUME = ".roy/cache/" 
COMMIT_VOLUME = ".roy/cache/" 
CHANGELOG_PATH = ".roy/changelog/" 
CONFIG_PATH = ".roy/changelog/" 
IGNORELIST_PATH = ".roy/.royignore"

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

# Hash value is built from author name, timestamp and commit message
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


def diff_file(f1, f2):
    with open(f1, 'r') as f:
        lines1 = f.read().strip().splitlines()

    with open(f2, 'r') as f:
        lines2 = f.read().strip().splitlines()

    res = ""
    
    for line in difflib.unified_diff(lines1, lines2, fromfile=f1, tofile=f2, lineterm=''):
        res += line + '\n'

    return res

def diff():
    cwd = os.getcwd()
    master_dir = MASTER_VOLUME 
    ignore = os.path.join(cwd, ".royignore")
    ignore_list = []

    with open (ignore) as f:
        lines = f.readlines()

    for l in lines:
        ignore_list.append(cwd + '/' + l.strip())

    for filename in os.listdir(cwd):
        f1 = os.path.join(cwd, filename)
        f2 = os.path.join(master_dir, filename)

        if os.path.isfile(f1) and os.path.isfile(f2):
            print(diff_file(f1, f2))
        elif str(f1) in ignore_list:
            print("ignoring ", f1)
            continue
        else:
            perror("could not find matching file in working directory")
            print(f1, f2)

def add(commit_log):
    pass

# View Commits
def log(root):
    pass

def send(root):
    pass


usage_string = """
usage: roy [-h | --help] <command> [<args>] 

commands:
start a VCS 
   setup                    Setup directory for version control system
show changes
   diff                     Show current changes to files that were made
stage changes
   add                      Stage current changes
sync changes
   sync                     Sync changes to master
view changelog
   log                      View changelog of commits 
checkout a commit 
   checkout <commit-id>     Switch to a commit 
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
        case "-diff":
            diff()

if __name__ == "__main__":
    main()
