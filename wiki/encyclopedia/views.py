from turtle import title
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django import forms

import re
import markdown2
import random

from . import util



#Complementary functions

def error(request, message):
    return render(request, "encyclopedia/error.html", {
        "message": message
    })

#Main views
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    new_entry = util.get_entry(entry)
    if new_entry == None:
        return error(request, "404! The entry page is not found")
    else:
        new_html = markdown2.markdown(new_entry)
        return render(request, "encyclopedia/entry.html", {
            "new_html": new_html,
            "entry": entry
        })

#Search form class
class NewForm(forms.Form):
    #<input class="search" type="text" name="q" placeholder="Search Encyclopedia">
    search_entry = forms.CharField(label="Search Encyclopedia", widget=forms.TextInput(attrs={'class': 'search'}))

def search(request):
    if request.method == "POST":
        search_entry = "None"
        form = NewForm(request.POST)
        if form.is_valid():
            search_entry = form.cleaned_data["search_entry"]
            entries = util.list_entries()
            if search_entry in entries:
                return(entry(request, search_entry))
            else:
                relevant = []
                for new_entry in entries:
                    if re.search(search_entry, new_entry):
                        relevant.append(new_entry)
                return render(request, "encyclopedia/search.html", {
                    "relevant": relevant
                })

#Form for data entry
class EntryForm(forms.Form):
    entry_title = forms.CharField(label = mark_safe("<p> Title: </p>"), label_suffix= "")
    content = forms.CharField(widget=forms.Textarea, label = mark_safe("<p> Content: </p>"), label_suffix="")

def new(request):
    return render(request, "encyclopedia/new.html", {
        "new_form": EntryForm()
    })

def new_result(request):
    if request.method == "POST":
        new_form = EntryForm(request.POST)
        if new_form.is_valid():
            title = new_form.cleaned_data["entry_title"]
            content = new_form.cleaned_data["content"]
            if title.capitalize() in util.list_entries():
                return error(request, "The title already exists")
            else:
                util.save_entry(title.capitalize(), content)
                return entry(request, title.capitalize())

#Edit form class
class edit_form(forms.Form):
    content = forms.CharField(label = mark_safe("<p> Content: </p>"), label_suffix="", widget = forms.Textarea)
    previous = forms.CharField(widget = forms.HiddenInput(), required=False)
       
        

def edit(request):
    if request.method == "GET":
        matches = re.search("wiki/(.+)", str(request.META.get("HTTP_REFERER")))
        title = matches.group(1)
        c_entry = util.get_entry(title)
        new_form = edit_form(initial={"content": c_entry, "previous": title})
        return render(request, "encyclopedia/edit.html", {
            "edit_form": new_form
        })
    elif request.method == "POST":
        form = edit_form(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            title = form.cleaned_data["previous"]
            util.save_entry(title, content)
        return entry(request, title)


def random_entry(request):
    entries = util.list_entries()
    new = random.choice(entries)
    return entry(request, new)
    
        
    
            