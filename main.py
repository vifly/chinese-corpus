from sc_wiki import get_sc_wiki_corpus


def main():
    sc_wiki_corpus = get_sc_wiki_corpus("./")
    corpus = sc_wiki_corpus
    output_path = "./corpus.txt"

    with open(output_path, "w") as f:
        f.writelines(corpus)


if __name__ == "__main__":
    main()
