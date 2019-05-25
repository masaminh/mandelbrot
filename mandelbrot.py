"""マンデルブロ集合を描画する."""
from argparse import ArgumentParser
from itertools import product
from os import makedirs, path

import numpy
from PIL import Image
from tqdm import tqdm


def main():
    """メイン関数."""
    parser = ArgumentParser()
    parser.add_argument('outdir')
    parser.add_argument('level', type=int)
    args = parser.parse_args()
    outpath = path.join(args.outdir, str(args.level))
    tile_num = 2 ** args.level
    tile_wid = 4.0 / tile_num

    lefttop = -2.0+2.0j
    delta = tile_wid / 256

    xylist = list(product(range(tile_num), range(tile_num)))
    for x, y in tqdm(xylist):
        img = get_image(lefttop + x * tile_wid - (y * tile_wid) * 1j, delta)
        outpath = path.join(args.outdir, str(args.level), str(x))
        makedirs(outpath, exist_ok=True)
        imgname = path.join(outpath, f'{y}.png')
        img.save(imgname)


def get_image(lefttop, delta):
    """マンデルブロ集合のpillowイメージを取得する

    Arguments:
        lefttop {complex} -- 左上
        delta {float} -- 1pxの差

    Returns:
        Image -- 作成したイメージ
    """
    imgarray = numpy.zeros((256, 256), dtype=numpy.uint8)

    for rstep, istep in product(range(256), range(256)):
        c = lefttop + rstep * delta - (istep * delta) * 1j
        z = 0
        for i in range(256):
            z = z ** 2 + c
            if abs(z) > 2:
                imgarray[istep][rstep] = 255 - i
                break

    img = Image.fromarray(imgarray)
    return img


if __name__ == "__main__":
    main()
