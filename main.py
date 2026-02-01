import argparse, yaml, requests, downloader, subprocess
prev = ""
parser = argparse.ArgumentParser(
    prog="oscollector",
    description="the new package manager"
)
subparsers = parser.add_subparsers(dest="command")
install_parser = subparsers.add_parser("install")
install_parser.add_argument("package")

g = parser.parse_args()

if g.command == "install":
    req = requests.get(f"https://cdn.jsdelivr.net/gh/oscolle/ctor/packages/{g.package}/details.yml")
    if req.status_code == 404:
        parser.error(f'Package "{g.package}" not found')
    else:
        data = yaml.safe_load(req.text)
        print(f"Found {data["details"]["name"]} by {data["details"]["author"]}")
        steps = data["install"]["steps"]
        for i in steps:
            action = list(i.keys())[0]
            if action == "download":
                url = i[action]["url"].replace("%pname%", prev)
                print(f"Downloading the file at {url}...")
                prev = downloader.download(url)
            elif action == "execute":
                action = list(i.keys())[0]
                command = i[action]["command"].replace("%pname%", prev)
                subprocess.run("")