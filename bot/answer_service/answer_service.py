import requests

from bot import config

retriver_service_url = config['RETRIVER_SERVICE_URL']

def get_answer(question) -> []:

    result = []

    # Получаем список документов в которых вероятнее всего есть ответ на заднный вопрос
    documents = __get_documents_by_question__(question) 

    # Идем циклом по документам и ищем ответ по тексту документа
    answers = []

    return documents


def __get_documents_by_question__(question: str) -> []:
    try:
        return requests.get(retriver_service_url + '/search-doc/{question}', verify=False)
    except Exception as e:
        return []