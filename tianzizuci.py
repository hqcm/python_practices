import requests
from lxml import etree


class Hanzi(object):
    "填字组词游戏"

    def __init__(self):
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
        }
        self.data = {
            "lb_a": "hp",
            "lb_b": "jq",
            #采用精确搜索模式：jq
            "lb_c": "mh",
            "tp": "tp3",
        }

    def getContent(self, url, word):
        self.data.update({"q": word})
        html = requests.post(url, headers=self.headers, data=self.data).content
        html = etree.HTML(html)
        words = html.xpath('//li/a/text()')
        return words

    '''
    def cumputeNum(self, word):
        "统计汉字个数"
        i = 0
        flag = True
        for _ in word:
            i += 1
        if i > 2:
            flag = False
        return flag
    '''

    def findword(self, word):
        "查找词组"
        words = []
        twowords = []
        self.data.update({"q": word})
        start_url = "http://www.zdic.net/sousuo/"
        html = requests.post(
            start_url, headers=self.headers, data=self.data).content
        html = etree.HTML(html)
        pages = html.xpath('//div[starts-with(@class,"ssfy")]/a/@href')
        #精准定位div; h小写
        pages.insert(0, "")
        for page in set(pages):
            url = start_url + page
            words += self.getContent(url, word)
        for word in words:
            twowords.append(word.strip())
            #去除词语后的空格
        return twowords

    def compareWords(self, word1, word2):
        "找出上面和左边词语的共有汉字"
        word = []
        words1 = self.findword(word1)
        words2 = self.findword(word2)
        for i in words1:
            for j in words2:
                if i[1] == j[1]:
                    word.append(i[1])
                    break
        return word

    def judgeWords(self, word):
        self.data.update({"q": word})
        start_url = "http://www.zdic.net/sousuo/"
        html = requests.post(
            start_url, headers=self.headers, data=self.data).content
        html = etree.HTML(html)
        page = html.xpath('//strong/text()')
        if page:
            return True
        else:
            return False

    def matchWords(self, word, word3, word4):
        "匹配右边和下边词语"
        words = []
        for i in word:
            words3 = i + word3
            words4 = i + word4
            if self.judgeWords(words3) & self.judgeWords(words4):
                words.append(i)
        return words


if __name__ == '__main__':
    word1 = "日"
    word2 = "学"
    word3 = "期"
    word4 = "望"
    hanzi = Hanzi()
    word = hanzi.compareWords(word1, word2)
    words = hanzi.matchWords(word, word3, word4)
    if words:
        for i in words:
            print(word1 + i + "+" + word2 + i + "+" + i + word3 + "+" + i + word4)
    else:
        print ("没有合适的词组")
