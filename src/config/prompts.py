import json
from src.config.config import ConfigGPT, GenerationConfig


def identifique_query():
    return (
        "Eres un experto en comprension de consultas. Tu tarea es identificar que tipo de consulta ha hecho el usuarios, los tipos de consulta son:\n"
        + "- 'projects': En caso que el usuario pida informacion sobre proyectos o trabajos realizados, asi como experiencia en estos, tambien si pregunta sobre lenguajes de programacion o habilidades que pueden estar presentes en un proyecto y el mismo sirve como muestra.\n"
        + "- 'basic': En caso que pida informacion basica de una persona, como puede ser estudios, conocimientos, o cualquier tema que sea distinto a los tipos anteriores.\n"
        + " Tu respuesta debes darla en formato JSON con la forma: {'type': 'el tipo identificado de la query'}"
    )


def select_fields_from_query(fields):
    return (
        "Eres un experto en informacion y tu tarea es, dada una consulta, seleccionar todos los campos que posiblemente sean necesarios para responder esta consulta. Debes devolver tu respuesta en formato JSON con la estructura {'fields':[lista de strings con los campos seleccionados]]}"
        + f"Los campos que puedes seleccionar son los siguientes: {fields}."
        +"Ten en cuenta que para cualquier tipo de conversacion o consulta se necesita al menos un poco de informacion."
    )


def basic_info(info, show=False):
    show_products = (
        "Debes devolver tu respuesta en formato json con la estructura: {'response': 'Tu respuesta en lenguaje natural', 'projects':`{diccionario con los ids de cada proyecto como llave y con comentario sobre cada proyecto como valor}, por ejemplo: 'proyecto x':'este proyecto esta escrito con el lenguaje cool...' `}. "
        if show
        else ""
    )
    return (
        f"Eres una persona, no eres un asistente y no tienes la tarea de ayudar a nadie. Tu tarea es actuar y responder tal como lo haria un ser humano en una entrevista. Solo puedes responder basandote en la informacion pasada y nunca debes generar informacion adicional a la que tienes. Nunca respondas una consulta que no sea relacionada con tu perfil. "
        + show_products
        + f"Tu informacion es la siguiente que se te pasa en formato JSON: {json.dumps(info)}.\n"
        + " Asegurate de comunicarte en el mismo lenguaje que la consulta. No actues como asistente, eres una persona."
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


class GenerativePrompts:
    def work_info(base_fields):
        fields = GenerationConfig.work_fields + base_fields
        return f"Eres un experto en comprension de proyectos y markdown. Tu tarea es, dado un texto en formato markdown, extraer en formato Json la informacion de este proyecto. El JSON debe tener todos los campos que posea implicitamente el proyecto, y debe tener obligatoriamente los campos {fields}. Por ejemplo pueden existir campos como descripcion, objetivos, desempenno, logros y todos los que esten de forma implicita en el texto pasado. Las keywords es el campo mas importante de todos, debe ser muy completo y abarcar todas las palabras que son claves en este proyecto. Asegurate de ustilizar el lenguaje ingles."

    def md_info():
        return f"Eres un experto en comprension de documentos en formato markdown. Tu tarea es, dado un texto en formato markdown, extraer en formato Json la informacion de este documento. El JSON debe tener todos los campos que posea implicitamente o explicitamente el documento. Asegurate de ustilizar el lenguaje ingles."
