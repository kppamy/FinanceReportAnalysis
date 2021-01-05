import pandas as pd
import os

def nothing():
    ts=pd.read_csv('/Users/chenay/pyt/FinanceReportAnalysis/finance_statement_new.csv',index_col=0,dtype={'SECCODE':str},low_memory=False)
    ts=ts.replace({',':''}, regex=True)
    ts=ts.drop_duplicates()
    ts.to_csv('financial_overview.csv', mode='a')


def merge_data_files(path='.', pattern='', dtype=None):
    '''
    Merge all files is between start and end
    :param start: short date str
    :param end: short date str
    :return:
    '''
    ff = [f for f in os.listdir(path) if f.find(pattern) != -1]
    data = pd.DataFrame()
    for f in ff:
        res = pd.read_csv(path + '/' + f, dtype=dtype, index_col=0)
        data = data.append(res)
    if len(data) > 0:
        data = data.drop_duplicates()
        new = data.to_csv(path+pattern+'_new.csv')


def remove_files(path='.', pattern='', exclude = None):
    ff = [f for f in os.listdir(path) if f.find(pattern) != -1]
    saves = [f for f in os.listdir(path) if f.find(exclude) != -1]
    for f in ff:
        if f not in saves:
            print('remove file ', f)
            os.remove(path + '/' + f)

merge_data_files('/Users/chenay/pyt/FinanceReportAnalysis/', 'finance_statement', dtype={'SECCODE':str})
nothing()
remove_files('/Users/chenay/pyt/FinanceReportAnalysis/','finance_statement','overview')
