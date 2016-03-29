# Created by Topology-Converter
#    using topology data from: topology.dot
#    in order to use this Vagrantfile you will need:
#        -Vagrant(v1.7+) installed: http://www.vagrantup.com/downloads 
#        -Virtualbox installed: https://www.virtualbox.org/wiki/Downloads 
#        -Cumulus Plugin for Vagrant installed: $ vagrant plugin install vagrant-cumulus 
#        -the "helper_scripts" directory that comes packaged with topology-converter.py 

Vagrant.configure("2") do |config|
  ##### GLOBAL OPTIONS #####
  config.vm.provider "virtualbox" do |v|
    v.gui=false
  end
  ##### DEFINE VMs #####
  ##### DEFINE VM for cumulus1 #####
  config.vm.define "cumulus1" do |cumulus1|
      cumulus1.vm.provider "virtualbox" do |v|
        v.name = "cumulus1"
      end
      cumulus1.vm.hostname = "cumulus1"
      cumulus1.vm.box = "ubuntu/trusty64"
      cumulus1.vm.synced_folder "./ansible/", "/home/vagrant/ansible"
      cumulus1.vm.network "forwarded_port", guest: 5901, host: 6901

          # Local_Interface: eth0 Topology_File_Line(11):   "oob-01":"swp5" -- "cumulus1":"eth0"
          cumulus1.vm.network "private_network", virtualbox__intnet: 'net11', auto_config: false

      #Apply the interface re-map
      cumulus1.vm.provision "file", source: "./helper_scripts/rename_eth_swp", destination: "/home/vagrant/rename_eth_swp"
      cumulus1.vm.provision "file", source: "./helper_scripts/cumulus1_remap_eth", destination: "/home/vagrant/remap_eth"
      cumulus1.vm.provision "file", source: "./helper_scripts/cumulus1_startup_commands", destination: "/home/vagrant/cumulus1_config"
      cumulus1.vm.provision "file", source: "./helper_scripts/hosts", destination: "/home/vagrant/hosts"
      cumulus1.vm.provision "file", source: "./helper_scripts/dhcp_vagrant.conf", destination: "/home/vagrant/dhcp_vagrant.conf"
      cumulus1.vm.provision "shell", inline: "chmod 777 /home/vagrant/cumulus1_config"
      cumulus1.vm.provision "shell", inline: "/home/vagrant/cumulus1_config"

      cumulus1.vm.provider "virtualbox" do |vbox|
        vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
      end
  end

  ##### DEFINE VM for host-01 #####
  config.vm.define "host-01" do |host_01|
      host_01.vm.provider "virtualbox" do |v|
        v.name = "host-01"
      end
      host_01.vm.hostname = "host-01"
      host_01.vm.box = "ubuntu/trusty64"

          # Local_Interface: eth1 Topology_File_Line(5):   "leaf-01":"swp1" -- "host-01":"eth1"
          host_01.vm.network "private_network", virtualbox__intnet: 'net5', auto_config: false

      #Apply the interface re-map
      host_01.vm.provision "file", source: "./helper_scripts/rename_eth_swp", destination: "/home/vagrant/rename_eth_swp"
      host_01.vm.provision "file", source: "./helper_scripts/host-01_remap_eth", destination: "/home/vagrant/remap_eth"
      host_01.vm.provision "file", source: "./helper_scripts/apply_interface_remap_host", destination: "/home/vagrant/apply_interface_remap"
      host_01.vm.provision "shell", inline: "chmod 777 /home/vagrant/apply_interface_remap"
      host_01.vm.provision "shell", inline: "/home/vagrant/apply_interface_remap"

      host_01.vm.provider "virtualbox" do |vbox|
        vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
      end
  end

  ##### DEFINE VM for host-02 #####
  config.vm.define "host-02" do |host_02|
      host_02.vm.provider "virtualbox" do |v|
        v.name = "host-02"
      end
      host_02.vm.hostname = "host-02"
      host_02.vm.box = "ubuntu/trusty64"

          # Local_Interface: eth1 Topology_File_Line(6):   "leaf-02":"swp1" -- "host-02":"eth1"
          host_02.vm.network "private_network", virtualbox__intnet: 'net6', auto_config: false

      #Apply the interface re-map
      host_02.vm.provision "file", source: "./helper_scripts/rename_eth_swp", destination: "/home/vagrant/rename_eth_swp"
      host_02.vm.provision "file", source: "./helper_scripts/host-02_remap_eth", destination: "/home/vagrant/remap_eth"
      host_02.vm.provision "file", source: "./helper_scripts/apply_interface_remap_host", destination: "/home/vagrant/apply_interface_remap"
      host_02.vm.provision "shell", inline: "chmod 777 /home/vagrant/apply_interface_remap"
      host_02.vm.provision "shell", inline: "/home/vagrant/apply_interface_remap"

      host_02.vm.provider "virtualbox" do |vbox|
        vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
      end
  end

  ##### DEFINE VM for leaf-01 #####
  config.vm.define "leaf-01" do |leaf_01|
      leaf_01.vm.provider "virtualbox" do |v|
        v.name = "leaf-01"
        v.memory = 200
      end
      leaf_01.vm.hostname = "leaf-01"
      leaf_01.vm.box = "CumulusVX-2.5.5"

          # Local_Interface: eth0 Topology_File_Line(7):   "oob-01":"swp1" -- "leaf-01":"eth0"
          leaf_01.vm.network "private_network", virtualbox__intnet: 'net7', cumulus__intname: 'eth0', auto_config: true, :mac => "cc37ab72b714"

          # Local_Interface: swp1 Topology_File_Line(5):   "leaf-01":"swp1" -- "host-01":"eth1"
          leaf_01.vm.network "private_network", virtualbox__intnet: 'net5', cumulus__intname: 'swp1', auto_config: true

          # Local_Interface: swp32 Topology_File_Line(1):   "spine-01":"swp1" -- "leaf-01":"swp32"
          leaf_01.vm.network "private_network", virtualbox__intnet: 'net1', cumulus__intname: 'swp32', auto_config: true

          # Local_Interface: swp33 Topology_File_Line(2):   "spine-02":"swp1" -- "leaf-01":"swp33"
          leaf_01.vm.network "private_network", virtualbox__intnet: 'net2', cumulus__intname: 'swp33', auto_config: true

      #Apply the interface re-map
      leaf_01.vm.provision "file", source: "./helper_scripts/rename_eth_swp", destination: "/home/vagrant/rename_eth_swp"
      leaf_01.vm.provision "file", source: "./helper_scripts/leaf-01_remap_eth", destination: "/home/vagrant/remap_eth"
      leaf_01.vm.provision "file", source: "./helper_scripts/apply_interface_remap", destination: "/home/vagrant/apply_interface_remap"
      leaf_01.vm.provision "shell", inline: "chmod 777 /home/vagrant/apply_interface_remap"
      leaf_01.vm.provision "shell", inline: "/home/vagrant/apply_interface_remap"

      leaf_01.vm.provider "virtualbox" do |vbox|
        vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc5', 'allow-vms']
      end
  end

  ##### DEFINE VM for leaf-02 #####
  config.vm.define "leaf-02" do |leaf_02|
      leaf_02.vm.provider "virtualbox" do |v|
        v.name = "leaf-02"
        v.memory = 200
      end
      leaf_02.vm.hostname = "leaf-02"
      leaf_02.vm.box = "CumulusVX-2.5.5"

          # Local_Interface: eth0 Topology_File_Line(8):   "oob-01":"swp2" -- "leaf-02":"eth0"
          leaf_02.vm.network "private_network", virtualbox__intnet: 'net8', cumulus__intname: 'eth0', auto_config: true, :mac => "cc37ab72b75e"

          # Local_Interface: swp1 Topology_File_Line(6):   "leaf-02":"swp1" -- "host-02":"eth1"
          leaf_02.vm.network "private_network", virtualbox__intnet: 'net6', cumulus__intname: 'swp1', auto_config: true

          # Local_Interface: swp32 Topology_File_Line(3):   "spine-01":"swp2" -- "leaf-02":"swp32"
          leaf_02.vm.network "private_network", virtualbox__intnet: 'net3', cumulus__intname: 'swp32', auto_config: true

          # Local_Interface: swp33 Topology_File_Line(4):   "spine-02":"swp2" -- "leaf-02":"swp33"
          leaf_02.vm.network "private_network", virtualbox__intnet: 'net4', cumulus__intname: 'swp33', auto_config: true

      #Apply the interface re-map
      leaf_02.vm.provision "file", source: "./helper_scripts/rename_eth_swp", destination: "/home/vagrant/rename_eth_swp"
      leaf_02.vm.provision "file", source: "./helper_scripts/leaf-02_remap_eth", destination: "/home/vagrant/remap_eth"
      leaf_02.vm.provision "file", source: "./helper_scripts/apply_interface_remap", destination: "/home/vagrant/apply_interface_remap"
      leaf_02.vm.provision "shell", inline: "chmod 777 /home/vagrant/apply_interface_remap"
      leaf_02.vm.provision "shell", inline: "/home/vagrant/apply_interface_remap"

      leaf_02.vm.provider "virtualbox" do |vbox|
        vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc5', 'allow-vms']
      end
  end

  ##### DEFINE VM for spine-01 #####
  config.vm.define "spine-01" do |spine_01|
      spine_01.vm.provider "virtualbox" do |v|
        v.name = "spine-01"
        v.memory = 200
      end
      spine_01.vm.hostname = "spine-01"
      spine_01.vm.box = "CumulusVX-2.5.5"

          # Local_Interface: eth0 Topology_File_Line(9):   "oob-01":"swp3" -- "spine-01":"eth0"
          spine_01.vm.network "private_network", virtualbox__intnet: 'net9', cumulus__intname: 'eth0', auto_config: true, :mac => "cc37ab72b7f2"

          # Local_Interface: swp1 Topology_File_Line(1):   "spine-01":"swp1" -- "leaf-01":"swp32"
          spine_01.vm.network "private_network", virtualbox__intnet: 'net1', cumulus__intname: 'swp1', auto_config: true

          # Local_Interface: swp2 Topology_File_Line(3):   "spine-01":"swp2" -- "leaf-02":"swp32"
          spine_01.vm.network "private_network", virtualbox__intnet: 'net3', cumulus__intname: 'swp2', auto_config: true

      #Apply the interface re-map
      spine_01.vm.provision "file", source: "./helper_scripts/rename_eth_swp", destination: "/home/vagrant/rename_eth_swp"
      spine_01.vm.provision "file", source: "./helper_scripts/spine-01_remap_eth", destination: "/home/vagrant/remap_eth"
      spine_01.vm.provision "file", source: "./helper_scripts/apply_interface_remap", destination: "/home/vagrant/apply_interface_remap"
      spine_01.vm.provision "shell", inline: "chmod 777 /home/vagrant/apply_interface_remap"
      spine_01.vm.provision "shell", inline: "/home/vagrant/apply_interface_remap"

      spine_01.vm.provider "virtualbox" do |vbox|
        vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-vms']
      end
  end

  ##### DEFINE VM for spine-02 #####
  config.vm.define "spine-02" do |spine_02|
      spine_02.vm.provider "virtualbox" do |v|
        v.name = "spine-02"
        v.memory = 200
      end
      spine_02.vm.hostname = "spine-02"
      spine_02.vm.box = "CumulusVX-2.5.5"

          # Local_Interface: eth0 Topology_File_Line(10):   "oob-01":"swp4" -- "spine-02":"eth0"
          spine_02.vm.network "private_network", virtualbox__intnet: 'net10', cumulus__intname: 'eth0', auto_config: true, :mac => "cc37ab72b7a8"

          # Local_Interface: swp1 Topology_File_Line(2):   "spine-02":"swp1" -- "leaf-01":"swp33"
          spine_02.vm.network "private_network", virtualbox__intnet: 'net2', cumulus__intname: 'swp1', auto_config: true

          # Local_Interface: swp2 Topology_File_Line(4):   "spine-02":"swp2" -- "leaf-02":"swp33"
          spine_02.vm.network "private_network", virtualbox__intnet: 'net4', cumulus__intname: 'swp2', auto_config: true

      #Apply the interface re-map
      spine_02.vm.provision "file", source: "./helper_scripts/rename_eth_swp", destination: "/home/vagrant/rename_eth_swp"
      spine_02.vm.provision "file", source: "./helper_scripts/spine-02_remap_eth", destination: "/home/vagrant/remap_eth"
      spine_02.vm.provision "file", source: "./helper_scripts/apply_interface_remap", destination: "/home/vagrant/apply_interface_remap"
      spine_02.vm.provision "shell", inline: "chmod 777 /home/vagrant/apply_interface_remap"
      spine_02.vm.provision "shell", inline: "/home/vagrant/apply_interface_remap"

      spine_02.vm.provider "virtualbox" do |vbox|
        vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-vms']
      end
  end

  ##### DEFINE VM for oob-01 #####
  config.vm.define "oob-01" do |oob_01|
      oob_01.vm.provider "virtualbox" do |v|
        v.name = "oob-01"
        v.memory = 200
      end
      oob_01.vm.hostname = "oob-01"
      oob_01.vm.box = "CumulusVX-2.5.5"

          # Local_Interface: swp1 Topology_File_Line(7):   "oob-01":"swp1" -- "leaf-01":"eth0"
          oob_01.vm.network "private_network", virtualbox__intnet: 'net7', cumulus__intname: 'swp1', auto_config: true

          # Local_Interface: swp2 Topology_File_Line(8):   "oob-01":"swp2" -- "leaf-02":"eth0"
          oob_01.vm.network "private_network", virtualbox__intnet: 'net8', cumulus__intname: 'swp2', auto_config: true

          # Local_Interface: swp3 Topology_File_Line(9):   "oob-01":"swp3" -- "spine-01":"eth0"
          oob_01.vm.network "private_network", virtualbox__intnet: 'net9', cumulus__intname: 'swp3', auto_config: true

          # Local_Interface: swp4 Topology_File_Line(10):   "oob-01":"swp4" -- "spine-02":"eth0"
          oob_01.vm.network "private_network", virtualbox__intnet: 'net10', cumulus__intname: 'swp4', auto_config: true

          # Local_Interface: swp5 Topology_File_Line(11):   "oob-01":"swp5" -- "cumulus1":"eth0"
          oob_01.vm.network "private_network", virtualbox__intnet: 'net11', cumulus__intname: 'swp5', auto_config: true

      #Apply the interface re-map
      oob_01.vm.provision "file", source: "./helper_scripts/rename_eth_swp", destination: "/home/vagrant/rename_eth_swp"
      oob_01.vm.provision "file", source: "./helper_scripts/oob-01_remap_eth", destination: "/home/vagrant/remap_eth"
      oob_01.vm.provision "file", source: "./helper_scripts/oob_config", destination: "/home/vagrant/oob_config"
      oob_01.vm.provision "file", source: "./helper_scripts/apply_interface_remap_oob", destination: "/home/vagrant/apply_interface_remap"
      oob_01.vm.provision "shell", inline: "chmod 777 /home/vagrant/apply_interface_remap"
      oob_01.vm.provision "shell", inline: "/home/vagrant/apply_interface_remap"

      oob_01.vm.provider "virtualbox" do |vbox|
        vbox.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc3', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc4', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc5', 'allow-vms']
        vbox.customize ['modifyvm', :id, '--nicpromisc6', 'allow-vms']
      end
  end

end
