from django import forms
from .models import Post, Comment


class PostWriteUpdateForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ['body']


class CommentWriteForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }


class ReplyWriteForm(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }


class PostSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))