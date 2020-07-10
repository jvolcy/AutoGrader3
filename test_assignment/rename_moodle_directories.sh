#/bin/bash
#this script renames Moodle subimission directories such that only the student name is left.
#for example, the directory
#    Debbie Smith_1395401_assignsubmission_file_
#would be renamed
#    Debbie Smith
#the script currently works blindly:  it assumes all directories where it is executed is
#a moodle directory.  Therefore, USE CAUTION BEFORE EXECUTING!!!


for i in *; do mv "$i" "`echo $i | awk -F'_' '{print $1}'`"; done


