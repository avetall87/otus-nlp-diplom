from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline

tokenizer = AutoTokenizer.from_pretrained("./model/tokenizer_ru_bert/")
model = AutoModelForQuestionAnswering.from_pretrained("./model/pretrained_ru_bert_sbersquad/")
question_answerer = pipeline("question-answering", model=model,tokenizer=tokenizer)
