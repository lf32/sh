from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from .models import Urldb

base_url="http://url96.herokuapp.com/"

class URLform(forms.Form):
    url_str  = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'placeholder':'shortname', 'autocomplete':'false'}))
    long_url  = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder':'https://www.example.com/this-is-a-big-url', 'autocomplete':'false'}))


def indexpage(request):
    newform = URLform()
    if request.method == "POST":
        form = URLform(request.POST)
        if form.is_valid():
            urldb = Urldb()
            if ' ' in form.cleaned_data["url_str"] or ' ' in form.cleaned_data["long_url"] :
                message = "INPUT DATA SHOULD NOT HAVE SPACES!!!"
                return render(request, 'website/index.html', {
                    'message': message,
                    'form': form
                    })

            if len(Urldb.objects.filter(data_url_str=form.cleaned_data["url_str"])) == 0:
                urldb.data_url_str = form.cleaned_data["url_str"]
                urldb.data_long_url = form.cleaned_data["long_url"]
                urldb.save()
                new_url = base_url + form.cleaned_data["url_str"]
                message = "HERE IS YOUR NEW URL :) " + new_url
                return render(request, 'website/index.html', {
                    'message': message,
                    'form': newform
                    })
            else:
                message = "URL WITH NAME " + form.cleaned_data["url_str"] + " ALREADY EXITS!!!"
                return render(request, 'website/index.html', {
                    'message':message,
                    'form': form
                    })
        else:
            message = "THE FORM IS INVALID!!!"
            return render(request, 'website/index.html', {
                'message': message,
                'form': URLform()
                })
    return render(request, 'website/index.html', {
        'form': newform
        })


def urlpage(request, site_tag):
    urldb = Urldb()
    if len(Urldb.objects.filter(data_url_str=site_tag)) > 0:
        print(str(Urldb.objects.filter(data_url_str=site_tag)[0].data_long_url))
        return HttpResponseRedirect(str(Urldb.objects.filter(data_url_str=site_tag)[0].data_long_url))
    return HttpResponseRedirect("/")
