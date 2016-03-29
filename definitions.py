

#This is the Vagrant Box that will be used for all switches
switch_code="CumulusVX-2.5.5"
#These are the hostnames for the switches
switches=["leaf-01","leaf-02","spine-01","spine-02","oob-01"]

#This is the Vagrant Box that will be used for all servers
server_code="ubuntu/trusty64"
#These are the hostnames for the servers
servers=["host-01","host-02","cumulus1"]


#DataBank Specials
#Debian hosts that should also have remapped interfaces.
debian_host_remaps=["host-01","host-02","cumulus1"]

# If set to anything other than "", the listed device will appear first in the Vagrantfile.
first_device_to_boot="cumulus1"

#Mac to Hostname Mapping -- Sets MAC on ETH0 interface for the following hostnames
mac_map={"leaf-01":"cc37ab72b714",
         "leaf-02":"cc37ab72b75e",
         "spine-01":"cc37ab72b7f2",
         "spine-02":"cc37ab72b7a8",
         "host-01":"A00000000001",
         "host-02":"A00000000002",
         "oob-01":"A00000000009",
        }


