import argparse
import urllib.parse

from veracode_api_py import Applications


def main():

    parser = argparse.ArgumentParser(
        description="This script updates Veracode App profiles parameter \"GIT Repo URL\" when it is blank."
    )

    parser.add_argument(
        "-o",
        "--organization_name",
        help="Organization name to target linking. ",
        required=True,
    )

    parser.add_argument(
        "-s",
        "--source_repo",
        choices=["GitHub", "ADO", "GitLab", "BitBucket"],
        default=["GitHub"],
        help="Source repository for URL linkin (GitHub, ADO, GitLab or BitBucket)",
        required=True,
    )

    parser.add_argument(
        "-f",
        "--force_update",
        help="Force all matching profiles to update the URL, even if already populated",
        required=False,
        action="store_true",
    )

    orgName = ""

    args = parser.parse_args()
    orgName = args.organization_name
    sourceRepo = args.source_repo
    forceUpdate = args.force_update

    veracodeOrgName = get_veracode_org_name(sourceRepo, orgName)
    applicationsAPI = Applications()
    apps = applicationsAPI.get_by_name(orgName)

    if len(apps) == 0:
        print("No apps found matching provided org name")
    else:
        for each_app in apps:
            if each_app["profile"]["name"].startswith(veracodeOrgName):
                profile = each_app["profile"]
                appName = profile["name"]
                print("match: " + appName)
                repoURL = get_repo_URL(sourceRepo, appName)
                print(repoURL)
                git_repo_url = profile["git_repo_url"]
                if not git_repo_url or forceUpdate:
                    update_profile(applicationsAPI, each_app, profile, appName, repoURL)


def update_profile(applicationsAPI, each_app, profile, appName, repoURL):
    teamGUIDs = []
    for each_team in profile.get("teams", []):
        teamGUIDs.append(each_team["guid"])
    businessOwnerName = None
    businessOwnerEmail = None
    businessOwner = profile.get("business_owners", [])
    if len(businessOwner) > 0:
        businessOwnerName = businessOwner[0].get("name", "")
        businessOwnerEmail = businessOwner[0].get("email", "")
    applicationsAPI.update(
        each_app["guid"],
        appName,
        profile.get("business_criticality"),
        profile.get("description", None),
        profile.get("business_unit", None).get("guid"),
        teamGUIDs,
        profile.get("policies", [])[0]["guid"],
        profile.get("custom_fields", []),
        businessOwnerName,
        businessOwnerEmail,
        repoURL,
        profile.get("custom_kms_alias", None),
        profile.get("tags", None),
    )


def get_repo_URL(sourceRepo, appName):
    match sourceRepo:
        case "GitHub":
            return "https://github.com/" + appName + "/"
        case "ADO":
            tempName = appName.split("/")
            lastSplitIndex = len(tempName) - 1
            # ADO format is https://dev.azure.com/<org_name>/<project_name>/_git/<repository_name>
            tempPath = (
                tempName[1]
                + "/"
                + tempName[lastSplitIndex - 1]
                + "/_git/"
                + tempName[lastSplitIndex]
            )
            tempPath = urllib.parse.quote(tempPath)
            return "https://dev.azure.com/" + tempPath
        case "GitLab":
            # GitLab format is https://gitlab.com/<org_name>/<repository_name>
            tempPath = appName.split("GITLAB/")[1]
            tempPath = urllib.parse.quote(tempPath)
            return "https://gitlab.com/" + tempPath
        case "BitBucket":
            return


def get_veracode_org_name(sourceRepo, orgName):
    match sourceRepo:
        case "GitHub":
            return "" + orgName
        case "ADO":
            return "ADO/" + orgName
        case "GitLab":
            return "GITLAB/" + orgName
        case "BitBucket":
            return "BITBUCKET/" + orgName


if __name__ == "__main__":
    main()
