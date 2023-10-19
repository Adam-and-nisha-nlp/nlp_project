import requests
import json
from env import github_token, github_username

def get_repository_details(repo_full_name):
    repo_url = f"https://api.github.com/repos/{repo_full_name}"
    readme_url = f"https://api.github.com/repos/{repo_full_name}/readme"
    repo_response = requests.get(repo_url, headers=headers)
    readme_response = requests.get(readme_url, headers=headers)
    if repo_response.status_code == 200 and readme_response.status_code == 200:
        repo_data = repo_response.json()
        readme_data = readme_response.json()
        language = repo_data["language"]
        readme_contents = requests.get(readme_data["download_url"]).text
        return {
            "repo": "/" + repo_full_name,
            "language": language,
            "readme_contents": readme_contents
        }
    else:
        return None

def get_repositories(query, sort="stars", order="desc", page=1, max_pages=10):
    base_url = "https://api.github.com/search/repositories"
    all_repos = []

    while page <= max_pages:
        params = {
            "q": query,
            "sort": sort,
            "order": order,
            "per_page": 10,  # You can get up to 100 results per page.
            "page": page  # Specify the page number
        }
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to fetch page {page} of repositories.")
            break

        response_json = response.json()
        all_repos.extend(response_json["items"])
        
        page += 1

        if "Link" in response.headers:
            next_link = response.headers["Link"]
            if 'rel="next"' not in next_link:
                break

    return all_repos

def scrape_breast_cancer_repositories():
    # Search for breast cancer related repositories and handle pagination
    query = "breast cancer"
    page = 1
    max_pages = 10

    breast_cancer_repos = get_repositories(query, page=page, max_pages=max_pages)

    with open("breast_cancer_repositories.json", "w") as json_file:
        json.dump(breast_cancer_repos, json_file, indent=4)

    return breast_cancer_repos

# Example usage:
if __name__ == "__main__":
    scraped_repositories = scrape_breast_cancer_repositories()
    print(f"Scraped {len(scraped_repositories)} breast cancer repositories.")
