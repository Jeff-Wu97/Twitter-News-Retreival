from flask import Flask, request, render_template, redirect, url_for
import search_rank
import conndb
import sqlite
import json
from snowballstemmer import EnglishStemmer
import re

# Read the stop word and create the stop word list
stwlist = [line.strip() for line in open('englishST.txt', encoding='utf-8').readlines()]

with open("profileImages.json", errors='ignore') as f1:
    profile_images_dict = json.loads(f1.readline())

app = Flask(__name__, static_url_path='')


@app.route("/", methods=['POST', 'GET'])
def main():
    if request.method == 'POST' and request.form.get('query'):
        query = request.form['query']
        return redirect(url_for('search', query=query))

    return render_template('index.html')


@app.route("/q/<query>", methods=['POST', 'GET'])
def search(query):
    docs = search_rank.ranked_retrieval(query)
    terms = preprocessing(query)
    if len(docs) != 0:
        result = highlight(docs, terms)
        return render_template('result1.html', docs=result, value=query, length=len(docs))
    else:
        empty_list = []
        return render_template('result1.html', docs=empty_list, value=query, length=0)


def preprocessing(text):
    # Create a list to store the text after removing the stop word
    post_list = []
    # Removes punctuation, Numbers, and so on from the string
    text0 = re.sub('[,\.(){}+-/~`?<>"_=:;!@#$%^&*]|\\\\|\'s|\'|\[|\]|\|', ' ', text)
    # Replace newline characters, case conversion, split into word list
    word_list = text0.replace('\n', ' ').lower().split()
    # Remove the stop word, stem extraction
    for word in word_list:
        if word in stwlist:
            continue
        else:
            word0 = EnglishStemmer().stemWord(word)
            post_list.append(word0)
    return post_list


def highlight(docs, terms):
    result = []
    for doc in docs[:1000]:
        account_name = doc.split()[0]
        tweet_id = doc.split()[1]
        cursor = sqlite.select("SELECT text,time from '%s' where tweet_id=(%s)" % (account_name, tweet_id))
        content = cursor[0][0]
        time = cursor[0][1]
        post_list = []
        word_list = content.split()
        for word in word_list:
            # word = str(word.encode('utf-8'))
            ppword = ''
            for i in word:
                if i in '[,\.(){}+-/~`?<>"_=:;!@#$%^&*]|\\\\|\'|\[|\]|\|':
                    i = ' ' + i + ' '
                    ppword = ppword + i
                else:
                    ppword = ppword + i
            post_i_list = []
            for i in ppword.split():
                post_i = i.lower()
                post_i = EnglishStemmer().stemWord(post_i)
                if post_i in terms:
                    post_i_list.append('<font color="red">{}</font>'.format(i))
                else:
                    post_i_list.append(i)
            post_i = ''.join(post_i_list)
            post_list.append(post_i)
        content = ' '.join(post_list)
        url = "https://twitter.com/%s/status/%s" % (account_name, tweet_id)
        result.append((url, content, account_name, time, profile_images_dict[account_name]))
    return result


if __name__ == '__main__':
    # 调试模式
    # app.run(debug=True)
    app.run()
