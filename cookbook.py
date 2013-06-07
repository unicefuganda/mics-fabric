# cookbook.py
# This file describes the packages to install and how to set them up.
#
# Ingredients: nginx, memecached, gunicorn, supervisord, virtualenv, git

recipe = [
  # First command as regular user
  {"action":"run", "params":"whoami"},

  # sudo apt-get update
  {"action":"sudo", "params":"apt-get update -qq",
    "message":"Updating apt-get"},

  # List of APT packages to install
  {"action":"apt",
    "params":["postgresql", "libpq-dev", "libxml2", "libxslt-dev", "nginx", "memcached", "git",
      "python-setuptools", "python-dev", "build-essential", "python-pip", "python-psycopg2"],
    "message":"Installing apt-get packages"},

  # List of pypi packages to install
  {"action":"pip", "params":["virtualenv", "virtualenvwrapper","supervisor"],
    "message":"Installing pip packages"},

  # postgres
  {"action":"run", "params":"sudo -u postgres createdb -O postgres mics", "message": "creating database"},
  {"action":"run", "params":"sudo -u postgres psql -c \"CREATE ROLE mics WITH ENCRYPTED PASSWORD 'mics';\"", "message": "creating database user"},
  {"action":"run", "params":"sudo -u postgres psql -c \"ALTER USER mics LOGIN;\"", "message": "adding db permissions"},

  # nginx
  {"action":"put", "params":{"file":"%(FABULOUS_PATH)s/templates/nginx.conf",
    "destination":"/home/%(SERVER_USERNAME)s/nginx.conf"},
    "message":"Configuring nginx"},
  {"action":"sudo", "params":"mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old"},
  {"action":"sudo", "params":"mv /home/%(SERVER_USERNAME)s/nginx.conf /etc/nginx/nginx.conf"},
  {"action":"sudo", "params":"chown root:root /etc/nginx/nginx.conf"},
  {"action":"put_template", "params":{"template":"%(FABULOUS_PATH)s/templates/nginx-app-proxy",
                                      "destination":"/home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s"}},
  {"action":"sudo", "params":"rm -rf /etc/nginx/sites-enabled/default"},
  {"action":"sudo", "params":"mv /home/%(SERVER_USERNAME)s/%(PROJECT_NAME)s /etc/nginx/sites-available/%(PROJECT_NAME)s"},
  {"action":"sudo", "params":"ln -s /etc/nginx/sites-available/%(PROJECT_NAME)s /etc/nginx/sites-enabled/%(PROJECT_NAME)s"},
  {"action":"sudo", "params":"chown root:root /etc/nginx/sites-available/%(PROJECT_NAME)s"},
  {"action":"sudo", "params":"/etc/init.d/nginx restart", "message":"Restarting nginx"},

  # virtualenvwrapper
  {"action":"sudo", "params":"mkdir -p %(VIRTUALENV_DIR)s", "message":"Configuring virtualenvwrapper"},
  {"action":"sudo", "params":"chown -R %(SERVER_USERNAME)s: %(VIRTUALENV_DIR)s"},
  {"action":"run", "params":"echo 'export WORKON_HOME=%(VIRTUALENV_DIR)s' >> /home/%(SERVER_USERNAME)s/.profile"},
  {"action":"run", "params":"echo 'source /usr/local/bin/virtualenvwrapper.sh' >> /home/%(SERVER_USERNAME)s/.profile"},
  {"action":"run", "params":"source /home/%(SERVER_USERNAME)s/.profile"},

  # webapps alias
  {"action":"run", "params":"""echo "alias webapps='cd %(APPS_DIR)s'" >> /home/%(SERVER_USERNAME)s/.profile""",
    "message":"Creating webapps alias"},

  # domain code
  {"action": "run", "params": "mkdir %(DOMAIN_HOME)s", "message": "Creating directory to store current and releases"},

  # webapps dir
  {"action":"sudo", "params":"mkdir -p %(APPS_DIR)s", "message":"Creating webapps directory"},
  {"action":"sudo", "params":"chown -R %(SERVER_USERNAME)s: %(APPS_DIR)s"},

  # git setup
  {"action":"run", "params":"git config --global user.name '%(GIT_USERNAME)s'",
    "message":"Configuring git"},
  {"action":"run", "params":"git config --global user.email '%(ADMIN_EMAIL)s'"},
  {"action":"put", "params":{"file":"%(GITHUB_DEPLOY_KEY_PATH)s",
                            "destination":"/home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s"}},
  {"action":"run", "params":"chmod 600 /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s"},
  {"action":"run", "params":"""echo 'IdentityFile /home/%(SERVER_USERNAME)s/.ssh/%(GITHUB_DEPLOY_KEY_NAME)s' >> /home/%(SERVER_USERNAME)s/.ssh/config"""},
  {"action":"run", "params":"ssh-keyscan github.com >> /home/%(SERVER_USERNAME)s/.ssh/known_hosts"},

  # Create virtualevn
  {"action":"run", "params":"mkvirtualenv --no-site-packages %(PROJECT_NAME)s",
    "message":"Creating virtualenv"},

  # install django in virtual env
  {"action":"virtualenv", "params":"pip install django",
    "message":"Installing django"},
  {"action":"run", "params":"cd %(DOMAIN_HOME)s; git clone -q -o deploy --depth 1 %(GIT_URL)s curr", "message":"Deploying mics"},

  # install gunicorn in virtual env
  {"action":"virtualenv", "params":"pip install gunicorn",
    "message":"Installing gunicorn"},
  {"action":"put", "params":{"file":"%(FABULOUS_PATH)s/templates/gunicorn.conf.py",
                            "destination":"%(PROJECT_PATH)s/gunicorn.conf.py"}},

  # Setup supervisor
  {"action":"run", "params":"echo_supervisord_conf > /home/%(SERVER_USERNAME)s/supervisord.conf",
    "message":"Configuring supervisor"},
  {"action":"put_template", "params":{"template":"%(FABULOUS_PATH)s/templates/supervisord.conf",
                                      "destination":"/home/%(SERVER_USERNAME)s/my.supervisord.conf"}},
  {"action":"run", "params":"cat /home/%(SERVER_USERNAME)s/my.supervisord.conf >> /home/%(SERVER_USERNAME)s/supervisord.conf"},
  {"action":"run", "params":"rm /home/%(SERVER_USERNAME)s/my.supervisord.conf"},
  {"action":"sudo", "params":"mv /home/%(SERVER_USERNAME)s/supervisord.conf /etc/supervisord.conf"},
  {"action":"sudo", "params":"supervisord"},
  {"action":"put", "params":{"file":"%(FABULOUS_PATH)s/templates/supervisord-init",
                            "destination":"/home/%(SERVER_USERNAME)s/supervisord-init"}},
  {"action":"sudo", "params":"mv /home/%(SERVER_USERNAME)s/supervisord-init /etc/init.d/supervisord"},
  {"action":"sudo", "params":"chmod +x /etc/init.d/supervisord"},
  {"action":"sudo", "params":"update-rc.d supervisord defaults"}
]