from .bilibili_dl import get_args, main


def run_cli():
    args = get_args()
    main(args)
