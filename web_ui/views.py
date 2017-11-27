from bbox.bboxDB import BrainBoxDB
from bbox.models import Account
from bbox.models import SystemSetting
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.html import escape, strip_tags
from server_tasks.send import get_server_token
import server_tasks.receive as receive_tasks
import server_tasks.send as send_tasks
from datetime import datetime


@login_required(login_url='login')
def index(request):
	user = auth.get_user(request=request)

	food_boxes = BrainBoxDB.get_all_foodBoxes()

	server_last_sync = BrainBoxDB.get_system_setting("Server_Last_Sync")

	if server_last_sync is None:
		server_last_sync = "Never"
	else:
		server_last_sync = datetime.strptime(server_last_sync.value_text, "%Y-%m-%d %H:%M:%S")

	context_dict = {
		"account_name": user.username,
		"food_boxes": food_boxes,
		"server_last_sync": server_last_sync
	}
	return render(
		request,
		template_name="web_ui/index.html",
		context=context_dict
	)


def login(request):
	# TODO - Get user_name from cookie
	user_name = "Username"
	login_error_msg = ""

	user = auth.get_user(request=request)
	if user.is_authenticated:
		return HttpResponseRedirect(redirect_to="/web_ui/")

	if request.method == "POST":
		user_name = escape(strip_tags(request.POST["user_name"]))
		password = escape(strip_tags(request.POST["password"]))

		if user_name is not None and user_name != "" and password is not None and password != "":
			user = auth.authenticate(
				request=request,
				username=user_name,
				password=password
			)
			if user is not None:
				auth.login(request=request, user=user)
				return HttpResponseRedirect(redirect_to="/web_ui")
			else:
				login_error_msg = "Wrong user name or password."
		else:
			# TODO - Log this in systemlog
			login_error_msg = "Invalid form data place holder."

	return render(
		request,
		template_name="web_ui/login.html",
		context={
			"user_name": user_name,
			"login_error_msg": login_error_msg
		}
	)


def register(request):
	register_error_msg = ""
	user_count = User.objects.filter(is_staff=False).count()
	if user_count > 0:
		# TODO - Allow deleting account info.
		server_address = BrainBoxDB.get_system_setting("Server_Address")  # type: SystemSetting
		if not server_address:
			server_address = "the website"
		else:
			server_address = server_address.value_text
		register_error_msg = (
			"This product already has a registered user on {0}. For retrieving the username and password please refer to {0}."
		).format(server_address)
	elif request.method == "POST":

		user_name = escape(strip_tags(request.POST["user_name"]))
		password = escape(strip_tags(request.POST["password"]))

		if user_name is not None and user_name != "" and password is not None and password != "":
			new_server_token, login_status = get_server_token(
				user_name=user_name,
				password=password
			)

			if not login_status:
				register_error_msg = "Bad login information."
			elif new_server_token is None:
				register_error_msg = "Something bad has happened, please try again later."
			else:
				try:
					new_user = User.objects.create_user(
						username=user_name,
						email=user_name,
						password=password,
						**{"is_staff": False}
					)
					auth.login(request=request, user=new_user)
					BrainBoxDB.add_account(
						user=new_user.email,
						password=new_user.password
					)
					Account.objects.filter(
						user_name=new_user.email
					).update(server_token=new_server_token)
					return HttpResponseRedirect(redirect_to="/web_ui/")
				except IntegrityError as e:
					# TODO - This should never actually happen.
					register_error_msg = "User name already exists. Though this should never happen."
	else:
		pass
	return render(
		request,
		template_name="web_ui/register.html",
		context={
			"register_error_msg": register_error_msg
		}
	)


@login_required()
def logout(request):
	auth.logout(request=request)
	return HttpResponseRedirect(redirect_to="/web_ui/")


@login_required()
def sync_box(request):
	# TODO
	return HttpResponseRedirect(redirect_to="/web_ui/")


@login_required()
def server_sync(request):
	receive_tasks.get_foodboxes()
	send_tasks.put_foodboxes()
	send_tasks.put_feedinglogs()
	receive_tasks.get_cards()
	return HttpResponseRedirect(redirect_to="/web_ui/")

