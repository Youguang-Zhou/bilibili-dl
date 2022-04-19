import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='bilibili-dl',
    version='1.0.12',
    description='Bilibili-dl 是一个下载 B 站视频的工具（目前只支持下载音频）',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Youguang-Zhou/bilibili-dl',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': ['bilibili-dl=bilibili_dl.cli:run_cli']
    },
    install_requires=[
        'tqdm',
        'requests',
        'progressbar'
    ],
)
