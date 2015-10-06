# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

PILLAR = {
  'korform' => {
    'db_username' => 'korform',
    'db_password' => 'korform',
    'root'        => '/vagrant',
    'owner'       => 'vagrant',
  },
}

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # Build it off a standard Debian 8.2 box
  config.vm.box = "box-cutter/debian82"
  
  # Prepare for Salt provisioning
  config.vm.synced_folder 'provisioning/salt', '/srv/salt'
  config.vm.provision :shell, inline: 'sudo mkdir -p /etc/salt && sudo touch /etc/salt/minion && sudo chown vagrant /etc/salt/minion' # Vagrant Issue #5973
  
  # Forward some ports
  config.vm.network "forwarded_port", guest: 8000, host: 8000 # Django
  
  # Set CPU count and RAM limits
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 1 # VB is HORRIBLY BROKEN with multicore
  end
  config.vm.provider "vmware_fusion" do |v|
    v.vmx["memsize"] = "2048"
    v.vmx["numvcpus"] = "2"
  end
  
  # Provision with Salt
  config.vm.provision :salt do |salt|
    salt.bootstrap_options = '-F -c /tmp -P -i vagrant' # Vagrant Issue #6011, #6029
    salt.minion_config = 'provisioning/salt_minion'
    
    salt.run_highstate = true
    salt.log_level = 'info'
    salt.colorize = true
    
    salt.pillar PILLAR
  end
end
