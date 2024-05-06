#!/bin/bash

# Function to check and install dependencies
check_dependencies() {
    local dependencies=(opam libcurl4-gnutls-dev libfuse-dev m4 pkg-config)

    for dependency in "${dependencies[@]}"; do
        if ! dpkg -l "$dependency" &> /dev/null; then
            echo "$dependency is not installed. Installing..."
            sudo apt-get install -y "$dependency"
        fi
    done
}

# Check and install dependencies
check_dependencies

# Check if google-drive-ocamlfuse is installed
if ! command -v google-drive-ocamlfuse &> /dev/null; then
    echo "google-drive-ocamlfuse is not installed. Installing..."
    sudo add-apt-repository ppa:alessandro-strada/ppa
    sudo apt-get update
    sudo apt-get install google-drive-ocamlfuse
fi

# Create a directory to mount Google Drive
mkdir -p ~/GoogleDrive

# Authenticate and mount specific folder
folder_id="YOUR_FOLDER_ID_HERE"
google-drive-ocamlfuse -id $folder_id ~/GoogleDrive

echo "Google Drive folder mounted successfully at ~/GoogleDrive"
