# Roy: A Simple Version Control System

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

$ roy add                                   # stages current changes

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
|   |-- master/                             # most up to date copy
|   |-- cache/                              # local changes
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

