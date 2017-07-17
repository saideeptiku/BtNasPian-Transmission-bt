#!/bin/bash
#
# before you do anything, please read through this file carefully
#


add_ppa_if_not_exits() {
	#     ppa exits in sources directory        OR   in sources file    
    if ! grep -q "$1" /etc/apt/sources.list.d/* -o  grep -q "$1" /etc/apt/sources.list ; 
    then
        # commands to add the ppa ...
        echo "$1 ppa will be added"
        sleep 0.5
        sudo add-apt-repository ppa:"$1" -y
        sudo apt update
    else
    	echo "$1 ppa will NOT be added"
    	sleep 0.5
    fi
}


# TODO: give this function options for openVPN and ppp
install_and_setup_transmission_daemon(){
	# add the ppa
	add_ppa_if_not_exits "transmissionbt/ppa"

	# install transmission
	sudo apt-get install transmission-cli transmission-common transmission-daemon -y

	# stop the daemon
	sudo service transmission-daemon stop
	
	# call settings script
	sudo python3 transmission-autorun-setup.py --configure 

	# make entry in rc.local
    sleep_txt="sleep 30"

    cwd=$(pwd)

    cmd_txt="sudo sh $cwd/my_transmission_daemon.sh > $cwd/daemon.log &"
    sudo python3 write_to_rc_local.py "$sleep_txt" "$cmd_txt"
	
	echo "done.."
			
}


remove_transmission(){
    # remove transmission
    sudo apt-get remove transmission-cli transmission-common transmission-daemon -y

    # make entry in rc.local
    sleep_txt="sleep 10"

    cwd=$(pwd)

    cmd_txt="date"
    sudo python3 write_to_rc_local.py "$sleep_txt" "$cmd_txt"

	echo "done..."
}


