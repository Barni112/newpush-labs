#!/usr/bin/env python3
import os
import secrets
import string
import sys


def generate_password(length=40):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <filename>", file=sys.stderr)
        sys.exit(1)
    filename = sys.argv[1]

    if os.path.exists(filename):
        with open(filename, "r") as f:
            password = f.read().strip()
    else:
        password = generate_password()
        with open(filename, "w") as f:
            f.write(password + "\n")
        os.chmod(filename, 0o440)
        os.chown(filename, 0, 0)
    return password


if __name__ == "__main__":
    print(main())
