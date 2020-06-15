from sklearn.cluster import DBSCAN
import argparse
from clustering import load_images, extract_features, load_model
from sklearn.neighbors import NearestNeighbors
import glob, os
import matplotlib.pyplot as plt
import numpy as np


def get_nearest_neighbor_dist(featutes, n_neighbors=2):
  neigh = NearestNeighbors(n_neighbors=n_neighbors)
  neigh.fit(featutes)
  dist, index = neigh.kneighbors(featutes)

  return dist, index

def sort_distance(mat):
  dist_mat = np.sort(mat[:, -1])
  return dist_mat

def kd_plot(mat, fname):
  fig, ax = plt.subplots()
  ax.plot(np.arange(len(mat)), mat)
  #plt.show()
  plt.savefig(fname)

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-in', '--image_dir', help='input directory')
  parser.add_argument('-p', '--plot_dir', help='plot directory')
  parser.add_argument('-mn', '--min_neighbors', type=int,help='min samples to use')
  args = parser.parse_args()
  n_neighbors = args.min_neighbors
  if not os.path.exists(args.plot_dir):
    os.makedirs(args.plot_dir)
  IMG_SHAPE = (160, 160, 3)
  tot_files = glob.glob(os.path.join(args.image_dir , "*.jpg"))
  model = load_model(IMG_SHAPE)
  mat = load_images(tot_files)
  features = extract_features(model, mat, batch_size=32)
  #import pdb;pdb.set_trace()
  dist, index = get_nearest_neighbor_dist(features, n_neighbors=n_neighbors)
  dist_mat = sort_distance(dist)
  kd_plot(dist_mat, os.path.join(args.plot_dir, 'plot_' + str(n_neighbors)+".png"))

if __name__ == '__main__':
  main()
