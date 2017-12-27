from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def my_paginator(list_obj, page, page_number):
	if page_number:
		page_number = int(page_number)
	else:
		page_number = 10
	paginator = Paginator(list_obj, page_number)
	try:
		ret = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		ret = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		ret = paginator.page(paginator.num_pages)
	return paginator.count, ret.object_list