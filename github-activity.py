import requests
import sys
from collections import defaultdict

def get_data(username: str):
    """
    Fetches user events from GitHub API.
    """
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)
    return response

def main():
    """
    Main function to process GitHub user events and categorize them.
    """
    if len(sys.argv) < 2:  # Ensure username is provided as a command-line argument
        print("No username provided!")
        exit(-1)

    username = sys.argv[1]
    response = get_data(username)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}: Failed to find username")
        return

    # Initialize data containers
    forked = []  # List of repositories the user forked
    starred = []  # List of repositories the user starred
    issued = []   # List of repositories where the user opened an issue
    pushed_repository = defaultdict(int)  # Dictionary to store total commits per repository

    # Process each event from the API response
    for event in response.json():
        payload = event.get('payload', {})  # Ensure payload exists
        event_type = event.get('type')
        repository = event.get('repo', {}).get('name', "Unknown Repo")  # Get repo name

        match event_type:
            case 'PushEvent':
                push_count = payload.get('size', 0)  # Default to 0 if missing
                pushed_repository[repository] += push_count  # Aggregate commits
            case 'WatchEvent':
                starred.append(repository)
            case 'IssuesEvent':
                issued.append(repository)
            case 'ForkEvent':
                forkee = payload.get('forkee', {})
                if forkee.get('fork'):
                    forked.append(forkee.get('full_name'))

    # Print output
    print("Output:")
    
    for repository, commit_count in pushed_repository.items():
        print(f"- Pushed {commit_count} commits in {repository}")

    for repository in forked:
        print(f"- Forked {repository}")

    for repository in starred:
        print(f"- Starred {repository}")

    for repository in issued:
        print(f"- Opened a new issue at {repository}")

if __name__ == "__main__":
    main()

