import os.path

fabconf = {}

#  Do not edit
fabconf['FABULOUS_PATH'] = os.path.dirname(__file__)

# Username for connecting to instaces
fabconf['SERVER_USERNAME'] = "mics"

# Full local path for .ssh
fabconf['SSH_PATH'] = "~/.ssh"

# Full local path for .ssh
fabconf['SSH_PRIVATE_KEY_PATH'] = "~/.ssh/mics_rsa"

# Project name: polls
fabconf['PROJECT_NAME'] = "mics"

# Where to install apps
fabconf['APPS_DIR'] = "/var/www/apps"

# Where you want your project installed: /APPS_DIR/PROJECT_NAME
fabconf['PROJECT_PATH'] = "%s/%s" % (fabconf['APPS_DIR'], fabconf['PROJECT_NAME'])

# App domains
fabconf['DOMAINS'] = "mics.com www.mics.com"

# Path for virtualenvs
fabconf['VIRTUALENV_DIR'] = "/var/www/apps/env"

# Email for the server admin
fabconf['ADMIN_EMAIL'] = "mics@thoughtworks.com"

# Git username for the server
fabconf['GIT_USERNAME'] = "mics-server"

# Name of the private key file used for github deployments
fabconf['GITHUB_DEPLOY_KEY_NAME'] = "github_rsa"

# Don't edit. Local path for deployment key you use for github
fabconf['GITHUB_DEPLOY_KEY_PATH'] = "%s/%s" % (fabconf['SSH_PATH'], fabconf['GITHUB_DEPLOY_KEY_NAME'])

# Path to the repo of the application you want to install
fabconf['GITHUB_REPO'] = "git@github.com:unicefuganda/mics.git"

# Virtualenv activate command
fabconf['ACTIVATE'] = "source /var/www/apps/env/%s/bin/activate" % fabconf['PROJECT_NAME']

# Name tag for your server instance
fabconf['INSTANCE_NAME_TAG'] = "mics Server"