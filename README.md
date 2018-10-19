# ゴミ収集日(仙台市限定)検索機能付きゴミ箱API

## 導入
``` bash
$ python -m venv smart-gomibako
$ cd smart-gomibako
$ source bin/activate
$ git clone https://github.com/fuurin/smart-gomibako
$ pip install -r requirements.txt
$ python server.py
```

## API仕様

|エンドポイント|メソッド|パラメータ|説明|
|:--|:--|:--|:--|
|/amount|GET|なし|現在のゴミの量を取得．0~5の6段階|
|/config|GET|なし|現在の設定ファイル(*1)の状態を取得する|
|/config|POST|name,category,collection|現在の設定ファイルの状態を変更する|
|/collection|GET|id,ku,kana1,kana2,juusho|地域を検索し，ゴミ収集日の検索結果(*2)を返す|
|/today|GET|なし|設定ファイルのカテゴリと収集地域IDから今日が収集日かを返す．(*4)|
|/tomorrow|GET|なし|設定ファイルのカテゴリと収集地域IDから明日が収集日かを返す．(*4)|

*1: 設定ファイルには，以下の3つがが含まれる
- name: ゴミ箱につける名前
- category: ゴミ箱のカテゴリ．以下の4つのいずれかを指定する
    - katei: 家庭ゴミ
    - pura: プラゴミ
    - kanbin: 缶，ビン
    - kamirui: 紙類
- collction: 収集地域ID

*2: 以下のように検索を行う
- idを指定： idが指定したidに一致する地域のゴミ収集日情報(*3)を返す
- kuを指定： 指定した区の地域のゴミ収集日情報リストを返す
  - kuとkana1を指定： 指定した区の中で，最初の文字がkana1である地域のゴミ収集日情報リストを返す
    - kuとkana1とkana2を指定：　指定した区の中で，最初の文字がkana1かつ次の文字が最初の文字がkana2である地域のゴミ収集日情報リストを返す
- juushoを指定：　住所が指定した住所に一致する地域のゴミ収集日情報を返す．
- パラメータ指定なし
    - configファイルにゴミ収集日情報のIDが登録されていればそのゴミ収集日情報を返す
    - configファイルにゴミ収集日情報のIDが登録されていなければ，全てのゴミ収集日情報を返す

*3: ゴミ収集日情報は，以下のように構成される．
- id: id
- kana1: 住所の1文字目のカタカナ,
- kana2: 住所の2文字目のカタカナ,
- juusho: 住所,
- katei: 家庭ゴミの収集日,
- pura: プラゴミの収集日,
- kanbin: カン，ビンの収集日,
- kamirui: 紙類の収集日

*4: カテゴリか収集日が設定されていなければnullを返す．configも同時に返す．