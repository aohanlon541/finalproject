from .models import User, Match


def create_new_matches(user):
    # get users at same level
    users = User.objects.filter()
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
