FROM node:22

# Install NodeJS, Python, Docker, and CDK
RUN apt-get update && apt-get install -y \
    make \
    software-properties-common \
    python3-pip \
    python3-venv \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && npm install -g aws-cdk ts-node \
    && rm -rf /var/lib/apt/lists/*

# Agregar la clave GPG oficial de Docker
RUN mkdir -m 0755 -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | tee /etc/apt/keyrings/docker.asc > /dev/null

# Agregar el repositorio de Docker
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \ 
    https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker
RUN apt-get update && apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
