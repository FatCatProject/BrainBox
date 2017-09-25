from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils.html import escape, strip_tags
from django.db import IntegrityError


@login_required(login_url='login')
def index(request):
	return render(request, template_name="web_ui/index.html")


def login(request):
	# TODO - Get user_name from cookie
	user_name = "User name"
	login_error_msg = ""

	user = auth.get_user(request=request)
	if user.is_authenticated:
		return HttpResponseRedirect(redirect_to="/web_ui/")

	if request.method == "POST":
		user_name = escape(strip_tags(request.POST["user_name"]))
		password = escape(strip_tags(request.POST["password"]))

		if user_name is not None and user_name != "" and password is not None and password != "":
			user = auth.authenticate(request=request, username=user_name, password=password)
			if user is not None:
				auth.login(request=request, user=user)
				return HttpResponseRedirect(redirect_to="/web_ui")
			else:
				login_error_msg = "Wrong user name or password."
		else:
			# TODO - Log this in systemlog
			login_error_msg = "Invalid form data place holder."

	return render(
		request, template_name="web_ui/login.html", context={"user_name": user_name, "login_error_msg": login_error_msg}
	)


def register(request):
	register_error_msg = ""
	user_count = User.objects.filter(is_staff=False).count()
	if user_count > 0:
		# TODO - Allow deleting account info.
		register_error_msg = "User already registered!"
	elif request.method == "POST":

		user_name = escape(strip_tags(request.POST["user_name"]))
		password = escape(strip_tags(request.POST["password"]))

		if user_name is not None and user_name != "" and password is not None and password != "":
			try:
				new_user = User.objects.create_user(
					username=user_name, email=user_name, password=password, **{"is_staff": False}
				)
				# TODO - log the user in
				return HttpResponseRedirect(redirect_to="/web_ui/")
			except IntegrityError as e:
				# TODO - This should never actually happen.
				register_error_msg = "User name already exists. Though this should never happen."

	else:
		pass
	return render(
		request, template_name="web_ui/register.html", context={"login_error_msg": register_error_msg}
	)


@login_required()
def logout(request):
	auth.logout(request=request)
	return HttpResponseRedirect(redirect_to="/web_ui/")

# from django.core import serializers
# data = serializers.serialize("xml", SomeModel.objects.all())
# XMLSerializer = serializers.get_serializer("xml")
# xml_serializer = XMLSerializer()
# xml_serializer.serialize(queryset)
# data = xml_serializer.getvalue()
