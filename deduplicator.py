#!/usr/bin/python3
from datetime import datetime
import os
import sys
from itertools import chain


COMPARE_SIZE = 0 
PATH = 1
OUTFILE = 2
PURGING = 3

files_dict = {}
dub_files_dict = {}

options = {}
options[PATH] = "."
options[COMPARE_SIZE] = True
options[OUTFILE] = "duplicate_files.txt"
options[PURGING] = False 


def print_help(argv):
    print(f"Usage:")
    print(f"{argv[0]} --path /home/$USER/.")
    print(f"Will gather all duplicate files in specified directory based on same file name and same file size.")
    print(f"{argv[0]} --size")
    print(f"Will gather all duplicate files in current directory based on same file name but ignore file size.")
    print(f"{argv[0]} --file outputfile.txt")
    print(f"Will gather all duplicate files and log it into 'outputfile.txt'.")
    print(f"{argv[0]} --purge")
    print(f"User will evaluate each file in 'outputfile.txt' then run this script with the purge flag. All remaining entries will have the dublicates removed. Please note that for files to be deleted the preceding header (Marked as '#N ...' where N is number of files) is to be left unaltered: the script relies on this to enumerate each file. The script will wipe the second and each subsequent entry and leave the first one in its place. The order can be altered if there is a preference to keep a copy in a certain directory over an other.")

def parse_args(argv):
    for i, arg in enumerate(argv):
        if "--help" in arg:
            print_help(argv)
            return 1
        if "--size" in arg:
            options[COMPARE_SIZE] = False 
        if "--path" in arg:
            try:
                path = argv[i+1]
                if (os.path.isdir(path)):
                    options[PATH] = argv[i+1]
                else:
                    print(f"Error: Not a valid path: '{path}'.")
                    print_help(argv)
                    return 1
            except IndexError:
                print(f"Error: no path provided after '--path' flag.")
                print_help(argv)
                return 1
        if "--file" in arg:
            try:
                (path_head, path_tail) = os.path.split(argv[i+1])
                if path_head == "" or os.path.exists(path_head):
                    options[OUTFILE] = argv[i+1]
                else:
                    print(f"Error: Not a valid file or non existing path: '{path_head}' for file '{path_tail}'.")
                    print_help(argv)
                    return 1
            except IndexError:
                print(f"Error: no file provided after '--file' flag.")
                print_help(argv)
                return 1
        if "--purge" in arg:
            options[PURGING] = True
    return 0



def list_files_recursive(path, total_size_duplicates, total_duplicates):
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            total_duplicates, total_size_duplicates = list_files_recursive(full_path, total_size_duplicates, total_duplicates)
        else:
            file_name = os.path.basename(full_path)
            file_size = os.path.getsize(full_path)
            if not file_name in files_dict:
                files_dict[file_name] = [[full_path, file_size]]
            else:
                file_size_other = files_dict[file_name][0][1]
                if ((options[COMPARE_SIZE] == False) or (file_size == file_size_other)):
                    total_size_duplicates += file_size
                    total_duplicates += 1
                    files_dict[file_name].append([full_path, file_size])
                    dub_files_dict[file_name] = files_dict[file_name]
    return total_duplicates, total_size_duplicates

def list_files(path="."):
    total_size_duplicates = 0
    total_duplicates = 0
    total_duplicates, total_size_duplicates = list_files_recursive(path, total_duplicates, total_size_duplicates)
    return total_duplicates, total_size_duplicates

def factor_size(size):
    labels = ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"]
    for i, label in enumerate(labels):
        if (size < 1024):
            return round(size, 2), label
        size /= 1024
    return size, "Way too many duplicates... what are you doing, fam?"

def write_to_file(file_dict, total_duplicates, total_size_duplicates):
    size, label = factor_size(total_size_duplicates)
    with open(options[OUTFILE], "w") as f:
        m = f"Total duplicate {total_duplicates} file(s) found, amounting to {size} {label}."
        f.write(f"### {m} ### \n")
        print(m)
        for k, v in dub_files_dict.items():
            f.write(f"#{len(v)} '{k}' found in:\n")
            for p in v:
                f.write(f"    {p[0]},    {p[1]}\n")
   
def gather_files():
    to_purge_list = []
    files = []
    with open(options[OUTFILE], "r") as f:
        for l in f:
            line = l.strip()
            if (line[0:3] == "###"):
                nr_of_files = int(line.split(' ')[3])
            elif (line[0] == '#'):
                dubs = int(line[1])
                dub_counter = 0
            else:
                if (dub_counter==0):
                    to_purge_list.append(files)
                    files = []
                else:
                    file = line.split(',')[0]
                    files.append(file)
                dub_counter += 1
        to_purge_list.append(files)
    to_purge_list = list(chain.from_iterable(to_purge_list))
    if (len(to_purge_list) != nr_of_files):
        print(f"Something went wrong composing a purge list from '{options[OUTFILE]}'. Run the script again and do not modify the lines starting with '#' in the output file. Expected {nr_of_files} but found {len(to_purge_list)}.")
    else:
        return to_purge_list


def purge_duplicate_files(file_list):
    for f in file_list:
        print(f"Removing '{f}'")
        os.remove(f)


if __name__ == "__main__":
    if (len(sys.argv) > 1):
        if parse_args(sys.argv) != 0:
            sys.exit(1)
    if options[PURGING] == False:
        total_duplicates, total_size_duplicates = list_files(options[PATH])
        write_to_file(dub_files_dict, total_duplicates, total_size_duplicates)
    else:
        purge_list = gather_files()
        purge_duplicate_files(purge_list)


