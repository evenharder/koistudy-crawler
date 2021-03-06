import requests
import html5lib
from bs4 import BeautifulSoup
import sys
import os
import io
from constant import *

class Spider:
    login_data = {
    '_filter' :'message_login',
    'user_id' :'',
    'password' :'',
    'module' :'member',
    'act' : 'procMemberLogin'}

    crawl_data = {
        'prob_num' : 0,
        'prob_name' : '',
        'code' : '',
        'prob_url' : '',
    }

    write_data = {}

    path = ''

    cookies = None

    def __init__(self):
        pass

    def login(self, id_, pw_):
        ret = {
            'status' : False,
            'message' : ''
        }
        try:
            self.login_data['user_id']=id_
            self.login_data['password']=pw_
            r = requests.post('http://koistudy.net/index.php',
                data = self.login_data, timeout=1)
        except requests.exceptions.ConnectionError:
            ret['message'] = 'ConnectionError raised. Please check your network status.'
        except requests.exceptions.Timeout:
            ret['message'] = 'Timeout raised. Please check your network status.'
        except requests.exceptions.TooManyRedirects:
            ret['message'] = 'TooManyRedirects raised. Please try again later.'
        else:
            soup = BeautifulSoup(r.text, 'html5lib')
            res = soup.find('h1').string
            if res == 'success':
                self.cookies = dict(PHPSESSID=r.cookies['PHPSESSID'])
                try:
                    r2 = requests.get('http://koistudy.net',
                        cookies=self.cookies, timeout=1)
                except requests.exceptions.ConnectionError:
                    ret['message'] = 'ConnectionError raised. Please check your network status.'
                except requests.exceptions.Timeout:
                    ret['message'] = 'Timeout raised. Please check your network status.'
                except requests.exceptions.TooManyRedirects:
                    ret['message'] = 'TooManyRedirects raised. Please try again later.'
                else:
                    ret['status']=True
                    soup2 = BeautifulSoup(r2.text, 'html5lib')
                    account = soup2.find('strong').string
                    ret['message']=account+'님, 환영합니다'
            else:
                ret['message']=res

        self.login_data['password']=''
        return ret

    def logout(self):
        self.login_data['user_id']=''
        self.cookies = None

    def get_problem_list(self):
        ls = [PROB_LIST_NETWORK_ERROR]
        try:
            r = requests.get('http://koistudy.net/?mid=view_prob&id=' +
                self.login_data['user_id'],    timeout=1)
        except requests.exceptions.ConnectionError:
            ls.append('ConnectionError raised. Please check your network status.')
        except requests.exceptions.Timeout:
            ls.append('Timeout raised. Please check your network status.')
        except requests.exceptions.TooManyRedirects:
            ls.append('TooManyRedirects raised. Please try again later.')
        else:
            soup = BeautifulSoup(r.text, 'html5lib')
            #soup.body.find(id='xe').find(id='container').find(id='body').find(id='content').find(id='gs13068').find(id='solved').p.font.b.find_all('a')
            res = soup.body.div.div.find(id='body').div.div.find(id='solved').p.font.b.find_all('a')
            ls = [int(a.string, 16) for a in res]
        return ls

    def crawl_init(self, write_data, path):
        self.write_data=write_data
        self.path=path

    def crawl_code(self, prob_num):
        self.crawl_data['prob_num'] = prob_num
        ret = CRAWL_NETWORK_ERROR
        message = ''
        try:
            r = requests.get('http://koistudy.net/?mid=prob_page&NO='+str(prob_num)+'&SEARCH=',
                cookies=self.cookies, timeout=1)
        except requests.exceptions.ConnectionError:
            message = 'ConnectionError raised.'
        except requests.exceptions.Timeout:
            message = 'Timeout raised.'
        except requests.exceptions.TooManyRedirects:
            message = 'TooManyRedirects raised.'
        else:
            soup = BeautifulSoup(r.text, 'html5lib')
            resc = soup.body.find(id='xe').div.find(id='body').div.find('center')

            if resc.string is not None:
                ret = CRAWL_PROBLEM_ERROR
                message = 'Cannot access this problem!'
            else:
                res = resc.find_all('a')[-1]['href']
                self.crawl_data['prob_name'] = resc.find_all('font')[2]\
                .contents[0]

                if res[:14] == '/?mid=src_page':
                    self.crawl_data['prob_url'] = 'http://koistudy.net'+res
                    try:
                        r2 = requests.get(self.crawl_data['prob_url'],
                            cookies=self.cookies, timeout=1)
                    except requests.exceptions.ConnectionError:
                        message = 'ConnectionError raised.'
                    except requests.exceptions.Timeout:
                        message = 'Timeout raised.'
                    except requests.exceptions.TooManyRedirects:
                        message = 'TooManyRedirects raised.'
                    else:
                        soup2 = BeautifulSoup(r2.text, 'html5lib')
                        self.crawl_data['code'] = soup2.body.find(id='xe')\
                        .div.find(id='body').find(id='content').pre.string
                        ret = CRAWL_SUCCESS
                else: #e.g. /?mid=view_prob
                    ret = CRAWL_PROBLEM_ERROR
                    message = 'Unable to crawl. Probably a C++11 bug in KOISTUDY.'

        return [ret, message]

    def get_comment(self):
        prob_num_str = self.get_prob_num_str()
        comment_list = []

        if self.write_data['option_watermark'] == 1:
            comment_list.append('Auto-generated by KOISTUDY Crawler')

        if self.write_data['option_id'] == 1:
            comment_list.append('Coder : ' + self.login_data['user_id'])

        if self.write_data['option_prob_title'] == 1:
            comment_list.append('Prob No. ' +
                self.get_prob_num_str(hexa=1, zerofill =1)
                 + ' : ' + self.crawl_data['prob_name'])

        if self.write_data['option_prob_url'] == 1:
            comment_list.append('Submission url : ' +
                self.crawl_data['prob_url'])

        comment_list[0] = '/* ' + comment_list[0]
        for i in range(1,len(comment_list)):
            comment_list[i] = ' * ' + comment_list[i]
        comment_list.append(' */')

        return comment_list

    def get_prob_num_str(self, **kwargs):
        write_hexa = self.write_data['hexa']
        write_zero = self.write_data['zerofill']

        for a in kwargs:
            if a.lower() == 'hexa':
                write_hexa = kwargs[a]
            elif a.lower() == 'zerofill':
                write_zero = kwargs[a]

        if write_hexa == 1:
            prob_num_str = '{:X}'.format(self.crawl_data['prob_num'])
        else:
            prob_num_str = str(self.crawl_data['prob_num'])

        if write_zero == 1:
            prob_num_str = prob_num_str.rjust(4, '0')

        return prob_num_str

    def write_code(self):
        ret = WRITE_SUCCESS
        prob_num_str = self.get_prob_num_str()
        prob_path = self.path

        if self.write_data['directory'] == 1:
            prob_path += '/' + prob_num_str
            os.makedirs(prob_path, exist_ok=True)

        if os.path.isdir(prob_path):
            f = io.open(prob_path + '/' + prob_num_str + '.cpp', 'w',
                encoding='utf8')

            if self.write_data['comment'] == 1:
                comment_list = self.get_comment()

                for comment in comment_list:
                    f.write(comment)
                    f.write('\n')

            f.write(self.crawl_data['code'])
            f.close()
        else:
            ret = WRITE_FAIL

        return ret
