#-*-coding:utf8-*-
from django.shortcuts import render,redirect,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from models import person,Web
from forms import WebForm
import sys
import province

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
x=0
website=['hahaha','lalla']
web=''
website2=iter(website)
def craptimer(request):
	global x,website2,web
	if(x==0):
		web=website2.next()
	x=(x+20)%100
	if(web==website[-1] and x==0):
		website2=iter(website)
		return HttpResponse('grap end')
	return render(request,'demo\craptimer.html',{'website':web,'x':x})
def crap(request):
	province.Page()
	return HttpResponse("crap successfully")

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