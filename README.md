# webFeels
Text Analyser that extracts keywords, phrases and calculates sentiment throughout the page or document

## Installation
This is an iPython notebook, specifically for Jupyter. You will need to install **anaconda** on your machine before you start, and make sure you have Python 2.7 (I know, why am I not using py3?). 

Once you have anaconda up and running, run `jupyter notebook` on your terminal/cmd in the path where the files are located. This will load the Notebook to your browser.

## Usage
Open **websiteFeelings**, which is the GUI for webFeels, and all you have to do is run the cell where the only piece of "code" is in (it starts wth %run). It is pretty straightforward from then on.

## Libraries
Make sure you `pip install` all the libraries necessary:
1. TextBlob
2. VaderSentiment

The rest should already be pre-installed. If not, the ImportErrors are easy enough to google. Stackoverflow has an answer for just about everything.

## Functionality
You can:
* **Input a URL**: webFeels will extract the text from the website and extract the keywords, phrases and sentences. If the website is in another language, webFeels will attempt to translate it to English.
* **Input plain text**: webFeels will do the same as above, only a bit faster since it doesn't need to download the website.
