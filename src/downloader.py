import os
import re
import subprocess
import urllib.request

from src.utils import *


def download(videos, is_audio_only):
    for bvid, cid, title, up_name, cover_url in videos:
        params = {'bvid': bvid, 'cid': cid}
        if is_audio_only:
            params['fnval'] = '16'  # dash格式
        else:
            params['fnval'] = '1'   # mp4格式
            params['qn'] = '64'     # 720P画质

        # 发送请求
        res = send_request(URL_PLAY, params)

        if is_audio_only:
            download_url = res['dash']['audio'][0]['base_url']
            # 如果标题里有书名号，则提取书名号里的内容作为新标题，否则保持原标题不变
            _title = re.search(r'\《(.+)\》', title)
            title = _title.group(1) if _title else title
            ext = 'mp3'
        else:
            download_url = res['durl'][0]['url']
            ext = 'mp4'

        # 处理特殊字符：/ 和 \
        title = re.sub(r'[/\\]', ' ', title)
        # 最终的文件名
        final_fname = f'{title}.{ext}'
        # 未处理的文件名
        raw_fname = f'{title}.raw.{ext}'
        # 封面名
        cover_fname = f'{title}.{cover_url.split(".")[-1]}'
        if os.path.exists(final_fname):
            print(f'[bilibili-dl] ⚠️  该文件已存在：{os.path.abspath(final_fname)}')
            continue
        else:
            print(f'[bilibili-dl] 当前下载内容：{title}')
            opener = urllib.request.build_opener()
            opener.addheaders = [
                ('User-Agent', 'User-Agent'),
                ('Referer', 'https://www.bilibili.com'),
                ('Connection', 'keep-alive'),
            ]
            urllib.request.install_opener(opener)
            # 下载音频和封面
            urllib.request.urlretrieve(download_url, raw_fname, show_progress)
            urllib.request.urlretrieve(cover_url, cover_fname)
            # 添加封面到音频上
            print(f'[ffmpeg] 正在合并封面中...')
            if is_audio_only:
                subprocess.call(f'ffmpeg -i "{raw_fname}" -i "{cover_fname}"     \
                                         -loglevel error                         \
                                         -map 0:0 -map 1:0                       \
                                         -metadata album="{title}"               \
                                         -metadata artist="{up_name}"            \
                                         -metadata:s:v title="Album cover"       \
                                         -metadata:s:v comment="Cover (Front)"   \
                                         -id3v2_version 3 -write_id3v1 1 "{final_fname}"', shell=True)
            else:
                subprocess.call(f'ffmpeg -i "{raw_fname}" -i "{cover_fname}"     \
                                         -loglevel error                         \
                                         -map 1 -map 0                           \
                                         -c copy                                 \
                                         -disposition:0 attached_pic "{final_fname}"', shell=True)
            os.remove(raw_fname)
            os.remove(cover_fname)
            print(f'[bilibili-dl] ✅ 下载完成: {os.path.abspath(final_fname)}')
