import os
import argparse
from tqdm import tqdm


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-root', '--root_dir', help='root directory')
  parser.add_argument('-o', '--output_dir', help='output directory')
  args = parser.parse_args()
  if not os.path.exists(args.output_dir):
    os.makedirs(args.output_dir)

  tot_dirs = [os.path.join(args.root_dir, dirname) for dirname in os.listdir(args.root_dir)]
  counter = 1
  for r_dir in tqdm(tot_dirs):
    for s_dir in os.listdir(r_dir):
      root_dirname = os.path.basename(r_dir)
      new_dirname =  '_'.join((str(counter), root_dirname, s_dir))
      os.rename(os.path.join(r_dir, s_dir), os.path.join(args.output_dir, new_dirname))
      counter += 1

if __name__ == '__main__':
  main()
