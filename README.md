# Дипломный проект OTUS-NLP
## Тема «Поиск ответов на пользовательские вопросы (ODQA)» принята на рассмотрение

Суть проекта: 
Построить вектор построить векторную БД для поиска ответов на впросы по содержимому текста.

Как это работает:
- Телеграм бот -  отвечает за фронт часть системы, через которую пользователи могут задавать вопросы
- retriver-service - сервис который принимает на вход вопрос пользователя переводит его в вектор и за счет косинусной близости ищет 3 наиболее вероятных документа
- squad-servive - сервис который ищет ответ на задаваемый вопрос в тексте документа

Сервисы retriver-service и squad-servive возвращают веса ответов, система не пропускает варианты документов из retriver-service менее 60%

К боту можно подключиться по ссылке - https://t.me/avetall87_qa_diplom_bot
