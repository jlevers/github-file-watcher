#!/bin/bash
set -eou pipefail

# Load .env
# export "$(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)"
source .env

last_checked_commit_file="latest_checked_commit"
latest_diff_file="latest_diff"

# Make sure all the necessary files are present
if [[ ! -f $last_checked_commit_file ]]; then
    touch $last_checked_commit_file
fi
if [[ ! -f $latest_diff_file ]]; then
    touch $latest_diff_file
fi

# Get repository name
IFS='/'; read -ra repo_parts <<< "$REPO"
repo_dir="watched-repo-${repo_parts[1]}"

if [[ ! -d "./$repo_dir" ]]; then
    git clone git@github.com:"$REPO" "$repo_dir"
    cd "$repo_dir"
    git rev-parse --short HEAD > "../$last_checked_commit_file"
    exit 1
else
    cd "$repo_dir"
    git pull
fi

last_checked_commit=$(cat "../$last_checked_commit_file")
current_commit=$(git rev-parse --short HEAD)

if [ "$last_checked_commit" = "$current_commit" ]; then
    exit
fi

git diff --name-only "$last_checked_commit..$current_commit" > "../$latest_diff_file"
cd ..

# Send email
poetry run python emailer.py $current_commit

echo "$current_commit" > $last_checked_commit_file
