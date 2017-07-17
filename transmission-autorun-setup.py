#!/usr/bin/python3

# TODO: remove options for VPN kind

import sys
import json
from pprint import pprint

new_settings = {
    "rpc-whitelist": "127.0.0.1, 192.168.*.*, 10.0.0.*",
}


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


def read_settings():
    # return dict of data
    with open('/var/lib/transmission-daemon/info/settings.json') as data_file:
        data = json.load(data_file)
    return data


def write_settings(data):
    # return dict of data
    with open('/var/lib/transmission-daemon/info/settings.json', 'w') as data_file:
        json.dump(data, data_file)


def set_boot_start(enable):
    # read daemon setting file
    lines = readfile("/etc/default/transmission-daemon")

    if not lines:
        print("ERROR: Transmission daemon settings not found!")

    for lin_num in range(len(lines)):

        if "ENABLE_DAEMON=0" in lines[lin_num] and enable:
            print("enabling daemon at boot!")
            lines[lin_num] = "ENABLE_DAEMON=1 \n"

        elif "ENABLE_DAEMON=1" in lines[lin_num] and not enable:
            print("disabling daemon on boot!")
            lines[lin_num] = "ENABLE_DAEMON=0 \n"

    writefile("/etc/default/transmission-daemon", lines, mode="w")


def config_transmission():
    # disable transmission run on boot
    # set_boot_start(False)

    # read transmission settings file and print it
    setting_dict = read_settings()

    # set new settings

    for setting_key in new_settings.keys():
        setting_dict[setting_key] = new_settings[setting_key]

    usr = input("set transmission username (enter is default): ")
    passwd = input("set password (enter is default): ")

    if usr:
        setting_dict["rpc-username"] = usr

    if passwd:
        setting_dict["rpc-password"] = passwd

    print("writing settings to file...")
    write_settings(setting_dict)


def process_arguments():
    all_args = ["transmission-autorun-setup.py",  # 0
                "--configure",  # 1
                "--deconfigure",  # 2
                "--bind-vpn-ppp",  # 3
                "--bind-vpn--openvpn"]  # 4

    # test if the args provided are a valid
    if not set(sys.argv).issubset(all_args) or not 1 < len(sys.argv) < 4:
        print("invalid arguments provided!\n", "valid args:\n", all_args[1:])

    if all_args[1] in sys.argv and not all_args[2] in sys.argv:

        # you should call configuration function here
        print("configuring Transmission now!")
        config_transmission()

        if all_args[3] in sys.argv:
            # TODO: setup rc.local with 3
            pass

        elif all_args[4] in sys.argv:
            # TODO: setup rc.local with 4
            pass


# main
process_arguments()
