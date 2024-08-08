from src.app.openai_.gpt import GPT
from src.database.config import DataConfig
from src.database.data import data
from src.database.irs import irs
import json


class Chat:
    def __init__(self, user=DataConfig.DefaultUser) -> None:
        self.gpt: GPT = GPT(info=data.get_info(user))
        self.history = []
        self.max_history_len = 5
        self.user = user

    async def send_query(self, query):
        return self.process_query(query)

    def process_query(self, query):
        self.history.append({"role": "user", "content": query})
        self.history = self.history[: self.max_history_len * 2]

        query_type = self.get_query_type(self.history)
        if query_type["type"] == "projects":
            show = query_type["show"]
            return self.process_projects(self.history, show=show)

        response = self.gpt.conversation(self.history)
        self.history.append({"role": "assistant", "content": response})
        return {"response": response, "projects": {}}

    def get_query_type(self, history):
        query_type = self.gpt.identifique_query(history)
        return query_type

    def process_projects(self, history, show):
        keywords = None  # TODO esto es para el caso que se pueda usar embeddings
        projects = irs.get_documents_from_query(query=keywords, user=self.user)
        ids = self.gpt.end_irs(projects=projects, history=history)["projects"]
        projects = [p for p in projects.values() if p["id"] in ids]
        response = self.gpt.conversation(self.history, projects=projects, show=show)
        self.history.append({"role": "assistant", "content": response})

        if show:
            return json.loads(response)
        else:
            return {"response": response, "projects": {}}
