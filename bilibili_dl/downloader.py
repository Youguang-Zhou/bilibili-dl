import os
import re
import subprocess
import urllib.request

import requests

from .utils import *


def download(play_url, videos, up_name):
    for bvid, cid, title, cover_url in videos:
        params = {'fnval': '16', 'bvid': bvid, 'cid': cid}
        r = requests.get(play_url, params).json()
        audio_url = r['data']['dash']['audio'][0]['base_url']
        # 如果标题里有书名号，则提取书名号里的内容作为新标题，否则保持原标题不变
        out_title = re.search(r'\《(.+)\》', title)
        out_title = out_title.group(1) if out_title else title
        # 处理特殊字符：/ 和 \
        out_title = re.sub(r'[/\\]', ' ', out_title)
        # 最终的文件名
        out = f'{out_title}.mp3'
        # 未处理的音频名
        out_audio_fname = f'{out_title}.raw.mp3'
        # 封面名
        out_cover_fname = f'{out_title}.{cover_url.split(".")[-1]}'
        if os.path.exists(out):
            print(f'[bilibili-dl] ⚠️  {out_title} 已经下载在路径：{os.path.abspath(out)}')
            continue
        else:
            print(f'[bilibili-dl] 当前下载内容：{title}')
            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/100.0.4896.75 Safari/537.36'),
                ('Referer',   f'https://api.bilibili.com/x/web-interface/view?bvid={bvid}'),
                ('Connection', 'keep-alive'),
            ]
            urllib.request.install_opener(opener)
            # 下载音频和封面
            urllib.request.urlretrieve(audio_url, out_audio_fname, show_progress)
            urllib.request.urlretrieve(cover_url, out_cover_fname)
            # 添加封面到音频上
            print(f'[ffmpeg] 正在合并封面中...')
            subprocess.call(f'ffmpeg -i "{out_audio_fname}" -i "{out_cover_fname}" \
                                     -loglevel error                               \
                                     -map 0:0 -map 1:0                             \
                                     -metadata album="{out_title}"                 \
                                     -metadata artist="{up_name}"                  \
                                     -metadata:s:v title="Album cover"             \
                                     -metadata:s:v comment="Cover (Front)"         \
                                     -id3v2_version 3 -write_id3v1 1 "{out}"', shell=True)
            os.remove(out_audio_fname)
            os.remove(out_cover_fname)
            print(f'[bilibili-dl] ✅ 下载完成: {os.path.abspath(out)}')
