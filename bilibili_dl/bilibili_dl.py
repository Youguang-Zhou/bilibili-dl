import argparse

from download import download
from utils import *

URL_SPACE = 'https://api.bilibili.com/x/space/arc/search'
URL_VIDEO_INFO = 'https://api.bilibili.com/x/web-interface/view'
URL_PLAY = 'https://api.bilibili.com/x/player/playurl'


def get_args():
    parser = argparse.ArgumentParser('Bilibili Downloader')

    parser.add_argument('bvid', nargs='?', help='BV号')
    parser.add_argument('--mid', help='up主id')
    parser.add_argument('--save-dir', default='downloads', help='保存目录')

    args = parser.parse_args()
    return args


def main(args):
    bvid = args.bvid
    mid = args.mid
    save_dir = args.save_dir
    # 获取要下载视频的BV号
    bvids = []
    if bvid:
        # 如果命令行参数里有BV号，则通过该BV号下载单个视频
        if len(bvid) != 12:
            raise Exception('BV号输入有误')
        else:
            bvids.append(bvid)
    elif mid:
        # 否则根据mid下载该up主的所有投稿视频
        bvids = get_all_bvids_by_mid(URL_SPACE, mid)
        if len(bvids) == 0:
            raise Exception('mid输入有误')
    else:
        raise Exception('使用-h查看帮助')
    # 通过BV号获取视频信息
    # videos如：[(bvid, cid, title, pic), ...]
    videos, up_name = get_video_info_by_bvids(URL_VIDEO_INFO, bvids)
    # 开始下载！
    download(URL_PLAY, videos, up_name, save_dir)


if __name__ == '__main__':
    args = get_args()
    main(args)
