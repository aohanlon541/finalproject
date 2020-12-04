import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Match, Message
from . import util


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        return render(request, "tennis-match/index.html")
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
@login_required
def get_matches(request):
    util.create_new_matches(request.user)
    return JsonResponse({
        'user': request.user.serialize(),
        'new_matches': util.get_new_matches(request.user),
        'existing_matches': util.get_existing_matches(request.user),
    }, status=200, safe=False)


@login_required
def get_new_matches(request):
    return JsonResponse({
        'new_matches': util.get_new_matches(request.user),
    }, status=200, safe=False)


@login_required
def get_existing_matches(request):
    return JsonResponse({
        'existing_matches': util.get_existing_matches(request.user),
    }, status=200, safe=False)


@csrf_exempt
@login_required
def edit_user(request):
    if request.method == "POST":
        try:
            user = request.user
            data = json.loads(request.body)
            user.level = data['level']
            user.gender = data['gender']
            user.singles = data['singles']
            user.doubles = data['doubles']
            user.mixed_doubles = data['mixed_doubles']
            user.picture = data['picture']
            user.save()
            return HttpResponse(status=200)
        except:
            return HttpResponse(status=400)


@csrf_exempt
@login_required
def get_match(request, match_id):
    if request.method == "PUT":
        try:
            match = Match.objects.get(id=match_id)
            messages = Message.objects.filter(match=match)
            users = User.objects.filter(id__in=match.serialize()['match_ids'])

            match.new = False
            match.save()

            return JsonResponse({
                'match': match.serialize(),
                'users': [match_users.serialize() for match_users in users],
                'messages': [match_message.serialize() for match_message in messages]
            }, status=200, safe=False)
        except Exception as e:
            return HttpResponse(status=400)


@csrf_exempt
@login_required
def message(request, match_id):
    if request.method == "POST":
        # try:
        match = Match.objects.get(id=match_id)
        data = json.loads(request.body)
        if 'id' in data:
            existing_message = Message.objects.get(id=data['id'])
            existing_message.text = data['text']
            existing_message.save()
            return JsonResponse({
                "updated_message": existing_message.serialize()
            }, status=200, safe=False)
        else:
            new_message = Message.objects.create(
                text=data['text'],
                match=match,
                created_by=request.user
            )
            new_message.save()
            return JsonResponse({
                "new_message": new_message.serialize()
            }, status=200, safe=False)
    # except Exception:
    #     return HttpResponse(status=400)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "tennis-match/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "tennis-match/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "tennis-match/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "tennis-match/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "tennis-match/register.html")
