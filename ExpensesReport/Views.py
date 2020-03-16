from django.http import HttpResponse

def welcome(request):
    return HttpResponse('anything')
def startpage(requ):
    return HttpResponse("")