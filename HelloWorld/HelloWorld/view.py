from django.shortcuts import render


def hello(request):
    context = {'name': "i am s", 'contry': "i am from china"}
    return render(request, "hello.html", context)

