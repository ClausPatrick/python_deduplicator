#!/bin/bash

mkdir -p test_dir/dir_b/dir_b/dir_c/dir_e
mkdir -p test_dir/dir_a/dir_b_b/dir_b_c/dir_b_e
mkdir -p test_dir/dir_c/dir_c_b/dir_c_c/dir_c_e
mkdir -p test_dir/dir_d/dir_d_b/dir_d_c/dir_d_e

date > file_same_size.txt
cp file_same_size.txt test_dir/dir_b
cp file_same_size.txt test_dir/dir_a/dir_b_b/
cp file_same_size.txt test_dir/dir_c/dir_c_b/dir_c_c/dir_c_e
cp file_same_size.txt test_dir/dir_d/dir_d_b/dir_d_c/dir_d_e


cat /proc/stat > file_diff_size.txt
cp file_diff_size.txt test_dir/dir_b
cat /proc/stat >> file_diff_size.txt
cp file_diff_size.txt test_dir/dir_a
cat /proc/stat >> file_diff_size.txt
cp file_diff_size.txt test_dir/dir_c/dir_c_b
cat /proc/stat >> file_diff_size.txt
cp file_diff_size.txt test_dir/dir_d/dir_d_b/dir_d_c

