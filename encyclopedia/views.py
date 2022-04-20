from django.shortcuts import render
from django.utils.safestring import mark_safe
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from . import util

import markdown
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="title search")

def index(request):
    dict = request.GET
    if dict:
        title = dict['q']
        if title in util.list_entries():
            page = util.get_entry(title)
            html = mark_safe(markdown.markdown(page))
            return render(request, "encyclopedia/page.html", {
            "page": html,
            "title": title,
            "request": request,
            })    
        else: 
            related = []
            for entry in util.list_entries():
                if title in entry:
                    related.append(entry)
            return render(request, "encyclopedia/index.html", {
                "entries": related
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    page = util.get_entry(title)
    html = mark_safe(markdown.markdown(page))
    if page is None:
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/page.html", {
        "page": html,
        "title": title,
        "request": request,
    })

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        page = request.POST["content"]
        if title in util.list_entries():
            return render(request, "encyclopedia/error_duplicate.html")
        else:
            util.save_entry(title, page)
            return render(request, "encyclopedia/page.html", {
                "page": mark_safe(markdown.markdown(page)),
                "title": title,
                "request": request,
            })
    return render(request, "encyclopedia/create.html")

def edit(request):
    if request.method == "GET":
        values = request.GET
        title = values["title"]
        page = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": page
        })
    elif request.method == "POST":
        title = request.POST["title"]
        page = request.POST["content"]
        util.save_entry(title, page)
        return render(request, "encyclopedia/page.html", {
            "page": mark_safe(markdown.markdown(page)),
            "title": title,
            "request": request,
        })
    return render(request, "encyclopedia/error.html")

def randomPage(request):
    entries = util.list_entries()
    title = random.choice(entries)
    page = util.get_entry(title)
    html = mark_safe(markdown.markdown(page))
    if page is None:
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/page.html", {
        "page": html,
        "title": title,
        "request": request,
    })
