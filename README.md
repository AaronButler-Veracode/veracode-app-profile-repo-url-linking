# Veracode App Profile Repo Linking Script

Python script to populate links in Veracode App Profiles using already existing data from the Veracode Repository scanning integrations (GitHub, ADO, GitLab, BitBucket (TBC). 

## Setup

Clone this repository:

    git clone https://github.com/AaronButler-Veracode/veracode-app-profile-repo-url-linking

Install dependencies:

    cd veracode-app-profile-repo-url-linking
    pip install -r requirements.txt

(Optional) Save Veracode API credentials in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

## Run

If you have saved credentials as above you can run:

    python veracode_app_profile_url_link.py (arguments)

Otherwise you will need to set environment variables:

    export VERACODE_API_KEY_ID=<YOUR_API_KEY_ID>
    export VERACODE_API_KEY_SECRET=<YOUR_API_KEY_SECRET>
    python veracode_app_profile_url_link.py (arguments)

Arguments supported include:

* --organization_name, -o  (required): Name of the organization name in your source repository.
* --source_repo, -s  (required): The target source repo you wish to link to. Currently only supports cloud versions of: GitHub, ADO, GitLab, BitBucket.
* --force_update, -f (optional): Default false. Forces the script to update fields that are already populated.