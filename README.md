# word2vec-toy-app
- [word2vec-toy-app](#word2vec-toy-app)
- [アプリの機能と概要](#アプリの機能と概要)
  - [単語分散表現のモデルのロード](#単語分散表現のモデルのロード)
  - [ロードした単語分散表現のモデルの全語彙の一覧を表示](#ロードした単語分散表現のモデルの全語彙の一覧を表示)
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
    - [パターンB：uvを使用(簡単かつ確実に動作させたい場合)](#パターンbuvを使用簡単かつ確実に動作させたい場合)
- [アプリ起動中に使えるAPI](#アプリ起動中に使えるapi)
- [`uv.lock`から`requirements.txt`を生成する方法](#uvlockからrequirementstxtを生成する方法)
- [使用ライブラリのライセンス](#使用ライブラリのライセンス)
  
<br>  
  
# アプリの機能と概要
Word2vecの学習済みモデルとGensimでサクッと遊ぶために、Gradioを用いて作成したローカル用のWebアプリです。  
  
GensimのWord2vecに関する機能を、ローカルで起動したWebアプリからGUIで使えるようにしてみたというものです。  

※Word2vecや単語のベクトル化については、この記事がわかりやすいのでオススメです。  
https://qiita.com/kuroitu/items/c18129bcdd0c343d16ba  
  
<br>  
  
| 技術項目                          | 使用しているもの             |
| --------------------------------- | ---------------------------- |
| プログラミング言語                | Python 3.11           |
| Pythonのバージョン管理とパッケージ管理       | uv 0.5.4                          |
| Pythonのリンターとフォーマッター       | Ruff 0.8.0                          |
| Pythonの仮想環境                  | venv                         |
| **Word2vecの利用** | Gensim 4.3.3 (LGPLv2.1)                      |
| **Web UIのアプリ** | Gradio 5.3.0 (Apache License 2.0)                      |
| Gradioに渡すDataFrame | Polars 1.1.0 (MIT) |
  
<br>    
  
## 単語分散表現のモデルのロード
・ディレクトリに配置したモデルを選択して読み込みます。  
・`gensim.models.KeyedVectors.load_word2vec_format`を使って読み込みます。  
https://radimrehurek.com/gensim/models/keyedvectors.html#gensim.models.keyedvectors.KeyedVectors.load_word2vec_format  
![](https://raw.githubusercontent.com/TweeTeaFOX223/word2vec-toy-app/main/README-image/model_load.PNG)
  
<br>    
  
## ロードした単語分散表現のモデルの全語彙の一覧を表示
・モデルを読み込むと自動的に↓に語彙のリストを表示します  
・Gensimのkeyedvectorsのkey_to_indexから取得して表示しています。  
https://stackoverflow.com/questions/66868221/gensim-3-8-0-to-gensim-4-0-0  
・Gradioのデータフレームの仕様で全行の表示はできないようです。  
・以下のように対処方法のアイディアはあるけど今回の実装は無し  
https://x.com/TweeTea277/status/1826586217510830603  
https://x.com/TweeTea277/status/1826589899631591776  
![](https://raw.githubusercontent.com/TweeTeaFOX223/word2vec-toy-app/main/README-image/word_list.PNG)
  
<br>    
  
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

Pythonのインストールが必須です。uvの使用は任意です（軽量・Python本体のバージョン管理が可能・簡単かつ確実な動作が可能となるので推奨です）。Ruffの使用は任意です(VSCodeでは使用する設定になっています `.vscode/settings.json`)。 →[uvとRuffのインストール＆使用方法のおすすめ記事](https://zenn.dev/turing_motors/articles/594fbef42a36ee)。

動作確認はWindows10とPowerShellとFirefoxでやりました。おそらく他のOSやターミナルでも動くと思います。

  
| インストールが必要 | 動作確認したver |
| ---------------------- | --------------- |
| Python                     | 3.11         |
| uv(任意)                | 0.5.4        |
  
<br>  
  
## [1]：リポジトリをクローン
ターミナルでリポジトリをクローンし、cdでディレクトリに入ってください。gitがない場合はZIPでダウンロードして解凍します。
```
git clone https://github.com/TweeTeaFOX223/word2vec-toy-app.git
cd word2vec-toy-app
```
  
<br>  
  
## [2]：学習済みモデルの準備
Word2vecの学習済みモデル(`.bin`か`.vec`)を、自分でコーパスから学習させて作成するか、インターネット上に公開されているモデルをダウンロードするかで入手してください。

- 自分でWord2vecとfastTextのモデルを作成する方法の解説記事  
https://qiita.com/ka-son11/items/50c16568924575b4eb69  
https://qiita.com/icoxfog417/items/42a95b279c0b7ad26589  

- インターネット上で公開されている学習済みモデルに関する記事  
https://qiita.com/Hironsan/items/513b9f93752ecee9e670  
https://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/  
  
<br>  
  
## [3]：学習済みモデルをディレクトリに配置
クローンしたプロジェクトのディレクトリの`./model_files/`以下に、入手した学習済みモデル(`.bin`か`.vec`)を配置します。ロードの選択時には再帰的に探すので、間にディレクトリを挟んでも大丈夫です。(`./model_files/model_name/model.bin`みたいな感じ)


`gensim.models.KeyedVectors.load_word2vec_format`を使って読み込みます。  
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
  
### パターンB：uvを使用(簡単かつ確実に動作させたい場合)
```
uv sync
uv run python gradio_app.py
```
  
<br>  
  
# アプリ起動中に使えるAPI
アプリ起動中にREST APIから関数を使用することができます。画面下部の`Use via API`から確認できます。詳しくはGradio公式ドキュメントをチェック！  
https://www.gradio.app/guides/getting-started-with-the-python-client
  
<br>  
  
# `uv.lock`から`requirements.txt`を生成する方法

このコマンドで生成できます。パッと検索しても書いてる記事見つからなかったので一応記載。  
```
uv export --format requirements-txt --output-file requirements.txt 
```  

公式ドキュメントより  https://docs.astral.sh/uv/reference/cli/#uv-export  
  
<br>  
  
# 使用ライブラリのライセンス

- Gensim (LGPLv2.1)  
https://github.com/piskvorky/gensim?tab=LGPL-2.1-1-ov-file#readme

- Gradio (Apache License 2.0)  
https://github.com/gradio-app/gradio/blob/main/LICENSE

- Polars  (MIT)  
https://github.com/pola-rs/polars?tab=License-1-ov-file