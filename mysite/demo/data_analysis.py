from models import Item
import datetime

def analysis1(company_name):
	item_list=Item.objects.fiter(company=company_name)
	


def analysis2(begin_year,begin_month,begin_data,end_year,end_month,end_year):
	start_date=datetime.date(begin_year,begin_month,begin_data)
	end_date=datetime.date(end_year,end_month,end_date)
	item_list=Item.objects.filter(time__range=(start_date,end_date))

