FROM node:23

# Install NodeJS, Python, Docker, and CDK
RUN apt-get update && apt-get install -y \
    make \
    software-properties-common \
    python3 \
    python3-pip \
    && npm install -g aws-cdk ts-node \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app