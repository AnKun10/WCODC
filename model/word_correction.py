import streamlit as st


class WordCorrection:
    def __init__(self):
        self.__file_path = "E:/Workspaces/My Projects/WCODC/dataset/vocab.txt"

    def __load_vocab(self) -> list:
        with open(self.__file_path, "r") as f:
            lines = f.readlines()
        words = sorted(set([line.strip().lower() for line in lines]))
        return words

    def __levenshtein(self, token1: str, token2: str) -> int:
        distances = [[0] * (len(token2) + 1) for _ in range(len(token1) + 1)]

        for t1 in range(len(token1) + 1):
            distances[t1][0] = t1

        for t2 in range(len(token2) + 1):
            distances[0][t2] = t2

        a, b, c = 0, 0, 0

        for t1 in range(1, len(token1) + 1):
            for t2 in range(1, len(token2) + 1):
                if token1[t1 - 1] == token2[t2 - 1]:
                    distances[t1][t2] = distances[t1 - 1][t2 - 1]
                else:
                    a = distances[t1][t2 - 1]
                    b = distances[t1 - 1][t2]
                    c = distances[t1 - 1][t2 - 1]

                    distances[t1][t2] = min(a, b, c) + 1
        return distances[-1][-1]

    def display(self):
        st.title("Word Correction using Levenshtein Distance")
        word = st.text_input('Word:')
        vocabs = self.__load_vocab()

        if st.button("Compute"):
            # Compute Levenshtein Distance
            leven_distances = dict()
            for vocab in vocabs:
                leven_distances[vocab] = self.__levenshtein(word, vocab)

            # Sorted by distance
            sorted_distances = dict(sorted(leven_distances.items(), key=lambda x: x[1]))
            correct_word = list(sorted_distances.keys())[0]

            col1, col2 = st.columns(2)
            col1.write('Vocabulary:')
            col1.write(vocabs)

            col2.write('Distances:')
            col2.write(sorted_distances)

