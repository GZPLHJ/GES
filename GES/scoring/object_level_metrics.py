import kwcoco
from kwcoco.coco_evaluator import CocoEvaluator
import argparse
#import ubelt as ub
import pandas as pd


def generate_object_metrics(gt_ds_path, pred_ds_path):

    true_dset = kwcoco.CocoDataset(gt_ds_path)
    pred_dset = kwcoco.CocoDataset(pred_ds_path)
    config = {
        'true_dataset': true_dset,
        'pred_dataset': pred_dset,
        'area_range': ['all'],
        'iou_thresh': [0.5],
        'use_image_names': True,
        'compat': 'all',
    }
    coco_eval = CocoEvaluator(config)
    results = coco_eval.evaluate()
    return results


def extract_object_results(coco_results):
    result_dict = {}

    measures = coco_results['area_range=all,iou_thresh=0.5'].nocls_measures
    #    nocls_df = pd.DataFrame(ub.dict_isect(
    #     measures, ['f1', 'g1', 'mcc', 'thresholds',
    #                'ppv', 'tpr', 'tnr', 'npv', 'fpr',
    #                'tp_count', 'fp_count',
    #                'tn_count', 'fn_count']))
    #
    #    print(nocls_df)
    result_dict['localization'] = float(
        measures['max_f1'].split("=")[1].split("@")[0])
    # pulls out the f1 scores for the classes
    for k in coco_results['area_range=all,iou_thresh=0.5'].ovr_measures.keys():
        #        print(k)
        result_dict[k] = float(
            coco_results['area_range=all,iou_thresh=0.5'].ovr_measures[k]
            ['max_f1'].split("=")[1].split("@")[0])


#        measures = coco_results['area_range=all,iou_thresh=0.5'].ovr_measures[k]
#        nocls_df = pd.DataFrame(ub.dict_isect(
#         measures, ['f1', 'g1', 'mcc', 'thresholds',
#                    'ppv', 'tpr', 'tnr', 'npv', 'fpr',
#                    'tp_count', 'fp_count',
#                    'tn_count', 'fn_count']))

#        print(nocls_df)
    return result_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("gt_ds", nargs='?',default=r"D:\GuoZhoupeng\object_detect\xfbd_code\kwcoco_file\instances_val2017_kwcoco_annotations_del_ex-smalllabel.json",help="Ground truth kwcoco dataset", type=str)
    parser.add_argument("pred_ds", nargs='?', default=r"D:\GuoZhoupeng\xfbd训练日志\训练日志3+score\yolov8x\重no del\val60cf\predrection_-image-id-kwcoco-score.json",help="Predicted kwcoco dataset", type=str)
    args = vars(parser.parse_args())
    results = generate_object_metrics(args['gt_ds'], args['pred_ds'])
    f1_results = extract_object_results(results)
    print(f1_results)
