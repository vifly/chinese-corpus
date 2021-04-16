import os

import jieba
import opencc
import requests


def download_file(url: str, storage_path: str, force_download: bool = False):
    """Download file at the given URL, can download large file.

    Args:
        url (str): File's URL
        storage_path (str): Download file storage path
        force_download (bool, optional): True if the file is exist and you want
        to overwrite it. Defaults to False.
    """
    if os.path.exists(storage_path) and not force_download:
        return
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(storage_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)


def convert_trad_to_sim(texts: list[str]) -> list[str]:
    cc = opencc.OpenCC('t2s')
    sim_texts = [cc.convert(text) for text in texts]
    return sim_texts


def is_chinese(char: str):
    if u'\u4e00' <= char <= u'\u9fa5':
        return True
    else:
        return False


def clean_texts(texts: list[str]) -> list[str]:
    only_chinese_texts = []
    for line in texts:
        only_chinese_texts.append("".join([c for c in line if is_chinese(c)]))

    return only_chinese_texts


def segment(texts: list[str], split_symbol: str = " ") -> list[str]:
    seg_texts = []
    for text in texts:
        seg_texts.append(split_symbol.join(jieba.cut(text, cut_all=False)) + "\n")

    return seg_texts
