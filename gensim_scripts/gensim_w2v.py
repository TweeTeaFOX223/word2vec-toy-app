import gensim
import polars as pl
# from gensim.models.fasttext import FastTextKeyedVectors


def most_sim_result_to_pldf(most_sim_result) -> pl.DataFrame:

    result_words = []
    result_cossim = []

    for word, cossim in most_sim_result:
        result_words.append(word)
        result_cossim.append(cossim)

    return pl.DataFrame(
        data={"単語": result_words, "コサイン類似度": result_cossim}
    ).with_row_index(
        offset=1  # 1から始まるインデックスのカラムを追加
    )


def word2vec_all_words_to_pldf(
    wordvec_model
) -> pl.DataFrame:
    word_data = []
    for word in (wordvec_model.key_to_index):
        word_data.append(word)

    words_df = pl.DataFrame(data={"単語": word_data}).with_row_index(
        offset=1  # 1から始まるインデックスのカラムを追加
    )

    return words_df


def check_word2vec_model_in_words(
        wordvec_model,
        target_words):

    exsist_words = []
    non_exsist_words = []

    # 入力された単語がモデルの語彙に存在する確認
    for target_word in target_words:
        if target_word in wordvec_model.key_to_index:
            exsist_words.append(target_word)
        else:
            non_exsist_words.append(target_word)

    return exsist_words, non_exsist_words


def gensim_wordvec_top_simword(
    wordvec_model,
        positive_words, negative_words
) -> pl.DataFrame:

    all_target_words = []

    if positive_words is None:
        positive_words = []
    if negative_words is None:
        negative_words = []

    all_target_words = [*positive_words, *negative_words]

    exsist_words, non_exsist_words = check_word2vec_model_in_words(
        wordvec_model,
        all_target_words
    )

    # 存在しなかった単語があったらリターン
    if len(non_exsist_words) >= 1:
        return pl.DataFrame(
            data={"エラー：モデルの語彙に存在しない単語が入力されました": non_exsist_words},
        )

    if positive_words == []:
        most_similar_vec = wordvec_model.most_similar(
            negative=negative_words, topn=200
        )
    # ネガティブワードがない場合はポジティブだけ表示
    elif negative_words == []:
        most_similar_vec = wordvec_model.most_similar(
            positive=positive_words, topn=200
        )
    else:
        most_similar_vec = wordvec_model.most_similar(
            positive=positive_words, negative=negative_words, topn=200
        )

    return most_sim_result_to_pldf(most_similar_vec)


def gensim_wordvec_two_words_sim(
    wordvec_model,
        target_words1, target_words2
):

    print("あああ", target_words1, target_words2)
    all_target_words = [*target_words1, *target_words2]

    exsist_words, non_exsist_words = check_word2vec_model_in_words(
        wordvec_model,
        all_target_words
    )

    # 存在しなかった単語があったらリターン
    if len(non_exsist_words) >= 1:
        return pl.DataFrame(
            data={"エラー：モデルの語彙に存在しない単語が入力されました": non_exsist_words}
        )

    # https://tedboy.github.io/nlps/generated/generated/gensim.models.Word2Vec.n_similarity.html#gensim.models.Word2Vec.n_similarity
    cos_similarity = wordvec_model.n_similarity(target_words1, target_words2)
    return cos_similarity


if __name__ == "__main__":

    wordvec_model = gensim.models.KeyedVectors.load_word2vec_format(
        "./gensim_scripts/word2vec_models/vector_neologd/model.bin",
        binary=True
    )
    # wordvec_model: FastTextKeyedVectors = \
    #     gensim.models.fasttext.load_facebook_model(
    #         "./gensim_scripts/fasttext-models/fasttext-157lang/cc.ja.300.bin"
    #     ).wv

    print(word2vec_all_words_to_pldf(wordvec_model))

    print(type(wordvec_model))

    sample1_posi, sample1_nega = "マクドナルド", "ハンバーガー"
    sample1_posi, sample1_nega = ["王", "女"], ["男"]

    result_df = gensim_wordvec_top_simword(
        wordvec_model, sample1_posi, sample1_nega)
    print(result_df)

    result_cossim = gensim_wordvec_two_words_sim(
        wordvec_model, sample1_posi, sample1_nega)
    print(result_cossim)
