import math
from .models import User, Match


def create_new_matches(user):
    create_singles_matches(user)
    create_doubles_matches(user)


def create_singles_matches(user):
    # get users at same level
    equal_users = User.objects.filter(
        gender=user.gender,
        level=user.level,
        singles=user.singles,
    ).exclude(id=user.id)
    # for each check if they have a relationship
    for equal_user in equal_users:
        match_exists = Match.objects.filter(match=user).filter(match=equal_user).exists()
        # if they dont created a new match
        if not match_exists:
            new_match = Match.objects.create(
                created_by=user,
                type='S'
            )
            new_match.match.add(user)
            new_match.match.add(equal_user)
            new_match.save()


def create_doubles_matches(user):
    equal_users = User.objects.filter(
        gender=user.gender,
        level=user.level,
        singles=user.singles,
    ).exclude(id=user.id)
    len_equal_users = len(equal_users)
    if len_equal_users < 3:
        return
    group_count = math.floor(len_equal_users/3)
    for x in range(group_count):
        group = equal_users[(x-1 if x > 0 else 0) * 3:3]
        match_exists = Match.objects\
            .filter(match=user)\
            .filter(match=group[0])\
            .filter(match=group[1])\
            .filter(match=group[2])\
            .exists()
        if not match_exists:
            new_match = Match.objects.create(
                created_by=user,
                type='D'
            )
            new_match.match.add(user)
            for member in group:
                new_match.match.add(member)
            new_match.save()


def get_new_matches(user):
    if user.level is None:
        return []
    matches = Match.objects.filter(match=user, new=True)
    return [match.serialize() for match in matches]


def get_existing_matches(user):
    if user.level is None:
        return []
    matches = Match.objects.filter(match=user, new=False)
    return [match.serialize() for match in matches]
