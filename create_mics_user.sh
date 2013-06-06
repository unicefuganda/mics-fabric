 #!/bin/bash
useradd -m mics
adduser mics sudo
usermod -s /bin/bash mics
echo 'mics ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers
