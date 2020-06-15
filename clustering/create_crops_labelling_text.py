import os
import argparse
import random
parser = argparse.ArgumentParser()
parser.add_argument('-t_f', '--txt_file')
parser.add_argument('-d', '--directory')
args = parser.parse_args()
l = os.listdir(args.directory)
random.shuffle(l)
with open (args.txt_file, 'w') as f:
  for i, dirname in enumerate(l):
    f.write('.'.join((str(i), dirname)) + '\n')
