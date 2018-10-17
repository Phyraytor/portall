
from django.shortcuts import render, render_to_response

from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry, User, Message, CommentProduct
from .forms import TopicForm, EntryForm, MessageForm, CommentProductForm


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
	# Если это личный кабинет текущего пользователя - перейти в его кабинет
	if int(account_id) == int(request.user.id)	:
		return HttpResponseRedirect( reverse('learning_logs:account') )
	topic = Topic.objects.first()	
	the_user = User.objects.get(id=account_id)
	entries = Entry.objects.filter(owner=the_user) 
	context = {'topics': topic, 'entries': entries, 'the_user': the_user}
	return render(request, 'learning_logs/accounts.html', context)

def messages(request):
	"""show list messages"""
	my_messages = Message.objects.filter(address_id=request.user.id)
	context = {'messages': my_messages}
	return render(request, 'learning_logs/messages.html', context) 

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
	comments = CommentProduct.objects.filter(product=obj_product)
	context = {'product': obj_product, 'comments': comments}
	return render(request, 'learning_logs/product.html', context)

@login_required
def send_message(request, address_id):
	""" Отправляет сообщение пользователю """
	if request.method != 'POST':
		# Data not send, create empty form
		form = MessageForm()
	else:
		#Data send; tread data
		form = MessageForm(request.POST)
		if form.is_valid():
			new_message = form.save(commit=False)
			new_message.address_id = address_id
			new_message.sender = request.user
			new_message.save()
			return HttpResponseRedirect( reverse('learning_logs:account'))
	context = {'form': form, 'address': address_id}
	return render(request, 'learning_logs/send_message.html', context)

@login_required
def comment_product(request, product_id):
	""" Оставить комментарий под товаром """
	if request.method != 'POST':
		# Data not send, create empty form
		form = CommentProductForm()
	else:
		#Data send; tread data
		form = CommentProductForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.product = Entry.objects.get(id=product_id)
			new_comment.commenter = request.user
			new_comment.save()
			return HttpResponseRedirect( reverse('learning_logs:topics'))
	context = {'form': form, 'product': product_id}
	return render(request, 'learning_logs/comment_product.html', context)


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