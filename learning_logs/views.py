from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .models import Topic, Entry
from .forms import CommentForm, TopicForm, EntryForm

def index(request):
    """the home page for learning log"""
    return render(request, 'learning_logs/index.html')


def topics(request):
    """show all topics"""
    if request.user.is_authenticated:
        topics = Topic.objects.filter(owner=request.user)\
                            .order_by('date_added')
        public_topics = Topic.objects.filter(public=True)
        
        context = {'topics': topics, 'public_topics': public_topics}
        return render(request, 'learning_logs/topics.html', context)
    else:
        public_topics = Topic.objects.filter(public=True)
        context = {'public_topics': public_topics}
        return render(request, 'learning_logs/topics.html', context)



def topic(request, topic_id):
    """shows the entries for single topic selected"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    entries = topic.entries.order_by('-date_added')
    comments = topic.comments.order_by('-date_added')
    paginator = Paginator(entries, 3)
    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)
    
    context = {'page': page, 'topic': topic, 'entries': entries, 
               'comments': comments}
    return render(request, 'learning_logs/topic.html', context)



@login_required
def new_topic(request):
    """users can add a new topic"""
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def delete_topic(request, topic_id):
    """delete a topic from my topics"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)
    if request.method != request.POST:
        topic.delete()
        return redirect('learning_logs:topics')



@login_required
def new_entry(request, topic_id):
    """users can add new entry to already made topic"""
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(topic, request)

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            messages.success(request, 'You just made a new entry!')
            return redirect('learning_logs:topic', topic_id=topic_id)
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """edit an entry made previously"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_topic_owner(topic, request)

    if request.method != "POST":
        form = EntryForm(instance=entry)

    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id = topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)


@login_required
def topic_comment(request, topic_id):
    """allows users to make a comment on a topic"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = CommentForm()
    else:
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.topic = topic
            new_comment.owner = request.user
            new_comment.save()
            return redirect('learning_logs:topics')
    
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/comment.html', context)

@login_required
def entry_comment(request, entry_id):
    """leave a comment on an entry"""
    






#functions made by me

def check_topic_owner(topic, request):
    """if current user is not the owner of the entry raise 404 error"""
    if topic.owner != request.user:
        raise Http404
    





