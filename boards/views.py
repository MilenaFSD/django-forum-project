from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden

from .models import Board, Topic, Post


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            starter=request.user
        )

        Post.objects.create(
            message=message,
            topic=topic,
            created_by=request.user
        )

        return redirect('board_topics', pk=board.pk)

    return render(request, 'new_topic.html', {'board': board})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)

    if request.method == 'POST':
        message = request.POST.get('message')

        Post.objects.create(
            topic=topic,
            message=message,
            created_by=request.user
        )

        return redirect('topic_posts', pk=pk, topic_pk=topic_pk)

    return render(request, 'reply_topic.html', {'topic': topic})


@login_required
def edit_post(request, pk, topic_pk, post_pk):
    post = get_object_or_404(Post, pk=post_pk, topic__pk=topic_pk)

    if post.created_by != request.user:
        return HttpResponseForbidden()

    if request.method == 'POST':
        message = request.POST.get('message')
        post.message = message
        post.save()

        return redirect('topic_posts', pk=pk, topic_pk=topic_pk)

    return render(request, 'edit_post.html', {'post': post})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})