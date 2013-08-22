#
# Cookbook Name:: rabbitmq-in-depth
# Recipe:: ipython
#
# Copyright 2013 Manning Publications
#
# Install required OS libraries
%w[ncurses-dev].each do |pkg|
  package pkg do
    action :install
  end
end

# Install the Python library dependencies
%w[nose pexpect pygments pyzmq readline requests tornado ipython].each do |pkg|
  python_pip pkg do
    action :install
  end
end

# Create the work Directories
%w[/var/log/ipython 
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
