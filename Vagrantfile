# -*- mode: ruby -*-
# vi: set ft=ruby :
require 'time'

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.provider "virtualbox" do |v|
    v.name = "rabbitmq_in_depth"
    v.customize ["setextradata", :id, "VBoxInternal/Devices/VMMDev/0/Config/GetHostTimeDisabled", "1"]
  end

  config.vm.box = "rabbitmq_in_depth"
  config.vm.box_url = "http://poisonpenllc.com/rabbitmq_in_depth.box"

  # Set the timezone to the host timezone
  timezone = 'Etc/GMT' + ((Time.zone_offset(Time.now.zone)/60)/60).to_s
  config.vm.provision :shell,:inline => "if [ $(grep -c UTC /etc/timezone) -gt 0 ]; then echo \"#{timezone}\" | sudo tee /etc/timezone && dpkg-reconfigure --frontend noninteractive tzdata; fi"

  # IPython
  config.vm.network :forwarded_port, guest: 8888, host: 8888

  # Supervisord
  config.vm.network :forwarded_port, guest: 9001, host: 9001

  # RabbitMQ AMQP
  config.vm.network :forwarded_port, guest: 5671, host: 5671
  config.vm.network :forwarded_port, guest: 5672, host: 5672

  # RabbitMQ Management Interface
  config.vm.network :forwarded_port, guest: 15670, host: 15670
  config.vm.network :forwarded_port, guest: 15671, host: 15671
  config.vm.network :forwarded_port, guest: 15672, host: 15672

  # RabbitMQ MQTT
  config.vm.network :forwarded_port, guest: 1883, host: 1883
  config.vm.network :forwarded_port, guest: 8883, host: 8883

  # RabbitMQ Stomp
  config.vm.network :forwarded_port, guest: 61613, host: 61613

end
