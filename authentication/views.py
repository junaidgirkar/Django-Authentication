from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, LoginForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

#################### index#######################################
def index(request):
	try:
		user = request.user
	except:
		user = "AnonymousUser"
	return render(request, 'index.html', {'title':'index', 'user':user})

########### register here #####################################
def register(request):
	if request.method == 'POST':
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			# username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			######################### mail system ####################################
			htmly = get_template('Email.html')
			d = { 'email': email }
			subject, from_email, to = 'welcome', 'your_email@gmail.com', email
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			# msg.send()
			##################################################################
			messages.success(request, f'Your account has been created ! You are now able to log in')
			return redirect('login')
	else:
		form = CustomUserCreationForm()
	return render(request, 'register.html', {'form': form, 'title':'reqister here'})

################ login forms###################################################
def Login(request):
	if request.method == 'POST':

		email = request.POST.get('email')
		try:
			validate_email(email)
		except ValidationError as e:
			print("bad email, details:", e)
		else:
			print("good email")
		password = request.POST.get('password')
		user = authenticate(request, email = email, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' wecome {email} !!')
			return redirect('index')
		else:
			messages.info(request, f'account done not exit plz sign in')
	else:
		form = LoginForm()
		return render(request, 'login.html', {'form':form, 'title':'log in'})
