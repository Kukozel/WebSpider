# coding:utf-8
import re


# HTML解析器
class HtmlParser(object):
    def parser(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        new_data = self._get_new_data(page_url, html_cont)
        return new_data

    def _get_new_data(self, page_url, html_cont):
        data = {}
        data['url'] = page_url
        # TODO:添加需要到数据库的数据项
        data['userName'] = self.searchItem('<td class="x"> 姓名 </td> <td class="y">(.*?)</td>', html_cont)
        data['birth'] = self.searchItem('<td class="x"> 出生年月 </td> <td class="y">(.*?)</td>', html_cont)
        data['sex'] = self.searchItem('<td class="x"> 性别 </td> <td class="y5">(.*?)</td>', html_cont)
        data['idCardNumber'] = self.searchItem('<td class="x"> 身份证号 </td> <td colspan="3" class="y">(.*?)</td>',
                                               html_cont)
        data['nativePlace'] = self.searchItem('<td class="x"> 籍贯 </td> <td class="y">(.*?)</td>', html_cont)
        data['height'] = self.searchItem('<td class="x"> 身高 </td> <td class="y">(.*?)</td>', html_cont)
        data['weight'] = self.searchItem('<td class="x"> 体重 </td> <td class="y">(.*?)</td>', html_cont)
        data['nowLocation'] = self.searchItem('<td class="x"> 现所在地 </td> <td class="y">(.*?)</td>', html_cont)
        data['maritalStatus'] = self.searchItem('<td class="x"> 婚姻状况 </td> <td class="y">(.*?)</td>', html_cont)
        data['politicsStatus'] = self.searchItem('<td class="x"> 政治面貌 </td> <td class="y">(.*?)</td>', html_cont)
        data['graduationTime'] = self.searchItem('<td class="x"> 毕业时间 </td> <td class="y">(.*?)</td>', html_cont)

        # 特殊处理
        arrFind = re.findall(
            '<td class="x"> 第一外语 </td> <td class="y">(.*?)</td> <td class="x"> 掌握程度 </td> <td class="y">(.*?)</td>',
            html_cont)
        arrList = [None, None]
        if len(arrFind) > 1:
            s1 = arrFind[0].strip()
            s2 = arrFind[1].strip()
            if s1 != '&nbsp;':
                arrList[0] = s1
            if s2 != '&nbsp;':
                arrList[1] = s2
        data['foreignFirst'] = arrList

        # 特殊处理
        arrFind = re.findall(
            '<td class="x"> 第二外语 </td> <td class="y">(.*?)</td> <td class="x"> 掌握程度 </td> <td class="y">(.*?)</td>',
            html_cont)
        arrList = [None, None]
        if len(arrFind) > 1:
            s1 = arrFind[0].strip()
            s2 = arrFind[1].strip()
            if s1 != '&nbsp;':
                arrList[0] = s1
            if s2 != '&nbsp;':
                arrList[1] = s2
        data['foreignSecond'] = arrList

        data['highestEducation'] = self.searchItem('<td class="x"> 最高学历 </td> <td class="y">(.*?)</td>', html_cont)
        data['workExperience'] = self.searchItem('<td class="x"> 工作经验 </td> <td class="y">(.*?)</td>', html_cont)
        data['workType'] = self.searchItem('<td class="x"> 工作类型 </td> <td class="y">(.*?)</td>', html_cont)
        data['email'] = self.searchItem('<td class="x"> 电子邮件 </td> <td colspan="2" class="y4" type="email">(.*?)</td>',
                                        html_cont)
        data['qq'] = self.searchItem('<td class="x"> QQ </td> <td class="y" type="qq">(.*?)</td>', html_cont)
        data['telNumber'] = self.searchItem(
            '<td class="x"> 联系电话 </td> <td colspan="3" class="y4" type="tel">(.*?)</td>', html_cont)
        data['major'] = self.searchItem('<td class="x"> 所学专业 </td> <td colspan="2" class="y4">(.*?)</td>', html_cont)
        data['jobHunt'] = self.searchItem('<td class="x"> 求职岗位 </td> <td colspan="3" class="y4">(.*?)</td>', html_cont)
        data['huntType'] = self.searchItem('<td class="x"> 职位类别 </td> <td colspan="2" class="y4">(.*?)</td>', html_cont)
        data['address'] = self.searchItem('<td class="x"> 联系地址 </td> <td colspan="3" class="y4">(.*?)</td>', html_cont)
        data['employmentCategory'] = self.searchItem('<td class="x"> 行业类别 </td> <td colspan="2" class="y4">(.*?)</td>',
                                                     html_cont)
        data['hopeLocation'] = self.searchItem('<td class="x"> 期望工作区域 </td> <td colspan="3" class="y4">(.*?)</td>',
                                               html_cont)
        data['hopeSalary'] = self.searchItem('<td class="x"> 期望月薪 </td> <td colspan="2" class="y4">(.*?)</td>',
                                             html_cont)

        # 特殊处理
        s = self.searchItem('<tr> <td class="x"> 自我评价 </td> <td colspan="6" class="y3">(.*?)</td>', html_cont)
        if s is not None:
            s = s.replace('<br/>', '')
            s = s.replace('&nbsp;', '')
            s = s.replace('&#176;', '')
        data['selfAssessment'] = s

        # 特殊处理
        eduList = []
        eduStr = self.searchItem(
            '<td colspan="2" class="x2"> 学校 </td> </tr>(.*?)<tr> <td colspan="7" class="x2"> <b>工作/实践经验</b>', html_cont)
        if len(eduStr) > 0:
            eduArr = re.findall('<tr>(.*?)</tr>', eduStr)
            if len(eduArr) > 0:
                for ed in eduArr:
                    oneEdu = {}
                    oneEdu['学历'] = re.findall('<td class="y2">(.*?)</td>', ed)[0].strip()
                    oneEdu['专业类型'] = re.findall('<td colspan="2" class="y2">(.*?)</td>', ed)[0].strip()
                    oneEdu['毕业时间'] = re.findall('<td class="y2">(.*?)</td>', ed)[1].strip()
                    oneEdu['学校'] = re.findall('<td colspan="2" class="y2">(.*?)</td>', ed)[1].strip()
                    eduList.append(oneEdu)
        if len(eduList) == 0:
            data['education'] = None
        else:
            data['education'] = eduList

        # 特殊处理
        workList = []
        workStr = self.searchItem('<b>工作/实践经验</b> </td> </tr>(.*?)</table>', html_cont)
        if len(workStr) > 0 and workStr[0].strip() != '':
            work1 = re.findall('所在单位 </td> <td colspan="3" class="y4"> <font color="#cc0000">(.*?)</font>', workStr)
            work2 = re.findall('职位名称 </td> <td colspan="2" class="y4">(.*?)</td>', workStr)
            work3 = re.findall('单位行业 </td> <td colspan="3" class="y4">(.*?)</td>', workStr)
            work4 = re.findall('时间 </td> <td colspan="2" class="y4">(.*?)</td>', workStr)
            work5 = re.findall('工作业绩 </td> <td colspan="6" class="y3">(.*?)</td>', workStr)
            if len(work1) > 0:
                for i in range(len(work1)):
                    wo = {}
                    wo['所在单位'] = work1[i].strip()[1:-1]
                    wo['职位名称'] = work2[i].strip()
                    wo['单位行业'] = work3[i].strip()
                    wo['时间'] = work4[i].strip()
                    wo5 = work5[i].strip()
                    wo5 = wo5.replace('<br/>', '')
                    wo5 = wo5.replace('&nbsp;', '')
                    wo['工作内容/工作业绩'] = wo5
                    workList.append(wo)
        if len(workList) == 0:
            data['workExps'] = None
        else:
            data['workExps'] = workList

        return data

    def searchItem(self, queryStr, html_cont):
        temp = re.findall(queryStr, html_cont)
        if len(temp) > 0:
            text = temp[0].strip()
            if text == '':
                return None
            return text
        return None
