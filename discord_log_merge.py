import os


def main():
    work_dir = r"D:\Dropbox\Documents\Discord_log_merge\html_logs"

    for root, dirs, files in os.walk(work_dir):

        print('files', files)
        for f in files:
            # ファイル名からチャンネル名を抜き取り
            channel_name = cut_out_channel_name(f)

            print(channel_name)


def cut_out_channel_name(file_name: str):
    ''' Discordログのファイル名から、テキストチャンネル名を切り出しする
    Args:
        file_name(str): Discordログのファイル名
    Returns:
         channel_name(str): チャンネル名
    '''

    import re

    pattern = r'.* - (.*) \[.*'
    result = re.match(pattern, file_name)

    if result:
        channel_name = result.group(1)

    return channel_name


if __name__ == '__main__':
    main()
