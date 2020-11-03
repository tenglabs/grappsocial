from django import forms
from .models import Post,Comment
from django.forms import Textarea
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible

class CreatePost(forms.ModelForm):
	captcha = ReCaptchaField(widget=ReCaptchaV2Invisible,label='')
	class Meta:
		model = Post
		fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': Textarea(attrs={ 'rows': 7,'placeholder': 'Type your comment here...'}),
        }



		