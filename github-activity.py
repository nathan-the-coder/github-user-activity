import requests
import sys
from collections import defaultdict

def fetch_user_events(username: str) -> requests.Response:
    """
    Fetches user events from the GitHub API.
    """
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)
    return response

def display_event_summary(commit_counts_by_repo, starred_repositories, repositories_with_issues, forked_repositories):
    """
    Displays the summary of user events.
    """
    print("Event Summary:")
    
    for repository, commit_count in commit_counts_by_repo.items():
        print(f"- Pushed {commit_count} commits in {repository}")
    
    for repository in forked_repositories:
        print(f"- Forked {repository}")

    for repository in starred_repositories:
        print(f"- Starred {repository}")

    for repository in repositories_with_issues:
        print(f"- Opened a new issue at {repository}")

def process_github_events(json_data):
    """
    Processes GitHub event data and categorizes events.
    """
    commit_counts_by_repo = defaultdict(int)
    starred_repositories = []
    repositories_with_issues = []
    forked_repositories = []

    for event in json_data:
        payload = event.get('payload', {})
        event_type = event.get('type')
        repository_name = event.get('repo', {}).get('name', "Unknown Repo")
        
        match event_type:
            case 'PushEvent':
                push_count = payload.get('size', 0)
                commit_counts_by_repo[repository_name] += push_count
            case 'WatchEvent':
                starred_repositories.append(repository_name)
            case 'IssuesEvent':
                repositories_with_issues.append(repository_name)
            case 'ForkEvent':
                forkee = payload.get('forkee', {})
                if forkee.get('fork'):
                    forked_repositories.append(forkee.get('full_name'))

    return commit_counts_by_repo, starred_repositories, repositories_with_issues, forked_repositories

def main():
    """
    Main function to process GitHub user events and categorize them.
    """
    if len(sys.argv) < 2:
        print("Error: No username provided!")
        exit(-1)

    username = sys.argv[1]
    response = fetch_user_events(username)

    if response.status_code != 200:
        print(f"Error: {response.status_code}: Failed to find username")
        return

    commit_counts_by_repo, starred_repositories, repositories_with_issues, forked_repositories = process_github_events(response.json())
    
    display_event_summary(commit_counts_by_repo, starred_repositories, repositories_with_issues, forked_repositories)

if __name__ == "__main__":
    main()

