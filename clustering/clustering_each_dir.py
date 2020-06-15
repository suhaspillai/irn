from subprocess import call
import argparse
import os
from tqdm import tqdm

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-img_dir', '--image_dir', help='directory where images are stored')
  parser.add_argument('-o_dir', '--out_dir', help='output directory')
  parser.add_argument('-org_img_dir', '--orginal_img_dir', help='original image directory without resizing')
  parser.add_argument('-t_f', '--txt_file', help='text file that has epsilon value and min samples')
  args = parser.parse_args()
  dbscan_params = []
  with open (args.txt_file, 'r') as f:
    for line in f:
      dir_name, eps, min_samples = line.strip().split(',')
      dbscan_params.append((dir_name, eps, min_samples))

  for dir_name, eps, min_samples in tqdm(dbscan_params):
    try:
      call (["python3", "clustering.py", "-img_dir", os.path.join(args.image_dir, dir_name), "-o_dir", os.path.join(args.out_dir, dir_name), "-org_img_dir", args.orginal_img_dir, "-e", eps, "-ms", min_samples])
    except:
      print('Encountered Error {}'.format(dir_name))

if __name__ == '__main__':
  main()
