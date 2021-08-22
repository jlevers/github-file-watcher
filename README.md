GitHub File Watcher
===================

Tracks updates to GitHub repositories, and sends you an email when a file you're watching gets updated.

## Requirements
* Python 3.x
* Poetry
* A Sendgrid account

## Setup
* Clone the repository: `git clone git@github.com:jlevers/github-file-watcher`
* Install Python packages with `poetry install`
* Copy `.env.example` to `.env` and populate the environment variables. The `REPO` variable should be formatted like `jlevers/github-file-watcher`, not like a full URL.
* Copy `paths_to_watch.example` to `paths_to_watch` and fill in the paths that you'd like to track for the repository you're watching. Globs are supported.

## Usage

Either run `checker.sh` by hand, or run it with a cron job so that you'll automatically get emails when the repository you're tracking gets updated. My cron entry (to run the checker once a day) looks like this:

```
0 0 * * * /path/to/checker.sh
```