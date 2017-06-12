from httplib2 import Http
import re

class Jxpg:
    def __init__(self, username, password, base_url="http://jwxt.imu.edu.cn/"):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.http = Http()

    def _login(self):
        login_url = self.base_url + "loginAction.do"
        login_param = "zjh=" + self.username + "&mm=" + self.password
        login_headers = {}
        login_headers["Content-Type"] = "application/x-www-form-urlencoded"
        response, content = self.http.request(uri=login_url, method="POST", body=login_param, headers=login_headers)
        content = content.decode("gbk")
        if "<title>学分制综合教务</title>" in content:
            self.cookie = str(response["set-cookie"]).replace("; path=/", "")
            return True, self.cookie
        else:
            return False, None
    def _get_all_course(self):
        url = "http://jwxt.imu.edu.cn/jxpgXsAction.do?oper=listWj"
        headers = {}
        headers["Cookie"] = self.cookie
        response, content = self.http.request(uri=url, method="GET", headers=headers)
        content = content.decode("gbk")
        results = []
        all_result = re.findall("<img name=\"[^\"]{0,200}\"", content)
        for e in all_result:
            e = e.replace(e[0:10], "")
            e = e[1:len(e)-1]
            results.append(e)
        return results

    def do(self):

        login_flag, cookie = self._login()
        if not login_flag:
            ValueError("用户名或者密码错误")
        results = self._get_all_course()
        url1 = "http://jwxt.imu.edu.cn/jxpgXsAction.do"
        url2 = "http://jwxt.imu.edu.cn/jxpgXsAction.do?oper=wjpg"

        headers = {}
        headers["Cookie"] = self.cookie
        headers["Content-Type"] = "application/x-www-form-urlencoded"


        count = 0
        for r in results:
            sp = r.split("#@")
            body1 = "wjbm=" + sp[0] + "&bpr=" + sp[1] + "&pgnr=" + sp[5] + "&oper=wjShow&wjmc=&bprm=&pageSize=20&page=1&currentPage=1&pageNo="
            body2 = "wjbm=" + sp[0] + "&bpr=" + sp[1] + "&pgnr=" + sp[5] + "&0000000004=5_1&0000000005=5_1&0000000006=5_1&0000000007=5_1&0000000008=5_1&0000000009=5_1&0000000010=5_1&0000000011=5_1&0000000012=5_1&0000000013=5_1&0000000014=5_1&0000000015=5_1&0000000016=5_1&0000000017=5_1&0000000018=5_1&0000000019=5_1&0000000020=5_1&0000000021=5_1&0000000002=5_1&0000000003=5_1&zgpj=%CD%A8%B9%FD%C9%CF%B1%BE%C3%C5%BF%CE%B3%CC%A3%AC%CE%D2%CC%E1%B8%DF%C1%CB%CC%E1%B3%F6%A1%A2%B7%D6%CE%F6%A1%A2%BD%E2%BE%F6%CF%E0%B9%D8%CE%CA%CC%E2%B5%C4%C4%DC%C1%A6%A1%A3"
            response, content = self.http.request(uri=url1, method="POST", body=body1, headers=headers)
            # print(response)
            # print(content.decode("gbk"))
            response, content = self.http.request(uri=url2, method="POST", body=body2, headers=headers)
            # print(content.decode("gbk"))
            content = content.decode("gbk")

            if "评估成功" in content:
                print("课程 " + sp[4] + " 评估成功")
                count = count + 1
        print("评估成功" + str(count) + "门课!")
jxpg = Jxpg("0141124373", "531652")
jxpg.do()
