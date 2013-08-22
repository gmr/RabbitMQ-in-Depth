#
# Cookbook Name:: rabbitmq-in-depth
# Recipe:: default
#
# Copyright 2013 Manning Publications
#
include_recipe 'apt'
include_recipe 'chef-cookbook-ssl'
include_recipe 'git'
include_recipe 'rabbitmq'
include_recipe 'supervisor'
include_recipe 'zeromq'
include_recipe 'rabbitmq-in-depth::ipython'

# Enable plugins
node[:rabbitmq][:enabled_plugins].each do |plgin|
  rabbitmq_plugin plgin do
    action :enable
    notifies :restart, 'service[rabbitmq-server]', :delayed
  end
end

# Ensure the libraries used in the Python examples are always up to date
%w[pika pamqp rabbitpy rmqid].each do |pkg|
  python_pip pkg do
    action [:install, :upgrade]
  end
end

git 'rabbitmq-in-depth' do
  destination '/opt/rabbitmq-in-depth'
  remote 'https://github.com/gmr/RabbitMQ-in-Depth.git'
  action :sync
end
