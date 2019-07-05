#! /usr/local/bin/python3
# coding=utf-8
import zipfile, os, re, sys
from optparse import OptionParser
from pprint import pformat


def get_zipfile_path(folder, destination):
    """
    获取压缩文件名
    :param folder: 被压缩目录的绝对路径
    :param destination: 放置压缩文件的绝对路径
    :return: 压缩文件的绝对路径
    """
    index = 1
    while True:
        # <basename_02.zip> 命名格式
        zipfile_name = os.path.basename(folder) + '_{:0>2}.zip'.format(index)
        zipfile_path = os.path.join(destination, zipfile_name)
        if not os.path.exists(zipfile_path):
            return zipfile_path
        index += 1


def create_zipfile(folder, destination, include_pattern=r'.*', exclude_pattern=None):
    """
    创建压缩文件，根据预期添加文件进行压缩。`expect`中除开`exclude`的
    :param folder: 被压缩目录的绝对路径
    :param destination: 放置压缩文件的绝对路径
    :param include_pattern: 预期文件名模式，不为None
    :param exclude_pattern: 排除文件名模式，可为None
    :return: zipfile绝对路径
    """
    zipfile_path = get_zipfile_path(folder, destination)
    print('zipfile path: ', zipfile_path)
    back_zipfile = zipfile.ZipFile(zipfile_path, mode='w')
    include_regex = re.compile(include_pattern)
    exclude_regex = re.compile(exclude_pattern) if exclude_pattern else None

    write_folders, write_files, filtered_files = [], [], []
    # 遍历目录
    for folder_name, sub_folders, files in os.walk(folder):
        write_folders.append(folder_name)
        # 遍历文件
        for file in files:
            base_name = os.path.basename(file)
            file_path = os.path.join(folder_name, file)
            if include_regex.match(base_name):
                if exclude_regex is not None and exclude_regex.match(base_name):
                    filtered_files.append(file_path)
                    continue
                write_files.append(file_path)
            else:
                filtered_files.append(file_path)
    # 遍历结束
    deal_with_options(back_zipfile, write_folders, write_files, filtered_files)
    back_zipfile.close()

    print('Added %d files' % len(write_files))


def deal_with_options(back_zipfile, write_folders, write_files, filtered_files):
    """
    遍历结束后，打印信息，提供确认操作，完成文件写入操作
    """

    def format_list(items):
        """根据options.pretty 选项返回list的字符串形式"""
        return pformat(items) if options.pretty else repr(items)

    # 如果有 verbose 选项，则详细输出信息
    if options.verbose:
        print('{:>3} folders: '.format(len(write_folders)), format_list(write_folders))
        print('{:>3} files: '.format(len(write_files)), format_list(write_files))
        print('{:>3} filtered: '.format(len(filtered_files)), format_list(filtered_files))
    # 否则 只打印添加的文件信息，且最多打印十条
    else:
        print('{:>3} files: '.format(len(write_files)), format_list(write_files[:10]))

    # 如果非 force 选项，则需要确认操作
    if not options.force:
        answer = input("continue processing?\t\t Y/N\n")
        while answer.lower() not in ('y', 'n'):
            answer = input("input must be Y/N")
        if answer.lower() == 'n':
            print("cancel processing...")
            back_zipfile.close()
            os.remove(back_zipfile.filename)
            sys.exit()
    # 正式写入内容
    if options.verbose:
        print('start writing files...')
    for file in write_files:
        back_zipfile.write(file)
    if options.verbose:
        print('complete writing files...')


if __name__ == '__main__':
    usage = '''Usage: %progress [options] arg1 arg2
    arg1: target folder which will be zipped
    arg2: destination folder where to place
    '''

    parser = OptionParser(usage=usage)
    parser.add_option('-f', '--force', dest='force', action='store_true', default=False,
                      help='process without any questions')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False,
                      help='show all messages to stdout')
    parser.add_option('-p', '--pretty', dest='pretty', action='store_true', default=False,
                      help='use pprint to show messages')
    parser.add_option('-i', '--include', dest='include', action="store", type="string", default=r'.*',
                      help='regex pattern which files should be included. Default Pattern: < .* >')
    parser.add_option('-e', '--exclude', dest='exclude', action="store", type="string",
                      help='regex pattern which files should be excluded. Default Pattern: None')

    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("incorrect number of arguments")

    create_zipfile(args[0], args[1], include_pattern=options.include, exclude_pattern=options.exclude)
