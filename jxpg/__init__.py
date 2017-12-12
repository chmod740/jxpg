import requests
from PIL import Image
import re

class Jxpg:
    def __init__(self, url='http://jwxt.imu.edu.cn/'):
        self.url = url
        self.req = requests.Session()
        self.req.get(url=url + "login")


    def show_captcha(self):
        response = self.req.get(self.url + 'img/captcha.jpg')
        open('tmp.jpg', 'wb').write(response.content)
        img = Image.open('tmp.jpg')
        img.show()

    def login(self, username, password, captcha):
        self.username = username
        self.password = password
        self.captcha = captcha
        # print('j_username=%s&j_password=%s&j_captcha=%s' % (username,password,captcha))
        response = self.req.post(url=self.url + 'j_spring_security_check', data={'j_username':username, 'j_password':password, 'j_captcha':captcha})
        if "<title>登录</title>" in str(response.content.decode("utf-8")):
            return False
        self.req.get(self.url + 'main/checkSelectCourseStatus')
        return True



    def get_evaluation_list(self):
        self.req.get(self.url + 'student/teachingEvaluation/evaluation/index')
        response = self.req.get(url=self.url + 'student/teachingEvaluation/teachingEvaluation/search')
        # print(response.content.decode("utf-8"))
        json = response.content.decode('utf-8')
        json = eval(json)
        dics = []
        for data in json.get('data'):
            if str(data.get('isEvaluated')) == '否':
                dic = {}
                dic['evaluatedPeople'] = str(data.get('evaluatedPeople'))
                dic['evaluatedPeopleNumber'] = str(data.get('id').get('evaluatedPeople'))
                dic['questionnaireCode'] = str(data.get('id').get('questionnaireCoding'))
                dic['questionnaireName'] = str(data.get('questionnaire').get('questionnaireName'))
                dic['evaluationContentNumber'] = str(data.get('id').get('evaluationContentNumber'))
                dic['evaluationContentContent'] = str(data.get('evaluationContent'))
                dics.append(dic)

        return dics


    def evaluate(self,dic):
        self.req.headers.update({'Referer': 'http://jwxt.imu.edu.cn/student/teachingEvaluation/evaluation/index', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'})
        response = self.req.post(url=self.url + 'student/teachingEvaluation/teachingEvaluation/evaluationPage', data=dic)
        # print(response.content.decode("utf-8"))
        results = re.findall("<input type=\"hidden\" name=\"tokenValue\" value=\"[^\"]{0,200}\"", response.content.decode("utf-8"))
        token_value = ''
        for res in results:
            token_value = str(res).replace('<input type="hidden" name="tokenValue" value="', '').replace('"', '')
        dic['tokenValue'] = token_value

        dic['0000000004'] = '5_1'
        dic['0000000003'] = '5_1'
        dic['0000000006'] = '5_1'
        dic['0000000007'] = '5_1'
        dic['0000000008'] = '5_1'
        dic['0000000009'] = '5_1'
        dic['0000000010'] = '5_1'
        dic['0000000011'] = '5_1'
        dic['0000000012'] = '5_1'
        dic['0000000013'] = '5_1'
        dic['0000000014'] = '5_1'
        dic['0000000015'] = '5_1'
        dic['0000000016'] = '5_1'
        dic['0000000017'] = '5_1'
        dic['0000000018'] = '5_1'
        dic['0000000019'] = '5_1'
        dic['0000000020'] = '5_1'
        dic['0000000021'] = '5_1'
        dic['0000000002'] = '5_1'
        dic['0000000005'] = '5_1'
        dic['zgpj'] = '通过上本门课程，我学会并理解了老师所讲授的课程内容。对我的学习帮助很大。'
        response = self.req.post(url=self.url + 'student/teachingEvaluation/teachingEvaluation/evaluation', data=dic)
        if '提交成功' in response.content.decode("utf-8"):
            return True
        else:
            return False
