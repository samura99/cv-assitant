from src.config.config import ConfigGPT
from src.config.prompts import basic_info, identifique_query, irs_prompt
from openai import OpenAI, AsyncOpenAI
import json


class GPT:
    """
    ## GPT
    GPT es usado para realizar servicios a la api de gpt openAI.
    #### inputs:
    - `model`: modelo de gpt que se utilizara
    """

    def __init__(
        self,
        info,
        model=ConfigGPT.DEFAULT_MODEL_NAME,
    ):
        self.client = OpenAI(api_key=ConfigGPT.OPENAI_API_KEY)
        self.asyncclient = AsyncOpenAI(api_key=ConfigGPT.OPENAI_API_KEY)
        self.info = info
        self.model = model
        self.current_price = 0

    def completion(self, history, system_message, json_format=False):
        messages = [item for item in history]
        messages.insert(0, {"role": "system", "content": system_message})

        completion = (
            self.client.chat.completions.create(model=self.model, messages=messages)
            if not json_format
            else self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
            )
        )

        self.get_price(completion.usage)
        message = completion.choices[0].message.content
        return message

    def identifique_query(self, history):
        system_message = identifique_query()
        return json.loads(self.completion(history, system_message, True))

    def conversation(self, history, projects=False, show=False):
        info = self.info
        if projects:
            info = {
                key: value
                for key, value in zip(info.keys(), info.values())
                if key in ConfigGPT.STRONG_FIELDS
            }
            info["projects"] = projects

        system_message = basic_info(info, show)
        return self.completion(history, system_message, json_format=show)

    def end_irs(self, projects, history):
        system_message = irs_prompt(projects)
        return json.loads(self.completion(history, system_message, True))

    def reload_price(self):
        self.current_price = 0

    def get_price(self, usage):
        """
        ## `def` get_price
        recibe el uso de la api y calcula el precio del uso del llamado actua a la api, usando los valores de precio dado por la documentacion oficial de openAI. Ademas aumenta el precio actual usado por la instacia de `class GPT`

        ### inputs:
            - `usage`: uso de la api retornado en el completion respuesta del llamado a la api de gpt
        ### outputs:
            - `price`: precio final del llamado a la api.
        """

        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens

        input_price = ConfigGPT.MODEL_PRICE[self.model]["input"]
        output_price = ConfigGPT.MODEL_PRICE[self.model]["output"]
        price = input_tokens * input_price + output_tokens * output_price

        self.current_price += price
        return price
