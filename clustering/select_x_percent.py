import os
import argparse
import random
from shutil import copyfile
import math
from tqdm import tqdm
from utils import create_dirs

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-in', '--input_dir')
  parser.add_argument('-o', '--output_dir')
  parser.add_argument('-p', '--percent', type=int, help='percentage of files to move')
  args = parser.parse_args()
  create_dirs(args.output_dir)
  percent = args.percent/100
  tot_dirs = [os.path.join(args.input_dir, dirname) for dirname in os.listdir(args.input_dir)]
  for dirname in tqdm(tot_dirs):
    tot_files = os.listdir(dirname)
    n = math.ceil(len(tot_files) * percent)
    random.shuffle(tot_files)
    cp_files = tot_files[:n]
    save_dir = os.path.join(args.output_dir, os.path.basename(dirname))
    create_dirs(save_dir)
    for fname in cp_files:
      copyfile(os.path.join(dirname, fname), os.path.join(save_dir, fname))

if __name__=='__main__':
  main()
