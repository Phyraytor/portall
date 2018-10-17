
from django.shortcuts import render, render_to_response

from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry, User
from .forms import TopicForm, EntryForm


# Create your views here.

def index(request):
	"""Home page application Learning Log"""
	return render(request, 'learning_logs/index.html')

 #так видит только владелец статьи
@login_required
def account(request):
	"""show list topic"""
	topic = Topic.objects.first()
	entries = Entry.objects.filter(owner=request.user) 
	context = {'topics': topic, 'entries': entries}
	return render(request, 'learning_logs/account.html', context)

def accounts(request, account_id):
	"""show list topic"""
	topic = Topic.objects.first()
	user = User.objects.filter(id=account_id)
	entries = Entry.objects.filter(owner=user) 
	context = {'topics': topic, 'entries': entries, 'the_user': user}
	return render(request, 'learning_logs/accounts.html', context)

def topics(request):
	"""show list topic"""
	topics = Topic.objects.order_by('date_added')
	context = {'topics': topics}
	return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
	"""show this topic and his text"""
	topic = Topic.objects.get(id=topic_id)
	#Проверка того, что тема принадлежит текущему пользователю. 
	#if topic.owner != request.user:
		#raise Http4
	products = topic.entry_set.all() #order_by('-date_added')
	context = {'topic': topic, 'products': products}
	return render(request, 'learning_logs/topic.html', context)

def product(request, product_id):
	"""show this product and his text"""
	obj_product = Entry.objects.get(id=product_id)
	context = {'product': obj_product}
	return render(request, 'learning_logs/product.html', context)

@login_required
def new_topic(request):
	"""Определяет новую тему"""
	if request.method != 'POST':
		# Data not send, create empty form
		form = TopicForm()
	else:
		#Data send; tread data
		form = TopicForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect( reverse('learning_logs:topics') )

	context = {'form': form}	
	return render(request, 'learning_logs/new_topic.html', context)

@login_required	
def new_entry(request):
	"""Определяет новое сообщение"""
	topic = Topic.objects.get(id=1)
	if request.method != 'POST':
		#Data not send, create empty form
		form = EntryForm()
	else:
		#Data send; tread data
		form = EntryForm(request.POST, request.FILES)
		if form.is_valid():
			new_enrty = form.save(commit=False)
			new_enrty.topic = topic
			new_enrty.owner = request.user
			new_enrty.save()
			return HttpResponseRedirect( reverse('learning_logs:account') )
	context = {'topic': topic, 'form': form}
	return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	"""Определяет новое сообщение"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if entry.owner != request.user:
		raise Http404
	if request.method != 'POST':
		#Data not send, create empty form
		form = EntryForm(instance=entry)
	else:
		#Data send; tread data
		form = EntryForm(request.POST, request.FILES, instance=entry)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect( reverse('learning_logs:account') )
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)	