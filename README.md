# EDINETからデータを取得する方法

EDINETとは、有価証券報告書をはじめとする開示書類を電子的に公開するシステムである。このシステムを活用することで、最大で過去3年分の有価証券報告書 (6年分の会計情報) を入手することが出来る。本資料では、まずEDINETを利用したデータのダウンロード方法について説明する。最終的に、XBRLファイルから企業の財務情報を入手する方法について説明する。

## 開示情報から得られる情報について:
 まず、有価証券報告書から得られる情報について説明しよう。有価証券報告書とは、...to be written


# データのダウンロード方法
本章では、EDINETからデータをダウンロードする方法について説明する。EDINETからデータをダウンロードする方法は2つある:
1. GUIからダウンロードする方法
   - プログラミングの知識はいらない
   - データをマニュアルで入力する必要がある
2. APIを活用してダウンロードする方法
   - プログラミングの知識が必要
   - データを自動で取得可能
     - 一番面倒なデータの加工はある程度私がやっておきました
     - 私のサンプルコードの設定を変更すれば、簡単に財務データを取得できると思います

本章では以上の方法を用いたデータのダウンロード方法を説明する。最終的に、XBRLファイルから財務情報を取得する方法について説明する。

※ 本ドキュメントでは、Pythonを利用した例を紹介します. また、コードの動作確認はLinux (Ubuntu20.04) 上で行なっています。windowsやmacで動くかどうかは知りません (多分動くと思う...)。


## GUI からダウンロードする方法
まず、GUIからダウンロードする方法について説明しよう。to be written...



## APIを活用してダウンロードする方法
次に、APIを活用してダウンロードする方法について説明しよう。to be written...




# XBRLファイルからデータを取得する
 XBRLファイルとは、有価証券報告書などの開示文書と同時に提出されるファイルである。また、そのファイルに記述されている内容は、PDF版の有価証券報告書と等価なものが記載されている。しかし、そのファイルのフォーマットは機械フレンドリーに作られている。そのため、人間が読むには適さない。本章では、そのxbrlファイルを適切に処理し、財務データを取得する方法について解説する。

 ※ここでの解説は[公式サイト](https://www.fsa.go.jp/search/20211109/2b-1_InstanceGuide.pdf)に準拠します。

## XBRLファイルのフォーマットについて
XBRLファイルは、html言語のようなタグの集合として構成される:

```html
  <jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults contextRef="CurrentYearInstant" unitRef="JPY" decimals="-6">29367000000</jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults>
```

XBRLファイルに記述されている内容を適切に理解するために、``<...>text</...>''のフォーマットで書かれるタグの読み方を一つ一つ説明しよう。

### ``<...>text</...>''の第一要素: 要素名
まず、``<...>''に含まれる第一要素である「jpcrp_cor:CashAndCashEquivalentsIFRSSummaryOfBusinessResults 」について説明しよう。この第一要素は、タグで囲まれるtextの内容を表す識別子である。この識別子が指す財務指標はは、タクソノミ対応表を確認することで調べることが出来る。また、[このディレクトリ](AboutAPI/ProcessedData/TagList) にもその対応表を配置した。


### ``<...>text</...>''の第二要素: コンテキストID
次に、``<...>''に含まれる第二要素である「contextRef="CurrentYearInstant"」について説明しよう。この第二要素は、そのデータがいつのものかを表す指標である:
|No|contextRef|意味|
|---|---|---|
|1|CurrentYear|当年度を意味します。|
|2|Interim|中間期を意味します。|
|3|Prior1Year|前年度を意味します。|
|4|Prior1Interim|前中間期を意味します。|
|5|Prior2Year|前々年度を意味します。|
|6|Prior2Interim|前々中間期を意味します。|
|7|Prior{n}Year|{n}年度前を意味します。|
|8|Prior{n}Interim|{n}年度前中間期を意味します。|
|9|CurrentYTD|当四半期累計期間を意味します。|
|10|CurrentQuarter|当四半期会計期間を意味します。|
|11|Prior{n}YTD|{n}年度前同四半期累計期間を意味します。|
|12|Prior{n}Quarter|{n}年度前同四半期会計期間を意味します。|
|13|FilingDate|提出日を意味します。|
|14|RecordDate|議決権行使の基準日を意味します。※1|
|15|RecentDate|最近日を意味します。※2、3|
|16|FutureDate|予定日を意味します。※3|
|17|Instant|時点を意味します。|
|18|Duration|期間を意味します。|
|19|メンバーの要素名|メンバーの要素名を意味します。|

### ``<...>text</...>''の第三要素: ユニットID
次に、``<...>''に含まれる第三要素である「unitRef="JPY"」について説明しよう。この第三要素は、そのデータに記載されている価格の単位を表す。日本の企業のであれば、多くの場合は日本円 (JPY) で単位が記述される。その他の単位に関しては、[このサイト](http://www.xbrl.org/utr/utr.xml) を参照

### ``<...>text</...>''の第四要素: 数値の精度
次に、``<...>''に含まれる第四要素である「decimals="-6"」について説明しよう。この第四要素は、そのデータに記載されている価格の精度を表す（100万単位など）。

### その他の要素について
この画像を参照してください:
![](image/OffDoc.png)

※ https://www.fsa.go.jp/search/20211109/2b-1_InstanceGuide.pdf より2022年9月30日時点の画像を引用.



## データの取得方法
ここでは、XBRLを読み込むためのパッケージである'xbrl'を使用したデータの取得例を説明します。

### XBRLファイルに含まれるタクソノミ要素リストの確認
まず、XBRLファイルに含まれるタクソノミ要素リスト（取得可能なデータリスト）を検索します
```python
# pathには、XBRLファイルの絶対パスを入力する
path = "***"
data = pd.read_csv(path,sep="\n",header=None)
# Tagsに利用可能なタクソノミを格納する
Tags = []
for i in data[0].values:
    i = i.split(" ")
    n = 0
    dic = {}
    N = len(i)
    for j in i:
        if len(j)==0:
            continue
        j = j.strip("<")
        if j[0]=="j":
            Tags.append(j)
        break
    pass
```

 
### 分析に必要なデータを抽出する
上のコマンドを実行して、Tagsに利用可能なデータの一覧を取得しました。Tagsの中に含まれるデータの中から必要なデータを取得し、取得します。
```python
import edinet
from edinet.xbrl_file import XBRLDir
import pandas as pd
# DOC_IDにダウンロードしてきたファイルのディレクトリを入力する
DOC_ID = "***"
xbrl_dir = XBRLDir("./"+DOC_ID)
# 例: 補助金収入を確認する
for i in xbrl_dir.xbrl.find_all("jpcrp_cor:AuditFeesConsolidatedSubsidiaries"):
    print(i._element["contextRef"], i.text)
    # Prior1YearDuration 23000000
    # CurrentYearDuration 23000000
```

この一連の分析手続きは、[リンク](Example/GetDataFromXBRL.ipynb)を確認してください。


# 具体例
- [ダウンロード可能なドキュメントを確認する方法](CheckDocID/get_doc_id.ipynb)
- [データをダウンロードする方法](DownloadData/Download.ipynb)
- [分析対象とするXBRLファイルで取得可能なデータ (タクソノミ) を確認する方法](GetAllTagsInXBRL/GetTags.ipynb)
- [データをダウンロードしてからXBRLファイルからデータを取得する方法](Example/GetDataFromXBRL.ipynb)



# 参考
- タクソノミの対応表: RefTags/TagList を確認
- xbrlの使い方: https://github.com/icoxfog417/xbrl_read_tutorial
- EDINET: https://disclosure.edinet-fsa.go.jp/
- タクソノミ要素リストの公式情報: https://www.fsa.go.jp/search/20211109.html
- apiを叩く方法: https://pypi.org/project/requests/
- [自然言語処理を研究している友人に教えてもらった本](https://www.amazon.co.jp/%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%83%BB%E6%B7%B1%E5%B1%A4%E5%AD%A6%E7%BF%92%E3%81%AB%E3%82%88%E3%82%8B%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E5%87%A6%E7%90%86%E5%85%A5%E9%96%80-scikit-learn%E3%81%A8TensorFlow%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%9F%E5%AE%9F%E8%B7%B5%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0-Compass-Data-Science/dp/4839966605/ref=asc_df_4839966605/?tag=jpgo-22&linkCode=df0&hvadid=422535116155&hvpos=&hvnetw=g&hvrand=10707588413728611630&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1009180&hvtargid=pla-890787647719&psc=1&th=1&psc=1)