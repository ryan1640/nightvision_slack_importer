import json
import requests
import markdown
from bs4 import BeautifulSoup
import sys
import getopt
import re
import jinja2
from datetime import datetime
import os
from pyhtml2pdf import converter

# slack token and channel id.
slack_token = ''
channel_id = ''

# path of the SARIF file to parse.
sarif_file_path = ''

opts, args = getopt.getopt(sys.argv[1:], 't:c:s:', ['token=', 'channel=', 'sarif='])
for opt, arg in opts:
    if opt in ('-t', '--token'):
        slack_token = arg
    elif opt in ('-c', '--channel'):
        channel_id = arg
    elif opt in ('-s', '--sarif'):
        sarif_file_path = arg



def get_utc_now(val):

    return datetime.utcnow().date()

def create_pdf_from_html(html_report_file_path, output_file_path):
    """Convert HTML content to PDF."""

    report_print_options = {
        "printBackground": True,
        "displayHeaderFooter": False,
        "marginTop":0,
        "marginLeft":0,
        "marginRight":0
    }
    converter.convert(f'file:///{html_report_file_path}', output_file_path,timeout=10,print_options=report_print_options)



def md2html(issue_description):
    """convert issue description from markdown to HTML with URLs converted to HTML links."""
    # convert Markdown to HTML
    html_description = markdown.markdown(issue_description)
    
    # convert URLs into clickable links
    url_pattern = re.compile(
        r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    )
    html_description = url_pattern.sub(
        lambda x: f'<a href="{x.group(0)}">{x.group(0)}</a>', html_description
    )
    
    soup = BeautifulSoup(html_description, 'html.parser')
    formatted_description = soup.prettify()


    return formatted_description

def generate_html_report(issues,output_path):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    templateEnv.filters['get_utc_now'] = get_utc_now
    TEMPLATE_FILE = "nightvision_report_template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    html_report_content =  template.render(issues=issues)

    with open(output_path,"w") as f:
        f.write(html_report_content)

    return os.path.abspath(output_path)


def upload_file_to_slack(file_path, channel_id):
    """upload the file to a Slack channel."""
    headers = {'Authorization': f'Bearer {slack_token}'}
    files = {'file': open(file_path, 'rb')}
    data = {'channels': channel_id}
    response = requests.post('https://slack.com/api/files.upload', headers=headers, files=files, data=data)

    if response.status_code == 200:
        resp = response.json()
        if resp['ok'] == True:
            print("Report sent to slack successfully.")
        else:
            print(f"Failed to upload file: {response.text}")
    else:
        print(f"Failed to upload file: {response.text}")


        
def generate_and_send_report():
    """Generate a report from SARIF and send it to slack."""
    issues = []


    with open(sarif_file_path, 'r') as file:
        sarif_data = json.load(file)
    for run in sarif_data.get('runs', []):
        for result in run.get('results', []):
            title = result['message']['text']
            severity = result["properties"]["nightvision-risk"]
            rule_id = result['ruleId']
            id = re.match(re.compile(r"[a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+-[a-z0-9]+"),rule_id)[0]
            description = md2html(next((rule['fullDescription']['text'] for rule in run['tool']['driver']['rules'] if rule['id'] == rule_id), "No description available."))
            
            issue = {
                "id":id,
                "title": title,
                "severity":severity,
                "rule_id":rule_id,
                "description":description
            }

            issues.append(issue)
    
          
    html_report_path = generate_html_report(issues,'nightvision-report.html')
    create_pdf_from_html(html_report_path, 'nightvision-report.pdf')
    upload_file_to_slack('nightvision-report.pdf', channel_id)

if __name__ == "__main__":
    generate_and_send_report()
