import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
from heapq import nlargest

nlp = spacy.load("en_core_web_sm")

#doc = "Machine learning (ML) is the scientific study of algorithms and statistical models that computer systems use to progressively improve their performance on a specific task. Machine learning algorithms build a mathematical model of sample data, known as “training data”, in order to make predictions or decisions without being explicitly programmed to perform the task. Machine learning algorithms are used in the applications of email filtering, detection of network intruders, and computer vision, where it is infeasible to develop an algorithm of specific instructions for performing the task. Machine learning is closely related to computational statistics, which focuses on making predictions using computers. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a field of study within machine learning and focuses on exploratory data analysis through unsupervised learning. In its application across business problems, machine learning is also referred to as predictive analytics."
with open("Textfileonheart.txt", "r") as file:
    doc = file.read()

doc = nlp(doc)

#Calculate the frequency of each token using the “Counter” function. Top 5 most frequent words. 
keyword = []
stopwords = list(STOP_WORDS)
pos_tag = ['PROPN', 'ADJ', 'NOUN', 'VERB']
for token in doc:
        if(token.text in stopwords or token.text in punctuation ):
                continue
        if(token.pos_ in pos_tag):
                keyword.append(token.text)
freq_word = Counter(keyword)
print(freq_word.most_common(5))

#result is stored as a key-value pair in sent_strength where keys are the sentences in the string doc and the values are the weight of each sentence
max_freq = Counter(keyword).most_common(1)[0][1]
for word in freq_word.keys():
        freq_word[word] = (freq_word[word]/max_freq)
print(freq_word.most_common(5))

sent_strength={}
for sent in doc.sents:
        for word in sent:
                if word.text in freq_word.keys():
                        if sent in sent_strength.keys():
                                sent_strength[sent]+=freq_word[word.text]
                        else: 
                                sent_strength[sent]=freq_word[word.text]
print(sent_strength)

#nlargest function is used to summarize the string, it takes 3 arguments,
summarized_sentences = nlargest(3, sent_strength, key=sent_strength.get)
print(summarized_sentences)

#finalized output
final_sentences = [w.text for w in summarized_sentences]
summary = ' '.join(final_sentences)
print(summary)