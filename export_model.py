# coding: utf-8

import argparse
import torch


def main():
    parse = argparse.ArgumentParser()
    parse.add_argument('-i', '--model-fp', type=str, default='yolov7.pt', help='model.pt path')
    parse.add_argument('--no-ema', action='store_false', help='whether to export the EMA model')
    parse.add_argument('-o', '--out-model-fp', type=str, required=True, help='exported model path')
    args = parse.parse_args()

    ckpt = torch.load(args.model_fp, map_location='cpu')  # load
    if args.no_ema:
        print(f'Exporting model without EMA to {args.out_model_fp} ...')
        torch.save(ckpt['model'].float().state_dict(), args.out_model_fp)
    else:
        print(f'Exporting EMA model to {args.out_model_fp} ...')
        torch.save(ckpt['ema'].state_dict(), args.out_model_fp)


if __name__ == '__main__':
    main()
