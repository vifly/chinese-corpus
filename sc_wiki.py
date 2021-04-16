import os

from gensim.corpora import WikiCorpus

from utils import download_file, convert_trad_to_sim, clean_texts, segment

WIKI_FILE_NAME = "zhwiki-latest-pages-articles.xml.bz2"


def download_latest_wiki(storage_dir: str, force_download: bool):
    url = "https://dumps.wikimedia.org/zhwiki/latest/" + WIKI_FILE_NAME
    download_file(url, os.path.join(storage_dir, WIKI_FILE_NAME), force_download)


def get_wiki_original_text(wiki_dump_path: str) -> list[str]:
    wiki = WikiCorpus(wiki_dump_path, dictionary=[])
    text_list = [" ".join(t) for t in wiki.get_texts()]

    return text_list


def get_sc_wiki_corpus(storage_dir: str = "/tmp", force_download: bool = False,
                       seg_split_symbol: str = " ") -> list[str]:
    download_latest_wiki(storage_dir, force_download)
    texts = get_wiki_original_text(os.path.join(storage_dir, WIKI_FILE_NAME))
    sc_texts = convert_trad_to_sim(texts)
    only_sc_texts = clean_texts(sc_texts)
    seg_texts = segment(only_sc_texts, seg_split_symbol)

    return seg_texts
