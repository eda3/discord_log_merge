import os


def main():
    work_dir = r"D:\Dropbox\Documents\Discord_log_merge\html_logs\debug"

    for root, dirs, files in os.walk(work_dir):

        print('files', files)
        for f in files:
            # ファイル名からチャンネル名を抜き取り
            channel_name = cut_out_channel_name(f)

            file_path = work_dir + os.sep + f

            file_reading(file_path)


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


def file_reading(file_path: str):
    from bs4 import BeautifulSoup

    chat_data = []

    # ファイル読み込み
    with open(file_path, encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

    chat_text = soup.find_all('div', class_='chatlog__message-group')[0]
    chat_timestamp = soup.find_all(
        'span', class_='chatlog__timestamp')[0].string


if __name__ == '__main__':
    main()
