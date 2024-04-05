from shapely.geometry import Polygon
from shapely import wkt
from shapely.geometry import box
import cv2
import numpy as np
import json
import kwimage
import rasterio
import copy
import os.path as osp


class BuildingPaster:

    def __init__(self,
                 original_pre_image_file,
                 original_post_image_file,
                 secondary_pre_image_file,
                 label_file,
                 allowed_damage_levels=[
                     'minor-damage', 'major-damage', 'destroyed'
                 ],
                 dilation_size=10):

        self.undamaged_image, self.undamaged_image_profile = \
            BuildingPaster.load_image_with_geoprofile(
                    original_pre_image_file)
        self.damaged_image, self.damaged_image_profile = \
            BuildingPaster.load_image_with_geoprofile(
                    original_post_image_file)
        self.secondary_image, self.secondary_image_profile = \
            BuildingPaster.load_image_with_geoprofile(
                    secondary_pre_image_file)

        assert np.all(self.undamaged_image.shape == self.damaged_image.shape
                      ), "Input images must be the same size"

        self.allowed_damage_levels = allowed_damage_levels
        self.dilation_size = dilation_size
        self.annotations = BuildingPaster.load_labels(label_file)
        self.process_annotations(self.annotations)

    @staticmethod
    def load_image_with_geoprofile(image_fn):
        with rasterio.open(osp.realpath(image_fn)) as src:
            image = src.read([1, 2, 3]).astype(np.uint8).transpose(1, 2, 0)
            geoprofile = src.profile
        return image, geoprofile

    @staticmethod
    def load_labels(label_fn):
        with open(label_fn, "r") as f:
            label_json = json.load(f)
        return label_json

    def process_annotations(self, annotations):
        # Should return a list of polygons defining buildings
        # we would like to paste into the "pre-event" image

        # should return which indicies in the annotations
        # have buildings we can paste
        features = annotations["features"]["xy"]
        self.pastable_building_indicies = []

        for bidx, b in enumerate(features):
            if b['properties']['subtype'] in self.allowed_damage_levels:
                self.pastable_building_indicies.append(bidx)

    def __len__(self):
        # length of object is how many buildings
        # it can paste into the undamaged image
        return len(self.pastable_building_indicies)

    def __getitem__(self, building_idx=0):
        # returns the undamaged image, with the building defined by
        # building_idx pasted in from the damaged building
        assert building_idx < len(self)

        #        poly = self.pastable_building_polys[building_idx]
        feature_idx = self.pastable_building_indicies[building_idx]
        poly = Polygon(
            wkt.loads(self.annotations['features']['xy'][feature_idx]["wkt"]))
        #        damage_level = self.annotations['features']['xy'][feature_idx][
        #            'properties']['subtype']

        # dilate polygon and ensure it fits correctly in the image
        image_area_polygon = box(0.0, 0.0, 1023.0, 1023.0)
        poly = poly.buffer(self.dilation_size,
                           single_sided=True,
                           cap_style=2,
                           join_style=2)
        poly = poly.intersection(image_area_polygon)

        mask = np.zeros_like(self.damaged_image).astype(np.uint8)[..., 0]
        cv2.fillPoly(mask, [
            np.array(list(poly.exterior.coords)).round().astype(
                np.int32).reshape(-1, 1, 2)
        ], [1])

        kwimage_poly = kwimage.Polygon.from_shapely(poly)
        bbox = kwimage_poly.bounding_box().data[0].round().astype(np.int32)
        center = kwimage_poly.bounding_box().to_cxywh().data[0, :2].astype(
            np.int32)
        damaged_image_section = self.damaged_image[bbox[1]:bbox[3],
                                                   bbox[0]:bbox[2]]

        mask = mask[bbox[1]:bbox[3], bbox[0]:bbox[2]] * 255

        modified_undamaged_image = self.undamaged_image
        modified_undamaged_image = cv2.seamlessClone(damaged_image_section,
                                                     modified_undamaged_image,
                                                     mask, center,
                                                     cv2.NORMAL_CLONE)

        pasted_annotation = copy.deepcopy(self.annotations)
        for bidx in range(len(self.annotations['features']['xy'])):
            if bidx == feature_idx:
                pasted_buid = pasted_annotation['features']['lng_lat'][bidx]['properties']['uid']
                continue
            pasted_annotation['features']['xy'][bidx]['properties'][
                'subtype'] = 'no-damage'
            pasted_annotation['features']['lng_lat'][bidx]['properties'][
                'subtype'] = 'no-damage'

        # new_pre_image, pasted_post_image,
        # pasted_labels, pasted_buid = bp[building_idx]
        return {"pre_image": self.secondary_image, 
                "pre_image_profile": self.secondary_image_profile,
                "post_image": modified_undamaged_image,
                "post_image_profile": self.undamaged_image_profile,
                "new_annotation": pasted_annotation, 
                "pasted_buid": pasted_buid}

