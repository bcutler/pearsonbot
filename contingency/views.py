# Create your views here.
from pprint import pformat
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse

from helpers import *
import json

def index(request):
	return render_to_response('contingency/index.html', {'groups':get_group_names()})

def compare_with(request):
	term1 = request.GET.get('term1')
	term2 = request.GET.get('term2')
	#print term1, term2
	table = fetch_data(term1,term2)
	table = to_contingency_table(table)
	#table = get_protovis_treemap(term1, term2)
	print table
	#statistic = chisq_test(table)
	
	#table = pformat(table)
	#print table
	res = json.dumps(table)
	print res
	return HttpResponse(res, mimetype='text/javascript')
	