import os


def main():
    work_dir = r"D:\Dropbox\Documents\Discord_log_merge\html_logs"

    for root, dirs, files in os.walk(work_dir):

        print('files', files)
        for f in files:
            print(f)


if __name__ == '__main__':
    main()
