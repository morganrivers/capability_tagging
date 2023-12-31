#!/bin/bash

# Title: Setup Git Repository with SSH keys
# Author: Morgan Rivers
# Date: June 2023
# Description: This script automates the process of setting up a Git repository with SSH keys. 
# It prompts the user for their GitHub username/organization, Git email, SSH key name, and 
# repository name. Then it generates a new SSH key, adds it to the SSH agent, and provides the
# public key to be added to GitHub as a deploy key. Afterward, it clones the repository, adds 
# any changes, commits them with a user-provided message, and finally, connects the local repository 
# to the remote one and pushes the commits. 
#
# Usage: Run this script in a Unix-like environment that has git and ssh installed. 

set -e  # Exit immediately if a pipeline returns a non-zero status

# User inputs
echo "Enter your GitHub username or organization:"
read git_username_or_org
echo "Enter your Git email:"
read git_email
echo "Enter a name for your SSH key file:"
read key_name
echo "Enter your repository name:"
read repo_name

# newline for readability
echo ""

# Check if ~/.ssh directory exists
if [[ ! -d ~/.ssh ]]; then
    # If not, create it
    mkdir ~/.ssh
    echo "Directory ~/.ssh created."
fi

# Go to .ssh directory
cd ~/.ssh


# Generate a new SSH keys
ssh-keygen -t ed25519 -C "$git_email" -f $key_name -q -N ""

# Start the SSH agent and add the key
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/$key_name

# newline for readability
echo ""

# Print the public key
echo "Your SSH public key is: (Copy the line below!)"
cat ~/.ssh/$key_name.pub

# newline for readability
echo ""

echo "Please add the SSH key to your GitHub under 'deploy keys' at this link:"
echo "https://github.com/$git_username_or_org/$repo_name/settings/keys"

echo "Don't forget to check 'Allow write access'!"
echo ""
echo "Once you have added the key, press any key to continue..."

# Wait for user to press a key
read -n 1 -s

# Change directory back to where the repo goes
cd -

# Ask user if they want to clone the repository
echo "Do you want to clone the repository? (This is not necessary if the directory already exists and you're setting a new SSH key.) [y/n]"
read response
response=$(get_response $response)
if [[ $response == "y" ]]; then
    git clone git@github.com:$git_username_or_org/$repo_name.git
    cd $repo_name
fi


# Ask user if they want to add a readme
echo "Do you want to add a README.md? [y/n]"
read response
response=$(get_response $response)
if [[ $response == "y" ]]; then
    # Check if README.md exists
    if [[ ! -e README.md ]]; then
        # If not, create it and write $repo_name to it as the title
        echo "# $repo_name" > README.md
    fi
    git add .
fi

# Ask user if they want to commit and push
echo "Do you want to commit and push changes? [y/n]"
read response
response=$(get_response $response)
if [[ $response == "y" ]]; then
    echo "Enter commit message:"
    read commit_msg
    git commit -m "$commit_msg"

    # newline for readability
    echo ""

    # Connect local repository to the remote one and push commits
    git remote add origin git@github.com:$git_username_or_org/$repo_name.git
    git push -u origin main
fi
