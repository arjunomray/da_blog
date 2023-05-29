from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, ContactForm
from django.http import HttpResponse


# Create your views here.
def post_list(request):
	posts =Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request,"blog/post_list.html", {'posts':posts})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email'],
                'message': form.cleaned_data['message'],
            }

            message = "\n".join(body.values())
            email = body['email']

            try:
                send_mail(subject, message, email, ['arjunomray@example.com'])
            except BadHeaderError:
                return HttpResponse("Invalid header found")
            return redirect('post_list')
    form = ContactForm()
    return render(request, "blog/contact.html", {"form":form})
def post_detail(request, pk):
	
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

