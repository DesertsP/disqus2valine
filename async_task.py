import threading
from save_data import *
from parse_xml import *


class ProcessThread(threading.Thread):
    def __init__(self, appid, appkey, file_path):
        threading.Thread.__init__(self)
        self.appid = appid
        self.appkey = appkey
        self.file_path = file_path

    def run(self):
        init_account(self.appid, self.appkey)
        parsed_list = parse_all_posts(self.file_path)
        save_all([build_object(p) for p in parsed_list])
