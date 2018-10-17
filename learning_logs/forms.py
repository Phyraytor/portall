from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['text']
		labels = {'text': ''}


class EntryForm(forms.ModelForm):
	#file = forms.ImageField()
	class Meta:
		model = Entry
		fields = ['name', 'price', 'text', 'file']
		labels = {'text': ''}
		
		widgets = {
			'name': forms.TextInput(),
			'price': forms.NumberInput(),
			'text': forms.Textarea( attrs={'cols': 80} ), 
		}