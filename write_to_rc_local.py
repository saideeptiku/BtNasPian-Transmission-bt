#!/usr/bin/python3
#
#
import sys


rc_local_path = "/etc/rc.local"
add_begin = "# this code was added by the transmission_setup.py script #"
end_begin = "# ------------- end of transmission additions ----------- #"


def readfile(filename):
    """
    read a file
    add each line to a list
    :param filename: name of file to be read
    :return: list of each line in file
    """
    # print("reading file: " + filename)

    lines = []
    try:
        with open(filename) as file:
            for line in file:
                lines.append(line.rstrip())
        return lines
    except FileNotFoundError:
        print("failed to open file: " + filename)
        return []


def writefile(filename, text_list, mode="w+"):
    """
    write a file line by line
    :param filename: name of file to be read
    :param text_list: list of text
    :param mode of file write
    :return: list of each line in file
    """

    file = open(filename, mode)
    for item in text_list:
        file.write(str(item) + "\n")
    file.close()


def print_lines(lines):
    for line in lines:
        print(line)


def get_line_number(txt, lines, exit_on_fail=True):

    try:
        return lines.index(txt)
    except ValueError:
        if exit_on_fail:
            print("Could not find ",txt,"in", rc_local_path, "file!")
            exit("exiting..")
        else:
            return None

def write_clean_file(rc_command_lines, file_lines):
    """
    this function will run if we have not written to rc_local before
    """
    exit_lin_num = get_line_number("exit 0", file_lines)

    # clear the exit line
    # add begin line
    file_lines[exit_lin_num] = add_begin 

    # add each line by line
    for line in rc_command_lines:
        file_lines.append(line)

    # add end line
    file_lines.append(end_begin)

    # add exit line back
    file_lines.append("exit 0")

    # write file
    writefile(rc_local_path, file_lines)


def write_to_rc_local(rc_command_lines):
    """
    write commands before exit 0 in rc.local
    every command set has an entry number
    this  function will also check if commands have alreay been written

    this function adds new entry every time it is run
    """
    print("INFO: writting the following to rc.local")
    print_lines(rc_command_lines)
    print("END INFO.\n")

    file_lines = readfile(rc_local_path)

    # have we previously written to this file

    add_begin_lin_num = get_line_number(add_begin, file_lines, exit_on_fail=False)

    end_begin_lin_num = get_line_number(end_begin, file_lines, exit_on_fail=False)

    # if we have written to this file before
    if add_begin_lin_num and end_begin_lin_num:

        print("WARNING: This script has already written to", rc_local_path, "before!")
        print("WARNING: Overwritting previous commands...")
        
        del file_lines[add_begin_lin_num:end_begin_lin_num + 1]

    # write to clean file
    write_clean_file(rc_command_lines, file_lines)

    print("done.")


if __name__ == '__main__':
    
    write_to_rc_local(sys.argv[1:])
