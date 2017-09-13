from django.http import HttpResponse

def root_page(request):
	return HttpResponse("Root page of bbox")