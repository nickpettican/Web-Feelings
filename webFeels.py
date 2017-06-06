#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ___            Digital Research Scripts               ___
# ___                by nickpettican                    ___

# ___        Copyright 2017 Nicolas Pettican            ___

# ___    This software is licensed under the Apache 2   ___
# ___    license. You may not use this file except in   ___
# ___    compliance with the License.                   ___
# ___    You may obtain a copy of the License at        ___

# ___    http://www.apache.org/licenses/LICENSE-2.0     ___

# ___    Unless required by applicable law or agreed    ___
# ___    to in writing, software distributed under      ___
# ___    the License is distributed on an "AS IS"       ___
# ___    BASIS, WITHOUT WARRANTIES OR CONDITIONS OF     ___
# ___    ANY KIND, either express or implied. See the   ___
# ___    License for the specific language governing    ___
# ___    permissions and limitations under the License. ___

# only works on Jupyter Notebooks
from ipywidgets import widgets
from ipywidgets import FloatProgress
from IPython.display import display
from IPython.display import HTML
from IPython.display import Javascript
from IPython.display import clear_output

print '\nStarting...\n'

from bs4 import BeautifulSoup
from lxml import etree
from lxml.html.clean import Cleaner
from collections import Counter
from textblob import TextBlob
from time import time, sleep
import pandas as pd
import matplotlib.pyplot as plt
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

clear_output()

plt.style.use('ggplot')

class webFeelings:
    
    def __init__(self):
        self.start_requests()
        self.display_GUI()
        
    def start_requests(self):
        try:
            self.browser = requests.Session()
            self.browser.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'})
        except Exception as e:
            print 'Error starting requests: %s' %(e)
        
    def display_GUI(self):
        self.url_caption = widgets.HTML('<div style="font-size: 1.5em; margin-top:2em; margin-bottom:1em">Insert the URL bellow and press ENTER</div>')
        self.url = widgets.Text(description='URL')
        self.url.width = '400px'
        display(self.url_caption, self.url)
        self.alt_txt_cap = widgets.HTML('<div style="font-size: 1.5em; margin-top:1em; margin-bottom:1em">Alternatively, paste the text</div>')
        self.alt_txt = widgets.Text(description='Text')
        self.alt_txt.width = '600px'
        display(self.alt_txt_cap, self.alt_txt)
        self.url.on_submit(self.extract_text)
        self.alt_txt.on_submit(self.extract_text)

    def keywords_and_display(self, old_prog):
        try:
            sleep(2)
            self.url_caption.close()
            self.url.close()
            self.alt_txt_cap.close()
            self.alt_txt.close()
            if old_prog:
                old_prog.close()
            caption = widgets.HTML('<br/><div style="font-size: 1.5em; margin-top:1em; margin-bottom:1em">Analysing keywords and phrases density</div>')
            prog = FloatProgress(min=0, max=100, description='Progress')
            display(caption, prog)
            def print_kws(b):
                clear_output()
                display(keywords)
            def print_phr(b):
                clear_output()
                for i in self.data['Phrases']:
                    print i
            def print_snt(b):
                clear_output()
                for i in self.data['Sentences']:
                    print i
            self.data = self.extract_keywords(self.text, prog)
            caption = widgets.HTML('<div style="font-size: 1.5em; margin-top:1em; margin-bottom:1em">Click to view respective data</div>')
            keywords = pd.DataFrame(self.data['Keywords'], columns=['Keyword', 'Density (%)'])
            kw_button = widgets.Button(description='Keywords')
            phr_button = widgets.Button(description='Phrases')
            snt_button = widgets.Button(description='Sentences')
            kw_button.width = '420px'
            phr_button.width = '420px'
            snt_button.width = '420px'
            display(caption, kw_button)
            display(phr_button)
            display(snt_button)
            kw_button.on_click(print_kws)
            phr_button.on_click(print_phr)
            snt_button.on_click(print_snt)
            sentiment_btn_cap = widgets.HTML('<br/><hr/><div style="font-size: 1.5em; margin-top:1em; margin-bottom:1em">Analyse sentiment throughout the page</div>')
            sentiment_btn = widgets.Button(description="Classic Sentiment Analysis")
            sentiment_btn.width = '420px'
            sentiment_btn.style = 'success'
            display(sentiment_btn_cap, sentiment_btn)
            sentiment_btn.on_click(self.sentiment_analysis)
            vader_sentiment_btn = widgets.Button(description="Social Media Sentiment Analysis")
            vader_sentiment_btn.width = '420px'
            vader_sentiment_btn.style = 'success'
            display(vader_sentiment_btn)
            vader_sentiment_btn.on_click(self.sentiment_analysis)
        except Exception as e:
            print 'Error while extracting keywords: %s' %(e)

    def extract_text(self, url):
        try:
            if url.value.startswith('http') and '://' in url.value:
                prog = FloatProgress(min=0, max=100, description='Progress')
                display(widgets.HTML('<br/>'), prog)
                tr0 = time()
                site = self.browser.get(url.value, timeout=10)
                if site.ok:
                    prog.value += 50
                    tr1 = time() - tr0
                    t0 = time()
                    cleaner = Cleaner()
                    cleaner.javascript = True
                    cleaner.style = True
                    cleaner.kill_tags = ['header', 'footer']
                    source_tree = etree.HTML(cleaner.clean_html(site.content))
                    text = source_tree.itertext()
                    t1 = time() - t0
                    self.text = '\n'.join([n.strip() for n in text if n.strip()])
                    prog.value += 50
                    self.keywords_and_display(prog)
                else:
                    display(widgets.HTML('<div style="font-size: 1.5em; margin-top:1em; margin-bottom:1em">404 - bad URL</div>'))
            else:
                self.text = url.value
                self.keywords_and_display(False)
        except Exception as e:
            print 'Error extracting text: %s' %(e)

    def extract_keywords(self, text, prog):
        try:
            blob = TextBlob(text)
            prog.value += 40
            try:
                if not blob.detect_language() == 'en':
                    try:
                        blob = blob.translate(to='en')
                    except Exception as e:
                        print 'Error translating to English: %s' %(e)
            except URLError as e:
                print 'Could not check language: no internet'
            total_words = float(len([word.strip() for word in text.split() if word.strip()]))
            words = [n for n, t in blob.tags if len(n) > 2 if 'NN' in t or 'JJ' in t or 'VB' in t]
            keywords = [[n, (count / total_words) * 100] for n, count in Counter(words).most_common(20)]
            prog.value += 20
            phrases = [n for n, count in Counter(blob.noun_phrases).most_common(20) if count >= 2 if len(n.strip()) > 5]
            prog.value += 20
            sentences = [n if '/n' not in n and len(n.strip()) > 2 else TextBlob(''.join([w for w in n.split('\n') 
                        if len(w.strip()) > 2])) if len(n.strip()) > 2 else False for n in blob.sentences]
            prog.value += 20
            return {
                'Keywords': keywords,
                'Phrases': phrases,
                'Sentences': [s for s in sentences if s]
            }
        except Exception as e:
            print "Error: %s" %(e)

    def sentiment_analysis(self, descrip):
        try:
            clear_output()
            plt.xlabel('Sentences In Page')
            plt.ylabel('Sentiment Score')
            if 'classic' in descrip.description.lower():
                sentimentDF = pd.DataFrame([[i, s.sentiment.polarity] for i, s in enumerate(self.data['Sentences'], 1)], columns=['Sentences_Number', 'Sentiment_Score'])
            else:
                vader = SentimentIntensityAnalyzer()
                sentimentDF = pd.DataFrame([[i, vader.polarity_scores(s.raw)['compound']] for i, s in enumerate(self.data['Sentences'], 1)], columns=['Sentences_Number', 'Sentiment_Score'])
            plt.plot(sentimentDF.Sentences_Number, sentimentDF.Sentiment_Score)
            plt.show()
        except Exception as e:
            print 'Error: %s' %(e)

analyser = webFeelings()
