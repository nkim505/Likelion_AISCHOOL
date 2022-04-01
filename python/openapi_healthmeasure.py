# '서울올림픽기념국민체육진흥공단_국민체력100 체력인증센터 측정결과 정보'
# https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15004104

import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

def callAPI(service_key,pageNo,numOfRows,testYm):
  """callAPI(서비스키, 페이지 번호, 한 페이지 결과 수, 측정년월)"""
    base_url = 'http://www.kspo.or.kr/openapi/service/nfaTestInfoService/getNfaTestRsltList'
    
    url = base_url + '?' + 'serviceKey=' + service_key + '&pageNo=' + pageNo +\
    '&numOfRows=' + numOfRows + '&testYm=' + testYm
    
    return url

service_key = '******************' # service key 입력

years = ['2018','2019','2020', '2021']

before_covid = ['2018', '2019']
after_covid = ['2020', '2021']

months = ['01','02','03','04','05','06','07','08','09','10','11','12']
short_months = ['01','02','03']

nums = ['09','10','12','13','14','15','16','17',
        '19','20','21','22','23','24','25',
        '26','27','30','31','32','33','34','35',
       '36','37','40','41']



#먼저 모든 달의 df을 합칠 빈 데이터프레임 'df_beforecovid','df_aftercovid' 생성

df_beforecovid = pd.DataFrame()        
df_aftercovid = pd.DataFrame()        

for year in years:
    
    if year in before_covid:
        df_beforecovid = pd.DataFrame()        
        for month in short_months:

            # 2020년의 한개 달(ex.202001)의 api를 호출함.
            print("=========")
            url = callAPI(service_key,'1','10000','{}{}'.format(year, month))
            print('getting maximum 10,000 data from {}{}'.format(year, month))
            #print(url)
            response = requests.get(url)
            print(response)
            response = requests.get(url).content
            soup = BeautifulSoup(response, 'lxml-xml')
            #print(soup)
            print('the total rows of {}{}: '.format(year, month),len(soup.find_all('item')))
            
            time.sleep(2)

            #soup에서 item 태그만 찾아서 하나의 list로 저장(index마다 1인의 측정값들 내재)
            items = soup.find_all('item')

            #items 내의 element들을 dictionary형태로 바꾸고 이를 다시 리스트로 묶어준 dict_list 생성
            dict_list = []
            for item in items:
                temp_dict = {}
                for num in nums:
                    try:
                        temp_dict['F0{}'.format(num)] = item.find('itemF0{}'.format(num)).get_text()
                    except:
                        pass
                dict_list.append(temp_dict)

            #2020년 01년의 각 element가 dict로 이루어진 dict_list를 그대로 dataframe으로 만들어주기    
            temp = pd.DataFrame.from_dict(dict_list)

            #2020년 01년 자료로 만든 df를 전체 df_yrs와 합치기
            df_beforecovid = pd.concat([df_beforecovid, temp])
            print("successfully concatenated with 'df_beforecovid'")

    elif year in after_covid:
        for month in short_months:

            # 2020년의 한개 달(ex.202001)의 api를 호출함.
            print("=========")
            url = callAPI(service_key,'1','10000','{}{}'.format(year, month))
            print('getting maximum 10,000 data from {}{}'.format(year, month))
            #print(url)
            response = requests.get(url)
            print(response)
            response = requests.get(url).content
            soup = BeautifulSoup(response, 'lxml-xml')
            #print(soup)
            print('the total rows of {}{}: '.format(year, month),len(soup.find_all('item')))

            time.sleep(2)


            #soup에서 item 태그만 찾아서 하나의 list로 저장(index마다 1인의 측정값들 내재)
            items = soup.find_all('item')

            #items 내의 element들을 dictionary형태로 바꾸고 이를 다시 리스트로 묶어준 dict_list 생성
            dict_list = []
            for item in items:
                temp_dict = {}
                for num in nums:
                    try:
                        temp_dict['F0{}'.format(num)] = item.find('itemF0{}'.format(num)).get_text()
                    except:
                        pass
                dict_list.append(temp_dict)

            #2020년 01년의 각 element가 dict로 이루어진 dict_list를 그대로 dataframe으로 만들어주기    
            temp = pd.DataFrame.from_dict(dict_list)

            #2020년 01년 자료로 만든 df를 전체 df_yrs와 합치기
            df_aftercovid = pd.concat([df_aftercovid, temp])
            print("successfully concatenated with 'df_aftercovid'")
