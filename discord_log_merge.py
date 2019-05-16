import os
import sys
from pathlib import Path



def main():

    current_dir: Path = Path().cwd()
    work_dir: Path = current_dir / 'html_logs'
    input_dir: Path = current_dir
    output_dir: Path = current_dir

    # テンプレートファイルからヘッダー部分を読み込み
    header_data = import_head(input_dir)

    chat_data = []
    for root, dirs, files in os.walk(work_dir):
        for f in files:
            # ファイル名からチャンネル名を抜き取り
            channel_name = cut_out_channel_name(f)

            file_path = work_dir / f
            # 各ファイルを読み込み
            chat_data += chat_log_merge(file_path, channel_name)

    # 時系列順に並び替え
    chat_data.sort(key=lambda x: x[0])

    # headerファイルとDiscordチャットログを合わせる
    result_data = merge_header_and_chatdata(header_data, chat_data)

    # 結合データをhtmlファイルとして出力
    output_path:Path = output_dir / 'output.html'
    with output_path.open(mode='w') as f:
        f.write(str(result_data))


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


def chat_log_merge(file_path: str, channel_name: str) -> list:
    from bs4 import BeautifulSoup
    import datetime

    chat_data = []

    # ファイル読み込み
    with open(file_path, encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

    chat_text_list = soup.find_all('div', class_='chatlog__message-group')
    chat_timestamp_list = soup.find_all('span', class_='chatlog__timestamp')

    # 並び替えのため、タイムスタンプを変更
    for i, timestamp in enumerate(chat_timestamp_list):
        data = timestamp.string
        dte = datetime.datetime.strptime(data, '%y-%b-%d %p %I:%M')
        change_timestamp = dte.strftime('%Y-%m-%d %H:%M')
        chat_timestamp_list[i] = change_timestamp

    # タイムスタンプ、チャット内容、チャンネル名をそれぞれリストに格納
    for chat_text, chat_timestamp in zip(chat_text_list, chat_timestamp_list):
        chat_data.append([chat_timestamp, chat_text, channel_name])

    return chat_data


def import_head(input_dir: Path) -> str:
    header_file_name = 'template_head.html'
    header_file_path:Path = input_dir / header_file_name

    with header_file_path.open() as f:
        result_data = f.read()

    return result_data


def merge_header_and_chatdata(header: str, chatdata: list) -> str:
    result_data = header

    for data in chatdata:
        channel_name = data[2]
        result_data += f'<div class="{channel_name}">\n'
        result_data += f'<strong>{channel_name}</strong>\n'
        result_data += str(data[1])
        result_data += '\n</div>\n'

    return result_data


if __name__ == '__main__':
    main()
