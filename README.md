# Roy: A Simple Version Control System
```
8888888b.                   
888   Y88b                  
888    888                  
888   d88P .d88b.  888  888 
8888888P" d88""88b 888  888 
888 T88b  888  888 888  888 
888  T88b Y88..88P Y88b 888 
888   T88b "Y88P"   "Y88888 
                        888 
                   Y8b d88P 
                    "Y88P"  
```

## Main Principles

#### Centralized Source Control System
Versioning and changes are commited to a single access point (that YOU own!)

```
      --------       ----------   update    ---------------
      | Main | ----> | Roy    | <---------> |  System A   |
      | Repo | <---- | Server |   commit    |  (client)   |
      --------       ----------             ---------------
```

#### Simple Commands and Settings
Roy should be intuitive. 

Complex commands to augment your working tree result in extra overhead during 
the development process.

A typical Roy workflow can be visualized as follows
```
      ----------       ----------       ----------
      | Make   | ----> | Stage  | ----> | Sync   |
      | Change |       | Change |       | Change |
      ----------       ----------       ----------
      Change in        Update Cache     Update master 
      current working
      directory
```

#### Roy Directory Architecture
Roy adheres to a simple directory structure. Built to be extendable with backup
systems if so desired. 
```
PROJECT DIRECTORY
|-- .roy
|   |
|   |-- master/                             # master volume 
|       |-- headref/                        # most recent version
|   |-- cache/                              # local staged changes
|   |-- commits/                            # directory states, based on commit ID 
|   |-- changelog                           # changelog for each commit made
|
|-- .royconfig                              # user and project configuration
|-- .royignore                              # file blacklist, directory level
```

#### On Disk Changes
Roy keeps track of changes made on disk. By default this is within the projects
directory.

Roy can be configured to have versioning exist outside of the project.

## Installation
#### Build from source
```
$ ./activate.sh                # activate virtual environment for build
$ ./build.sh                   # build  -  roy found in dist/, will refactor for install on system
```

## Usage
```
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
```

#### Example - Getting Started
```
$ roy setup
$ touch README && echo "readme" >  ./README
$ roy stage README
$ roy sync "first commit" 
$ roy log                      # view changelog containing the first commit
```
