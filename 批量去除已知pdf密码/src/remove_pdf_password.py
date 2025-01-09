import os
import pikepdf
import time


def remove_password(file, password):
    try:
        # 使用指定密码解锁 PDF
        pdf = pikepdf.open(file, password=password, allow_overwriting_input=True)
        pdf.save(file)
        print(f'{file} remove password success')
    except Exception as e:
        print(f'{file} remove password failed: {e}')

def main():
    password = input("Enter the password to unlock PDFs: ")
    files = [file for file in os.listdir() if file.endswith('.pdf')]
    print(f'PDF files: {files}')
    for file in files:
        remove_password(file, password)
    print('All PDF files have been unlocked successfully!!!')
    time.sleep(5)
    # 关闭终端
    exit()

if __name__ == '__main__':
    main()
