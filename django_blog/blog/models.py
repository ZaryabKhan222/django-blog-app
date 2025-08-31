from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class PublishedManager(models.Manager):
    """Custom manager to get only published posts"""
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publication_date')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    content = models.TextField()
    publication_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published'
    )
    
    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager
    
    class Meta:
        ordering = ['-publication_date']
        indexes = [
            models.Index(fields=['-publication_date']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                      args=[self.publication_date.year,
                            self.publication_date.month,
                            self.publication_date.day,
                            self.slug])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True,
        blank=True
    )
    guest_name = models.CharField(
        max_length=80,
        blank=True,
        help_text="Name for guest comments (if not logged in)"
    )
    guest_email = models.EmailField(
        blank=True,
        help_text="Email for guest comments (if not logged in)"
    )
    text = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_date']
        indexes = [
            models.Index(fields=['created_date']),
        ]
    
    def __str__(self):
        return f'Comment by {self.get_author_name()} on {self.post}'
    
    def get_author_name(self):
        if self.author:
            return self.author.username
        return self.guest_name or 'Anonymous'