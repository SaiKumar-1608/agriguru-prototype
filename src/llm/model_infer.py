from transformers import pipeline

qa = pipeline("question-answering", model="distilbert-base-uncased")
context = "Apply 30 kg nitrogen and ensure soil moisture between 30-50%."
query = "How much nitrogen should be applied?"
result = qa(question=query, context=context)
print("Answer:", result['answer'])
