# coding: utf-8
import argparse
import glob
import json
import os
import os.path as osp
import sys

import numpy as np


def float_to_str_list(a_list):
    return [f'{x:.6f}' for x in a_list]


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_dir", help="input annotated directory")
    parser.add_argument("output_dir", help="output dataset directory")
    parser.add_argument("--labels", help="labels file", required=True)
    args = parser.parse_args()

    if osp.exists(args.output_dir):
        print("Output directory already exists:", args.output_dir)
        sys.exit(1)
    os.makedirs(args.output_dir)
    print("Creating dataset:", args.output_dir)

    class_name_to_id = {}
    for i, line in enumerate(open(args.labels).readlines()):
        class_id = i - 1  # starts with -1
        class_name = line.strip()
        if class_id == -1:
            assert class_name == "__ignore__"
            continue
        class_name_to_id[class_name] = class_id

    label_files = glob.glob(osp.join(args.input_dir, "*.json"))
    for image_id, filename in enumerate(label_files):
        label_file = json.load(open(filename))
        height, width = label_file['imageHeight'], label_file['imageWidth']

        objects = []
        for shape in label_file['shapes']:
            points = shape["points"]
            label = shape["label"]
            label_id = class_name_to_id[label]

            shape_type = shape.get("shape_type", "polygon")

            if shape_type == "rectangle":
                (x1, y1), (x2, y2) = points
                x1, x2 = sorted([x1, x2])
                y1, y2 = sorted([y1, y2])
                points = [x1, y1, x2, y1, x2, y2, x1, y2]
            else:
                points = np.asarray(points).flatten().tolist()

            for i in range(len(points)):
                if 2 * i >= len(points):
                    break
                points[2 * i] /= width
                points[2 * i + 1] /= height
            assert 0.0 <= max(points) <= 1.0
            assert 0.0 <= min(points) <= 1.0

            objects.append(' '.join([str(label_id)] + float_to_str_list(points)))

        base_name = osp.basename(filename).rsplit('.', maxsplit=1)[0]
        with open(osp.join(args.output_dir, base_name + '.txt'), 'w') as f:
            for obj in objects:
                f.write(obj + '\n')


def to_index_file():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_dir", help="input annotated directory")
    parser.add_argument("output_fp", help="output index file")
    args = parser.parse_args()

    label_files = glob.glob(osp.join(args.input_dir, "*g"))
    with open(args.output_fp, 'w') as f:
        for image_id, filename in enumerate(label_files):
            f.write(filename + '\n')


if __name__ == "__main__":
    # main()
    to_index_file()
