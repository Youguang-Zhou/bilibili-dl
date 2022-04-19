# Bilibili-dl

## 1. 简介

Bilibili-dl 是一个下载 B 站视频的工具（目前只支持下载音频）。

## 2. 安装

```
pip install bilibili-dl
```

## 3. 使用

所需依赖：[ffmpeg](https://ffmpeg.org)

```
bilibili-dl [-h] [--mid MID] [bvid]

positional arguments:
  bvid                 BV号

options:
  -h, --help
  --mid MID            up主id
```

- 通过 BV 号下载单个视频的音频：

```
bilibili-dl [bvid]
```

- 通过 mid 下载该 up 主的所有投稿视频的音频:

```
bilibili-dl [--mid MID]
```

## 4. 感谢

感谢以下项目提供的支持：

- [SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)

- [nuster1128/bilibiliAudioDownloader](https://github.com/nuster1128/bilibiliAudioDownloader.git)

## 5. License

[Creative Commons Attribution-NonCommercial 4.0 International](LICENSE)
