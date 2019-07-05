
### 在环境变量导出目录中创建软连接
```
# qiubaisen @ qiubosendeiMac in ~/Documents/workspace/script/soft_links [19:30:37]
$ ls -l
total 16
lrwxr-xr-x  1 qiubaisen  staff  87 Jul  5 19:30 backup -> /Users/qiubaisen/PycharmProjects/CrashCourse/automate_python/back_up_zip/back_up2zip.py
lrwxr-xr-x  1 qiubaisen  staff  84 Jun 30 21:52 mcb -> /Users/qiubaisen/PycharmProjects/CrashCourse/automate_python/multi_clipboard/mcb.pyw
```

### 获取帮助
```
# qiubaisen @ qiubosendeiMac in ~/Downloads/《Python编程》源代码文件 [19:34:42]
$ backup -h
Usage: backupress [options] arg1 arg2
    arg1: target folder which will be zipped
    arg2: destination folder where to place


Options:
  -h, --help            show this help message and exit
  -f, --force           process without any questions
  -v, --verbose         show all messages to stdout
  -p, --pretty          use pprint to show messages
  -i INCLUDE, --include=INCLUDE
                        regex pattern which files should be included. Default
                        Pattern: < .* >
  -e EXCLUDE, --exclude=EXCLUDE
                        regex pattern which files should be excluded. Default
                        Pattern: None
```

### 备份所有`.py`结尾的文件
```
# qiubaisen @ qiubosendeiMac in ~/Downloads/《Python编程》源代码文件 [19:39:21]
$ backup -pvi '.*\.py$' chapter_13 ~/Movies/temp
zipfile path:  /Users/qiubaisen/Movies/temp/chapter_13_02.zip
  2 folders:  ['chapter_13', 'chapter_13/images']
  7 files:  ['chapter_13/alien.py',
 'chapter_13/alien_invasion.py',
 'chapter_13/bullet.py',
 'chapter_13/game_functions.py',
 'chapter_13/game_stats.py',
 'chapter_13/settings.py',
 'chapter_13/ship.py']
  3 filtered:  ['chapter_13/.DS_Store',
 'chapter_13/images/alien.bmp',
 'chapter_13/images/ship.bmp']
continue processing?		 Y/N
n
cancel processing...
```

### 备份所有 `.py` 结尾，名字中不含`game`的文件
```
# qiubaisen @ qiubosendeiMac in ~/Downloads/《Python编程》源代码文件 [19:54:18]
$ backup -pv -i '.*\.py' -e '.*?game.*' chapter_13 ~/Movies/temp
zipfile path:  /Users/qiubaisen/Movies/temp/chapter_13_01.zip
  2 folders:  ['chapter_13', 'chapter_13/images']
  5 files:  ['chapter_13/alien.py',
 'chapter_13/alien_invasion.py',
 'chapter_13/bullet.py',
 'chapter_13/settings.py',
 'chapter_13/ship.py']
  5 filtered:  ['chapter_13/.DS_Store',
 'chapter_13/game_functions.py',
 'chapter_13/game_stats.py',
 'chapter_13/images/alien.bmp',
 'chapter_13/images/ship.bmp']
continue processing?		 Y/N
y
start writing files...
complete writing files...
Added 5 files

# qiubaisen @ qiubosendeiMac in ~/Movies/temp [19:57:30]
$ unzip -v chapter_13_01.zip
Archive:  chapter_13_01.zip
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
    1346  Stored     1346   0% 06-15-2016 02:16 b66573cb  chapter_13/alien.py
    1254  Stored     1254   0% 06-15-2016 02:16 d3b1ecaa  chapter_13/alien_invasion.py
    1139  Stored     1139   0% 06-15-2016 02:16 f52d50da  chapter_13/bullet.py
     780  Stored      780   0% 06-15-2016 02:16 afaad86e  chapter_13/settings.py
    1545  Stored     1545   0% 06-15-2016 02:16 2f239823  chapter_13/ship.py
--------          -------  ---                            -------
    6064             6064   0%                            5 files
```

### 直接备份
```
# qiubaisen @ qiubosendeiMac in ~/Downloads/《Python编程》源代码文件 [19:55:13]
$ backup -f chapter_13 ~/Movies/temp
zipfile path:  /Users/qiubaisen/Movies/temp/chapter_13_02.zip
 10 files:  ['chapter_13/.DS_Store', 'chapter_13/alien.py', 'chapter_13/alien_invasion.py', 'chapter_13/bullet.py', 'chapter_13/game_functions.py', 'chapter_13/game_stats.py', 'chapter_13/settings.py', 'chapter_13/ship.py', 'chapter_13/images/alien.bmp', 'chapter_13/images/ship.bmp']
Added 10 files

# qiubaisen @ qiubosendeiMac in ~/Movies/temp [20:00:28]
$ unzip -v chapter_13_02.zip
Archive:  chapter_13_02.zip
 Length   Method    Size  Cmpr    Date    Time   CRC-32   Name
--------  ------  ------- ---- ---------- ----- --------  ----
    6148  Stored     6148   0% 07-05-2019 19:38 05dcadf6  chapter_13/.DS_Store
    1346  Stored     1346   0% 06-15-2016 02:16 b66573cb  chapter_13/alien.py
    1254  Stored     1254   0% 06-15-2016 02:16 d3b1ecaa  chapter_13/alien_invasion.py
    1139  Stored     1139   0% 06-15-2016 02:16 f52d50da  chapter_13/bullet.py
    6329  Stored     6329   0% 06-15-2016 02:16 e4e37ae9  chapter_13/game_functions.py
     462  Stored      462   0% 06-15-2016 02:16 1c1b9d6c  chapter_13/game_stats.py
     780  Stored      780   0% 06-15-2016 02:16 afaad86e  chapter_13/settings.py
    1545  Stored     1545   0% 06-15-2016 02:16 2f239823  chapter_13/ship.py
   10494  Stored    10494   0% 06-15-2016 02:16 3abbaf52  chapter_13/images/alien.bmp
    8694  Stored     8694   0% 06-15-2016 02:16 2bdf0dfe  chapter_13/images/ship.bmp
--------          -------  ---                            -------
   38191            38191   0%                            10 files
```