from django import forms
from links.models import Link, Comment

class LinkSubmissionForm(forms.ModelForm):
    class Meta():
        model = Link
        fields = ['title', 'url']

class CommentModelForm(forms.ModelForm):
    link_pk = forms.IntegerField(widget=forms.HiddenInput)
    parent_comment_pk = forms.IntegerField(widget=forms.HiddenInput, required=False)
    class Meta():
        model = Comment
        fields = ['body']
