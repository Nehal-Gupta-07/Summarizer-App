import spacy #latest version
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from heapq import nlargest
nlp = spacy.load("en_core_web_sm")
from newspaper import Article ,Config
from flask import send_file
import pdb


  
def summarizer(text): 

    try:    
        ratio=0.2
        doc = nlp(text)
        processed_txt=[token.text for token in doc if not token.is_stop and not token.is_punct and token.text!="\n"] 

        l=set(processed_txt) #getting the unique words of the text
        words={i:processed_txt.count(i)for i in l} #frequency of each unique word

        max_freq=max(words.values())

        for word in words.keys():
            words[word]=words[word]/max_freq #score given to each word based on usage
        
        sentence_tokens=[sent for sent in doc.sents]
        
        sentence_scores={}
        # finding score of each sentence
        for sent in sentence_tokens:
            for word in sent:
                if word.text in words.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = words[word.text]
                    else:
                        sentence_scores[sent]+= words[word.text]
        
        select_length = int(len(sentence_tokens)*ratio) #length of summaries in number of sentences

        summary = nlargest(select_length, sentence_scores, key = sentence_scores.get) #finding most important sentences

        final_summary = [word.text for word in summary]
        final_summary = " ".join(final_summary)
        if len(final_summary)==0:
            title = "Text too short"
        else:
            title = "Summary"
        return final_summary , title
    except:
        title="Text too short"
        return " " , title






def news_scraping(url):
    try:
        config = Config()
        config.request_timeout = 100
        article = Article(url,config=config)
        article.download()
        article.parse()
        article.nlp()
        return article.title , article.keywords , article.summary , article.publish_date
    except:
        return "Invalid URL" , "" , " "," "






def ner(text):
    NER = spacy.load("en_core_web_sm")
    text1 = NER(text)
    names=[]
    org=[]
    product=[]
    gpe=[]

    for word in text1.ents:
        if(word.label_ == "PERSON"):
            names.append(word)
        if(word.label_ == "ORG"):
            org.append(word)
        if(word.label_ == "PRODUCT"):
            product.append(word)
        if(word.label_ == "GPE"):
            gpe.append(word)
    dic={}
    a=[]
    for i in names:
        if i.text not in a:
            a.append(i.text)
    for i in names:
        if i.text in a:
            dic[i.text]=i.label_
            a.remove(i.text)
    b=[]
    for i in org:
        if i.text not in b:
            b.append(i.text)
    for i in org:
        if i.text in b:
            dic[i.text]=i.label_
            b.remove(i.text)
    c=[]
    for i in product:
        if i.text not in c:
            c.append(i.text)
    for i in product:
        if i.text in c:
            dic[i.text]=i.label_
            c.remove(i.text)
    d=[]
    for i in gpe:
        if i.text not in d:
            d.append(i.text)
    for i in gpe:
        if i.text in d:
            dic[i.text]=i.label_
            d.remove(i.text)
    if len(dic)==0:       
        return (dic) , "No Named Entities Found"
    else:
        return (dic) ,"NER"
    
    


def word_cloud_generator(text):
    
    doc = nlp(text)
    
    processed_txt=[token.text for token in doc if not token.is_stop and not token.is_punct] 
    processed_text= " ".join(processed_txt)
    
    l = processed_text.split(" ")
    a=[]
    for i in l:
        if i not in a:
            a.append(i)
    words={i:l.count(i)for i in a}
    
    sorted_dict = dict(sorted(words.items(), key=lambda x:x[1],reverse=True))
    x=dict(list(sorted_dict.items())[0:30])
    
    wordcloud = WordCloud(width = 1000, height = 1000,
                background_color ='white',
                min_font_size = 10).generate_from_frequencies(x)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig('static\wordcloud.png')
    root_folder = "static"
    img_name = "wordcloud.png" 
    img_path = root_folder+ "/"  + img_name
    if len(x)==1 and list(x.keys())[0]=="":
        return  " ", "Invalid Input"
    else:
        return img_path , "Word Cloud"
