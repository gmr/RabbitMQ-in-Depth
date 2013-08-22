#
# Cookbook Name:: rabbitmq_in_depth
# Recipe:: default
#
# Copyright 2013, Gavin M. Roy
#
include_recipe 'apt'
include_recipe 'chef-cookbook-ssl'
include_recipe 'git'
include_recipe 'rabbitmq'
include_recipe 'supervisor'
include_recipe 'zeromq'

# Install required OS libraries
%w[ncurses-dev].each do |pkg|
  package pkg do
    action :install
  end
end

# Enable plugins
node[:rabbitmq][:enabled_plugins].each do |plgin|
  rabbitmq_plugin plgin do
    action :enable
    notifies :restart, 'service[rabbitmq-server]', :delayed
  end
end

# Install the Python library dependencies
%w[nose pexpect pygments pyzmq readline requests tornado ipython].each do |pkg|
  python_pip pkg do
    action :install
  end
end

# Ensure the libraries used in the Python examples are always up to date
%w[pika pamqp rmqid].each do |pkg|
  python_pip pkg do
    action [:install, :upgrade]
  end
end

# Create the work Directories
%w[/opt/rabbitmq_in_depth 
   /opt/rabbitmq_in_depth/notebooks 
   /var/log/ipython 
   /home/vagrant/.ipython
   /home/vagrant/.ipython/profile_default].each do |dir|
  directory dir do
    action :create
    owner  'vagrant'
    group  'vagrant'
    mode   0755
  end
end

# Create the ipython notebook configuration
cookbook_file '/home/vagrant/.ipython/profile_default/ipython_notebook_config.py' do
  action :create
  owner  'vagrant'
  group  'vagrant'
  mode   0755
  source 'ipython_notebook_config.py'
end

# Create the ipython notebook service
supervisor_service 'ipython' do
  action :enable
  command 'ipython notebook'
  user 'vagrant'
  numprocs 1
  stdout_logfile '/var/log/ipython/stdout.log'
  stderr_logfile '/var/log/ipython/stderr.log'
end
