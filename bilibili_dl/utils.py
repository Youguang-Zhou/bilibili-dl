import math

import progressbar
import requests
from tqdm import tqdm

pbar = None


def show_progress(block_num, block_size, total_size):
    '''
    下载时显示进度条
    '''
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


def get_all_bvids_by_mid(space_url, mid):
    '''
    获取该up主的所有投稿视频的BV号
    '''
    try:
        params = {'mid': mid, 'pn': '1', 'ps': '50'}
        r = requests.get(space_url, params).json()
        total_pages = r['data']['page']['count']
        bvids = [v['bvid'] for v in r['data']['list']['vlist']]
        for page_num in range(2, math.ceil(total_pages/int(params['ps']))+1):
            params['pn'] = page_num
            r = requests.get(space_url, params).json()
            bvids.extend(v['bvid'] for v in r['data']['list']['vlist'])
        return bvids
    except Exception:
        raise Exception('获取BV号失败！')


def get_video_info_by_bvids(video_info_url, bvids):
    '''
    根据BV号获取视频详细信息(bvid, cid, title, pic)
    '''
    try:
        print('[bilibili-dl] 获取视频详细信息中...')
        if type(bvids) == str:
            bvids = [bvids]
        videos = []
        up_name = ''
        for bvid in tqdm(bvids):
            params = {'bvid': bvid}
            r = requests.get(video_info_url, params).json()
            data = r['data']
            videos.append((data['bvid'],
                           data['cid'],
                           data['title'],
                           data['pic']))
            up_name = data['owner']['name']
        return videos, up_name
    except Exception:
        raise Exception('获取视频详细信息失败！')
