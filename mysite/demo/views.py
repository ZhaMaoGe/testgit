#-*-coding:utf8-*-
from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from models import person,Web,Item
from forms import WebForm
import sys
import province
import data_analysis

import verifycode
# Create your views here.
reload(sys)
sys.setdefaultencoding('utf8')

#登陆界面函数
def index(request,num=0):
	request.session.set_test_cookie()
	if(request.session.test_cookie_worked()):
		request.session.delete_test_cookie()
		request.session['verifycode']=verifycode.photo_create()
		request.session.set_expiry(0)
		dic={0:u'账户',1:u'账号信息错误',2:u'验证码错误',3:u'用户未登录'}
		return render(request,'demo\index.html',{'account':dic[num]})
	else: 
		return HttpResponse('please enable the cookie')

#提交登录表单时的函数
def login(request):
	if(request.method=="POST"):
		#验证码是否正确
		if(request.session['verifycode']==request.POST['verifycode']):
			user=person.objects.filter(user_name=request.POST['username'])
			#用户名与密码是否正确
			if(user and user[0].password==request.POST['password']):
				request.session['username']=user[0].user_name
				request.session['password']=user[0].password
				#redirect到系统界面
				return redirect('demo:system')
			else:
				return index(request,1)
		else:
			return index(request,2)
	else:
		return redirect('demo:index')

#进入系统管理界面
def system(request):
	if(request.session.get('username')):
		username=request.session['username']
		return render(request,'demo\system.html',{'username':username,'adminurl':"http://localhost:8000/admin"})
	else:
		return index(request,3)
def logout(request):
	if(request.session.get('username')):
		request.session.flush()
		return render(request,'demo\logout.html')
	else:
		return redirect('demo:index')

#进度条函数
begin_crap=0#是否开始抓取,初始化进度条,0为开始 1开始 2结束
web=''
def craptimer(request):
	global timer,web
	if(begin_crap==0):
		return HttpResponse('grap not begin')
	elif(begin_crap==2):
		return HttpResponse('grap end,some web can not be grapped')
	else:	
		return render(request,'demo\craptimer.html',{'website':web,'x':int(province.per)})
#网页抓取函数
web_to_crapper=[]
def crap(request):
	global web_to_crapper,begin_crap
	begin_crap=0
	province.per=0.0
	if(request.session.get('username')):
		username=request.session['username']
		if(request.method=="GET"):
			website_list=Web.objects.all()#数据库内存入的网址
			return render(request,'demo\webcrap.html',{'status1':'block','status2':'none','website_list':website_list})
		elif(request.method=="POST"):
			web_key=request.POST.get('web_to_crapper',0)
			if(web_key==0):
				pass
			else:
				web_to_crapper=web_key.split('*')
				print web_to_crapper
				return render(request,'demo\webcrap.html',{'status1':'none','status2':'block','website_list':[]})
			#province.Page()
	else:
		return index(request,3)
#因为要先把进度条显示出来才能抓取，所以又定义了此函数，开始抓取
website_dict={'http://clkg.gzcz.gov.cn/home/list-1153531755759540.html':province.Page,}
def crap_begin(request):
	province.per=0.0
	global web,web_to_crapper,begin_crap
	web=""
	begin_crap=1
	print "begin"
	for web_temp in web_to_crapper:
		if website_dict.get(web_temp):
			web=web_temp
			website_dict[web_temp]()
	begin_crap=2
	province.per=0.0
	return render(request,'demo\webcrap.html',{'status1':'none','status2':'block','website_list':[]})

def upweb(request):
	if request.method =='POST':
		if 'sub' in request.POST:
			wf = WebForm(request.POST,request.FILES)
			
			if wf.is_valid():
				destination = open('demo/upload/webfile.txt', 'wb+')
				f = request.FILES['webfile']
				for chunk in f.chunks():
					destination.write(chunk)
				destination.close()
				webfp = open("demo/upload/webfile.txt",'r')
				webAddr = webfp.readlines()
				return render(request,'demo/website.html',{'objects': webAddr})

		else:
				key=request.POST.get('webaddr')
				st=""
				for ch in key:
					if ch=='*':
						Web.objects.create(webAddr=st)
						st=""
					else:
						st=st+ch
				return redirect('demo:upweb')

	else:
		wf = WebForm()
	return render(request,'demo/website.html',{})


def query(request):
	if(request.session.get('username')):
		if (request.method=='POST'):
			way_list=request.POST.getlist('way')
			result=Item.objects.all()
			for way in way_list:
				if(way=='name'):
					result=result.filter(name=request.POST.get('name',''))
				if(way=='company'):
					result=result.filter(company=request.POST.get('company',''))
				if(way=='time'):
					result=result.filter(time__range=(request.POST.get('data_begin',''),request.POST.get('data_end','')))
				if(way=='money'):
					result=result.filter(money__range=(request.POST.get('money_begin',''),request.POST.get('money_end','')))
			return render(request,'demo/dataquery.html',{'table_list':result,'status1':'block'})
		else:
			return render(request,'demo/dataquery.html',{'table_list':[],'status1':'none'})
	else:
		return index(request,3)


#数据分析函数
def analysis(request):
	if(request.session.get('username')):
		if(request.method=="POST"):
			if(request.POST.get('name')):
				t=request.POST.get('name')
				#data_analysis.analysis1(t)
				data_analysis.analysis2(t)
				return render(request,'demo/data_analysis.html',{'dict_list':{}})
			elif(request.POST.get('time_begin')):
				dic={}
				Item_list=Item.objects.filter(time__range=(request.POST.get('time_begin',''),request.POST.get('time_end','')))
				for i in Item_list:
					if(not dic.get(i.company)):
						dic[i.company]=i.money
					else:
						dic[i.company]=dic[i.company]+i.money
				return render(request,'demo/data_analysis.html',{'dict_list':dic})
			else:
				return render(request,'demo/data_analysis.html',{'dict_list':{}})
		else:
			return render(request,'demo/data_analysis.html',{'dict_list':{}})
	else:
		return index(request,3)