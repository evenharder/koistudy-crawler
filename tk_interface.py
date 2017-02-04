from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askdirectory
from tkinter.scrolledtext import *
import queue
import os
import sys
import io
from spider import Spider
from constant import *

class GUI:

    status = 0
    spider=Spider()
    is_crawling = False
    check_queue_count = 0
    path = ''

    def __init__(self):
        self.root=Tk()
        self.root.title('KOISTUDY Crawler')
        self.root.resizable(width=False, height=False)
        self.canvas=Canvas(self.root, width=350, height=50)
        self.canvas.grid(row=1, column=1, sticky=(N,E,W,S))

        self.frame_login=LabelFrame(self.root, text='Login')
        self.frame_login.grid(row=2, column=1, sticky=(N,E,W,S))

        self.label_id=Label(self.frame_login, text='ID')
        self.label_id.grid(row=1, column=1, padx=5, sticky=(N,S))

        self.entry_id=Entry(self.frame_login, width=15)
        self.entry_id.grid(row=1, column=2, padx=15, sticky=(N,S))

        self.label_pw=Label(self.frame_login, text='Password')
        self.label_pw.grid(row=2, column=1, sticky=(N,S))

        self.entry_pw=Entry(self.frame_login, show='*', width=15)
        self.entry_pw.grid(row=2, column=2, sticky=(N,S))

        self.button_login=Button(self.frame_login, text='Log in',
            command=self.koi_login)
        self.button_login.grid(row=1, column=3, sticky=(N,S,E))

        self.button_logout=Button(self.frame_login, text='Log out',
            command=self.koi_logout)
        self.button_logout.grid(row=2, column=3, sticky=(N,S,E))

        self.frame_crawl=LabelFrame(self.root, text='Crawling')
        self.frame_crawl.grid(row=3, column=1, sticky=(N,E,W,S))

        self.variable_zerofill=IntVar()
        self.button_zerofill=Checkbutton(self.frame_crawl,
            text='Enable leading zeros', variable=self.variable_zerofill)
        self.button_zerofill.grid(row=1, column=1, sticky=(W,E))

        self.variable_directory=IntVar()
        self.button_directory=Checkbutton(self.frame_crawl,
            text='Create directories', variable=self.variable_directory)
        self.button_directory.grid(row=1, column=2, sticky=(W,E))

        self.variable_comment=IntVar()
        self.button_comment=Checkbutton(self.frame_crawl,
            text='Add metadata on header',
            variable=self.variable_comment, command=self.config_comment)
        self.button_comment.grid(row=2, column=1, sticky=(W,E))

        self.variable_hexa=IntVar()
        self.button_hexa=Checkbutton(self.frame_crawl,
            text='Hexadecimal',
            variable=self.variable_hexa)
        self.button_hexa.grid(row=2, column=2, sticky=(W,E))

        self.variable_option_watermark=IntVar()
        self.button_option_watermark=Checkbutton(self.frame_crawl,
            text='Watermark', variable=self.variable_option_watermark)
        self.button_option_watermark.grid(row=3, column=1, sticky=(W,E))

        self.variable_option_id=IntVar()
        self.button_option_id=Checkbutton(self.frame_crawl,
            text='KOISTUDY id', variable=self.variable_option_id)
        self.button_option_id.grid(row=3, column=2, sticky=(W,E))

        self.variable_option_prob_title=IntVar()
        self.button_option_prob_title=Checkbutton(self.frame_crawl,
            text='Problem title', variable=self.variable_option_prob_title)
        self.button_option_prob_title.grid(row=4, column=1, sticky=(W,E))

        self.variable_option_prob_url=IntVar()
        self.button_option_prob_url=Checkbutton(self.frame_crawl,
            text='Submission url', variable=self.variable_option_prob_url)
        self.button_option_prob_url.grid(row=4, column=2, sticky=(W,E))

        self.button_clear=Button(self.frame_crawl, text='Clear Info',
            command=self.text_clear)
        self.button_clear.grid(row=1, column=3, sticky=(W,E))

        self.button_open=Button(self.frame_crawl, text='Open',
            command=self.open_dir)
        self.button_open.grid(row=2, column=3, sticky=(W,E))

        self.button_crawl=Button(self.frame_crawl, text='Crawl',
            command=self.koi_crawl)
        self.button_crawl.grid(row=3, column=3, sticky=(W,E))

        self.button_abort=Button(self.frame_crawl, text='Abort',
            command=self.koi_abort)
        self.button_abort.grid(row=4, column=3, sticky=(W,E))

        self.frame_progress=LabelFrame(self.root, text='Progress')
        self.frame_progress.grid(row=4, column=1, sticky=(N,E,W,S))

        self.scrolledtext=ScrolledText(self.frame_progress)
        self.scrolledtext.bind('<Key>', lambda e: 'break')
        self.scrolledtext.grid(row=1, column=1, columnspan=2, sticky=(N,E,W,S))

        self.progressbar_crawl=Progressbar(self.frame_progress,
            orient='horizontal', length=350, value=0,
            maximum=1000, mode='determinate')
        self.progressbar_crawl.grid(row=2, column=1, sticky=(N,S))

        self.variable_scroll_down=IntVar()
        self.variable_scroll_down.set(1)
        self.button_scroll_down=Checkbutton(self.frame_progress,
            text='Enable auto-scrolling', variable=self.variable_scroll_down)
        self.button_scroll_down.grid(row=2, column=2, sticky=(N,S))

        self.config_comment()
        self.config_button(TK_LOGOUT)

        self.print_help_text()

        self.root.protocol('WM_DELETE_WINDOW', self.terminateTk)
        self.root.mainloop()

    def print_help_text(self):
        message = HELP_MESSAGE + '\n'
        self.text_print(message, scroll=False)

    def create_write_data(self):
        data = {
            'zerofill' : self.variable_zerofill.get(),
            'directory' : self.variable_directory.get(),
            'hexa' : self.variable_hexa.get(),
            'comment' : self.variable_comment.get(),
            'option_watermark' : self.variable_option_watermark.get(),
            'option_id' : self.variable_option_id.get(),
            'option_prob_title' : self.variable_option_prob_title.get(),
            'option_prob_url' : self.variable_option_prob_url.get()
        }

        if data['option_watermark'] == 0 and \
        data['option_id'] == 0 and \
        data['option_prob_title'] == 0 and \
        data['option_prob_url'] == 0:
            data['comment'] = 0

        return data

    def config_comment(self):
        if self.variable_comment.get() == 1:
            self.button_option_watermark['state']=NORMAL
            self.button_option_id['state']=NORMAL
            self.button_option_prob_title['state']=NORMAL
            self.button_option_prob_url['state']=NORMAL
        else:
            self.button_option_watermark['state']=DISABLED
            self.button_option_id['state']=DISABLED
            self.button_option_prob_title['state']=DISABLED
            self.button_option_prob_url['state']=DISABLED

    def config_button(self, status):
        self.status = status
        if status == TK_LOGOUT:
            self.button_login['state']=NORMAL
            self.button_logout['state']=DISABLED
            self.button_open['state']=DISABLED
            self.button_crawl['state']=DISABLED
            self.button_abort['state']=DISABLED

            self.entry_id['state']=NORMAL
            self.entry_pw['state']=NORMAL
            self.entry_id.delete(0, END)

        elif status == TK_LOGIN:
            self.button_login['state']=DISABLED
            self.button_logout['state']=NORMAL
            self.button_open['state']=NORMAL
            self.button_crawl['state']=DISABLED
            self.button_abort['state']=DISABLED

            self.entry_id['state']=DISABLED
            self.entry_pw['state']=DISABLED
            self.entry_pw.delete(0, END)

            self.button_zerofill['state']=NORMAL
            self.button_directory['state']=NORMAL
            self.button_comment['state']=NORMAL
            self.button_hexa['state']=NORMAL
            self.config_comment()

        elif status == TK_CRAWL_READY:
            self.button_login['state']=DISABLED
            self.button_logout['state']=NORMAL
            self.button_open['state']=NORMAL
            self.button_crawl['state']=NORMAL
            self.button_abort['state']=DISABLED

            self.entry_id['state']=DISABLED
            self.entry_pw['state']=DISABLED

            self.button_zerofill['state']=NORMAL
            self.button_directory['state']=NORMAL
            self.button_comment['state']=NORMAL
            self.button_hexa['state']=NORMAL
            self.config_comment()

        elif status == TK_CRAWLING:
            self.button_login['state']=DISABLED
            self.button_logout['state']=DISABLED
            self.button_open['state']=DISABLED
            self.button_crawl['state']=DISABLED
            self.button_abort['state']=NORMAL

            self.button_zerofill['state']=DISABLED
            self.button_directory['state']=DISABLED
            self.button_comment['state']=DISABLED
            self.button_hexa['state']=DISABLED
            self.button_option_watermark['state']=DISABLED
            self.button_option_id['state']=DISABLED
            self.button_option_prob_title['state']=DISABLED
            self.button_option_prob_url['state']=DISABLED

    def koi_login(self):
        ret = self.spider.login(self.entry_id.get(), self.entry_pw.get())
        self.text_print(ret['message'])
        if ret['status'] is True :
            self.entry_pw.delete(0, END)
            self.config_button(TK_LOGIN)

    def text_print(self, message, **kwargs):
        scroll_end = self.variable_scroll_down.get()

        for a in kwargs:
            if a.lower() == 'scroll' and kwargs[a] is False:
                scroll_end = 1

        self.scrolledtext.insert(END, message + '\n')
        if scroll_end == 1:
            self.scrolledtext.see(END)

    def text_clear(self):
        self.scrolledtext.delete(1.0, END)

    def koi_logout(self):
        self.spider.logout()
        self.scrolledtext.insert(END, 'Logged out.'+'\n')
        self.config_button(TK_LOGOUT)
        self.path = ''

    def open_dir(self):
        self.path = askdirectory(
            initialdir = os.path.abspath(''),
            title = 'Please select a directory.')

        if self.path:
            self.config_button(TK_CRAWL_READY)
            message = 'Directory : '+self.path
        else:
            self.config_button(TK_LOGIN)
            message = 'Directory not selected.'

        self.text_print(message)

    def koi_crawl(self): #select directory
        if not os.path.isdir(self.path):
            self.text_print('The selected directory does not exist.')
            self.config_button(TK_LOGIN)
            return

        self.queue=queue.Queue()
        self.prob_list = self.spider.get_problem_list()
        self.check_queue_count = 0

        if len(self.prob_list) == 0:
            self.text_print('You haven\'t solved any problems.')

        elif self.prob_list[0] == PROB_LIST_NETWORK_ERROR:
            self.text_print(self.prob_list[1])

        else:
            os.makedirs(self.entry_id.get(), exist_ok=True)
            self.config_button(TK_CRAWLING)
            self.spider.crawl_init(self.create_write_data(), self.path)
            self.progressbar_crawl['maximum']=len(self.prob_list)
            self.root.after(50, self.check_queue)
            self.koi_crawl_prob(0, 0)

    def koi_crawl_prob(self, index, flag):
        is_crawling = True

        if self.status != TK_CRAWLING:
            message = 'Crawling aborted......'
            is_crawling = False

        elif index == len(self.prob_list):
            self.queue.put(QUEUE_SUCCESS)
            message = 'Crawling completed.'
            is_crawling = False

        elif flag:
            message = 'Network Error. Reconnect after ' + str(flag) + ' second'
            if flag > 1:
                message = message + 's'
            message = message + '......'

            self.root.after(1000, lambda: self.koi_crawl_prob(index, flag-1))
        else:
            crawl_message = self.spider.crawl_code(self.prob_list[index])
            message = 'Prob No. ' + self.spider.get_prob_num_str(zerofill=1,
                hexa=1) + ' : '
            if crawl_message[0] == CRAWL_NETWORK_ERROR:
                message += crawl_message[1]
                self.root.after(1000, lambda: self.koi_crawl_prob(index,
                    NETWORK_RECONNECT_TIME))
            elif crawl_message[0] == CRAWL_PROBLEM_ERROR:
                message += crawl_message[1]
                self.root.after(20, lambda: self.koi_crawl_prob(index+1, 0))
            else:
                ret = self.spider.write_code()
                if ret == WRITE_FAIL:
                    message += 'Invalid directory. Abort crawling.'
                    self.koi_abort()
                else:
                    message += 'Successfully crawled.'
                    self.root.after(20, lambda: self.koi_crawl_prob(index+1, 0))

        if is_crawling:
            message += ' (' + str(index+1) + '/' + str(len(self.prob_list)) + ')'

        self.text_print(message)

        if is_crawling:
            self.progressbar_crawl['value']=index
        else:
            self.progressbar_crawl.stop()

    def koi_abort(self):
        self.config_button(TK_LOGIN)
        self.queue.put(QUEUE_ABORT)

    def exit(self):
        self.queue.put(QUEUE_EXIT)
        self.status = TK_EXIT

    def terminateTk(self):
        self.root.destroy()
        sys.exit()

    def check_queue(self):
        self.check_queue_count += 1
        try:
            message = self.queue.get(0)
            if message == QUEUE_SUCCESS:
                self.config_button(TK_LOGIN)
            elif message == QUEUE_ABORT:
                pass
            elif message == QUEUE_EXIT:
                if is_crawling is False:
                    self.terminateTk()
                else:
                    self.root.after(500, self.check_queue)
        except:
            self.root.after(500, self.check_queue)

