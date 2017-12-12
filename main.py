from jxpg import Jxpg

total_count = 0
success_count = 0

print("IMU教务系统一键评估脚本v1.0.3 by hupeng")
username = input("请输入用户名：")
password = input("请输入密码：")
print('\n')
jxpg = Jxpg()
jxpg.show_captcha()
print("如果图片打开失败，请在同级目录中手动打开tmp.jpg")
captcha = input("请输入验证码：")
if jxpg.login(username, password, captcha):
    dics = jxpg.get_evaluation_list()
    total_count = len(dics)
    for dic in dics:
        print(dic)
        if jxpg.evaluate(dic):
            success_count = success_count + 1

    print("评估结果，需要评估总数:" + str(total_count) + ",成功总数：" + str(success_count))

else:
    print("登录失败")
try:
    import os
    os.remove("tmp.jpg")
except:
    pass
input("请按回车键退出")

