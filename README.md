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

Therefore, the commands Roy supports are the following:
```
$ roy setup                                 # sets up repository

$ roy diff                                  # shows changes that have been made

$ roy add                                   # stages current changes

$ roy send                                  # syncs the saved changes to main
```


