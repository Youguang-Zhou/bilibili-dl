import argparse

from .src.downloader import download
from .src.utils import get_all_bvids_by_mid, get_videos_by_bvids
from .version import __version__


def get_args():
    parser = argparse.ArgumentParser('Bilibili Downloader')
    parser.add_argument('-v', '--version', action='version', version=__version__, help='查看版本号')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('bv', nargs='?', help='BV号')
    group.add_argument('--mid', nargs='?', help='space.bilibili.com/{mid}')

    parser.add_argument(
        '-a',
        '--audio-only',
        action='store_true',
        default=False,
        help='仅下载音频 (默认: False)',
    )

    return parser.parse_args()


def main(args):
    bv: str = args.bv
    mid: str = args.mid
    is_audio_only: bool = args.audio_only

    # 获取要下载视频的BV号
    bv_list = []
    if bv:
        # 如果命令行参数里有BV号，则通过该BV号下载单个视频
        if bv.startswith('BV') and len(bv) == 12:
            bv_list.append(bv)
        else:
            raise Exception('BV号输入错误')
    elif mid:
        # 否则根据mid下载该up主的所有投稿视频
        bv_list = get_all_bvids_by_mid(mid)
        if len(bv_list) == 0:
            raise Exception('mid输入错误')
    else:
        raise Exception('使用-h查看帮助')

    # 通过BV号获取视频信息
    videos = get_videos_by_bvids(bv_list)

    # 开始下载！
    download(videos, is_audio_only)


if __name__ == '__main__':
    main(args=get_args())
