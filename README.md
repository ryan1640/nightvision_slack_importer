# NightVision Slack Importer

## Description

`NightVision Slack Importer` is a tool used to automate the process of importing security vulnerability findings from a nightvision scan results file into user-friendly PDF reports and share these reports within the designated Slack channel.


## Installation

Before running the tool, ensure you have Python and Google Chrome installed on your system. Follow these installation steps:


1. **Clone the Repository:**
   ```
      git clone https://github.com/yourusername/nightvision_slack_importer.git
      cd nightvision_slack_importer
   ```
1. **Install Dependencies:**
   ```
      python3 -m venv .venv
      source .venv/bin/activate
      pip3 install -r requirements.txt
   ```

## Usage
   To use the NightVision Slack Importer, provide the path to your SARIF file along with your Slack API token and the Slack channel ID:
   
   ```
     source .venv/bin/activate
     python3 nightvision_slack_importer.py --sarif <path_to_sarif_file> --token <your_slack_token> --channel <slack_channel_id>
   ```

  ### Flags:

   | Flag            | Description                                                                        | 
   | --------------- |------------------------------------------------------------------------------------|
   | -s, --sarif     |  Path to the SARIF file containing the security analysis results.                  |                    
   | -t, --token    |  Your Slack API token, which must have permissions to post messages and upload files.   |                    
   | -c, --channel   |  The ID of the Slack channel where the report will be posted.                          |                    
