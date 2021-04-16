import re
from snowballstemmer import EnglishStemmer
import csv
import json
import conndb
import sqlite

# Read the stop word and create the stop word list
stwlist = [line.strip() for line in open('englishST.txt', encoding='utf-8').readlines()]


def preprocessing(text):
    # 创建列表存储去除停词后的文本
    final_post_list = []

    final_word_list = []
    text_list = text.split()
    for word in text_list:
        word = str(word.encode('utf-8'))  # 先将字符串转为utf-8编码，以便去除部分表情符号
        if "http://" in word or "https://" in word:  # 去除URL网页链接
            continue
        elif "\\" in word:  # 去除带反斜线'\'的表情符号等其他符号代码
            if word[0] != "\\":
                word0 = word.lower().split("\\")[0]
                word0 = re.sub('[,\.(){}+-/~`?<>"_=:;!@#$%^&*]|\\\\|\'s|\'|\[|\]|\|', ' ', word0)
                for w in word0.lower().split():
                    final_word_list.append(w)
        else:
            # 去除字符串中的标点,大小写转换
            word0 = re.sub('[,\.(){}+-/~`?<>"_=:;!@#$%^&*]|\\\\|\'s|\'|\[|\]|\|', ' ', word)
            for w in word0.lower().split():
                if w != "rt":  # 去除“RT”字段，该字段代表转发
                    final_word_list.append(w)

    # 去除停词，词干提取
    for word in final_word_list:
        if word in stwlist:
            continue
        else:
            word0 = EnglishStemmer().stemWord(word)
            final_post_list.append(word0)

    return final_post_list


def to_invert_index():
    with open("invert_index.json", errors='ignore') as f1:
        invert_index_dict = json.loads(f1.readline())
    # invert_index_dict = {}
    with open("index_reminder.json", errors='ignore') as f2:
        reminder_dict = json.loads(f2.readline())
    # reminder_dict = {}
    with open("All_tweet_num.txt", errors='ignore') as f3:
        count_All_tweet_num = int(f3.readline())
    with open('newsUser.csv', newline='', encoding='utf-8-sig') as csv_file:
        rows = csv.reader(csv_file)
        # 循环遍历数据库中的每一个推特账号
        for row in rows:
            accountName = row[0]
            # reminder = 0
            reminder = int(reminder_dict[accountName])
            # 从指定位置开始遍历数据库，提取出ID和TEXT
            cursors = sqlite.select("SELECT tweet_id,text,id from '%s' where ID>(%d)" % (accountName, reminder))
            if len(cursors) != 0:  # 只有当数据库中有新数据加入时，才会更新索引表
                # 循环遍历一个数据表中的每一条推文信息
                for cur in cursors:
                    doc_id = accountName + ' ' + cur[0]
                    doc_text = cur[1]
                    id_num = cur[2]
                    doc_word_list = preprocessing(doc_text)
                    # 推文中词频统计
                    doc_word_count_dict = {}
                    for word in doc_word_list:
                        if word in doc_word_count_dict.keys():
                            doc_word_count_dict[word] += 1
                        else:
                            doc_word_count_dict[word] = 1
                    # print(doc_word_list)
                    # 生成invert_index_dict，字典嵌套字典嵌套字典
                    for word in doc_word_list:
                        if word not in invert_index_dict.keys():
                            invert_index_dict.update({word: {doc_id: doc_word_count_dict[word]}})
                        else:
                            invert_index_dict[word].update({doc_id: doc_word_count_dict[word]})
                    # print(invert_index_dict)
                    count_All_tweet_num += 1
                # 遍历结束后记录下此次遍历到的位置并存入字典，便于下一次遍历开始时定位
                new_reminder = str(id_num)
                reminder_dict[accountName] = new_reminder
                print("%s index update successfully!" % accountName)
            else:
                print("%s no new data." % accountName)
        # 所有用户遍历结束后将所有此次遍历到的位置的字典并存入json文件，便于下一次遍历开始时定位
        js = json.dumps(reminder_dict)
        file = open('./index_reminder.json', 'w')
        file.write(js)
        file.close()
        # 将索引表字典转json文件
        js = json.dumps(invert_index_dict)
        file = open('./invert_index.json', 'w')
        file.write(js)
        file.close()
        print("All account update successfully!")
        # 统计数据库中推文总数并存入文件
        file = open("./All_tweet_num.txt", 'w')
        file.write(str(count_All_tweet_num))
        file.close()


# to_invert_index()
