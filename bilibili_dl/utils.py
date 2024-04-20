import math

import progressbar
import requests
from tqdm import tqdm

URL_SPACE = 'https://api.bilibili.com/x/space/wbi/arc/search'
URL_VIDEO_INFO = 'https://api.bilibili.com/x/web-interface/view'
URL_PLAY = 'https://api.bilibili.com/x/player/playurl'


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


def send_request(url, params):
    '''
    发送get请求
    '''
    return requests.get(url, params, headers={'User-Agent': 'User-Agent'}).json()['data']


def get_all_bvids_by_mid(mid):
    '''
    获取该up主的所有投稿视频的BV号
    '''
    params = {'mid': mid, 'pn': '1', 'ps': '50'}
    try:
        res = send_request(URL_SPACE, params)
        total_pages = res['page']['count']
        bvids = [v['bvid'] for v in res['list']['vlist']]
        for page_num in range(2, math.ceil(total_pages / int(params['ps'])) + 1):
            params['pn'] = page_num
            res = send_request(URL_SPACE, params)
            bvids.extend(v['bvid'] for v in res['list']['vlist'])
        return bvids
    except Exception:
        raise Exception('获取BV号失败！')


def get_video_info_by_bvids(bvids):
    '''
    根据BV号获取视频详细信息(bvid, cid, title, up_name, pic)
    '''
    try:
        print('[bilibili-dl] 获取视频详细信息中...')
        if type(bvids) == str:
            bvids = [bvids]
        videos = []
        for bvid in tqdm(bvids, leave=False):
            res = send_request(URL_VIDEO_INFO, params={'bvid': bvid})
            # 检查该视频是否为分p视频
            if res['videos'] == 1:
                videos.append((res['bvid'], res['cid'], res['title'], res['owner']['name'], res['pic']))
            else:
                # 分p列表
                pages = res['pages']
                for p in pages:
                    videos.append((res['bvid'], p['cid'], p['part'], res['owner']['name'], p['first_frame']))
        return videos
    except Exception:
        raise Exception('获取视频详细信息失败！')
