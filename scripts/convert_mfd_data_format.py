# coding: utf-8
import argparse
import glob
import os
import os.path as osp


def float_to_str_list(a_list):
    return [f'{x:.6f}' for x in a_list]


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_dir", default="data/IBEM_dataset/images", help="input annotated directory")
    parser.add_argument("output_dir", default="data/IBEM_dataset/labels", help="output label directory")
    args = parser.parse_args()

    # if osp.exists(args.output_dir):
    #     print("Output directory already exists:", args.output_dir)
    #     sys.exit(1)
    # os.makedirs(args.output_dir)
    print("Creating dataset:", args.output_dir)

    dirs = glob.glob(osp.join(args.input_dir, "*"))
    for _dir in dirs:
        if not os.path.isdir(_dir):
            continue
        fps = glob.glob(osp.join(_dir, '*.txt'))
        new_label_dir = osp.join(args.output_dir, osp.basename(_dir))
        os.makedirs(new_label_dir, exist_ok=True)
        for fp in fps:
            img_fn = osp.basename(fp).replace('color_', '').replace('txt', 'jpg')
            new_label_fn = img_fn.replace('.jpg', '.txt')
            objects = []
            with open(fp, 'r') as f:
                for i, line in enumerate(f.readlines()):
                    if i < 4:
                        continue
                    line = line.replace(' ', '')
                    line = line.strip('\n').split('\t')
                    label = line[-1]
                    x1 = float(line[0]) / 100
                    y1 = float(line[1]) / 100
                    x2 = x1 + float(line[2]) / 100
                    y2 = y1 + float(line[3]) / 100
                    points = [x1, y1, x2, y1, x2, y2, x1, y2]
                    assert 0.0 <= min(points) <= max(points) <= 1.0
                    objects.append(' '.join([label] + float_to_str_list(points)))

            with open(osp.join(new_label_dir, new_label_fn), 'w') as f:
                for obj in objects:
                    f.write(obj + '\n')


def to_index_file():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("input_dir", help="input annotated directory")
    parser.add_argument("output_fp", help="output index file")
    args = parser.parse_args()

    dirs = glob.glob(osp.join(args.input_dir, "*"))
    res_fps = []
    for _dir in dirs:
        if not os.path.isdir(_dir):
            continue
        fps = glob.glob(osp.join(_dir, '*g'))
        res_fps.extend(fps)

    with open(args.output_fp, 'w') as f:
        for filename in res_fps:
            f.write(filename + '\n')


if __name__ == "__main__":
    # main()
    to_index_file()