#encoding:utf8
import matplotlib
import string
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .models import Item
import datetime


def analysis2(company_name):
	item_list=Item.objects.filter(company=company_name).order_by('time')
	fig=plt.figure()
	ax=fig.add_subplot(111)
	times=[]
	moneys=[]
	for item in item_list:
	    Money=item.money
	    date=item.time
	    if(date in times):
	    	t=times.index(date)
	    	moneys[t]=moneys[t]+Money
	    else:
	    	times.append(date)
	    	moneys.append(Money)
	while(len(times)<4):
		times.append('xxxx-xx-xx')
		moneys.append(0)
	for i in range(len(times)):
		ax.bar(i,moneys[i],width=0.5)
	m=plt.xticks(range(len(times)),times)
	ax.set_xticklabels(times,rotation=90,size=8)
	plt.xlabel('date')
	plt.ylabel('money')
	plt.title('bar')
	fig.savefig("demo/static/demo/images/bar.png")




