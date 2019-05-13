import os


def main():
    work_dir = r"D:\Dropbox\Documents\Discord_log_merge\html_logs\debug"
    input_dir = r"D:\Dropbox\Documents\Discord_log_merge"

    # テンプレートファイルからヘッダー部分を読み込み
    result_data = import_head(input_dir)

    chat_data = []
    for root, dirs, files in os.walk(work_dir):
        for f in files:
            # ファイル名からチャンネル名を抜き取り
            channel_name = cut_out_channel_name(f)

            file_path = work_dir + os.sep + f
            # 各ファイルを読み込み
            chat_data += chat_log_merge(file_path, channel_name)

    sorted(chat_data, key=lambda x: x[0])

    # headerファイルとDiscordチャットログを合わせる
    merge_header_and_chatdata(result_data, chat_data)


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

    chat_data = []

    # ファイル読み込み
    with open(file_path, encoding='utf-8') as f:
        html = f.read()
        soup = BeautifulSoup(html, 'html.parser')

    chat_text_list = soup.find_all('div', class_='chatlog__message-group')
    chat_timestamp_list = soup.find_all('span', class_='chatlog__timestamp')

    # タイムスタンプ、チャット内容、チャンネル名をそれぞれリストに格納
    for chat_text, chat_timestamp in zip(chat_text_list, chat_timestamp_list):
        chat_data.append([chat_timestamp.string, chat_text, channel_name])

    return chat_data


def import_head(input_dir: str) -> str:
    header_file_name = 'template_head.html'
    header_file_path = input_dir + os.sep + header_file_name

    with open(header_file_path, encoding='utf-8') as f:
        result_data = f.read()

    return result_data


if __name__ == '__main__':
    main()
