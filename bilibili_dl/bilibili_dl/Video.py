from dataclasses import dataclass


@dataclass
class Video:
    bvid: str  # BV号
    cid: str  # 分p号
    title: str  # 标题
    up_name: str  # up名称
    cover_url: str  # 封面url
