import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


nltk.download('punkt_tab') # Recurso necessário para tokenização


frase = "Instalar o NLTK é muito fácil!"
palavras = nltk.word_tokenize(frase)


print('------------------')
texto = "IA está transformando o mundo"
print(word_tokenize(frase))

stop_words = set(stopwords.words('portuguese'))

filtrando = [p for p in palavras if p.lower() not in stopwords]

print(filtrando)
