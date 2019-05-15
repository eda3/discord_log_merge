import os
import pprint


def main():
    work_dir = r"D:\Dropbox\Documents\Discord_log_merge\html_logs\debug"
    input_dir = r"D:\Dropbox\Documents\Discord_log_merge"
    output_dir = r"D:\Dropbox\Documents\Discord_log_merge"

    # テンプレートファイルからヘッダー部分を読み込み
    header_data = import_head(input_dir)

    chat_data = []
    for root, dirs, files in os.walk(work_dir):
        for f in files:
            # ファイル名からチャンネル名を抜き取り
            channel_name = cut_out_channel_name(f)

            file_path = work_dir + os.sep + f
            # 各ファイルを読み込み
            chat_data += chat_log_merge(file_path, channel_name)

    # 時系列順に並び替え
    chat_data.sort(key=lambda x: x[0])

    # headerファイルとDiscordチャットログを合わせる
    result_data = merge_header_and_chatdata(header_data, chat_data)

    # 結合データをhtmlファイルとして出力
    output_path = output_dir + os.sep + 'output.html'
    with open(output_path, 'w', encoding='utf-8') as f:
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


def chat_log_merge(file_path: str, channel_name: str):
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


def import_head(input_dir: str) -> str:
    header_file_name = 'template_head.html'
    header_file_path = input_dir + os.sep + header_file_name

    with open(header_file_path, encoding='utf-8') as f:
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
