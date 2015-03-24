#!/bin/bash
vagrant destroy -f
vagrant up primary
vagrant package --vagrantfile ../Dist/Vagrantfile --output rmqid-primary.box primary
scp -i ~/.ssh/poisonpenllc rmqid-primary.box root@gavinroy.com:/var/www/gavinroy.com/downloads/rabbitmq-in-depth/
vagrant up secondary
vagrant package --vagrantfile ../Dist/Vagrantfile --output rmqid-secondary.box secondary
scp -i ~/.ssh/poisonpenllc rmqid-secondary.box root@gavinroy.com:/var/www/gavinroy.com/downloads/rabbitmq-in-depth/
