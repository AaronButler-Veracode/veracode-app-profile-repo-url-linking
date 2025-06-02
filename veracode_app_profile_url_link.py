import argparse
import logging
import urllib.parse

from veracode_api_py import Applications


def list_of_strings(choices):
    """Return a function that splits and checks comma-separated values."""

    def splitarg(arg):
        values = arg.split(",")
        for value in values:
            if value not in choices:
                raise argparse.ArgumentTypeError(
                    "invalid choice: {!r} (choose from {})".format(
                        value, ", ".join(map(repr, choices))
                    )
                )
        return values

    return splitarg

def main():
    
    parser = argparse.ArgumentParser(
        description="This script lists modules in which static findings were identified."
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
        choices=['GitHub', 'ADO', 'GitLab', 'BitBucket'],
        default=['GitHub'],
        help="Source repository for URL linkin (GitHub, ADO, GitLab or BitBucket)",
        required=True,
    )

    orgName = ""

    args = parser.parse_args()
    orgName = args.organization_name
    sourceRepo = args.source_repo

    veracodeOrgName = get_veracode_org_name(sourceRepo, orgName)
    applicationsAPI = Applications()
    apps = applicationsAPI.get_by_name(orgName)

    if len(apps) == 0 :
       print("No apps found matching provided org")
    else:
      for each_app in apps:
          if each_app["profile"]["name"].startswith(veracodeOrgName):
              profile = each_app["profile"]
              appName = profile["name"]
              print("match: " + appName)
              repoURL = get_repo_URL(sourceRepo, appName)
              print(repoURL)
              git_repo_url = profile["git_repo_url"]
              if not git_repo_url:
                  git_repo_url =  repoURL
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
                      git_repo_url,
                      profile.get("custom_kms_alias", None),
                      profile.get("tags", None),
                  )

def get_repo_URL(sourceRepo, appName):
    match sourceRepo:
        case "GitHub":
          return "https://github.com/" + appName + "/"
        case "ADO":
          tempName = appName.split('/')
          lastSplitIndex = len(tempName) - 1
          # ADO format is https:<base_url>/<org_name>/<project_name>/_git/<repository_name>
          tempPath = tempName[1] + "/" + tempName[lastSplitIndex - 1] + "/_git/" + tempName[lastSplitIndex]
          tempPath = urllib.parse.quote(tempPath)
          return "https://dev.azure.com/" + tempPath
       
def get_veracode_org_name(sourceRepo, orgName):
    match sourceRepo:
        case "GitHub":
          return "" + orgName
        case "ADO":
          return "ADO/" + orgName

if __name__ == "__main__":
    main()
