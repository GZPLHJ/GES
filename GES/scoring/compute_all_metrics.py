import argparse
from object_level_metrics import generate_object_metrics, extract_object_results
from xview2_metrics import XviewMetrics
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("gt_masks_dir",
        help="path where the gt masks are located (.png)",
        type=str)
parser.add_argument("pred_masks_dirc",
        help="path where the predicted masks are located (.png)",
        type=str)
parser.add_argument("gt_kwcoco_ds",
        help="the gt kwcoco dataset",
        type=str)
parser.add_argument("pred_kwcoco_ds",
        help="the predicted kwcoco dataset",
        type=str)

args = vars(parser.parse_args())
gt_masks_dir = args['gt_masks_dir']
pred_masks_dir = args['pred_masks_dir']
gt_kwcoco_ds = args['gt_kwcoco_ds']
pred_kwcoco_ds = args['pred_kwcoco_ds']

object_res = generate_object_metrics(gt_kwcoco_ds, pred_kwcoco_ds)
object_res_dict = extract_object_results(object_res)

xview2_metrics_dict = XviewMetrics.compute_score(pred_masks_dir, gt_masks_dir)

object_res_dict = {k+"_object":v for k,v in object_res_dict.items()}
xview2_metrics_dict = {k+"_pixel":v for k,v in xview2_metrics_dict.items()}

all_metrics = {**object_res_dict, **xview2_metrics_dict}

print("\n\nResults:")
print("--------------------")
print(pd.Series(all_metrics))

#print("Object Level Results")
#print("____________________")
#print(object_res_dict)
#print("Original xView2 Results")
#print("_______________________")
#print(xview2_metrics_dict)
