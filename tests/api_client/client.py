import requests
import asyncio
import websockets
import json
from requests.exceptions import RequestException


class APIClient:
    def __init__(
        self,
        http_url: str = "http://127.0.0.1:8000/api/v1",
        ws_url="ws://127.0.0.1:8000/api/v1",
        port: str = "8000",
    ) -> None:
        self.http_url = f"{http_url}"
        self.ws_url = f"{ws_url}"
        self.port = port

    def load_data(self, username, user_key):
        url = f"{self.http_url}/data/user/load/{username}"

        headers = {
            "API-KEY": user_key,
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Si la respuesta es exitosa, devolvemos los datos del repositorio
            return response.json()

        except RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None

    def register(self, username, git_repo, git_token):
        url = f"{self.http_url}/data/users/register/{username}/{git_repo}"

        headers = {
            "Authorization": f"Bearer {git_token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Si la respuesta es exitosa, devolvemos los datos del repositorio
            return response.json()

        except RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None

    async def websocket_chat(self, user):
        uri = f"{self.ws_url}/open_chat"
        config = user

        async with websockets.connect(uri, ping_interval=None) as websocket:
            # Enviar un mensaje al servidor
            await websocket.send(config)
            # Esperar y recibir un mensaje del servidor
            response = await websocket.recv()
            print(f"Respuesta del servidor: {response}")

            while True:
                try:
                    query = input("> ")
                    await websocket.send(query)
                    # print(f"> {query}")

                    response = await asyncio.wait_for(websocket.recv(), timeout=11120)
                    # response = await websocket.recv()
                    try:
                        response = json.loads(response)
                        print(f"< {response['response']}")
                    except:
                        print(f"< {response}")

                except Exception as e:
                    print(e)
                    break