from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from main_site.form import LoginForm


class LoginView(View):
	def post(self, request):
		user = LoginForm(request.POST)
		if user.is_valid():
			request.session.set_expiry(28800)
			user_login = user.cleaned_data.get('login')
			user_pass  = user.cleaned_data.get('password')
			aut_user = authenticate(username=user_login, password=user_pass)
			if aut_user is not None and aut_user.is_active:
				login(request, aut_user)
				return redirect('/price/')
		return redirect('/')


class LogoutView(View):
	def get(self, request):
		if request.user.is_authenticated():
			logout(request)
		return redirect('/')
