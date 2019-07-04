本项目是python学习过程中的一些demo

1. [《Python编程:从入门到实践》](https://book.douban.com/subject/26829016/)
    * `Macintosh, python3.7.3, pygame1.9.2`
    * 尝试了下 `pygame` 部分，其余部分跳过
    * 对应目录 [`alien_invasion`](./alien_invasion)
    ```bash
    brew install hg sdl sdl_image sdl_ttf sdl_mixer portmidi 
    pip install pygame=='1.9.2' 
    ```
    
2. [《Python编程快速上手:让繁琐工作自动化》](https://book.douban.com/subject/26836700/)    
    1. 电话号码和email地址提取器
        * 章节 `7.15`
        * [`phone_email_extractor.py`](./automate_python/phone_email_extractor/phone_email_extractor.py)
        * 剪贴板 `pyperclip`
        * 正则表达式 `re`
    2. 多重剪贴板
        * 章节 `8.6`
        * [`mcb.pyw`](./automate_python/multi_clipboard/mcb.pyw)
        * 持久化 `shelve`
        * 创建软连接并添加到环境变量中
    3. 备份为压缩文件
        * 章节 `9.5`
        * [back_up2zip.py](./automate_python/back_up_zip/back_up2zip.py)
        * 压缩文件 `zipfile`