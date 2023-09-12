from django import forms
from .models import Topic, Entry, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text', 'public']
        labels = {'text': 'topic', 'public': 'public'}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


class CommentForm(forms.ModelForm):
    """form for a comment on a topic"""
    class Meta:
        model = Comment
        fields = ['comment', ]
        labels = {'comment': ''}
        widgets = {'comment': forms.Textarea(attrs={'cols': 80})}









































