
import numpy as np
import os

import chainercv
from chainercv.datasets import VOCInstanceSegmentationDataset
from tqdm import tqdm

def run(args):
    dataset = VOCInstanceSegmentationDataset(split=args.chainer_eval_set, data_dir=args.voc12_root)
    
    #gt_masks = [dataset.get_example_by_keys(i, (1,))[0] for i in range(len(dataset))]
    #gt_labels = [dataset.get_example_by_keys(i, (2,))[0] for i in range(len(dataset))]
    gt_masks = []
    gt_labels = []
    pred_class = []
    pred_mask = []
    pred_score = []
    i = 0
    for id in tqdm(dataset.ids):
        try:
          ins_out = np.load(os.path.join(args.ins_seg_out_dir, id + '.npy'), allow_pickle=True).item()
          pred_class.append(ins_out['class'])
          pred_mask.append(ins_out['mask'])
          pred_score.append(ins_out['score'])
          gt_masks.append(dataset.get_example_by_keys(i, (1,))[0])
          gt_labels.append(dataset.get_example_by_keys(i, (2,))[0])
          i+=1
        except:
          print('File not found')

    print('0.5iou:', chainercv.evaluations.eval_instance_segmentation_voc(pred_mask, pred_class, pred_score,
                                                         gt_masks, gt_labels, iou_thresh=0.5))
