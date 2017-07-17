#!/bin/bash

kill_transmission(){
# kill transmission-daemon if it is running

	transmission_da_pid=$(pgrep transmission-da)
	if [ ${transmission_da_pid} ]; then
    	echo "transmission is running... killing...\n"
        sudo killall transmission-daemon && echo "Closing existing tranmission-daemon processes ..." && sleep 20
	fi
}


stop_transmission(){
# stop transmission-daemon if it is running

    transmission_da_pid=$(pgrep transmission-da)
    if [ ${transmission_da_pid} ]; then
        sudo service transmission-daemon stop  && echo "stopping transmission-daemon...\n" && sleep 20
    fi
}


manage_transmission_vpn_bind(){
	while true
	do
        # Get VPN IP to bind to
        bind_address=$(ip addr show ppp0 | grep inet | awk '{print $2}')

		# if vpn is not running then kill transmission	
        if [ -z ${bind_address} ]; then
            echo "\nVPN doesn't seem to be up."
            stop_transmission
            sleep 10
            #stop_transmission
            echo "waiting for VPN...\n"
        else

            # if transmission is running sleep for some time
            transmission_da_pid=$(pgrep transmission-da)
            if [ ${transmission_da_pid} ]; then
                date && echo "Transmission is running...\n" 
                sleep 10

            # if transmission is not running then start it and bind with vpn
            else
                #transmission-daemon --rpc-bind-address=127.0.0.1 --bind-address-ipv4=$bind_address &            
                sudo service transmission-daemon start
                echo "transmission-daemon started and bound to address $bind_address.\n"
                sleep 20
    		fi
        fi

	done

}


manage_transmission_vpn_bind
