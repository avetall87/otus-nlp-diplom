import requests
from dotenv import dotenv_values

config = dotenv_values("./bot/env/.env")
retriver_service_url = config['RETRIVER_SERVICE_URL']
squad_service_url = config['SQUAD_SERVICE_URL']

def get_answer(question) -> []:

    empty_result_descr = 'К сожалению подходящего ответа не нашлось ...'


    answers = []

    # Получаем список документов в которых вероятнее всего есть ответ на заднный вопрос
    documents = __get_documents_by_question__(question) 

    # Идем циклом по документам и ищем ответ по тексту документа
    for document in documents:

        answer = __get_answer_by_context__(document['raw_text'], question)

        if answer == None or answer == '':
           answer = empty_result_descr
        else:
           answer = f'''
Вероятность ответа: {round(float(answer['score']), 3)}           
Ответ: {answer['answer']}
           '''         

        answers.append(
            f'''
Что мне удалось найти (документ):
    - Документ: {document['raw_text']}
    - Вероятность: {round(float(document['weight']), 2)} 
    - Идентификатор документа: {document['entity_chiper']}
{answer}
-----  
            '''
            )

    if len(answers) == 0:
        answers.append(empty_result_descr)

    return answers


def __get_documents_by_question__(question: str) -> []:
    try:
        response = requests.get(retriver_service_url + f'/search-doc/{question}', verify=False)
        return response.json()
    except Exception as e:
        return []


def __get_answer_by_context__(context: str, question: str) -> str:
    try:
        response = requests.post(squad_service_url + '/squad', json={'context':context, 'question':question}, verify=False)
        return response.json()
    except Exception as e:
        return 'Ошибка, не получилось найти ответ на Ваш вопрос ... '    