from argparse import ArgumentParser, BooleanOptionalAction
import sys

from src.downloader import download
from src.utils import *


def get_args():
    parser = ArgumentParser('Bilibili Downloader')

    parser.add_argument('bvid', nargs='?', help='BV号')
    parser.add_argument('--mid', help='up主id')
    parser.add_argument('--audio-only', '-a',
                        action=BooleanOptionalAction, default=False, help='仅下载音频')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    else:
        return parser.parse_args()


def main(args):
    bvid = args.bvid
    mid = args.mid
    is_audio_only = args.audio_only

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
        bvids = get_all_bvids_by_mid(mid)
        if len(bvids) == 0:
            raise Exception('mid输入有误')
    else:
        raise Exception('使用-h查看帮助')

    # 通过BV号获取视频信息，videos如：[(bvid, cid, title, up_name, pic), ...]
    videos = get_video_info_by_bvids(bvids)

    # 开始下载！
    download(videos, is_audio_only)


if __name__ == '__main__':
    args = get_args()
    main(args)
