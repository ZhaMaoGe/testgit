#coding:utf8
from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class person(models.Model):
	user_name=models.CharField(u'用户名',max_length=100)
	password=models.CharField(u'密码',max_length=100)
	email=models.CharField(u'邮箱',max_length=20)
	def __str__(self):
		return self.user_name
@python_2_unicode_compatible
class Item(models.Model):
	name=models.CharField(u'项目名称',max_length=100)
	time=models.CharField(u'中标时间',max_length=40)
	company=models.CharField(u'中标公司',max_length=100)
	money=models.FloatField(u'中标金额')
	def __str__(self):
		return self.name
@python_2_unicode_compatible
class Web(models.Model):
	webAddr=models.CharField(max_length=100)
	def __str__(self):
		return self.webAddr