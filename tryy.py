import string
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords
stop_words=set(stopwords.words("english"))

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

import enchant
d = enchant.Dict("en_US")

import nltk
valid_words = set(nltk.corpus.words.words())

# text = "RT @SRT_for_ever The God of Cricket Is Taking Shape Gradually..... @sachin_rt @100MasterBlastr https //t.co/9f9LTEIfb0 "
output = open("new_preprocessed.txt","a")

f = open('new_tweets.txt','r')

for text in f:
    text = text.split(',text:')[1]
    input_str = text.lower() #lower case
    input_str = ''.join([i for i in input_str if not i.isdigit() and i not in string.punctuation]) #remove numbers and punctuations

    #remove @xyz and checking for english words
    remove_names_str = ""
    for word in input_str.split(' '):
        if(not word.startswith('@') and len(word)>2 and d.check(word)):
            remove_names_str+=" "+word

    #tokenization and remove stop words
    tokenized_word=word_tokenize(remove_names_str)
    filtered_sent=[]
    for w in tokenized_word:
        if w not in stop_words:
            filtered_sent.append(w)

    #Stemming
    # ps = PorterStemmer()
    # stemmed_words=[]
    # for w in filtered_sent:
    #     stemmed_words.append(ps.stem(w))

    #lementization
    from nltk.stem import WordNetLemmatizer
    lemmatizer=WordNetLemmatizer()
    lemintiz_words = []
    for word in filtered_sent:
        lemintiz_words.append(lemmatizer.lemmatize(word))

    #POS and removing proper nouns
    tagged_sentence = nltk.tag.pos_tag(lemintiz_words)
    edited_sentence = [word for word,tag in tagged_sentence if tag != 'NNP' and tag != 'NNPS']
    # print(' '.join(edited_sentence))
    output.write(" ".join(edited_sentence))
    output.write("\n")

output.close()