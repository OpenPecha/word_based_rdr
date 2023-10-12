from github import Github

from rules_generator.github_token import GITHUB_TOKEN

REPO_OWNER = "OpenPecha"
REPO_NAME = "word-segmentation-data"


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


if __name__ == "__main__":
    file_downloader = GitHubFileDownloader(GITHUB_TOKEN, REPO_OWNER, REPO_NAME)
    json_urls = file_downloader.get_json_file_download_urls_from_repo()
    for url in json_urls:
        print(url)
