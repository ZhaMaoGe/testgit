#-*-coding:utf8-*-
from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import json
import sys
import re
import string
from models import Item
valid=1
invalid=0
HomeUrl="http://clkg.gzcz.gov.cn"
url="http://clkg.gzcz.gov.cn/home/list-1153531755759540.html"
num=0
per=0.0
Page_amount=10
def Count():
    global num
    num=num+1


def Spider(url):
    html=requests.get(url)
    root=etree.HTML(html.text)
    ul_content=root.xpath('//div[@id="info"]/ul')[0]

    str=u'项目名称'
    span=ul_content.xpath('//li/span[contains(text(),"%s")]'%str)[0]
    list=span.xpath('../text()')
    name=''.join(list).replace('\n','').replace('\t','').replace(' ','').replace('\r','')

    str=u'评审时间'
    span=ul_content.xpath('//li/span[contains(text(),"%s")]'%str)[0]
    list=span.xpath('../text()')
    time=''.join(list).replace('\n','').replace('\t','').replace(' ','').replace('\r','')

    str=u'中标（成交）信息'
    span=ul_content.xpath('//li/span[contains(text(),"%s")]'%str)[0]
    tr_list=span.xpath('../ul/table[@id="tabrow"]/tbody/tr')
    company_list=[]
    money_list=[]
    flag=valid
    for tr_num in range(len(tr_list)):
        temp=tr_list[tr_num].xpath('.//td//text()')
        if len(temp)<2:
            flag=invalid
            break
        company=temp[1]
        money=tr_list[tr_num].xpath('./td[@id="turnoverAmount"]/text()')
        if not len(money)==1:
            flag=invalid
        else:
            money_list.append(money[0].replace('\n','').replace('\t','').replace(' ','').replace('\r',''))
            flag=valid
        company_list.append(company.replace('\n','').replace('\t','').replace(' ','').replace('\r',''))
    if not len(company_list) == len(money_list):
        flag=invalid
    if flag==valid:
        for i in range(len(company_list)):
            #item={'name':name,'time':time,'company':company_list[i],'money':money_list[i]}
            newItem=Item(name=name,time=time,company=company_list[i],money=money_list[i])
            newItem.save()

def Divide(url):
    global num,Page_amount,per
    Count()
    temp=float(num)/float(Page_amount)
    per=temp*100.0
    html=requests.get(url)
    root = etree.HTML(html.text)
    li_list=root.xpath('//div[@class="xnrx"]/ul/li/a/@href')
    #name=root.xpath('//div[@class="xnrx"]/ul/li/a/text()')
    for i in range(len(li_list)):
        li_url=HomeUrl+li_list[i]
        Spider(li_url)


#构建UrlList(每一页)
def Page():
    global Page_amount
    #求页数
    html=requests.get(url).text
    root=etree.HTML(html)
    li_list=root.xpath('//body//div//div[@class="body"]//div[@class="you"]//div[@class="page"]/ul/li')


    #倒数第三个是最终页页码
    li=li_list[len(li_list)-3]
    Page_amount=string.atoi(li.xpath('./a/text()')[0])


    Page_size=15
    url_current=url+'?pageNo=1&pageSize=15'
    UrlList=[]
    for Page_num in range(1,Page_amount+1):
        CurrentUrl = re.sub('pageNo=\d+','pageNo=%d'%Page_num,url_current,re.S)
        UrlList.append(CurrentUrl)
    pool = ThreadPool(4)
    pool.map(Divide, UrlList)
    pool.close()
    pool.join()
    # for i in range(Page_amount):
    #     Divide(UrlList[i])
    

