# Roy: A Simple Version Control System

import os
import sys 
import tempfile
import shutil
import hashlib
from datetime import datetime
import difflib

# Hardcoded Config TODO remove
CONFIG_USER_NAME = "foobar"

# Denotes an initial commit
NULL_SHA1 = 0000000000000000000000000000000000000000 

### === PATHS === ####
BASE_DIR = ".roy/" # base dir for Roy instance
MASTER_VOLUME = ".roy/master/" 
CACHE_VOLUME = ".roy/cache/" 
COMMIT_VOLUME = ".roy/commits/" 
CHANGELOG_PATH = ".roy/changelog/" 
CONFIG_PATH = ".roy/changelog/" 
IGNORELIST_PATH = ".roy/.royignore"

# Error Handles
def perror(msg):
    print("error: " + msg)

### === Data Stuctures - used for navigating change history === ###
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
    m = -42069
    m = hashlib.sha1()

    m.update(str(name).encode('utf-8'))
    m.update(str(timestamp).encode('utf-8'))
    m.update(str(commit_msg).encode('utf-8'))

    print(m.hexdigest())

    assert m != -42069, "hash error: could not create hash"

    return m.hexdigest()

# Create file and set timestamp
def touch(path):
    with open(path, 'a') as f:
        os.utime(path, None) # set access and modified times
        f.close()

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return path

    perror("path already exists")
    return

def clear_cache_volume():
    for filename in os.listdir(CACHE_VOLUME):
        os.remove(filename)

    assert len(os.listdir(CACHE_VOLUME)) == 0, "cache error: could not be cleared"

# ain't this a funny function... FOR DEBUGGING PURPOSES ONLY. TODO
def clear_master_volume():
    for filename in os.listdir(MASTER_VOLUME):
        os.remove(filename)

    assert len(os.listdir(MASTER_VOLUME)) == 0, "master error: could not be cleared"

### === Roy Command Functionality === ###
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
    master_dir = os.listdir(MASTER_VOLUME)
    ignore = os.path.join(cwd, ".royignore")
    ignore_list = []
    changed_list = []

    # In the case that diff is run before a commit is made
    if len(master_dir) == 0:
        perror("master volume not set up")
        return -1

    with open (ignore) as f:
        lines = f.readlines()

    for l in lines:
        ignore_list.append(cwd + '/' + l.strip())

    for filename in os.listdir(cwd):
        f1 = os.path.join(cwd, filename)
        f2 = os.path.join(MASTER_VOLUME, filename)

        if str(f1) in ignore_list:
            print("ignoring ", f1)
            continue
        elif os.path.isfile(f1) and os.path.isfile(f2):
            print(diff_file(f1, f2))
            #add to changed_list
            changed_list.append(f1)

        else:
            perror("could not find matching file in working directory")
            print(f1, f2)

    return changed_list

# Add file(s) to the local cache staging directory
# to_stage: list of paths in the project directory to stage/copy to cache
def add(to_stage):
    pass

# View Commits
def log(root):
    pass

# Sync changes to the master volume 
def sync(commit_msg):
    # create commit id with create_hash
    commit_id = NULL_SHA1
    if len(os.listdirs(MASTER_VOLUME)):
        commit_id = str(create_hash(CONFIG_USER_NAME, datetime.now(), commit_msg))

    # create directory for snapshot
    print(commit_id)
    snapshot = mkdir(os.path.join(MASTER_VOLUME, commit_id + '/'))

    for filename in os.listdir(CACHE_VOLUME):
        buf = filename.split('/')
        base_name = buf[len(buf) - 1]
        shutil.copyfile(filename, snapshot+base_name)

        assert os.path.isfile(snapshot + base_name), "Unable to write " + base_name + " to master"
    return 

### === Driver === ###

# Usage message 
usage_string = """
usage: roy [-h | --help] <command> [<args>] 

commands:
start a VCS 
   setup                    Setup directory for version control system
show changes
   diff                     Show current changes to files that were made
stage changes
   add <filename>           Stage changes
sync changes
   sync                     Sync changes to master
view changelog
   log                      View changelog of commits 
checkout a commit 
   checkout <commit-id>     Switch to a commit 
"""

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
        case "setup":
            setup()
            print("roy: setup complete")
        case "diff":
            diff()
        case "add":
            if len(sys.argv) == 3:
                arg1 = sys.argv[2]

                if not os.path.isfile(arg1):
                    perror("add - could not find " + arg1)
                    exit(1)

                # add to cache
                buf = arg1.split('/')
                base_name = buf[len(buf) - 1]

                shutil.copyfile(arg1, CACHE_VOLUME+base_name)

                assert os.path.isfile(CACHE_VOLUME+base_name), "Unable to write " + base_name + " to cache"
                return
            perror("add command without <filename> is not supported yet")
        case "sync":
            if len(sys.argv) == 3:
                arg1 = sys.argv[2]

                if len(arg1) == 0:
                    perror("commit message cannot be empty")
                    return

                sync(arg1)
                return

            perror("sync command missing proper commit message")

        # for debugging TODO remove
        case "clearcache":
            clear_cache_volume()
        case "clearmaster":
            clear_master_volume()

if __name__ == "__main__":
    main()
