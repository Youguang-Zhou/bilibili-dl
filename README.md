# Bilibili-dl

## 1. 简介

Bilibili-dl 是一个下载 B 站音视频的工具（目前视频下载最高只支持720P）。

## 2. 安装

```
pip install bilibili-dl
```

## 3. 使用

所需依赖：[ffmpeg](https://ffmpeg.org)

```
bilibili-dl [-h] 
            [--mid MID]
            [--audio-only | -a]
            [--version]
            [bvid]

positional arguments:
  bvid                  BV号

options:
  -h, --help            
  --mid MID             up主id
  --audio-only, -a      仅下载音频 (default: False)
  --version             查看版本号
```

- 通过 BV 号下载单个视频：

```
bilibili-dl [bvid]
```

- 通过 mid 下载该 up 主的所有投稿视频:

```
bilibili-dl [--mid MID]
```
如仅需要音频则在以上命令后面加 `--audio-only` 或 `-a` 即可。

## 4. 感谢

感谢以下项目提供的支持：

- [SocialSisterYi/bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)

- [nuster1128/bilibiliAudioDownloader](https://github.com/nuster1128/bilibiliAudioDownloader.git)

## 5. License

[Creative Commons Attribution-NonCommercial 4.0 International](LICENSE)
