import gensim
import polars as pl
from gensim.models.fasttext import FastTextKeyedVectors


def fasttext_all_words_to_pldf(fasttext_model: FastTextKeyedVectors):
    word_data = []
    for word in fasttext_model.key_to_index:
        word_data.append(word)

    words_df = pl.DataFrame(data={"単語": word_data}).with_row_index(
        offset=1  # 1から始まるインデックスのカラムを追加
    )

    return words_df


def check_fasttext_model_in_words(fasttext_model: FastTextKeyedVectors, target_words):
    exsist_words = []
    non_exsist_words = []

    # 入力された単語がモデルの語彙に存在する確認
    for target_word in target_words:
        if target_word in fasttext_model.key_to_index:
            exsist_words.append(target_word)
        else:
            non_exsist_words.append(target_word)

    return exsist_words, non_exsist_words


if __name__ == "__main__":
    wordvec_model: FastTextKeyedVectors = gensim.models.fasttext.load_facebook_model(
        "./model_files/fasttext-models/fasttext-157lang/cc.ja.300.bin"
    ).wv

    print(type(wordvec_model))

    print(fasttext_all_words_to_pldf(wordvec_model))

    # similarities = wordvec_model.wv.most_similar(
    #     positive=['computer', 'human'], negative=['interface'])
    # most_similar = similarities[0]

    # print(similarities)
    # print(most_similar)
