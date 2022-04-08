import os

import setuptools

cwd = os.getcwd()

with open(f'{cwd}/README.md') as f:
    long_description = f.read()

with open(f'{cwd}/requirements.txt') as f:
    requirements = f.read().split('\n')


setuptools.setup(
    name='bilibili-dl',
    version='1.0.8',
    description='Bilibili-dl 是一个下载 B 站视频的工具（目前只支持下载音频）',
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Youguang-Zhou/bilibili-dl',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['bilibili-dl=bilibili_dl.cli:run_cli']
    },
)
