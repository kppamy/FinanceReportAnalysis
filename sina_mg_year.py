# -*- coding: utf-8 -*-

__author__ = "Gallen_qiu"
'''最近5年的财报'''
import requests,json,time
from bs4 import BeautifulSoup
from my_queque import *
from concurrent.futures import ThreadPoolExecutor
# from pymongo.collection import Collection
import pandas as pd
class Xinalang():
    def __init__(self):
        self.queue=Queue()
        self.info=[]
        self.dict_list=[]

    def req(self,ninfo):
        try:
            info=json.loads(ninfo)
            scode=info["SECCODE"]
            year=info["year"]
            # print(scode,year)
            data_=info
            url0='http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{}/ctrl/{}/displaytype/4.phtml'.format(scode,year)
            url1='http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/{}/ctrl/{}/displaytype/4.phtml'.format(scode,year)
            url2='http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{}/ctrl/{}/displaytype/4.phtml'.format(scode,year)
            url_list=[]
            url_list.extend([url0,url1,url2])
            # data_year=[]
            data = {}
            for url in url_list:
                headers={}
                response=requests.get(url,headers=headers,timeout=5)
                soup=BeautifulSoup(response.content.decode("gb2312"),"lxml")

                '''报表日期'''
                trs = soup.select("tbody tr")

                for tr in trs:
                    tds=tr.select("td")
                    if tds != []:
                        # print(tds)
                        try:
                            value = tds[1].text
                            if value == "--":
                                value = 0.00
                            try:
                                data[tds[0].text] = float(value)
                            except:
                                data[tds[0].text] = value
                        except:
                            pass



                # data_year.append(data)
                data_.update(data)

            # data_["data"]=data_year
            print(info["SECCODE"],info["year"])
            self.dict_list.append(data_)
        except TimeoutError:
            print("timeout!!!!!!!")
            self.info.append(ninfo)
        except:
            print("unknow error!!!!!!!!!")
            info = json.loads(ninfo)
            print(info["SECCODE"], info["year"])

    def scheduler(self):
        year_list=[2019]
        # year_list=[2015,2016,2017,2018,2019]

        with open("./stockCode.txt", encoding="utf8") as f:
            lines=f.readlines()
        print('read stocks from txt: '+str(len(lines)))
        for line in lines:
            # print(line)
            info=json.loads(line)
            for year in year_list:
                info["year"]=year
                info_str=json.dumps(info)
                # print(json.loads(info_str))
                self.queue.put(info_str)
        total = self.queue.qsize()
        print('put into the queue '+str(total))
        counter = 0
        batch = 100
        while counter <= total:
            pool = ThreadPoolExecutor(max_workers=8)
            while self.queue.qsize() > 0:
                counter = counter + 1
                pool.submit(self.req, self.queue.get())
                # print('submit:  ' + str(counter))
                if counter % batch == 0:
                    break
            pool.shutdown()
            if counter % batch == 0:
                self.write_json(counter // batch)
            elif counter == total:
                self.write_json(total)
                counter = counter + 1
        print("Left："+str(len(self.info)))
        while len(self.info) > 0:
            self.req(self.info.pop())


    def write_json(self, batch):
        try:
            # # 建立连接
            # client = pymongo.MongoClient('localhost', 27017)
            # # 建立数据库
            # db = client["XinlangFinance"]
            #
            # # 从原有的txt文件导入share_id：
            #
            # # 表的对象化
            # mgtable = Collection(db, 'FinanceReport_data')

            # mgtable.insert_many(self.dict_list)
            print('#######################save file '+str(batch)+' ####################################')
            csv = pd.DataFrame(self.dict_list)
            csv.to_csv('finance_statement'+str(batch)+'.csv')
        except:
            print("error wite file！！")
            pass


if __name__ == '__main__':
    start_time=time.time()

    X = Xinalang()
    X.scheduler()

    print("Time cost：{}s".format(time.time()-start_time))


