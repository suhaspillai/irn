from subprocess import call
import argparse
import os
from tqdm import tqdm


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-img_dir', '--image_dir', help='directory where images are stored')
  parser.add_argument('-pt','--plt_dir', help='plot directory')
  args = parser.parse_args()
  tot_dirs = tot_dirs = os.listdir(args.image_dir)
  list_mn_neighbors = [3, 4, 5]
  for dir_name in tqdm(tot_dirs):
    input_dirname = os.path.join(args.image_dir, dir_name)
    for mn_neighbors in tqdm(list_mn_neighbors):
      call(["python3","dbscan_kd_plot.py", "-in", input_dirname, "-p" , os.path.join(args.plt_dir, os.path.basename(input_dirname)), "-mn", str(mn_neighbors)])

if __name__ == '__main__':
  main()
