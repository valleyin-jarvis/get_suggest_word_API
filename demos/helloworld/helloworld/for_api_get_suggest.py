#!/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert

import time
import os
import sys
import re #正規表現モジュール


#サイト情報をまとめる
TOP_URL = "http://kouho.jp/"

#ディレクトリを取得
dir_name = (os.path.dirname(__file__))

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--window-size=1920,1080')

#ブラウザ読み込み
driver = webdriver.Chrome(chrome_options=options) #chromedriver.exe読み込み
driver.set_page_load_timeout(300) #ページロード最大300秒(5分)


####　関数 #################################

#chrome起動→ログインページに移動
def drive_get():
    try:
        driver.get(TOP_URL)
        time.sleep(0.5)
        print("success input Web page!")
        return True
    except:
        print("false input Web page!")
        return False


#値を渡してGoボタンをクリック
def send_word_and_go_button(word):
    try:
        rakuten_check_button = driver.find_element_by_css_selector("#rakuten")
        rakuten_check_button.click()
        time.sleep(0.1)

        keyword = driver.find_element_by_name("keyword")
        keyword.send_keys(word)
        time.sleep(0.3)

        go_button = driver.find_element_by_css_selector("#submitbtn")
        go_button.click()
        print("success send word and go button!")

        time.sleep(1)
        
        return True
    except:
        print("false send word and go button!")
        return False

#htmlコードの正規表現
def regular_expression(word):
    try:
        suggest_words = []

        #まず全体から必要なhtmlのかたまりを取得
        html_source = driver.page_source
        pattern = '<ul class="ul30 clearfix">(.*?)</ul>'
        keyword_source = re.findall(pattern, html_source,re.S)

        #サジェストワードのhtml群を取得
        pattern2 = '<li class="li30" .*?>(.*?)</li>'
        matchs = re.findall(pattern2, keyword_source[0],re.S)

        #サジェストワードの取得
        pattern3 = '<p>(.*?)</p>'
        words = re.findall(pattern3,matchs[0],re.S)

        for row in words:
            pattern4 =  word +'.*?' #サジェストワードにある検索ワードを取り除く
            reword = re.sub(pattern4,'',row)

            pattern5 =  word.lower() +'.*?'
            #サジェストワードにある小文字の検索ワードを取り除く
            reword2 = re.sub(pattern5,'',reword)
            reword2 = reword2.strip() 

            suggest_words.append(reword2)

        return True,suggest_words
    except:
        print("false regular_expression!")
        suggest_words = None
        return False,suggest_words

"""↓実行部分↓"""################################################################
def get_suggest_word(word):
    try:
        print(word)
        if drive_get() == True:#chrome起動→検索ページに移動
            if send_word_and_go_button(word) == True:
                regular_expression_data = regular_expression(word)

                for row in regular_expression_data[1]:
                    print(row)

        #driver.close()#ブラウザを閉じる
        #driver.quit()#ドライバーの終了
        #sys.exit()

        return True,regular_expression_data[1]

    except:
        print("false get_suggest_word!")
        suggest_words = None

        return False,suggest_words
