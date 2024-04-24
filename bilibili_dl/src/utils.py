import math
from typing import Dict, List

import progressbar
import requests
from tqdm import tqdm

from .constants import URL_USER_SPACE, URL_VIDEO_INFO
from .Video import Video


class ProgressBar:
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if self.pbar is None:
            self.pbar = progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


def send_request(url: str, params: Dict[str, str]):
    '''
    发送get请求
    '''
    return requests.get(url, params, headers={'User-Agent': 'User-Agent'}).json()['data']


def get_all_bvids_by_mid(mid: str):
    '''
    获取该up主的所有投稿视频的BV号
    '''
    params = {'mid': mid, 'pn': '1', 'ps': '50'}
    try:
        res = send_request(URL_USER_SPACE, params)
        total_pages = res['page']['count']
        bvids = [v['bvid'] for v in res['list']['vlist']]
        for page_num in range(2, math.ceil(total_pages / int(params['ps'])) + 1):
            params['pn'] = page_num
            res = send_request(URL_USER_SPACE, params)
            bvids.extend(v['bvid'] for v in res['list']['vlist'])
        return bvids
    except Exception:
        raise Exception('获取BV号失败！')


def get_videos_by_bvids(bvids: List[str]):
    '''
    根据BV号获取视频详细信息(bvid, cid, title, up_name, pic)
    '''
    try:
        print('[bilibili-dl] 获取视频详细信息中...')
        videos = []
        for bvid in tqdm(bvids, leave=False):
            res = send_request(URL_VIDEO_INFO, params={'bvid': bvid})
            # 检查该视频是否为分p视频
            if res['videos'] == 1:
                videos.append(
                    Video(
                        bvid=res['bvid'],
                        cid=res['cid'],
                        title=res['title'],
                        up_name=res['owner']['name'],
                        cover_url=res['pic'],
                    )
                )
            else:
                # 分p列表
                pages = res['pages']
                print(f'[bilibili-dl] 当前视频为分p视频，共{len(pages)}p')
                for p in pages:
                    videos.append(
                        Video(
                            bvid=res['bvid'],
                            cid=p['cid'],
                            title=p['part'],
                            up_name=res['owner']['name'],
                            cover_url=p['first_frame'],
                        )
                    )
        return videos
    except Exception:
        raise Exception('获取视频详细信息失败')
