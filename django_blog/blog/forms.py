from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your post content here...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('Title must be at least 5 characters long.')
        return title
    
    def clean_content(self):
        content = self.cleaned_data['content']
        if len(content) < 20:
            raise forms.ValidationError('Content must be at least 20 characters long.')
        return content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'guest_name', 'guest_email']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
            'guest_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional for guests)'
            }),
            'guest_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your email (optional for guests)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.is_authenticated:
            # Hide guest fields for authenticated users
            self.fields.pop('guest_name', None)
            self.fields.pop('guest_email', None)
    
    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 5:
            raise forms.ValidationError('Comment must be at least 5 characters long.')
        return text