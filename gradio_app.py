import glob
import os
from os.path import splitext

import gensim
import gradio as gr
import polars as pl

import gensim_scripts.gensim_w2v as gensim_w2v


# 状態管理のクラス(Stateの変数は全てここに入れる) ###########################################
class GradioState:
    def __init__(self):
        self.loaded_w2v_model_file = None


# モデルファイルのパスのリスト(定数) ###########################################
def glob_win_pass_slash_fix(globlist):
    fixedgloblist = []
    for filepass in globlist:
        abs_filepath = os.path.abspath(filepass)
        fixedgloblist.append(abs_filepath.replace("\\", "/"))
    return fixedgloblist


GENSIM_WORDVEC_MODELS = glob_win_pass_slash_fix(
    glob.glob("./model_files/**/*.vec", recursive=True)
) + glob_win_pass_slash_fix(glob.glob("./model_files/**/*.bin", recursive=True))


# Gradio内部で行う処理の関数 ###########################################
def loadTextDfPass(file_pass) -> pl.DataFrame:
    return pl.DataFrame(
        [open(file_pass, "r", encoding="UTF-8").read()],
        schema=["中身"],
        orient="col",
    )


# ボタンを有効化する
def ready_interactive():
    return gr.update(interactive=True)


def gr_load_word2vec_model(gradio_state: GradioState, model_pass):
    print("load model:" + model_pass)

    if "/fasttext-models/" in model_pass:
        gradio_state.loaded_w2v_model_file = gensim.models.fasttext.load_facebook_model(
            model_pass
        ).wv

    elif "/word2vec-models/" in model_pass:
        if ".bin" in splitext(model_pass):
            binary = True
        else:
            binary = False

        gradio_state.loaded_w2v_model_file = (
            gensim.models.KeyedVectors.load_word2vec_format(model_pass, binary=binary)
        )

    print("あああああ", gradio_state.loaded_w2v_model_file)
    return model_pass


def gr_get_word2vec_model_words_list(gradio_state: GradioState):
    word2vec_model = gradio_state.loaded_w2v_model_file
    return gensim_w2v.word2vec_all_words_to_pldf(word2vec_model)


def gr_top_similar_words(gradio_state: GradioState, positive_words, negative_words):
    check_none = (positive_words is None) and (negative_words is None)
    check_empty = (positive_words == []) and (negative_words == [])
    if check_none or check_empty:
        raise gr.Error("ネガティブとポジティブの両方に単語が入力されていません!")

    word2vec_model = gradio_state.loaded_w2v_model_file

    return gensim_w2v.gensim_wordvec_top_simword(
        word2vec_model, positive_words, negative_words
    )


def gr_two_words_similar(gradio_state: GradioState, target_words1, target_words2):
    check_none = (target_words1 is None) or (target_words2 is None)
    check_empty = (target_words1 == []) or (target_words2 == [])
    if check_none or check_empty:
        raise gr.Error("どちらか片方の単語が入力されていません!")

    word2vec_model = gradio_state.loaded_w2v_model_file

    return gensim_w2v.gensim_wordvec_two_words_sim(
        word2vec_model, target_words1, target_words2
    )


# GradioのUI ###########################################

with gr.Blocks() as main_app:
    gradio_state = gr.State(GradioState())

    with gr.Row(variant="compact"):
        gr.Markdown(
            (
                "# Gensim 4.3.3のWord2vecのデモアプリ  "
                "\n・単語分散表現のモデル(`.bin`か`.vec`)を試せます。  "
                "\n・アプリ起動前に`./model_files/`にモデルのファイルを入れておいてください。  "
                "\n・下記リンクにあるWord2vecとfastTextの何個かのモデルでの動作を確認済み  "
                "\n https://qiita.com/"
                "Hironsan/items/513b9f93752ecee9e670  "
                "\n https://www.cl.ecei.tohoku.ac.jp/"
                "~m-suzuki/jawiki_vector/  "
            )
        )

    with gr.Row(variant="panel"):
        with gr.Column(scale=9):
            word2vec_model_select = gr.Dropdown(
                GENSIM_WORDVEC_MODELS,
                label="配置したモデルから使用するものを選択！",
            )
        with gr.Column(scale=1, min_width=160):
            word2vec_model_load_btn = gr.Button(
                "モデルをロード", variant="primary", size="lg", min_width=36
            )
    with gr.Row(variant="panel"):
        word2vec_loaded_model = gr.Textbox(label="ロードされたモデルのパス")

    with gr.Tab("ロードしたモデルの全語彙の一覧"):
        gr.Markdown(
            (
                "\n **ロードした単語分散表現のモデルの全語彙の一覧を表示** \n  "
                "\n・モデルを読み込むと自動的に↓に語彙のリストを表示します  "
                "\n・読み込んだWord2vecモデルの語彙に無い単語を入力するとエラーです。  "
                "\n・Gensimのkeyedvectorsのkey_to_indexから取得して表示しています。  "
                "\nhttps://stackoverflow.com/questions/"
                "66868221/gensim-3-8-0-to-gensim-4-0-0"
            )
        )
        word2vec_model_words_list = gr.Dataframe(label="モデルの全語彙の一覧")

    with gr.Tab("入力した単語とコサイン類似度上位の単語を出力"):
        with gr.Row():
            gr.Markdown(
                (
                    "\n **入力した単語リストに対して、コサイン類似度が上位の単語のランキングを出力** \n  "
                    "\n・「入力した単語と似ている単語200件のランキング」を表示します。  "
                    "\n・ポジティブはプラスの影響を、ネガティブはマイナスの影響を与えます  "
                    "\n・読み込んだWord2vecモデルの語彙に無い単語を入力するとエラーです。  "
                    "\n・単語(キー)のベクトルに関して色々と計算をした結果を出します。  "
                    "\n・詳細はGensimのdocの「gensim.models.keyedvectors."
                    "KeyedVectors.most_similar」をチェック！  "
                    "\n https://radimrehurek.com/"
                    "gensim/models/keyedvectors.html"
                    "#gensim.models.keyedvectors.KeyedVectors.most_similar  "
                )
            )
        with gr.Row():
            with gr.Column(scale=2):
                positive_word = gr.Dropdown(
                    label="プラスの影響を与える単語を入力！(ポジティブ)",
                    multiselect=True,
                    allow_custom_value=True,
                )
                negative_word = gr.Dropdown(
                    label="マイナスの影響を与える単語を入力！(ネガティブ)",
                    multiselect=True,
                    allow_custom_value=True,
                )

                examples = gr.Examples(
                    example_labels=[
                        "ポジティブ「りんご」",
                        "ポジティブ「王、女」・ネガティブ「男」",
                        "ポジティブ「マクドナルド」・ネガティブ「ハンバーガー」",
                        "ポジティブ「ハンバーガー」・ネガティブ「マクドナルド」",
                    ],
                    examples=[
                        [["りんご"], []],
                        [["王", "女"], ["男"]],
                        [["マクドナルド"], ["ハンバーガー"]],
                        [["ハンバーガー"], ["マクドナルド"]],
                    ],
                    inputs=[positive_word, negative_word],
                    label="クイック入力",
                )

            with gr.Column(scale=3):
                similarwords_btn = gr.Button(
                    "分散表現から似ている単語を出力！",
                    variant="primary",
                    interactive=False,
                )
                similar_result = gr.Dataframe(label="似ている単語の上位200個")

    with gr.Tab("2つの単語リストのコサイン類似度を出力"):
        with gr.Row():
            gr.Markdown(
                (
                    "\n **入力した2つの単語リストのコサイン類似度を出力** \n  "
                    "\n・「入力した2つの単語リストのコサイン類似度」を表示します。  "
                    "\n・読み込んだWord2vecモデルの語彙に無い単語を入力するとエラーです。  "
                    "\n・詳細はGensimのdocの「gensim.models.keyedvectors."
                    "KeyedVectors.n_similarity」をチェック！  "
                    "\n https://radimrehurek.com/"
                    "gensim/models/keyedvectors.html#"
                    "gensim.models.keyedvectors.KeyedVectors.n_similarity  "
                )
            )

        with gr.Row():
            with gr.Column(scale=2):
                target_words1 = gr.Dropdown(
                    label="単語リスト1を入力！",
                    multiselect=True,
                    allow_custom_value=True,
                )
                target_words2 = gr.Dropdown(
                    label="単語リスト2を入力",
                    multiselect=True,
                    allow_custom_value=True,
                )

                target_examples = gr.Examples(
                    example_labels=[
                        "りんご・バナナ",
                        "マクドナルド・ハンバーガー",
                        "「メロン・スイカ」・「野菜」",
                    ],
                    examples=[
                        [["りんご"], ["バナナ"]],
                        [["マクドナルド"], ["ハンバーガー"]],
                        [["メロン", "スイカ"], ["野菜"]],
                    ],
                    inputs=[target_words1, target_words2],
                    label="クイック入力",
                )

            with gr.Column(scale=3):
                two_words_sim_btn = gr.Button(
                    "2つの単語リストのコサイン類似度を出力",
                    variant="primary",
                    interactive=False,
                )
                two_words_sim_result = gr.Textbox()

    # GradioのUIのイベントリスナーを設定する ###############################################

    word2vec_model_load_btn.click(
        fn=gr_load_word2vec_model,
        inputs=[gradio_state, word2vec_model_select],
        outputs=word2vec_loaded_model,
    )

    word2vec_loaded_model.change(
        fn=ready_interactive,
        outputs=similarwords_btn,
    )

    word2vec_loaded_model.change(
        fn=ready_interactive,
        outputs=two_words_sim_btn,
    )

    word2vec_loaded_model.change(
        fn=gr_get_word2vec_model_words_list,
        inputs=[gradio_state],
        outputs=word2vec_model_words_list,
    )

    similarwords_btn.click(
        fn=gr_top_similar_words,
        inputs=[gradio_state, positive_word, negative_word],
        outputs=similar_result,
    )

    two_words_sim_btn.click(
        fn=gr_two_words_similar,
        inputs=[gradio_state, target_words1, target_words2],
        outputs=two_words_sim_result,
    )


main_app.launch(share=False)
main_app.launch(share=False)
