#topology_converter readme
Using the script:
topology_converter.py topology.dot

This will create the vagrant file.

#helper_scripts
dhcp_vagrant.conf - Edit domains and hostnames and mac addresses
    option host-name "leaf-01";
    option domain-name "cumulus.local";
remap_eth - Create new mapping of interfaces
hosts - rename IP and hostnames

#Hard coded names
topology_converter.py - switch case statement with hard coded device names at line 86:
    if hostname == "oob-01":
    elif hostname == "cumulus1":
    elif hostname in debian_host_remaps:
    else:
    if hostname != "cumulus1":
