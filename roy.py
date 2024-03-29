# 8888888b.                   
# 888   Y88b                  
# 888    888                  
# 888   d88P .d88b.  888  888 
# 8888888P" d88""88b 888  888 
# 888 T88b  888  888 888  888 
# 888  T88b Y88..88P Y88b 888 
# 888   T88b "Y88P"   "Y88888 
#                         888 
#                    Y8b d88P 
#                     "Y88P"  
#
# A Simple Version Control System

import os
import sys 
import tempfile
import shutil
import hashlib
from datetime import datetime
import difflib

### === Globals === ###
# Denotes an initial commit
NULL_SHA1 = '0000000000000000000000000000000000000000'
HEAD_ID = NULL_SHA1

### === PATHS === ####
CWD = os.getcwd()
BASE_DIR = ".roy/" # base dir for Roy instance
MASTER_VOLUME = ".roy/master/" 
CACHE_VOLUME = ".roy/cache/" 
COMMIT_VOLUME = ".roy/commits/" 
CHANGELOG_PATH = ".roy/changelog" 
CONFIG_PATH = CWD + "/.royconfig" 
IGNORELIST_PATH = CWD + "/.royignore"

### === Error Handles === ###
def perror(msg):
    print("error: " + msg)

### === Structs - used for navigating change history === ###
# Each commit will be a singly linked list node
class Commit:
    def __init__(self, commit_id, author, commit_message, files, timestamp):
        self.commit_id = commit_id
        self.commit_message = commit_message
        self.author = author
        self.timestamp = timestamp

### === Helpers === ###
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
        os.remove(CACHE_VOLUME+'/'+filename)

    assert len(os.listdir(CACHE_VOLUME)) == 0, "cache error: could not be cleared"

# ain't this a funny function... FOR DEBUGGING PURPOSES ONLY. TODO
# Clear head ref in master volume
def clear_headref_master():
    for filename in os.listdir(TAIL_REF_MASTER):
        os.remove(filename)

    assert len(os.listdir(TAIL_REF_MASTER)) == 0, "master error: could not be cleared"

### === Config === ###
def print_config():
    with open(CONFIG_PATH, 'r') as f:
        res = f.readlines()
        f.close()

        for r in res:
            print(r)

        return

    perror("print_config() could no process .royconfig")

def write_config():
    pass

def read_config():
    if not os.path.exists(CONFIG_PATH):
        name = input("royconfig_author_name = ") 
        with open(CONFIG_PATH, 'w') as f:
            f.write(name)
            f.close()
            
    # exists, read and return
    with open(CONFIG_PATH, 'r') as f:
        res = f.readlines()
        f.close()
        return res


    perror("read_config() could not process .royconfig")
    exit(1)

### === Roy Command Functionality === ###
def setup():
    # check for config file setup
    read_config()

    # already exists, exit setup
    if os.path.exists(BASE_DIR):
        perror("roy version control system already set up")
        return
    
    mkdir(BASE_DIR)
    mkdir(MASTER_VOLUME)
    mkdir(CACHE_VOLUME)
    touch(CHANGELOG_PATH)
    touch(CONFIG_PATH)
    touch(IGNORELIST_PATH)

    print("roy: setup complete")

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

    for filename in os.listdir(CACHE_VOLUME):
        f1 = os.path.join(cwd, filename)
        # refactor to include a reference to the tail
        # TODO read changelog to obtain tail reference
        f2 = os.path.join(cwd, TAIL_REF_MASTER + filename)

        if str(f1) in ignore_list:
            print("ignoring ", f1)
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
def stage():
    if len(sys.argv) == 3:
        arg1 = CWD + '/' + sys.argv[2]
        print("staging", arg1)

        if os.path.isfile(arg1):
            # add to cache
            buf = arg1.split('/')
            base_name = buf[len(buf) - 1]

            shutil.copyfile(arg1, CACHE_VOLUME+base_name)

            assert os.path.isfile(CACHE_VOLUME+base_name), "Unable to write " + base_name + " to cache"

            return
        else:
            perror("failed to stage - " + arg1)
    perror("add command without <filename> is not supported yet")

# View Changelog
def log():
    with open(CHANGELOG_PATH, 'r') as f:
        res = f.readlines()
        f.close()

    for r in res:
        print(r)

    return


    perror("log() could no process changelog")
    exit(1)

# Switch to a version
def checkout(root):
    pass

# Sync changes to the master volume 
def sync():
    if os.stat(CACHE_VOLUME).st_size == 0:
        perror("nothing to sync from cache")
        return

    if len(sys.argv) == 3:
        arg1 = sys.argv[2]

        if len(arg1) == 0:
            perror("commit message cannot be empty")
            return

        # Write to .changelog
        # create commit id with create_hash
        curr_time = datetime.now()
        commit_id = NULL_SHA1
        commit_msg = arg1
        
        if os.stat(CHANGELOG_PATH).st_size != 0:
            commit_id = str(create_hash(read_config()[0], curr_time, commit_msg))
        author = read_config()[0]
        timestamp = curr_time
        
        with open(CHANGELOG_PATH, 'a') as f:
            f.write(str(commit_id))
            f.write('\n')
            f.write(commit_msg)
            f.write('\n')
            f.write(author)
            f.write('\n')
            f.write(str(timestamp))
            f.write('\n')
            f.close()

        snapshot = mkdir(os.path.join(MASTER_VOLUME, str(commit_id) + '/'))

        for filename in os.listdir(CACHE_VOLUME):
            buf = filename.split('/')
            base_name = buf[len(buf) - 1]
            shutil.copyfile(CACHE_VOLUME+'/'+filename, snapshot+base_name)

            assert os.path.isfile(snapshot + base_name), "Unable to write " + base_name + " to master"

        # Clear cache
        clear_cache_volume();
        return 
    else:
        perror("sync command missing proper commit message")
        print("usage: \n   sync <commit-msg> -- example: sync \"initial commit\"")

### === Driver === ###
usage_string = """
usage: roy [-h | --help] <command> [<args>] 

commands:
start a VCS 
   setup                    Setup directory for version control system
edit config 
   config                   Edit the config file
show changes
   diff                     Shows changes between current working directory and master volume
stage changes
   stage <filename>         Stage changes to cache
clear cache
   clear                    Clears staged changes/cache volume
sync changes
   sync <commit-msg>        Sync changes to master
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
        case "log":
            log()
        case "setup":
            setup()
        case "diff":
            diff()
        case "stage":
            stage()
        case "sync":
            sync()
        case "clear":
            clear_cache_volume()
        case "config":
            read_config()

if __name__ == "__main__":
    main()
