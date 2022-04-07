import math
import os
import re
import subprocess
import urllib.request

import progressbar
import requests
from tqdm import tqdm

URL_SPACE      = 'https://api.bilibili.com/x/space/arc/search'
URL_VIDEO_INFO = 'https://api.bilibili.com/x/web-interface/view'
URL_PLAY       = 'https://api.bilibili.com/x/player/playurl'
FOLDER  = 'download'   # 下载文件夹名称
MID     = ''
UP_NAME = ''

os.makedirs(FOLDER, exist_ok=True)

# 获取该up主的所有投稿视频的BV号
def get_all_bvids_from_user_space(space_url, mid):
    params = {'mid': mid, 'pn': '1', 'ps': '50'}
    r = requests.get(space_url, params).json()
    total_pages = r['data']['page']['count']
    bvids = [v['bvid'] for v in r['data']['list']['vlist']]
    for page_num in range(2, math.ceil(total_pages/int(params['ps']))+1):
        params['pn'] = page_num
        r = requests.get(space_url, params).json()
        bvids.extend(v['bvid'] for v in r['data']['list']['vlist'])
    return bvids

bvids = get_all_bvids_from_user_space(URL_SPACE, MID)

# 根据BV号获取视频详细信息(bvid, cid, title, pic)
def get_video_info(video_info_url, bvids):
    if type(bvids) == str:
        bvids = [bvids]
    videos = []
    for bvid in tqdm(bvids):
        params = {'bvid': bvid}
        r = requests.get(video_info_url, params).json()
        data = r['data']
        videos.append((data['bvid'],data['cid'],data['title'],data['pic']))
    return videos

videos = get_video_info(URL_VIDEO_INFO, bvids)

# 下载时显示进度条
pbar = None
def show_progress(block_num, block_size, total_size):
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

# 开始下载！
for bvid, cid, title, cover_url in videos:
    print(title)
    r = requests.get(URL_PLAY, {'fnval': '16', 'bvid': bvid, 'cid': cid}).json()
    audio_url = r['data']['dash']['audio'][0]['base_url']
    # 如果标题里有书名号，则提取书名号里的内容作为新标题，否则保持原标题不变
    out_title = re.search(r'\《(.+)\》', title)
    out_title = out_title.group(1) if out_title else title
    # 最终的文件名
    out = f'{FOLDER}/{out_title}.mp3'
    # 未处理的音频名
    out_audio_fname = f'{FOLDER}/{out_title}.raw.mp3'
    # 封面名
    out_cover_fname = f'{FOLDER}/{out_title}.{cover_url[-3:]}'
    if os.path.exists(out):
        print(f'{out} already downloaded.')
        continue
    else:
        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/100.0.4896.75 Safari/537.36'),
            ('Referer',    f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        # 下载音频和封面
        urllib.request.urlretrieve(audio_url, out_audio_fname, show_progress)
        urllib.request.urlretrieve(cover_url, out_cover_fname)
        # 添加封面到音频上
        subprocess.call(f'ffmpeg -i "{out_audio_fname}" -i "{out_cover_fname}" \
                                 -map 0:0 -map 1:0                             \
                                 -metadata artist={UP_NAME}                       \
                                 -metadata:s:v title="Album cover"             \
                                 -metadata:s:v comment="Cover (Front)"         \
                                 -id3v2_version 3 -write_id3v1 1 "{out}"', shell=True)
        os.remove(out_audio_fname)
        os.remove(out_cover_fname)
        print(f'Downloaded: {out}')
