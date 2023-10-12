from pathlib import Path

import requests
from github import Github
from retrying import retry

from rules_generator.github_token import GITHUB_TOKEN  # noqa

REPO_OWNER = "OpenPecha"
REPO_NAME = "word-segmentation-data"
RESOURCES_DIR = Path(__file__).resolve().parent.parent.parent / "resources"


class GitHubFileDownloader:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name

    def get_json_file_download_urls_from_repo(self):
        # Create a GitHub instance using your token
        g = Github(self.token)

        try:
            # Get the repository
            repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")

            # Get the list of contents in the "output" folder
            folder_contents = repo.get_contents("output")

            # Filter and extract JSON file download URLs
            json_file_urls = []
            for content_file in folder_contents:
                if content_file.name.endswith(".json"):
                    json_file_urls.append(content_file.download_url)

            return json_file_urls
        except Exception as error:
            print(f"An error occurred: {error}")
            return []


@retry(
    stop_max_attempt_number=3,  # Maximum number of retries
    wait_fixed=2000,  # Delay between retries in milliseconds (2 seconds)
    retry_on_exception=lambda x: isinstance(
        x, requests.exceptions.RequestException
    ),  # Retry on network errors
)
def download_file_with_url(
    download_url, new_downloaded_file_name, destination_folder=RESOURCES_DIR
):

    if download_url is None:
        print("Download URL is None")
        return
    # Send a GET request to download the file
    response = requests.get(download_url)

    new_downloaded_file_name = new_downloaded_file_name
    local_file_path = Path(destination_folder) / new_downloaded_file_name
    if response.status_code == 200:
        # Open the local file and save the downloaded content
        with open(local_file_path, "wb") as local_file:
            local_file.write(response.content)
        print(f"File downloaded and saved to {local_file_path}")
    else:
        print(
            f"Failed to download file {new_downloaded_file_name}. Status code: {response.status_code}"
        )


if __name__ == "__main__":
    pass
