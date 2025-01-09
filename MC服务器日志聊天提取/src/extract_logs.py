# 说明：
# 1. 下载MCMANAGER中logs文件夹的内容到本地文件夹
# 2. 将该脚本的exe文件放到本地logs文件夹中
# 3. 双击运行该脚本，可以将所有log文件中的用户聊天内容提取到一个txt文件中


import os
import gzip
import re
import shutil

def move_existing_logs(directory, log_dir):
    """将当前目录下已有的 .log 文件移动到指定文件夹"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    for filename in os.listdir(directory):
        if filename.endswith('.log'):
            src_path = os.path.join(directory, filename)
            dest_path = os.path.join(log_dir, filename)

            # 如果目标文件已存在，覆盖它
            shutil.move(src_path, dest_path)
            print(f"移动文件: {src_path} -> {dest_path}")

def decompress_gz_files(directory, log_dir):
    """解压当前目录下所有的 .gz 文件并将 .log 文件放入指定文件夹"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    for filename in os.listdir(directory):
        if filename.endswith('.gz'):
            gz_path = os.path.join(directory, filename)
            log_path = os.path.join(log_dir, os.path.splitext(filename)[0])

            # 如果解压后的文件已存在，则替换
            with gzip.open(gz_path, 'rt', encoding='utf-8') as gz_file:
                with open(log_path, 'w', encoding='utf-8') as log_file:
                    log_file.write(gz_file.read())

            print(f"解压完成: {gz_path} -> {log_path}")
            os.remove(gz_path)  # 删除 .gz 文件
            print(f"删除文件: {gz_path}")

def extract_content_from_logs(log_dir, output_file):
    """从 .log 文件中提取 <...> 包含的内容及其后面一整行的内容"""
    pattern = re.compile(r"<.*?>.*")
    
    with open(output_file, 'a', encoding='utf-8') as out_file:  # 以追加模式打开输出文件
        for filename in os.listdir(log_dir):
            if filename.endswith('.log'):
                log_path = os.path.join(log_dir, filename)

                with open(log_path, 'r', encoding='utf-8') as log_file:
                    for line in log_file:
                        match = pattern.search(line)
                        if match:
                            out_file.write(match.group() + '\n')

                print(f"处理完成: {log_path}")

def main():
    current_directory = os.getcwd()
    log_directory = os.path.join(current_directory, 'logs')
    output_file = os.path.join(current_directory, 'extracted_content.txt')

    print("移动已有的 .log 文件...")
    move_existing_logs(current_directory, log_directory)

    print("开始解压 .gz 文件...")
    decompress_gz_files(current_directory, log_directory)

    print("开始提取 .log 文件中的内容...")
    extract_content_from_logs(log_directory, output_file)

    print(f"所有操作完成，提取结果保存在: {output_file}")

if __name__ == "__main__":
    main()
