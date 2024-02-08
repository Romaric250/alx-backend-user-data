#!/usr/bin/env python3
"""
Password Encryption and Validation Module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """

    hashes the password it takes as params using bcrypt
    """
    encode = password.encode()
    hashed = bcrypt.hashpw(encode, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    checks if hash is valide
    """

    valid_password = False
    encode = password.encode()
    if bcrypt.checkpw(encode, hashed_password):
        valid_password = True
    return valid_password
