import json
import requests
import sys

def get_data(username: str):
    resp = requests.get(f"https://api.github.com/users/{username}/events")
    return resp.json()

def main():
    if len(sys.argv) < 1:
        print("No username provided!")
        exit(-1)
    
    data = get_data(sys.argv[1])
    starred = []
    forked = []
    push_count = 0
    pushed_repository = []

    for obj in data:
        payload = obj.get('payload')
        if isinstance(payload, dict):
            forkee = payload.get('forkee')
            if isinstance(forkee, dict):
                if forkee.get('fork'):
                    forked.append(forkee.get('html_url'))

    print("Output:")

    for repository in pushed_repository:
        print(repository['push_count'], 

if __name__ == "__main__":
    main()
