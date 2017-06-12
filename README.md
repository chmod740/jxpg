# jxpg
# 内蒙古大学教学评估 Python3脚本
### *此版本为非官方版本,由运行此脚本产生的后果与本人无关,请谨慎使用
##### 项目进展：开发完成
##### 项目地址：https://github.com/imu-hupeng/jxpg
## SDK用法简介
### 1.安装(下面两种方式任选其一即可)
#### 1.1 推荐使用pip安装，命令： pip install jxpg
#### 1.2 下载源码，使用setup.py安装
### 2.教学评估操作
调用格式：
```python
from jxpg import Jxpg
jxpg = Jxpg(username="<你的教务系统学号>", password="<你的密码>")
jxpg.do()
```
输出样例:
> 评估成功7门课!

评估后的结果样例:
