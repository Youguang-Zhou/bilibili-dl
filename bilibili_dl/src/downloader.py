import os
import re
import subprocess
import urllib.request
from typing import List

from .constants import URL_DOWNLOAD
from .utils import ProgressBar, send_request
from .Video import Video


def download(videos: List[Video], is_audio_only: bool):
    for video in videos:

        params = {'bvid': video.bvid, 'cid': video.cid}

        if is_audio_only:
            params['fnval'] = '16'  # dash格式
        else:
            params['fnval'] = '1'  # mp4格式
            params['qn'] = '64'  # 720P画质

        res = send_request(URL_DOWNLOAD, params)

        download_url = None
        ext = None
        title = None
        if is_audio_only:
            download_url = res['dash']['audio'][0]['base_url']
            ext = 'mp3'
            # 对于音频，如果标题里有书名号，则提取书名号里的内容作为新标题，否则保留其原标题
            match = re.search(r'\《(.+)\》', video.title)
            title = match.group(1) if match else video.title
        else:
            download_url = res['durl'][0]['url']
            ext = 'mp4'
            # 对于视频，保留其原标题
            title = video.title

        # 处理特殊字符
        title = re.sub(r'[.:?/\\]', ' ', title).strip()
        title = re.sub(r'\s+', ' ', title)
        # 最终的文件名
        final_fname = f'{title}.{ext}'
        # 未处理的文件名
        raw_fname = f'{title}.raw.{ext}'
        # 封面名
        cover_fname = f'{title}.{video.cover_url.split(".")[-1]}'

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
            urllib.request.urlretrieve(download_url, raw_fname, ProgressBar())
            urllib.request.urlretrieve(video.cover_url, cover_fname)
            # 添加封面到音频上
            print(f'[ffmpeg] 正在合并封面中...')
            if is_audio_only:
                subprocess.call(
                    f'ffmpeg -i "{raw_fname}" -i "{cover_fname}"                 \
                                         -loglevel error                         \
                                         -map 0:0 -map 1:0                       \
                                         -metadata album="{title}"               \
                                         -metadata artist="{video.up_name}"      \
                                         -metadata:s:v title="Album cover"       \
                                         -metadata:s:v comment="Cover (Front)"   \
                                         -id3v2_version 3 -write_id3v1 1 "{final_fname}"',
                    shell=True,
                )
            else:
                subprocess.call(
                    f'ffmpeg -i "{raw_fname}" -i "{cover_fname}"                 \
                                         -loglevel error                         \
                                         -map 1 -map 0                           \
                                         -c copy                                 \
                                         -disposition:0 attached_pic "{final_fname}"',
                    shell=True,
                )
            os.remove(raw_fname)
            os.remove(cover_fname)
            print(f'[bilibili-dl] ✅ 下载完成: {os.path.abspath(final_fname)}')
