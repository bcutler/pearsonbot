# Create your views here.
from pprint import pformat
from django.shortcuts import get_object_or_404, render_to_response
from helpers import get_contingency_table, chisq_test, get_group_names

def index(request):
	return render_to_response('contingency/index.html', {'groups':get_group_names()})

def compare_with(request):
	term1 = request.GET.get('term1')
	term2 = request.GET.get('term2')
	#print term1, term2
	table = get_contingency_table(term1,term2)
	#statistic = chisq_test(table)
	
	table = pformat(table)
	
	return render_to_response('contingency/compare.html', {
		'table': table,
		"groups": get_group_names()
	})
