#!/bin/bash
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv F7B8CEA6056E8E56 && \
echo "deb http://www.rabbitmq.com/debian/ testing main" > /etc/apt/sources.list.d/rabbitmq.list && \
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv D208507CA14F4FCA && \
echo "deb http://packages.erlang-solutions.com/debian precise contrib" > /etc/apt/sources.list.d/erlang-solutions.list
apt-get update -qq
apt-get remove -y -qq chef puppet
apt-get autoremove -y -qq

# Add the vagrant node primary addresses
echo "
# Vagrant Node Private Addresses
192.168.50.4 primary
192.168.50.5 secondary
" >> /etc/hosts

# Let aptitude know it's a non-interactive install
export DEBIAN_FRONTEND=noninteractive

# Install packages
apt-get install -y -qq git rabbitmq-server python-pip python-dev ncurses-dev libjpeg8 python-imaging python-numpy python-opencv

# Clean up apt-leftovers
apt-get -qq -y remove curl unzip
apt-get autoremove -y
apt-get clean
rm -rf /var/lib/{apt,dpkg,cache,log}/

# Stop the already running RabbitMQ server
service rabbitmq-server stop

# Add the erlang cookie
echo "XBCDDYAVPRVEYREVJLXS" > /var/lib/rabbitmq/.erlang.cookie
chmod go-rwx /var/lib/rabbitmq/.erlang.cookie
chown rabbitmq:rabbitmq /var/lib/rabbitmq/.erlang.cookie

#  Update the RabbitMQ configuration
echo "[{rabbit, [{loopback_users, []}]}]." > /etc/rabbitmq/rabbitmq.config

# Add the plugins
PLUGINS=( rabbitmq_consistent_hash_exchange rabbitmq_management rabbitmq_management_visualiser rabbitmq_federation rabbitmq_federation_management rabbitmq_shovel rabbitmq_shovel_management rabbitmq_mqtt rabbitmq_stomp rabbitmq_tracing rabbitmq_web_stomp rabbitmq_web_stomp_examples rabbitmq_amqp1_0 )
for plugin in "${PLUGINS[@]}"
do
  rabbitmq-plugins --offline enable ${plugin}
done

# Get the RabbitMQ-In-Depth git repo
mkdir -p /opt
if [ ! -d "/opt/rabbitmq-in-depth" ]; then
  git clone https://github.com/gmr/RabbitMQ-in-Depth.git /opt/rabbitmq-in-depth
fi
chown -R vagrant:vagrant /opt/rabbitmq-in-depth

echo "
jinja2
mosquitto
nose
pika
pamqp
pexpect
pygments
pyzmq
jsonschema
rabbitpy
readline
requests
stomp.py
statelessd
tornado
ipython
"  > /tmp/requirements.pip
pip install -r /tmp/requirements.pip
rm /tmp/requirements.pip


# Configuration file for ipython-notebook.
mkdir -p /var/log/ipython
mkdir -p /home/vagrant/.ipython/profile_default
echo "c = get_config()

c.InteractiveShell.autoindent = True
c.NotebookApp.ip = '*'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
c.NotebookApp.ipython_dir = u'/home/vagrant/.ipython'
c.NotebookApp.notebook_dir = u'/opt/rabbitmq-in-depth/notebooks'
c.ContentsManager.hide_globs = [u'__pycache__', '*.pyc', '*.pyo', '.DS_Store', '*.so', '*.dylib', '*~', 'ch6']
" > /home/vagrant/.ipython/profile_default/ipython_notebook_config.py
chown vagrant:vagrant -R /home/vagrant/.ipython

echo "# IPython Notebook Upstart Script
respawn

chdir /home/vagrant
setuid vagrant

start on runlevel [2345]
stop on runlevel [06]

exec ipython notebook --ipython-dir=/home/vagrant/.ipython
" > /etc/init/ipython.conf

echo "# Statelessd Upstart Script
respawn

start on runlevel [2345]
stop on runlevel [06]

exec /usr/local/bin/tinman -c /etc/statelessd.yml -f
" > /etc/init/statelessd.conf

echo "%YAML 1.2
---
Daemon:
  pidfile: /var/run/statelessd/statelessd.pid
  user: nginx

Application:
  debug: False
  xsrf_cookies: false
  paths:
    base: /usr/local/share/statelessd
    static: static
    templates: templates
  rabbitmq:
    host: localhost
    port: 5672

HTTPServer:
  no_keep_alive: false
  ports: [8900]
  xheaders: false

Routes:
 - ['/([^/]+)/([^/]+)/([^/]+)', statelessd.Publisher]
 - [/stats, statelessd.Stats]
 - [/, statelessd.Dashboard]

Logging:
  version: 1
  formatters:
    verbose:
      format: '%(levelname) -10s %(asctime)s %(processName)-20s %(name) -35s %(funcName) -30s: %(message)s'
      datefmt: '%Y-%m-%d %H:%M:%S'
    syslog:
      format: '%(levelname)s <PID %(process)d:%(processName)s> %(name)s.%(funcName)s(): %(message)s'
  filters: []
  handlers:
    console:
      class: logging.StreamHandler
      formatter: verbose
      debug_only: false
    syslog:
      class: logging.handlers.SysLogHandler
      facility: daemon
      address: /dev/log
      formatter: syslog
  loggers:
    clihelper:
      level: WARNING
      propagate: true
      handlers: [console, syslog]
    pika:
      level: INFO
      propagate: true
      handlers: [console, syslog]
    pika.adapters:
      level: DEBUG
      propagate: true
      handlers: [console, syslog]
    pika.connection:
      level: DEBUG
      propagate: true
      handlers: [console, syslog]
    statelessd:
      level: INFO
      propagate: true
      handlers: [console, syslog]
    tinman:
      level: INFO
      propagate: true
      handlers: [console, syslog]
    tornado:
      level: WARNING
      propagate: true
      handlers: [console, syslog]
  disable_existing_loggers: true
  incremental: false
" > /etc/statelessd.yml

service rabbitmq-server start
service ipython start
service statelessd start
