import pymysql
import requests
import logging
class Operational_DB:
    headers = {
        'Referer': 'https://www.baidu.com',
    }
    def __init__(self):
        # 初始化连接配置和连接参数
        db_settings = {
            'host': 'localhost',
            'db': 'weibo',
            'user': 'root',
            'password': 'wwt123',
            'charset': 'utf8',
            'use_unicode': True
        }

        # self.db_setting = crawler.settings.get('db_setting')
        self.conn = pymysql.connect(**db_settings)
        self.cursor = self.conn.cursor()

    def insert_proxytable(self,ip,port,ip_type):
        sql = "insert into proxy(ip,port,ip_type) values('%s','%s','%s')"%(ip,port,ip_type)
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def get_random_ip(self):
        """获取有效的ip地址"""
        # 建立索引映射
        ip, port, ip_type = 0, 1, 2
        # sql查询语句,随机获取一行值
        sql = 'select ip, port, ip_type from proxy order by rand() limit 1'
        try:
            # 从数据库中获取一行值
            self.cursor.execute(sql)
            # 对于查询结果不能直接获取，需要通过fetchall，索引来取每个值
            info_list = self.cursor.fetchall()
            logging.log(info_list)
            for info in info_list:
                ip = info[ip]
                port = info[port]
                ip_type = info[ip_type]
            logging.log(ip)
            logging.log(port)
            logging.log(ip_type)

        except Exception as e:
            logging.log(e)
            print(e)
        else:
            # proxy_url = '{ip_type}://{ip}:{port}'.format(ip_type=ip_type, ip=ip, port=port)
            # logging.log(proxy_url)
            # return proxy_url
            effective_ip = self.check_ip(ip, port, ip_type)
            if effective_ip:
                return effective_ip
            else:
                self.del_usedless_ip(ip)
                return self.get_random_ip()

    def check_ip(self, ip, port, ip_type):
        logging.log("check_ip is running ")
        """检查这个ip是否有效"""
        http_url = 'https://www.baidu.com'
        proxy_url = '{ip_type}://{ip}:{port}'.format(ip_type=ip_type, ip=ip, port=port)
        logging.log(proxy_url)
        try:
            prox_dict = {
                'http': proxy_url
            }
            response = requests.get(http_url, proxies=prox_dict, headers=self.headers)
        except Exception as e:
            print(e)
            return False
        else:
            if 200 <= response.status_code <= 300:
                return proxy_url
            else:
                self.del_usedless_ip(ip)
                return False
        pass

    def del_usedless_ip(self, ip):
        """删除无效的ip"""
        logging.log("del_usedless_ip is running")
        sql = "delete from proxy where ip='%s'" % ip
        self.cursor.execute(sql)
        self.conn.commit()

    def insert_weibo(self,weibo_id,hottop):
        sql = "insert into weibo(weibo_id,hottop) values('%s','%s')" % (weibo_id,hottop)
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
    def check_weibo(self,weibo_id):
        sql = "select * from weibo where weibo_id = '%s';"%weibo_id
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result is not None:
            return False
        else:
            return True
    def mark_weibo(self,weibo_id):
        sql = "update weibo set flag = 1 where weibo_id = '%s';"%weibo_id
        self.cursor.execute(sql)
        self.conn.commit()
    def load_weibo(self):
        #返回没有爬取过的微博
        sql = "select * from weibo where flag = 0;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
        # 返回值是一个tumple的list ex:[(),(),...,()]


