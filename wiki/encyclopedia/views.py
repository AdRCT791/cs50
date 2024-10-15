from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponseRedirect
import markdown2
import random
from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(label="Content", widget=forms.Textarea(), required=True)

class EditPageForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea(), required=True)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = markdown2.markdown(util.get_entry(title))
    if entry_content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested page was not found."
        })
    else:
        return render(request, "encyclopedia/entry.html", {
        "entry": entry_content,
        "title": title
        })  

def random_page(request):
    random_entry = random.choice(util.list_entries())
    
    return redirect (f"/wiki/{random_entry}", {
    })

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title.lower()) is not None:
                return render(request, "encyclopedia/new.html",{
                "form":form,
                "error_message": "An entry with this title already exists."
                })
            else:
                util.save_entry(title, content)

            return redirect(f"/wiki/{title}")
        else:
            return render(request, "encyclopedia/new.html",{
                "form":form
            })

    return render(request, "encyclopedia/new.html", {
         "form":NewPageForm()
         })

def edit_page(request, title):
    current_content = util.get_entry(title)

    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            util.save_entry(title, new_content)
            return redirect(f"/wiki/{title}")
    else:
        form = EditPageForm(initial={"content":current_content})

    return render(request, "encyclopedia/edit.html", {
        "form":form,
        "title":title
    })
