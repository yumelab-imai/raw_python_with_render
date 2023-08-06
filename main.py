# for FastAPI
# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def index():
#     return {"Hello": "World"}


# for Flask
from flask import Flask, jsonify

from flask import request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

import requests
import textract
from pypdf import PdfReader
from transformers import GPT2TokenizerFast
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains.question_answering import load_qa_chain
# from langchain.llms import OpenAI
# from langchain.chains import ConversationalRetrievalChain
from data import pdf_urls
import sys

# 対象データの読み込み
from data import pdf_urls

app = Flask(__name__)
app.debug = False

line_bot_api = LineBotApi(os.getenv('YOUR_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('YOUR_CHANNEL_SECRET'))
print('その１')
@app.route("/callback", methods=['POST'])
def callback():
    print('その２')
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):







    # ここから
    # PDFのダウンロードと保存を行う関数
    def download_and_save_pdf(url, filename):
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
        else:
            print("Error: Unable to download the PDF file. The URL might be incorrect. Status code:", response.status_code)
            sys.exit()

    # PDFの読み込みを行う関数
    def read_pdf(filename):
        with open(filename, 'rb') as file:
            page_contents = ''
            reader = PdfReader(filename)
            number_of_pages = len(reader.pages)
            page_contents = ""
            for page_number in range(number_of_pages):
                pages = reader.pages
                page_contents += pages[page_number].extract_text()

            return page_contents





    # 各PDFの全ページからデータを取得
    pages_contents = ''
    for i, url in enumerate(pdf_urls):
        # PDFをダウンロードして保存
        filename = f'sample_document{i+1}.pdf'
        download_and_save_pdf(url, filename)
        
        # PDFを読み込み
        pages_contents += read_pdf(filename)


    chunks = pages_contents
    print('URLのPDF群から情報を抽出しました。')
    print(chunks)

    text = chunks

    # tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

    # def count_tokens(text: str) -> int:
    #     return len(tokenizer.encode(text))

    # Split text into chunks
    # text_splitter = RecursiveCharacterTextSplitter(
    #     # Set a really small chunk size, just to show.
    #     # chunk_size = 512,
    #     chunk_size = 512,
    #     chunk_overlap  = 24,
    #     length_function = count_tokens,
    # )

    # chunks3 = text_splitter.create_documents([text])

    print('step 222')
    # print(chunks3)
    # ここまで





    print('その３~4')
    # LINE bot => おうむ返し
    message = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message)
        )


if __name__ == "__main__":
    print('その６')
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)