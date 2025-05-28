from django.shortcuts import render, redirect
from .models import Carpet, CustomerComment
from .forms import CustomerCommentForm
from django.http import HttpResponse
from django.contrib import messages


def comments_view(request):
    comments = CustomerComment.objects.filter(approved=True).order_by('-created_at')
    form = CustomerCommentForm()

    if request.method == 'POST':
        form = CustomerCommentForm(request.POST)
        if form.is_valid():
            form.save()

            
            messages.success(request, "Yorumunuz onaya gönderilmiştir.")

            
            return redirect('comments')  

    return render(request, 'web/comments.html', {'comments': comments, 'form': form})
