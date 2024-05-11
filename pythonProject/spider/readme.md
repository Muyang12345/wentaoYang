[comment_user.py](comment_user.py)
爬取用户评论

1.运行chorme转发9222端口
user-data-dir为用户数据目录，可以指定一个目录，这样就不会影响到默认的用户数据目录
```shell
chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\selenum\AutomationProfile"
```
2.拿到直播间连接，修改程序直播链接url，运行程序
保存文件格式为{comments{%Y%m%d%H%M%S}.csv}
```shell
python comment_user.py
```


[huoyue_user.py](huoyue_user.py)
爬取活跃用户

1.运行chorme转发9223端口
user-data-dir为用户数据目录，可以指定一个目录，这样就不会影响到默认的用户数据目录
```shell
chrome.exe --remote-debugging-port=9223 --user-data-dir="D:\selenum\AutomationProfile"
```
2.修改程序直播链接url，运行程序
保存文件格式为{huoyue{%Y%m%d%H%M%S}.csv}
```shell
python huoyue_user.py
```