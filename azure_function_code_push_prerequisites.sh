#!/bin/bash
set -e

# Update system
sudo apt update

# Install system tools
sudo apt install -y \
  python3 \
  python3-pip \
  nodejs \
  npm \
  dotnet-sdk-8.0

# Install Azure Functions Core Tools
sudo npm install -g azure-functions-core-tools@4 --unsafe-perm true

# Verify installs
az version
node --version
npm --version
dotnet --version
func --version
python3 --version
