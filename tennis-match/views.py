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
from .forms import RegisterForm


def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        util.create_new_matches(request.user)
        return JsonResponse({
            'new_matches': util.get_new_matches(request.user),
            'existing_matches': util.get_existing_matches(request.user)
        }, status=200, safe=False)
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))


@csrf_exempt
@login_required
def get_match(request, match_id):
    try:
        match = Match.objects.get(id=match_id)
        messages = Message.objects.filter(match=match)
        return JsonResponse({
            'match': match.serialize(),
            'messages': [message.serialize() for message in messages]
        }, status=200, safe=False)
    except Exception:
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
        form = RegisterForm(request.POST)
        email = form["email"]

        # Ensure password matches confirmation
        password = form["password"]
        confirmation = form["confirmation"]
        if password.data != confirmation.data:
            return render(request, "tennis-match/register.html", {
                "message": "Passwords must match."
            })
        level = form["level"]
        gender = form["gender"]
        singles = form["singles"]
        doubles = form["doubles"]
        mixed_doubles = form["mixed_doubles"]
        picture = form["picture"]
        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password, level, gender, singles, doubles, mixed_doubles, picture)
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
