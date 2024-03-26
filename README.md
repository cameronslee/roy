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

Therefore, the commands Roy supports are simply the following:
```
$ roy setup                                 # sets up version control system

$ roy diff                                  # shows changes that have been made

$ roy stage <filename>                      # stages changes to cache

$ roy sync                                  # sync changes to master volume 

$ roy log                                   # view changelog of commits

$ roy checkout <commit-id>                  # switch to a commit 
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

