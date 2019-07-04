import zipfile, os, re

"""
-v verbose 详细输出
-h help 指令说明
-p preview 预览结果，不进行真实压缩
-m mute 不打印结果
-i include 包含的模式，默认所有'.*'
-e exclude 排除的模式，默认为'.*\.zip$'
-f force 直接执行，不要确认
-s source 源目录
-d destination 目标目录
"""


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
    verbose_print('zipfile path: ', zipfile_path)
    back_zipfile = zipfile.ZipFile(zipfile_path, mode='w')
    include_regex = re.compile(include_pattern)
    exclude_regex = re.compile(exclude_pattern) if exclude_pattern else None

    # 遍历目录
    num_files = 0
    for folder_name, sub_folders, files in os.walk(folder):
        verbose_print("adding folder: ", folder_name)
        back_zipfile.write(folder_name)
        # 遍历文件
        for file in files:
            base_name = os.path.basename(file)
            file_path = os.path.join(folder_name, file)
            if include_regex.match(base_name):
                if exclude_regex is not None and exclude_regex.match(base_name):
                    verbose_print('filtered file: ', file_path)
                    continue
                num_files += 1
                verbose_print("adding file: ", file_path)
                back_zipfile.write(file_path)

    back_zipfile.close()
    verbose_print('Added {} files'.format(num_files))


def verbose_print(*val):
    if setting_verbose:
        print(*val)


if __name__ == '__main__':
    setting_verbose = True
    os.chdir('/Users/qiubaisen/PycharmProjects/CrashCourse/automate_python')
    create_zipfile('back_up_zip'
                   , '/Users/qiubaisen/Movies/temp')
