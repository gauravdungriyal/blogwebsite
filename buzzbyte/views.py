import markdown2
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from datetime import date
from django.contrib.auth.models import User
from google import genai
from google.genai import types
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
class NewBlogForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Title',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-auto rounded-xl '
                     'text-[#131416] focus:outline-0 focus:ring-0 border border-[#dee0e3] bg-white '
                     'focus:border-[#dee0e3] h-14 placeholder:text-[#6c757f] p-[15px] text-base font-normal leading-normal'
        })
    )
    imgurl = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Imgage URL',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-auto rounded-xl '
                     'text-[#131416] focus:outline-0 focus:ring-0 border border-[#dee0e3] bg-white '
                     'focus:border-[#dee0e3] h-14 placeholder:text-[#6c757f] p-[15px] text-base font-normal leading-normal'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Description',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-auto rounded-xl '
                     'text-[#131416] focus:outline-0 focus:ring-0 border border-[#dee0e3] bg-white '
                     'focus:border-[#dee0e3] min-h-20 max-h-36 placeholder:text-[#6c757f] p-[15px] text-base font-normal leading-normal'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Tell your story...',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-auto rounded-xl '
                     'text-[#131416] focus:outline-0 focus:ring-0 border border-[#dee0e3] bg-white '
                     'focus:border-[#dee0e3] min-h-36 placeholder:text-[#6c757f] p-[15px] text-base font-normal leading-normal'
        })
    )

    category = forms.ChoiceField(
        choices=[('', 'Select a category'), ('Meditation', 'Meditation'), ('Self-Improvement', 'Self-Improvement'),('Relationships','Relationships'),('Technology','Technology'),('Lifestyle','Lifestyle'),('Business','Business')],
        widget=forms.Select(attrs={
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-auto rounded-xl '
                     'text-[#131416] focus:outline-0 focus:ring-0 border border-[#dee0e3] bg-white '
                     'focus:border-[#dee0e3] h-14 placeholder:text-[#6c757f] p-[15px] text-base font-normal leading-normal'
        })
    )

    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Add tags (comma-separated)',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl '
                     'text-[#131416] focus:outline-0 focus:ring-0 border border-[#dee0e3] bg-white '
                     'focus:border-[#dee0e3] h-14 placeholder:text-[#6c757f] p-[15px] text-base font-normal leading-normal'
        })
    )
class NewCommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Add a comment...',
            'class': 'form-input flex w-full min-w-0 flex-1 resize-none overflow-auto rounded-xl '
                     'text-[#131416] focus:outline-0 focus:ring-0 border border-[#dee0e3] bg-white '
                     'focus:border-[#dee0e3] min-h-20 max-h-36 placeholder:text-[#6c757f] p-[15px] text-base font-normal leading-normal'
        })
    )

def index(request):
    all_categories=['Meditation','Self-Improvement','Relationships','Technology','Lifestyle','Business']
    return render(request,'buzzbyte/index.html',{
        "blogs":Blog.objects.all(),
        "all_categories":all_categories
    })
def writeblog(request):
    if request.method == "POST":
        form = NewBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            content = form.cleaned_data['content']
            client = genai.Client(api_key="AIzaSyC8kBwuF_s5Z-UfoE0ZvJdpLVjki6pMRFc")

# Make a request to the model
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                system_instruction="""
You are a Markdown formatter. Your job is to convert raw, unstructured or semi-structured text into clean, properly formatted Markdown.

Follow these rules:
1. Use **#** for H1 headings (main titles), **##** for H2, and **###** for H3 subheadings.
2. Bold important labels, keywords, and section titles using **double asterisks**.
3. Use bullet points for lists. Use sub-bullets if needed.
4. Use proper line breaks and spacing to improve readability.
5. Convert numbered instructions into Markdown numbered lists.
6. Use code blocks (```) for any code or terminal commands.
7. Don't include any explanation — only return the formatted Markdown.

Example:
Raw Input:
"Title: Setup Guide
Steps:
1. Install Python
2. Run the script
Note: Ensure Python 3.8+ is installed."

Expected Markdown Output:
# Setup Guide

## Steps

1. **Install Python**
2. **Run the script**

**Note:** Ensure Python 3.8+ is installed.
"""),
                contents=content
)
            content = response.text
            category = form.cleaned_data['category']
            tags = form.cleaned_data['tags']
            imgurl=form.cleaned_data['imgurl']
            authname=request.user.username.title()
            f=Blog(title=title,description=description,content=content,tags=tags,category=category,imgurl=imgurl,authname=authname)
            f.save()
            return HttpResponseRedirect(reverse('index'))
    return render(request,'buzzbyte/writeblog.html',{
        "form":NewBlogForm()
    })
def article(request,id):
    tag_string = Blog.objects.get(id=id).tags
    taglist = tag_string.replace(' ', '').split(',')
    return render(request,'buzzbyte/article.html',{
        'content':markdown2.markdown(Blog.objects.get(id=id).content),
        'title':Blog.objects.get(id=id).title,
        'description':Blog.objects.get(id=id).description,
        'tags':taglist,
        'category':Blog.objects.get(id=id).category,
        'imgurl':Blog.objects.get(id=id).imgurl,
        'authname':Blog.objects.get(id=id).authname,
        'date':Blog.objects.get(id=id).date,
        'id':Blog.objects.get(id=id).id,
        'comments': Blog.objects.get(id=id).comments.all(),
    })

def  login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        if username == "" or password == "":
            return render(request, "buzzbyte/login.html", {
                "message": "Username and password cannot be empty."
            })
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "buzzbyte/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "buzzbyte/login.html")
        
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if username == "" or email == "" or password == "" or confirmation == "":
            return render(request, "buzzbyte/register.html", {
                "message": "All fields are required."
            })
        if password!=confirmation:
            return render(request, "buzzbyte/register.html", {
                "message": "Passwords must match."
            })
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"),{
            "user":request.user
        })
    else:
        return render(request, "buzzbyte/register.html")

def category(request,category):
        return render(request, "buzzbyte/index.html",{
        "blogs": Blog.objects.filter(category=category),
        "all_categories": ['Meditation', 'Self-Improvement', 'Relationships', 'Technology', 'Lifestyle', 'Business']
    })

def comment(request):
    if request.method == "POST":
            content = request.POST['comment']
            blog_id=request.POST['blog_id']
            if not content or not blog_id:
                return HttpResponse("Content and blog ID are required.")
            blog = Blog.objects.get(id=blog_id)
            comment = Comment(content=content, blog=blog, user=request.user,date=date.today())
            comment.save()
            return HttpResponseRedirect(reverse('article', args=[blog_id]))
    return HttpResponse("Invalid request method.")

def search(request):
   if request.method == "POST":
       blog=Blog.objects.all()
       blog_list=[]
       query=request.POST['search']
       for b in blog:
           lower_title = b.title.lower()
           lower_query = query.lower()
           if lower_query in lower_title:
               blog_list.append(b)
       return render(request,'buzzbyte/index.html',{
              "blogs": blog_list,
              "all_categories": ['Meditation', 'Self-Improvement', 'Relationships', 'Technology', 'Lifestyle', 'Business']
       })
   
def delete(request,id):
    blog=Blog.objects.get(id=id)
    blog.delete()
    return HttpResponseRedirect(reverse('index'))