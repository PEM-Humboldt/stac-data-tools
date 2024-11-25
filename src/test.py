# test.py
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description="STAC Collection Manager")
    parser.add_argument(
        "-u", "--username", required=True, help="Username for authentication"
    )
    parser.add_argument(
        "-p", "--password", required=True, help="Password for authentication"
    )

    args = parser.parse_args()
    print(f"Username: {args.username}")
    print(f"Password: {args.password}")


if __name__ == "__main__":
    main()
