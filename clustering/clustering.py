import tensorflow as tf
import numpy as np
import cv2
import argparse
import glob
from tensorflow import keras
import os
from tqdm import tqdm
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from shutil import copyfile

def load_images(tot_files, size=160):
  list_array=[]
  for fname in tqdm(tot_files):
    mat = cv2.imread(fname)
    if mat.shape[0] !=size or mat.shape[1] != size :
      mat = cv2.resize(mat, (size, size))
    list_array.append(mat.reshape(1, mat.shape[0], mat.shape[1], mat.shape[2]))
  mat = np.vstack(list_array)
  return mat

def normalize(mat):
  mat = ((mat/255) * 2) - 1
  return mat

def extract_features(model, mat, batch_size=32):
  features_extracted=[]
  for i in tqdm(range(0, len(mat), batch_size)):
    sub_mat=mat[i:i+batch_size]
    sub_mat = normalize(sub_mat)
    mat_features = model.predict(sub_mat)
    features_extracted.append(mat_features)
  mat = np.vstack(features_extracted)
  return mat

def get_clusters(mat, eps=0.2, min_samples=3):
  clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(mat)
  #clustering = KMeans(n_clusters=30, random_state=0).fit(mat)
  #print(clustering.labels_)
  return clustering.labels_

def move_img_based_on_clusters(labels, tot_files, out_dir, org_dir=None):
  for i in tqdm(range(len(labels))):
    if not os.path.exists(os.path.join(out_dir, str(labels[i]))):
      os.makedirs(os.path.join(out_dir, str(labels[i])))
    if org_dir is not None:
      dir_name = tot_files[i].split('/')[-2]
      fname =  os.path.basename(tot_files[i])
      copyfile(os.path.join(org_dir, dir_name, fname), os.path.join(os.path.join(out_dir, str(labels[i])), '_'.join((dir_name, fname))))
    #else:
      #copyfile(tot_files[i], os.path.join(os.path.join(out_dir, str(labels[i])), os.path.basename(tot_files[i])))

def load_model(IMG_SHAPE, model_type='mobile_net_v2'):
  if model_type:
    base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
                                                    include_top=False,
                                                   weights='imagenet')
  flatten_layer = keras.layers.Flatten()(base_model.outputs[0])
  model = keras.Model(inputs=base_model.inputs, outputs=flatten_layer)
  return model

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-img_dir', '--image_dir', help='directory where images rae stored')
  parser.add_argument('-o_dir', '--out_dir', help='output directory')
  parser.add_argument('-org_img_dir', '--orginal_img_dir', help='original image directory without resizing')
  parser.add_argument('-r_all', '--run_for_all_dirs', default=False, type=bool, help='run for all the directories')
  parser.add_argument('-e', '--eps', type=float, default =0, help='epsilon value')
  parser.add_argument('-ms', '--min_samples', type=int, default=3, help='min samples to use')

  tot_files = []
  args = parser.parse_args()
  if not os.path.exists(args.out_dir):
    os.makedirs(args.out_dir)
  if args.run_for_all_dirs:
    all_dirs = os.listdir(args.image_dir)
    for sub_dir in all_dirs:
      tot_files += glob.glob(os.path.join(args.image_dir , sub_dir, "*.jpg"))
  else:
    tot_files = glob.glob(os.path.join(args.image_dir , "*.jpg"))
  IMG_SHAPE = (160, 160, 3)
  # base_model = tf.keras.applications.MobileNetV2(input_shape=IMG_SHAPE,
  #                                                 include_top=False,
  #                                                weights='imagenet')
  # flatten_layer = keras.layers.Flatten()(base_model.outputs[0])
  # model = keras.Model(inputs=base_model.inputs, outputs=flatten_layer)
  model = load_model(IMG_SHAPE)
  mat = load_images(tot_files)
  #mat = normalize(mat)
  mat = extract_features(model, mat, batch_size=32)
  print(args.eps, args.min_samples)
  labels = get_clusters(mat, eps=args.eps, min_samples=args.min_samples)
  move_img_based_on_clusters(labels, tot_files, args.out_dir, org_dir=args.orginal_img_dir)
if __name__ == '__main__':
  main()

# get features
#run KNN
