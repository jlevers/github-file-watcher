from dotenv import load_dotenv
import glob
import os
import sendgrid
from sendgrid.helpers.mail import *
import sys

load_dotenv()

repo = os.environ.get('REPO')
repo_dir = f'watched-repo-{repo.split("/")[1]}'

with open('latest_diff') as latest_diff_file, open('paths_to_check') as watched_paths_file:
    diff_paths = latest_diff_file.read().split('\n')
    watched_paths = watched_paths_file.read().split('\n')

os.chdir(repo_dir)
changed_watched_files = set()
# Find files in the repository that were changed since the last commit and are matched by one of
# the tracked file globs provided by the user
for w in watched_paths:
    matching_glob = glob.glob(w)
    changed_watched_files |= (set(matching_glob) & set(diff_paths))

# If no matched files were changed, we're done
if len(changed_watched_files) == 0:
    exit()
os.chdir('..')

with open('latest_checked_commit') as f: latest_checked_commit = f.read().strip()

base_url = f'https://github.com/{repo}'
diff_url = f'{base_url}/compare/{latest_checked_commit}..{sys.argv[1]}'
changed_files = list(changed_watched_files)
changed_files_str = ''.join([f'<li>{f}</li>' for f in changed_files])

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
from_email = Email(os.environ.get('SEND_FROM'))
to_email = To(os.environ.get('SEND_TO'))
subject = f'Changes detected in {repo}'
content = HtmlContent(f'Check out the diff <a href=\"{diff_url}\">here</a>.<br><br>Watched files changed:<ul>{changed_files_str}</ul>')
mail = Mail(from_email=from_email, to_emails=to_email, subject=subject, html_content=content)
response = sg.client.mail.send.post(request_body=mail.get())