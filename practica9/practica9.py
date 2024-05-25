from wordcloud import WordCloud
from collections import Counter
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
import codecs

nltk.download("punkt")
nltk.download("stopwords")

def open_file(path: str) -> str:
    try:
        with codecs.open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print("El archivo especificado no se encontró.")
        return ""
    except Exception as e:
        print(f"Error al abrir el archivo: {e}")
        return ""

def tokenize_and_filter(text: str, language='spanish') -> list:
    stopwords_set = set(stopwords.words(language))
    stopwords_set.add("responder")
    stopwords_set.add("respuesta")
    stopwords_set.add("día")
    stopwords_set.add("respuestas")
    stopwords_set.add("días")
    stopwords_set.add("semanas")
    stopwords_set.add("editado")
    stopwords_set.add("mes")
    stopwords_set.add("hace")
    stopwords_set.add("dia")
    stopwords_set.add("dias")
    stopwords_set.add("meses")
    words = nltk.word_tokenize(text)
    return [word.lower() for word in words if word.isalnum() and word.lower() not in stopwords_set]

all_words = open_file("../data/texto.txt")
if all_words:
    words = tokenize_and_filter(all_words)

    wordcloud = WordCloud(
        background_color="white",
        min_font_size=5
    ).generate(" ".join(words))

    plt.figure(figsize=(8, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("../img_prac9/word_cloud.png")
    plt.close()
