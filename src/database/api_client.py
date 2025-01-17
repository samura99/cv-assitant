from database.api.api import (
    load_data,
    save_data,
    register,
    get_key,
    get_repo,
    get_token,
)


def get_user_data(user):
    return load_data(user)


def set_user_data(user, data):
    return save_data(user, data)


def register_user(user, repo, token):
    user_key = register(user=user, repo=repo, token=token)
    return user_key


def get_user_key(user):
    return get_key(user)


def get_user_repo(user):
    return get_repo(user)


def get_user_key(user):
    return get_key(user)


def get_user_token(user):
    return get_token(user)
