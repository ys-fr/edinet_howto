import pandas as pd
import datetime
import requests
import sys

# 1: ダウンロードしたいデータのDocIDを入力
# 2: 展開先のディレクトリを指定
key = sys.args
# ダウンロードしたいデータをCheckDocID/AvailableData.csvから選択する
# そのデータのdocIDをDOCIDに入力する
DOCID = key[0]
xbrl_path = edinet.api.document.get_xbrl(
            DOC_ID, save_dir=key[1],
            expand_level="dir")
xbrl_dir = XBRLDir("./data/" + DOC_ID)
