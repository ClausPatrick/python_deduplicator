# Python (version 3) deduplication script

## Motivation

A small script intended to sort out storage devices with duplicate files. Everyone has some drive around where one keeps adding copies of other drives onto as one changes a computer or other devices. 

## Usage

Run script in a directory and <i>duplicate_files.txt</i> will be generated containing path, file and size of each duplicate. The critiria is based on <i>file name</i> and <i>file size</i>. This critiria can be weakend with the following flag:

```
    --size
```

Furthermore: 
```
    --path /home/$USER/.
```
    
Specifies a different path where duplicates are gathered.

```
    --file
```
    
Should the output file be written somewhere else or named something different. 
Finally:

```
    --purge
```
    
Once the output file has been composed, user will evaluate each file in the output file then run this script with the purge flag. All remaining entries will have the dublicates removed. Please note that for files to be deleted the preceding header (Marked as '#N ...' where N is number of files) is to be left unaltered: the script relies on this to enumerate each file. The script will wipe the second and each subsequent entry and leave the first one in its place. The order can be altered if there is a preference to keep a copy in a certain directory over an other.

An additional script ```setup_test_dir.sh``` is added that generates some directories and some files of which some have same, some have different file size. The test structure looks like this:


```
└── test_dir
    ├── dir_a
    │   ├── dir_b_b
    │   │   ├── dir_b_c
    │   │   │   └── dir_b_e
    │   │   └── file_same_size.txt
    │   └── file_diff_size.txt
    ├── dir_b
    │   ├── dir_b
    │   │   └── dir_c
    │   │       └── dir_e
    │   ├── file_diff_size.txt
    │   └── file_same_size.txt
    ├── dir_c
    │   └── dir_c_b
    │       ├── dir_c_c
    │       │   └── dir_c_e
    │       │       └── file_same_size.txt
    │       └── file_diff_size.txt
    └── dir_d
        └── dir_d_b
            └── dir_d_c
                ├── dir_d_e
                │   └── file_same_size.txt
                └── file_diff_size.txt
```

When running 
```
python3 deduplicator
```
in the parent directory, will result in an output file <i>duplicate_files.txt</i> with the following entries:

```
### Total duplicate 5 file(s) found, amounting to 10.3 KiB. ### 
#2 'file_diff_size.txt' found in:
    ./file_diff_size.txt,    10436
    ./test_dir/dir_d/dir_d_b/dir_d_c/file_diff_size.txt,    10436
#5 'file_same_size.txt' found in:
    ./test_dir/dir_d/dir_d_b/dir_d_c/dir_d_e/file_same_size.txt,    29
    ./test_dir/dir_c/dir_c_b/dir_c_c/dir_c_e/file_same_size.txt,    29
    ./test_dir/dir_b/file_same_size.txt,    29
    ./test_dir/dir_a/dir_b_b/file_same_size.txt,    29
    ./file_same_size.txt,    29
```

When running the script with the ```--purge``` flag all entries will be removed except <i>file_diff_size.txt </i> and <i>test_dir/dir_d/dir_d_b/dir_d_c/dir_d_e/file_same_size.txt</i>. 


## Requirements

Python3
(tested with Python 3.13.5)

### Imports

- import os
- import sys
- from itertools import chain

