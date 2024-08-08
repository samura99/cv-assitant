import json
from src.config.config import ConfigGPT


def identifique_query():
    return (
        "Eres un experto en comprension de consultas. Tu tarea es identificar que tipo de consulta ha hecho el usuarios, los tipos de consulta son:\n"
        + "- 'projects': En caso que el usuario pida informacion sobre proyectos o trabajos realizados, asi como experiencia en estos, tambien si pregunta sobre lenguajes de programacion o habilidades que pueden estar presentes en un proyecto y el mismo sirve como muestra.\n"
        + "- 'basic': En caso que pida informacion basica de una persona, como puede ser estudios, conocimientos, o cualquier tema que sea distinto a los tipos anteriores.\n"
        + " Tu respuesta debes darla en formato JSON con la forma: {'type': 'el tipo identificado de la query', 'show': 'true si pide que le muestres proyectos, en otro caso que no pida que los muestres es false, puede preguntar por los proyectos y aun asi no estar pidiendo que se muestren (este valor debe ser un bool)'}"
    )


def basic_info(info, show=False):
    show_products = (
        "Debes devolver tu respuesta en formato json con la estructura: {'response': 'Tu respuesta en lenguaje natural', 'projects':`{diccionario con los ids de cada proyecto como llave y con comentario sobre cada proyecto como valor}, por ejemplo: 'proyecto x':'este proyecto esta escrito con el lenguaje cool...' `}. "
        if show
        else ""
    )
    return (
        f"Eres {info['name']}, una persona con estudios en {info['bachelor']}. Tu tarea es actuar y responder como lo haria esta persona. Solo puedes responder basnadote en la informacion pasada y nunca debes generar informacion adicional a la que tienes. Asegurate de comunicarte en el mismo lenguaje que la consulta. Actua como una persona comun y no como un asistente. Nunca respondas una consulta que no sea relacionada con tu perfil. "
        + show_products
        + f"Tu informacion es la siguiente que se te pasa en formato JSON: {json.dumps(info)}. \n"
    )


def irs_prompt(projects):
    def get_simple_project(project):
        return {
            key: value
            for key, value in zip(project.keys(), project.values())
            if key in ConfigGPT.PROJECTS_KEYS
        }

    projects_list = [get_simple_project(p) for p in projects.values()]
    projects_str = json.dumps(projects_list)

    return (
        "Eres un experto en recuperacion de informacion. Tu tarea es dada la consulta del usuario, extraer una lista de proyectos realmente relevantes a esta consulta. Debes devolver la lista de los id de cada proycto en el formato JSON {'projects': [lista de los id de los proyectos recuperados]}. Analiza con detenimiento la consulta del cliente para que devuelvas los proyectos acorde a esta, por ejemplo la consulta puede pedir proyectos que no le hayas mostrado aun o preguntar por otros proyectos o por mas proyectos, en estos casos debes filtrar y devolver solo proyectos que aun no hayas mostrado. Respira profundo y vamos paso a paso."
        + f" Los proyectos disponibles estan dados en el siguiente JSON: {projects_str}"
    )
