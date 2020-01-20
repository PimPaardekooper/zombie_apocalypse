import os

def is_verification():
    return bool(os.environ["verification_mode"])