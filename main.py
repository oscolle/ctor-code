import argparse
parser = argparse.ArgumentParser(
    prog="oscollector",
    description="the new package manager"
)
subparsers = parser.add_subparsers(dest="command")
install_parser = subparsers.add_parser("install")
install_parser.add_argument("package")

g = parser.parse_args()

if g.command == "install":
    print("Totally installing " + g.package + "!")