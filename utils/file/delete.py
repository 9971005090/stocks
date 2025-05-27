import os

__all__ = ['DELETE_IF_EXISTS']

def DELETE_IF_EXISTS(file):
    if os.path.exists(file):
        os.remove(file)