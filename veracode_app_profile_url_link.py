from veracode_api_py import Applications


def main():
    applicationsAPI = Applications()
    apps = applicationsAPI.get_all()

    orgName = "Veracode-AB"

    for each_app in apps:
        if each_app["profile"]["name"].startswith(orgName):
            profile = each_app["profile"]
            appname = profile["name"]
            print("match: " + appname)
            repoURL = "https://github.com/" + appname + "/"
            print(repoURL)
            git_repo_url = profile["git_repo_url"]
            if not git_repo_url:
                git_repo_url = repoURL
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
                    appname,
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

if __name__ == "__main__":
    main()
