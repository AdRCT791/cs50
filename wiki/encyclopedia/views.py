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

#Entry View function. 

def entry(request, title):
    entry_content = (util.get_entry(title))

    #check if the query requested by the user exist. If not the user is presented with an error message
    if entry_content is None or entry_content == "":
        return render (request, "encyclopedia/404.html", {
            "message": "The requested page was not found."
        })
    else:
        entry_content_markdown = markdown2.markdown(entry_content)
        return render(request, "encyclopedia/entry.html", {    
        "entry": entry_content_markdown,
        "title": title
        })  

#Random View function. 
def random_page(request):
    random_entry = random.choice(util.list_entries())
    return redirect (f"/wiki/{random_entry}", {
    })

#Add New Page view function
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

#Edit page view function
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

#Search Query
def search(request):

    return render(request, "encyclopedia/search.html")
