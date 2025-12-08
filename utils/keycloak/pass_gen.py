#!/usr/bin/env python3
import secrets
import string


def generate(length=32):
    alphabet = string.ascii_letters + string.digits
    alphabet = alphabet.replace("\"", "").replace("'", "").replace("\\", "")
    return "".join(secrets.choice(alphabet) for _ in range(length))


print(generate())
