import os

def create_dirs(path):
  if not os.path.exists(path):
    os.makedirs(path)
