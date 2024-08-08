import os
import json


def open_json(path):
    try:
        with open(path, "r") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        raise Exception("File not found.")


data_path = os.path.join(os.getcwd(), "data")


def get_user_data(user, data="info"):
    for folder in os.listdir(data_path):
        folder_path = os.path.join(data_path, folder)
        if folder == user:
            for file in os.listdir(folder_path):
                path = os.path.join(folder_path, file)
                if not os.path.isdir(path) and file == f"{data}.json":
                    return open_json(path)

    raise Exception("User not found.")


class LocalData:
    def get_info(user):
        return get_user_data(user, "info")

    def get_projects(user):
        return get_user_data(user, "projects")

    def get_full_projects():
        pass

    def get_full_info():
        return open_json(os.path.join(data_path, "info.json"))


class Requests:
    def get_info(user):
        pass

    def get_projects(user):
        pass

    def get_full_projects(user):
        pass

    def get_full_info(user):
        pass
