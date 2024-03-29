from django.shortcuts import render, redirect, HttpResponse,get_object_or_404

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import Questions, Team, Events, SolvedTimestamps, Machines, SolvedQuestions, SolvedMachines,TakenQuestionHint
import CTFFinal.settings as settings 
from django.utils import timezone
from constance import config
from django.views.decorators.cache import cache_page
from django.db.models.query import QuerySet
from datetime import datetime
from django.utils.timezone import make_aware
import pytz


def handler404(request, exception, *args, **kwargs):
	response = render(None,"404.html")
	response.status_code = 404
	return response

def handler500(request):
	response = render(None,"500.html")
	response.status_code = 500
	return response


def teamlogin(request):

	if request.user.is_authenticated:
		return redirect("/quest")
	
	if request.method == "POST":
		username = request.POST.get("teamname")
		password = request.POST.get("password")
		team = authenticate(username=username, password=password)
		if team is not None:
			login(request, team)
			
			return redirect("/quest")

		else:
			messages.error(request, "Invalid credentials!")
	return render(request, "app/login.html")



def register(request):

	team = Team()
	if request.method == "POST":

		receiptid = request.POST.get("receiptid")
		team.username = request.POST.get("teamname")
		team.password = make_password(request.POST.get("passwd"))
		
		if settings.MODE == 'production':
			result = Events.objects.using("receipts").filter(receiptid = receiptid)
			query_count = len(result)
			team.email = result[0].email1
			team.first_name = result[0].name1

		elif settings.MODE == 'development':
			query_count = (Events.objects.filter(receiptid = receiptid).count())
		
		try:
			if query_count == 0:
				raise TypeError

			team.clean_fields()
			team.save()
		except Exception as e:
			messages.error(request, "Invalid form submission! Check your data correctly.")
			return render(request, "app/register.html")
		login(request, team)
		return render(request, "app/instructions.html")
	return render(request, "app/register.html")


def profile(request,username):
	'''TODO: Fix ranking issue'''
	user = get_object_or_404(Team,username = username)
	# rank = Team.objects.filter(points__gt = user.points,lastSubmission__lt = user.lastSubmission).order_by("-points","lastSubmission").exclude(username = "chaitanyarahalkar").count()
	# if rank == 0:
	# 	rank = 1
	# else:
	# 	rank += 1
	
	root_owns = SolvedMachines.objects.filter(user = user,root=True).count()
	timestamps = SolvedTimestamps.objects.filter(username = user)
	vals = SolvedQuestions.objects.filter(user = user)

	stats_dict = {"web":0,"reversing":0 ,"steg":0 ,"foren":0,"crypt":0,"misc":0,"machines":root_owns}

	for val in vals:
		stats_dict[val.question.questionType] += 1

	stats = list(stats_dict.values())

	return render(request,"app/profile.html",{"user":user,"challenges_solved":len(vals),"root_owns":root_owns,"timestamps":timestamps,"stats":stats})

def index(request):
	return render(request, "app/index.html")



def instructions(request):
	return render(request, "app/instructions.html")



def about(request):
	return render(request, "app/about.html")

@login_required(login_url="/login/")
def waiting(request):
	return render(request,"app/waiting.html")




@login_required(login_url="/login/")
def machine(request,id = 1):

	if timezone.localtime().timestamp() < config.START_TIME.timestamp():
		return redirect('/waiting')

	if timezone.localtime().timestamp() > config.END_TIME.timestamp():
		return redirect('/leaderboard')

	machine = Machines.objects.get(machineId = id)
	
	if request.method == "POST":
		rating = request.POST.get("radio_btn")
		flag = request.POST.get("flag").strip().lower()
		solved = SolvedMachines.objects.filter(machine = machine,user=request.user)

		if machine.userFlag.strip().lower() == flag:
			if not solved:
				
				request.user.points += int((0.4) * machine.machinePoints)
				request.user.lastSubmission = timezone.localtime()
				messages.success(request,"User flag is correct!")
				request.user.save()
				SolvedMachines(machine = machine, user = request.user).save()
				SolvedTimestamps(username=request.user,points=request.user.points,timestamp_record=timezone.localtime(timezone=pytz.timezone("Asia/Calcutta"))).save()
			else:
				messages.error(request,"Already solved!")

		elif machine.rootFlag.strip().lower() == flag:
			
			if isinstance(solved,QuerySet):
				m = solved[0]
				if not m.root:
					
					m.root = True
					machine.machineSolvers += 1

					if rating == "EA":
						machine.easyRating += 1

					elif rating == "ME":
						machine.mediumRating += 1 

					elif rating == "HA":
						machine.hardRating += 1

					request.user.points += int((0.6) * machine.machinePoints)
					request.user.lastSubmission = timezone.localtime()
					messages.success(request,"Root flag is correct!")
					request.user.save()
					machine.save()
					m.save()
					SolvedTimestamps(username=request.user,points=request.user.points,timestamp_record=timezone.localtime(timezone=pytz.timezone("Asia/Calcutta"))).save()
				else:
					messages.error(request,"Already solved!")
			else:
				messages.error(request,"Submit the user flag before submitting the root flag.")

		else:
			messages.error(request,"Invalid flag!")
		

	return render(request,"app/machine.html", {'machine': machine })

def teamlogout(request):
	#request.user.timeRequired = timezone.localtime().timestamp() - request.session.get("time")
	#request.user.save()
	logout(request)
	return redirect("/leaderboard")



@login_required(login_url="/login/")
def quest(request):

	if timezone.localtime().timestamp() < config.START_TIME.timestamp():
		return redirect('/waiting')

	if timezone.localtime().timestamp() > config.END_TIME.timestamp():
		return redirect('/leaderboard')

	questions = Questions.objects.all().order_by('questionId')
	machines = Machines.objects.all().order_by('machineId')
	solved_questions = SolvedQuestions.objects.filter(user = request.user)
	solved_machines = SolvedMachines.objects.filter(user = request.user)
	solved_question_ids = [entry.question.questionId for entry in solved_questions]
	solved_machine_ids = [entry.machine.machineId for entry in solved_machines]

	if request.method == "POST":

		flag = request.POST.get("flag").strip().lower()
		flag_id = int(request.POST.get("qid"))
		rating = request.POST.get("radio_btn")
		question = Questions.objects.get(questionId=flag_id)
		solved = SolvedQuestions.objects.filter(question=question,user=request.user)


		if flag == question.questionFlag.strip().lower():
			if not solved:

				request.user.points += question.questionPoints
				request.user.lastSubmission = timezone.localtime()
				print("time",request.user.lastSubmission)
				question.questionSolvers += 1

				if rating == "EA":
					question.easyRating += 1

				elif rating == "ME":
					question.mediumRating += 1

				elif rating == "HA":
					question.hardRating += 1

				messages.success(request, "Flag is correct!")
				
				question.save()
				request.user.save()
				SolvedQuestions(question = question, user = request.user).save()
				SolvedTimestamps(username = request.user,points = request.user.points,timestamp_record=timezone.localtime(timezone=pytz.timezone("Asia/Calcutta"))).save()

				solved_question_ids.append(question.questionId)
			else:
				messages.error(request, "Already solved!")
		else:
			messages.error(request, "Invalid flag!")

	return render(
		request,
		"app/quests.html",
		context={
			"challenges": questions,
			"num_challenges": len(questions),
			"total_count": len(questions) + len(machines),
			"machines": machines,
			"solved_question_ids": solved_question_ids,
			"solved_machine_ids": solved_machine_ids

		},
	)




def leaderboard(request):
	teams = (Team.objects.all().exclude(username = 'chaitanyarahalkar').order_by(
		"-points", "lastSubmission")[:10])
	leaderboard = list()
	for rank, team in zip(range(1, len(teams) + 1), teams):
		leaderboard.append((rank, team))


	usernames = list()
	for team in teams:
		data = SolvedTimestamps.objects.filter(username = team)
		usernames.append({'name': team.username,'data': data})

	return render(request, "app/leaderboard.html",
				  {"leaderboard": leaderboard,"usernames":usernames})


@login_required(login_url="/login/")
def timer(request):
	
	if request.method == "GET":
		difference = int(config.END_TIME.timestamp() - timezone.localtime().timestamp())
		if difference == 0:
			logout(request)
		return HttpResponse(difference)

def waiting_time(request):
	if request.method == "GET":
		difference = int(config.START_TIME.timestamp() - timezone.localtime().timestamp())
		return HttpResponse(difference)

@csrf_protect
def hint(request):
	if request.method == "POST":

		hint_id = int(request.POST.get("hintid"))
		question = Questions.objects.get(questionId=hint_id)
		taken = TakenQuestionHint.objects.filter(question = question, user = request.user)

		questionHint = question.questionHint
		questionPoints = question.questionPoints

		if not taken:

			request.user.points -= int(0.1 * questionPoints)
			request.user.save()
			TakenQuestionHint(question = question,user = request.user, hint = True).save()
			SolvedTimestamps(username = request.user,points = request.user.points,timestamp_record=timezone.localtime(timezone=pytz.timezone("Asia/Calcutta"))).save()
		
		return JsonResponse({
			"hint": questionHint,
			"points": request.user.points
		})


def validate_username(request):

	teamname = request.GET.get("teamname", None)
	data = {
		"is_taken": Team.objects.filter(username__iexact=teamname).exists()
	}
	if data["is_taken"]:
		data["error_message"] = "A user with this username already exists."
	return JsonResponse(data)
