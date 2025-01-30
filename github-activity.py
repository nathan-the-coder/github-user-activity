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
    forked = []
    push_sizes = []
    pushed_repository = []

    for obj in data:
        payload = obj.get('payload')
        print(obj.get('type'))
        match obj.get('type'):
            case 'PushEvent':
                push_count = payload.get('size')
                repository = obj.get('repo')['name']
                pushed_repository.append({"size":push_count, "name":repository, "created_at": obj.get("created_at")})
            case 'CreateEvent':
                pass
            case 'ForkEvent':
                if isinstance(payload, dict):
                    forkee = payload.get('forkee')
                    if isinstance(forkee, dict):
                        if forkee.get('fork'):
                            forked.append(forkee.get('full_name'))

    print("Output:")

    for repository in pushed_repository:
        print(f"- Pushed {repository.get('size')} commits in {repository.get('name')} at {repository.get('created_at')}") 

    for repository in forked:
        print(f"- Forked {repository}")

if __name__ == "__main__":
    main()
