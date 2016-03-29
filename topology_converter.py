#
#
#    Topology Converter
#       converts a given topology.dot file to a Vagrantfile
#           can use the virtualbox Vagrant provider
# Initially written by Eric Pulvino 2015-10-19
#
#    Changelog:
#   v1.0 -- 2015-10-19: Initial version constructed
#   v2.0 -- 2016-01-07: Added Support for MAC handout, empty playbook, [EMPTY] connections, "vagrant" interface remapping
#                       warnings for interface reuse.
#   to do: 
#       -Use proper dot file parsing library
#       -Add support for libvirt Vagrant file output
#       -Add Sanity checking for "good" hostnames (no leading numbers, no spaces, etc)


import os
import re
import sys
from definitions import *
from collections import defaultdict

#Hardcoded Variables
topology_file=sys.argv[1] #accept our topology file as input
VAGRANTFILE="./Vagrantfile" #Set our vagrantfile output. Existing VAGRANTFILES will be overwritten
script_storage="./helper_scripts" #Location for our generated remap files
clean_up=False #Don't use this-- it removes the generated remap_eth files
verbose=False #Debugging Mode
switch_mem="200" #in MB
generate_ansible_hostfile=False

#MAC Address Configuration
custom_mac=True  #set this to False to use all randomly generated macs.
sequential_mac=False #set this to False to use the MAC Map from the definitions File
start_mac="A00000000000" #If Custom Mac is true this is the starting MAC for assignment
dhcp_mac_file="./dhcp_mac_map" #If Sequential MAC is true, This file will be created to store the mapping


#Static Variables
#Do not change!
warning=False

###### Functions
def mac_fetch(hostname,mac_file,interface):
    global sequential_mac
    global start_mac
    global mac_map
    mac_string=""
    if interface != "eth0": return mac_string
    if not sequential_mac and hostname in mac_map: 
        mac_string=", :mac => \""+mac_map[hostname]+"\""
    elif sequential_mac: 
        new_mac = hex(int(start_mac, 16) + 1)[2:].upper()
        start_mac = new_mac
        mac_string=", :mac => \""+new_mac+"\""
        mac_file.write(hostname+", "+new_mac+"\n")
    return mac_string

def Generate_VM_Config(vfile,hostname,connection_map,hostname_code_mapper,mac_file):
    filtered_hostname=hostname.replace("-","_")
    vfile.write("  ##### DEFINE VM for "+hostname+" #####\n")
    vfile.write("  config.vm.define \"" + hostname + "\" do |" + filtered_hostname + "|\n")
    vfile.write("      "+filtered_hostname+".vm.provider \"virtualbox\" do |v|\n")
    vfile.write("        v.name = \""+hostname+"\"\n")
    if hostname_code_mapper[hostname][0] == "switch":
        vfile.write("        v.memory = "+switch_mem+"\n")
    vfile.write("      end\n")
    vfile.write("      "+filtered_hostname+".vm.hostname = \""+hostname+"\"\n")
    vfile.write("      "+filtered_hostname+".vm.box = \""+hostname_code_mapper[hostname][1]+"\"\n")


    
    vfile.write("\n")
    for (interface,net_name,line,line_number) in connection_map[hostname]:
        vfile.write("          # Local_Interface: "+interface+" Topology_File_Line("+line_number+"):"+line)
        mac_string="" #set to empty default
        if custom_mac and interface == "eth0":
            mac_string=mac_fetch(hostname,mac_file,interface)
        if hostname_code_mapper[hostname][0] == "server":
            vfile.write("          "+filtered_hostname+".vm.network \"private_network\", virtualbox__intnet: '"+net_name+"', auto_config: false"+mac_string+"\n\n")
        else:
            vfile.write("          "+filtered_hostname+".vm.network \"private_network\", virtualbox__intnet: '"+net_name+"', cumulus__intname: '"+interface+"', auto_config: true"+mac_string+"\n\n")


    if hostname_code_mapper[hostname][0] == "switch" or hostname in debian_host_remaps:
        vfile.write("      #Apply the interface re-map\n")
        vfile.write("      "+filtered_hostname+".vm.provision \"file\", source: \""+script_storage+"/rename_eth_swp\", destination: \"/home/vagrant/rename_eth_swp\"\n")
        vfile.write("      "+filtered_hostname+".vm.provision \"file\", source: \""+script_storage+"/"+hostname+"_remap_eth\", destination: \"/home/vagrant/remap_eth\"\n")
        if hostname == "oob-01":
            vfile.write("      "+filtered_hostname+".vm.provision \"file\", source: \""+script_storage+"/oob_config\", destination: \"/home/vagrant/oob_config\"\n")
            vfile.write("      "+filtered_hostname+".vm.provision \"file\", source: \""+script_storage+"/apply_interface_remap_oob\", destination: \"/home/vagrant/apply_interface_remap\"\n")
        elif hostname == "cumulus1":
            vfile.write("      "+filtered_hostname+".vm.provision \"file\", source: \""+script_storage+"/cumulus1_startup_commands\", destination: \"/home/vagrant/cumulus1_config\"\n")
            vfile.write("      "+filtered_hostname+".vm.provision \"file\", source: \""+script_storage+"/hosts\", destination: \"/home/vagrant/hosts\"\n")
            vfile.write("      "+filtered_hostname+".vm.provision \"file\", source: \""+script_storage+"/dhcp_vagrant.conf\", destination: \"/home/vagrant/dhcp_vagrant.conf\"\n")
            vfile.write("      "+filtered_hostname+".vm.provision \"shell\", inline: \"chmod 777 /home/vagrant/cumulus1_config\"\n")
            vfile.write("      "+filtered_hostname+".vm.provision \"shell\", inline: \"/home/vagrant/cumulus1_config\"\n\n")    
        elif hostname in debian_host_remaps:
            vfile.write("      "+filtered_hostname+".vm.provision \"file\", source: \""+script_storage+"/apply_interface_remap_host\", destination: \"/home/vagrant/apply_interface_remap\"\n")
        else:
            vfile.write("      "+filtered_hostname+".vm.provision \"file\", source: \""+script_storage+"/apply_interface_remap\", destination: \"/home/vagrant/apply_interface_remap\"\n")
        if hostname != "cumulus1":
            vfile.write("      "+filtered_hostname+".vm.provision \"shell\", inline: \"chmod 777 /home/vagrant/apply_interface_remap\"\n")
            vfile.write("      "+filtered_hostname+".vm.provision \"shell\", inline: \"/home/vagrant/apply_interface_remap\"\n\n")    

    
    vfile.write("      "+filtered_hostname+".vm.provider \"virtualbox\" do |vbox|\n")
    count=1
    for (interface,net_name,line,line_number) in connection_map[hostname]:
        vfile.write("        vbox.customize ['modifyvm', :id, '--nicpromisc"+str(count+1)+"', 'allow-vms']\n")
        count +=1
    vfile.write("      end\n")
    vfile.write("  end\n\n")


def getKey(item):
    base = 10
    if item[0][0:3].lower() == "eth": base = 0
    val = float(item[0][3:].replace("s","."))
    return val + base

def remove_generated_files(hostname_code_mapper):
    import os
    for hostname in hostname_code_mapper:
        if hostname_code_mapper[hostname][0]=="switch":
            os.remove(script_storage+"/"+hostname+"_remap_eth")

def generate_remapping_files(hostname_code_mapper,connection_map,debian_host_remaps):
    for hostname in hostname_code_mapper:
        if hostname_code_mapper[hostname][0]=="switch" or hostname in debian_host_remaps:
            #We must create a remap file
            filename=script_storage+"/"+hostname+"_remap_eth"
            with open(filename,"wb") as remap_file:
                remap_file.write("""# Which method to use to re-map the NICs
# Options are "simple", which just renumberes ethN->swpN, or "mapped" which
# uses the array below to re-map ethN names.
REMAP_METHOD="mapped"
# Map of ethN names to new names. The new name can be anything you like, as
# long as the kernel accepts it.
MAP="
     eth0=vagrant\n""")
                count=1
                for (interface,net_name,line,line_number) in connection_map[hostname]:
                    remap_file.write("     eth"+str(count)+"="+interface+"\n")
                    count+=1
                remap_file.write("\"\n")


def parse_topology_file():
    global warning
    print "\n######################################"
    print "          Topology Converter"
    print "######################################"
    #Print collected Content from Definitions.py file
    print "\n\nSwitch OS will be: \"" + switch_code + "\""
    print "   On the following devices..."
    for device in switches:
        print "    * " + device
    print 
    print ""
    print "Server OS will be: \"" + server_code + "\""
    print "   On the following devices..."
    for device in servers:
        print "    * " + device

    #Open topology file
    with open(topology_file,"r") as f1:
        file_contents= f1.readlines()
    #Key is hostname, value is [(port,net_number,topo_line,topo_line_number)]
    ##### This could be done with a class
    connection_map=defaultdict(list)
    #Map Hostnames seen in Topology file to Hostnames defined in the Definitions.py File
    #Key is hostname, value is ("switch/server","box_vers_to_run")
    hostname_code_mapper={}
    
    #Parse Topology_File
    net_number=1
    line_number=0
    print "\n###############################"
    print "   Topology File Contents:"
    print "###############################"
    for line in file_contents:
        if line_number == 0: line_number +=1; continue #Skip First line
        elif not re.match("^.* -- .*$",line): continue
        
        new_net=True
        net_name="net" + str(net_number)
        line_pieces=line.split("--")
        
        left_side=line_pieces[0].replace("\n","").replace(" ","").replace('"','')
        right_side=line_pieces[1].replace("\n","").replace(" ","").replace('"','')

        if left_side != "[EMPTY]":
            lhostname,linterface=left_side.split(":")
        if right_side != "[EMPTY]":
            rhostname,rinterface=right_side.split(":")

        #### Adding [EMPTY] Support checking
        if left_side == "[EMPTY]" and right_side == "[EMPTY]":
            warning=True
            print "WARNING: Topology File (Line %s) -- Both sides set to [EMPTY], skipping line." %(line_number)
            line_number +=1
            continue #Skip this line

        #check for hostname existance in definitions.py
        if left_side != "[EMPTY]":
            if lhostname in switches: hostname_code_mapper[lhostname]=("switch",switch_code)
            elif lhostname in servers: hostname_code_mapper[lhostname]=("server",server_code)
            else:
                print "ERROR: We have found a Hostname (\""+lhostname+"\") in the Topology File that is not specified"
                print "       as a switch or server in the definitions.py file!"
                exit(1)
        if right_side != "[EMPTY]":
            if rhostname in switches: hostname_code_mapper[rhostname]=("switch",switch_code)
            elif rhostname in servers: hostname_code_mapper[rhostname]=("server",server_code)
            else:
                print "ERROR: We have found a Hostname (\""+rhostname+"\") in the Topology File that is not specified"
                print "       as a switch or server in the definitions.py file!"
                exit(1)

        #check to see if interface/hostname combo has already been declared elsewhere
        left_exists = -1
        index=0
        if left_side != "[EMPTY]":
            if lhostname in connection_map:
                for link in connection_map[lhostname]:
                    if link[0] == linterface:
                        left_exists=index
                        new_net=False
                        #leftside interface already exists use his net_name
                        warning=True
                        print "WARNING: Topology File (Line %s) -- Interface %s%s is already used." %(line_number,lhostname,linterface)
                        net_name=link[1]
                    index+=1

        right_exists = -1
        index=0
        if right_side != "[EMPTY]":
            if rhostname in connection_map:
                for link in connection_map[rhostname]:
                    if link[0] == rinterface:
                        right_exists=index
                        print "WARNING: Topology File (Line %s) -- Interface %s%s is already used." %(line_number,rhostname,rinterface)
                        warning=True
                        if not new_net and net_name!=link[1]:
                            print "WARN: Both interfaces have already been used in the following topology file line:"
                            print "    " + line
                            print "   Move this line to the top of the topology file and try again."
                            exit(1)
                        new_net=False
                        #rightside interface already exists use his net_name
                        net_name=link[1]
                    index+=1

        #add interfaces to connection map
        if left_exists == -1 and left_side != "[EMPTY]": connection_map[lhostname].append([linterface,net_name,line,str(line_number)])
        else:
            connection_map[lhostname][left_exists][2] = "Multiple Lines Generated this Line\n"
            connection_map[lhostname][left_exists][3] = "multi"

        if right_exists == -1 and right_side != "[EMPTY]": connection_map[rhostname].append([rinterface,net_name,line,str(line_number)])
        else:
            connection_map[rhostname][right_exists][2] = "Multiple Lines Generated this Line\n"
            connection_map[rhostname][right_exists][3] = "multi"
    

        print "   "+net_name + "    " + left_side + " " + right_side
        if new_net: net_number +=1
        line_number +=1

    if warning:
        print "\n\n  **** WARNING!!! **** "
        print "             There are warnings above! LOOK AT THEM!<<<"  
        print "  **** WARNING!!! **** "

    #Sort the list for proper interface mapping
    for hostname in connection_map:
        connection_map[hostname].sort(key=getKey)
    if verbose:
        for hostname in connection_map:
            print "\nHostname: " + hostname
            for (interface,net_name,line,line_number) in connection_map[hostname]:
                print "    " + interface + " -- " + net_name
    return hostname_code_mapper,connection_map

def generate_vagrantfile(hostname_code_mapper,connection_map):
    global verbose
    #Build Vagrant_file for VirtualBox

    mac_file = open(dhcp_mac_file,"w")
    with open(VAGRANTFILE,"w") as vfile:
        vfile.write("# Created by Topology-Converter\n#    using topology data from: "+topology_file+"\n")
        vfile.write("#    in order to use this Vagrantfile you will need:\n")
        vfile.write("#        -Vagrant(v1.7+) installed: http://www.vagrantup.com/downloads \n")
        vfile.write("#        -Virtualbox installed: https://www.virtualbox.org/wiki/Downloads \n")
        if generate_ansible_hostfile:
            vfile.write("#        -Ansible (v1.9+) installed: http://docs.ansible.com/ansible/intro_installation.html \n")
        vfile.write("#        -Cumulus Plugin for Vagrant installed: $ vagrant plugin install vagrant-cumulus \n")
        vfile.write("#        -the \"helper_scripts\" directory that comes packaged with topology-converter.py \n\n")
        vfile.write("""Vagrant.configure(\"2\") do |config|
  ##### GLOBAL OPTIONS #####
  config.vm.provider \"virtualbox\" do |v|
    v.gui=false
  end""")        #If using ansible, we'll generate a hostfile
        if generate_ansible_hostfile:
            with open("./helper_scripts/empty_playbook.yml","w") as playbook:
                playbook.write("""---
- hosts: all
  user: vagrant
  tasks:
    - command: "uname -a"
""")
            vfile.write("""
  #Generating Ansible Host File at following location:
  #    ./.vagrant/provisioners/ansible/inventory/vagrant_ansible_inventory
  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "./helper_scripts/empty_playbook.yml"
  end""")
    
        vfile.write("\n  ##### DEFINE VMs #####\n")
        if first_device_to_boot != "":
            Generate_VM_Config(vfile,first_device_to_boot,connection_map,hostname_code_mapper,mac_file)
        for hostname in servers:
            if first_device_to_boot == hostname: continue
            elif hostname in connection_map:
                Generate_VM_Config(vfile,hostname,connection_map,hostname_code_mapper,mac_file)
            else:
                if verbose: print "Hostname %s which exists in server list that is not found in topology file... skipping."
        for hostname in switches:
            if first_device_to_boot == hostname: continue
            elif hostname in connection_map:
                Generate_VM_Config(vfile,hostname,connection_map,hostname_code_mapper,mac_file)
            else:
                if verbose: print "Hostname %s which exists in server list that is not found in topology file... skipping."
            
        vfile.write("end\n")
    mac_file.close()
    if not custom_mac: os.remove(dhcp_mac_file)

def main():
    hostname_code_mapper,connection_map = parse_topology_file()

    generate_remapping_files(hostname_code_mapper,connection_map,debian_host_remaps)
    
    generate_vagrantfile(hostname_code_mapper,connection_map)

    if clean_up: remove_generated_files(hostname_code_mapper)

    
if __name__ == "__main__":
    main()
    print "\nVagrantfile has been generated!\n"
    if warning:
        print "\nDONE WITH ***WARNING***\n"
    else:
        print "\nDONE!\n"
exit(0)

