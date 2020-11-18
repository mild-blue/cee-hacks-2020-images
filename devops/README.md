# Devops

## Docker Setup

1. `sudo apt-get remove docker docker-engine docker.io containerd runc`
1. `sudo apt-get update`
1. `sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg-agent \
        software-properties-common`
1. `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`
1. `sudo add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"`
1. `sudo apt-get update`
1. `sudo apt-get install -y docker-ce docker-ce-cli containerd.io`
1. `sudo groupadd docker`
1. `sudo usermod -aG docker $USER`
1. `newgrp docker`

## Docker Compose Setup

1. `sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
1. `sudo chmod +x /usr/local/bin/docker-compose`
1. `sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose`
