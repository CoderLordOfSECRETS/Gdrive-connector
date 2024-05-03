#!/bin/bash

# Clone the GitHub repository
git clone https://github.com/your_username/your_repository.git
cd your_repository

# Install dependencies
pip3 install -r requirements.txt

# Run the Python script
python3 your_script.py

# Check if the script ran successfully
if [ $? -eq 0 ]; then
    # Mount the Google Drive folder using FUSE
    google-drive-ocamlfuse -headless -label label_name -id client_id -secret client_secret
    mkdir -p /global
    google-drive-ocamlfuse /global
    echo "Google Drive folder mounted successfully."
else
    echo "Script execution failed. Exiting."
    exit 1
fi
