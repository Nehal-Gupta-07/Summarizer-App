from flask import Flask , render_template , url_for , request 
from features import summarizer , news_scraping , ner ,word_cloud_generator
import pdb
app=Flask(__name__)





@app.route('/')
def index():
    return render_template('index.html')
 





@app.route('/web-scraper' , methods=["GET","POST"])
def web_scraper():
    if request.method=='GET':
        show_answer = False
        web_title = web_summary = ""
    if request.method=='POST':
        show_answer = True
        url=request.form.get("url")
        web_title ,web_keywords ,web_summary ,web_publish_date=news_scraping(url)

    return render_template("web_scraping.html",web_title=web_title,web_summary=web_summary,show_answer=show_answer)





@app.route('/text-summarizer',methods=["GET","POST"])
def text_summarizer():
    if request.method=='GET':
        show_answer = False
        summary = ""
        title = ""
    if request.method=='POST':
        show_answer = True
        text = request.form.get("textarea")
        summary , title = summarizer(text)
    return render_template('text_summarizer.html' , summary=summary,title=title,show_answer=show_answer)





@app.route('/NER',methods=["GET","POST"])
def NER():
    if request.method=='GET':
        show_answer = False
        ner_answers={}
        NERtitle=""
    if request.method=='POST':
        show_answer = True
        nertext = request.form.get("nertextarea")
        ner_answers , NERtitle= ner(nertext)
    return render_template("ner.html", ner_answers=ner_answers,show_answer=show_answer,NERtitle=NERtitle)







@app.route('/word-cloud-generator',methods=["GET","POST"])
def wordcloud():
    if request.method=='GET':
        show_answer = False
        wordcloud_image=""
        title = ""
    if request.method=="POST":
        show_answer = True
        cloudtext = request.form.get("cloudtextarea")
        wordcloud_image , title=word_cloud_generator(cloudtext)
         


    return render_template("word_cloud_generator.html",show_answer=show_answer,wordcloud_image=wordcloud_image,title=title)






if __name__ == "__main__":
    app.run()