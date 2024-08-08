from src.database.config import DataConfig

if DataConfig.Local:
    from src.database.api_client import LocalData as API
else:
    from src.database.api_client import Requests as API


class IRS:
    def __init__(self) -> None:
        self.documents = None
        if DataConfig.RamIRS:
            self.set_ducuments()

    def set_ducuments(self):
        self.documents = API.get_full_projects()

    def get_documents_from_query(self, query, user=DataConfig.DefaultUser):
        # TODO Aqui hay que hacer un IRS
        documents = self.get_documents_from_user(user)
        return documents

    def get_documents_from_user(self, user):
        # Esto lo que tiene que hacer es una llamada a una api con base de datos. Tambien pueden existir ambas opciones para quien no tiene base de datos
        if DataConfig.RamIRS:
            return self.documents[user]
        else:
            return API.get_projects(user)


irs = IRS()
