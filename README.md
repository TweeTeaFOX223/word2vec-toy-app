# word2vec-toy-app
**これは作りかけのアプリです。(とりあえず動きはする)**

# 目次
- [word2vec-toy-app](#word2vec-toy-app)
- [目次](#目次)
- [アプリの機能と概要](#アプリの機能と概要)
  - [ロードしたモデルの語彙リストを表示](#ロードしたモデルの語彙リストを表示)
  - [入力した単語リストに対してコサイン類似度が上位の単語のランキングを出力](#入力した単語リストに対してコサイン類似度が上位の単語のランキングを出力)
  - [入力した2つの単語リストのコサイン類似度を出力](#入力した2つの単語リストのコサイン類似度を出力)
- [ライセンスについて](#ライセンスについて)
- [アプリの使用方法](#アプリの使用方法)
  - [\[0\]：必要となる環境](#0必要となる環境)
  - [\[1\]：リポジトリをクローン](#1リポジトリをクローン)
  - [\[2\]：学習済みモデルの準備](#2学習済みモデルの準備)
  - [\[3\]：学習済みモデルをディレクトリに配置](#3学習済みモデルをディレクトリに配置)
  - [\[4\]：Pythonの仮想環境の作成とアプリ実行](#4pythonの仮想環境の作成とアプリ実行)
    - [パターンA：venvとrequirements.txtを使用(普通)](#パターンavenvとrequirementstxtを使用普通)
    - [パターンB：Poetryを使用(確実に動かしたい場合)](#パターンbpoetryを使用確実に動かしたい場合)
- [アプリ起動中に使えるAPI](#アプリ起動中に使えるapi)
- [使用ライブラリのライセンス](#使用ライブラリのライセンス)


# アプリの機能と概要
Word2vecの学習済みモデルとGensimでサクッと遊ぶために、Gradioを用いて作成したローカル用のWebアプリです。  
  
GensimのWord2vecに関する機能を、ローカルで起動したWebアプリからGUIで使えるようにしてみたというものです。  

※Word2vecや単語のベクトル化については、この記事がわかりやすいのでオススメです。  
https://qiita.com/kuroitu/items/c18129bcdd0c343d16ba  
  
<br>  
  
| 技術項目                          | 使用しているもの             |
| --------------------------------- | ---------------------------- |
| プログラミング言語                | Python 3.11           |
| パッケージ管理        | Poetry 1.8.3                          |
| Pythonの仮想環境                  | venv                         |
| **Word2vecの利用** | Gensim 4.3.3 (LGPLv2.1)                      |
| **GUIのWebアプリ** | Gradio 4.37.2 (Apache License 2.0)                      |
| Gradioに渡すDataFrame | Polars 1.1.0 (MIT) |
  
<br>    
  
## ロードしたモデルの語彙リストを表示
未完成の機能なので後で書く。  
https://stackoverflow.com/questions/66868221/gensim-3-8-0-to-gensim-4-0-0  
  
## 入力した単語リストに対してコサイン類似度が上位の単語のランキングを出力
・「入力した単語と似ている単語200件のランキング」を表示します。  
・ポジティブはプラスの影響を、ネガティブはマイナスの影響を与えます  
・読み込んだWord2vecモデルの語彙に無い単語を入力するとエラーです。  
・単語(キー)のベクトルに関して色々と計算をした結果を出します。  
・詳細はGensimのdocの「`gensim.models.keyedvectors.KeyedVectors.most_similar`」をチェック！  
https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.KeyedVectors.most_similar  
![](https://raw.githubusercontent.com/TweeTeaFOX223/word2vec-toy-app/main/README-image/most_similar.PNG)
  
<br>    
  
## 入力した2つの単語リストのコサイン類似度を出力
・「入力した2つの単語リストのコサイン類似度」を表示します。  
・読み込んだWord2vecモデルの語彙に無い単語を入力するとエラーです。  
・詳細はGensimのdocの「gensim.models.keyedvectors.KeyedVectors.n_similarity」をチェック！  
https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.KeyedVectors.n_similarity  
![](https://raw.githubusercontent.com/TweeTeaFOX223/word2vec-toy-app/main/README-image/n_similarity.PNG)
  
<br>    
  
# ライセンスについて
Gensimのライブラリをimportしていることが、LGPLにおける静的リンクに該当すると解釈したので、コピーレフトによりライセンスはLGPLv2.1にしました。  
https://future-architect.github.io/articles/20200821/#%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3%E3%82%B9%E3%81%AE%E5%88%86%E9%A1%9E  
https://stackoverflow.com/questions/8580223/using-python-module-on-lgpl-license-in-commercial-product  
  
<br>  
  
# アプリの使用方法 
## [0]：必要となる環境

Pythonのインストールが必須です。Poetryの使用は任意です。動作確認はWindows10とPowerShellとFirefoxでやりました。おそらく他のOSやターミナルでも動くと思います。
  
| インストールが必要 | 動作確認したver |
| ---------------------- | --------------- |
| Python                     | v3.11         |
| Poetry(任意)                | v1.8.3        |
  
<br>  
  
## [1]：リポジトリをクローン
ターミナルでリポジトリをクローンし、cdでディレクトリに入ってください。gitがない場合はZIPでダウンロードして解凍します。
```
git clone https://github.com/TweeTeaFOX223/word2vec-toy-app.git
cd word2vec-toy-app
```
  
<br>  
  
## [2]：学習済みモデルの準備
Word2vecかfastTextの学習済みモデル(`.bin`か`.vec`)を、自分でコーパスから学習させて作成するか、インターネット上に公開されているモデルをダウンロードするかで入手してください。

- 自分でWord2vecとfastTextのモデルを作成する方法の解説記事  
https://qiita.com/ka-son11/items/50c16568924575b4eb69  
https://qiita.com/icoxfog417/items/42a95b279c0b7ad26589  

- インターネット上で公開されている学習済みモデルに関する記事  
https://qiita.com/Hironsan/items/513b9f93752ecee9e670  
https://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/  
  
<br>  
  
## [3]：学習済みモデルをディレクトリに配置
クローンしたプロジェクトのディレクトリに、入手した学習済みモデル(`.bin`か`.vec`)を配置します。

- Word2vecのモデルは`./model_files/word2vec-models/`に配置します。※`gensim.models.fasttext.load_facebook_model`を使って読み込みます。  
https://radimrehurek.com/gensim/models/fasttext.html#gensim.models.fasttext.load_facebook_model  
  
- fastTextのモデルは`./model_files/fasttext-models`に配置します。※`gensim.models.KeyedVectors.load_word2vec_format`を使って読み込みます。  
https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.KeyedVectors.load_word2vec_format  

  
<br>  
  
## [4]：Pythonの仮想環境の作成とアプリ実行
Windows10とPowerShellの場合のコマンドです。これを実行するとローカルホストにアプリが起動します。  

### パターンA：venvとrequirements.txtを使用(普通)
```
python -m venv venv
./venv/Scripts/pip.exe install -r requirements.txt
./venv/Scripts/python.exe gradio_app.py
```
  
<br>  
  
### パターンB：Poetryを使用(確実に動かしたい場合)
```
poetry install
poetry run python gradio_app.py
```
  
<br>  
  
# アプリ起動中に使えるAPI
アプリ起動中にREST APIから関数を使用することができます。画面下部の`Use via API`から確認できます。詳しくはGradio公式ドキュメントをチェック！  
https://www.gradio.app/guides/getting-started-with-the-python-client
  
<br>  
  
# 使用ライブラリのライセンス

- Gensim 4.3.3 (LGPLv2.1)  
https://github.com/piskvorky/gensim?tab=LGPL-2.1-1-ov-file#readme

- Gradio 4.37.2 (Apache License 2.0)  
https://github.com/gradio-app/gradio/blob/main/LICENSE

- Polars 1.1.0 (MIT)  
https://github.com/pola-rs/polars?tab=License-1-ov-file