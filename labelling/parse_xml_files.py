import argparse
import xml.etree.ElementTree as ET
import os
from glob import glob
import cv2
from clustering.utils import create_dirs
from tqdm import tqdm

def parse_xml(fname, save_dir):
  tree = ET.parse(fname)
  root = tree.getroot()
  file_path = root.findall('path')[0].text
  print(file_path)
  img = cv2.imread(file_path)
  print(img.shape)
  for child in root.findall('object'):
    name = child.find('name').text
    save_path = os.path.join(save_dir, name)
    x_min = child.find('bndbox').find('xmin').text
    x_max = child.find('bndbox').find('xmax').text
    y_min = child.find('bndbox').find('ymin').text
    y_max = child.find('bndbox').find('ymax').text
    save_fname = os.path.join(save_path, os.path.basename(file_path)+'_'.join((y_min, y_max, x_min, x_max)) + '.jpg')
    #print(img[int(x_min):int(x_max), int(y_min):int(y_max)].shape)
    cv2.imwrite(save_fname, img[int(y_min):int(y_max)+1, int(x_min):int(x_max)+1])

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--dir', help='directory containing xml files')
  parser.add_argument('-s', '--save_dir', help='save directory')
  args = parser.parse_args()
  tot_files = glob(os.path.join(args.dir, "*.xml"))
  create_dirs(os.path.join(os.path.join(args.save_dir), 'sugarcane_crop'))
  create_dirs(os.path.join(os.path.join(args.save_dir), 'others'))
  for fname in tqdm(tot_files):
    parse_xml(fname, args.save_dir)


if __name__ == '__main__':
  main()
