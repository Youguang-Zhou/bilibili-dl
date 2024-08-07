# Bilibili-dl

## 1. 简介

Bilibili-dl 是一个下载 B 站音视频的工具（目前视频下载最高只支持 720P）。

## 2. 安装

```
pip install bilibili-dl
```

## 3. 使用

所需依赖：[ffmpeg](https://ffmpeg.org)

```
bilibili-dl [-h] [-v]
            [bv]
            [--mid [MID]]
            [--audio-only | -a]

positional arguments:
  bv                BV号

options:
  -h, --help        show this help message and exit
  -v, --version     查看版本号
  --mid [MID]       space.bilibili.com/{mid}
  --audio-only, -a  仅下载音频 (默认: False)
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

## 5. License

[Creative Commons Attribution-NonCommercial 4.0 International](LICENSE)
