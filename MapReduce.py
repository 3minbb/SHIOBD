from bs4 import BeautifulSoup
import requests
import re

def iter_group(queue):
    buf = []
    prev_key = None

    for val in queue:
        cur_key, cur_val = val
        if cur_key == prev_key or prev_key is None:
            buf.append(cur_val)
        else:
            yield prev_key, buf
            buf = []
            buf.append(cur_val)
        prev_key = cur_key

    if buf:
        yield cur_key, buf

class MapReduce:
    def __init__(self):
        self.queue = []

    def send(self, key, value):
        self.queue.append((key, value))

    def count(self):
        return len(self.queue)

    def __iter__(self):
        return iter_group(sorted(self.queue, key=lambda x: x[0]))

url = input("Введите ссылку: ")
response = requests.get(url)
wiki_text = BeautifulSoup(response.text, "html.parser").get_text()

x = MapReduce()
words = re.findall(r'\w+', wiki_text.lower())
for word in words:
    x.send(word, 1)

result = {}
for word, ones in x:
    if word not in result:
        result[word] = 0
    result[word] += sum(ones)

for word, count in sorted(result.items(), key=lambda x: x[1], reverse=True):
    print(word, count)

print("Уникальных слов:", x.count())

user_word = input("Введите слово для вывода результата: ").lower()
if user_word in result:
    print(f"Результат для слова '{user_word}': {result[user_word]}")
else:
    print(f"Слово '{user_word}' не найдено в статье.")