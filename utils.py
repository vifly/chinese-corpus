import os
from typing import Iterable, Iterator

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


def convert_trad_to_sim(texts: Iterable[str]) -> Iterator[str]:
    cc = opencc.OpenCC('t2s')
    sim_texts = (cc.convert(text) for text in texts)
    return sim_texts


def is_chinese(char: str):
    if u'\u4e00' <= char <= u'\u9fa5':
        return True
    else:
        return False


def replace_non_chinese_char_with_space(char):
    if is_chinese(char):
        return char
    return " "


def clean_texts(texts: Iterable[str]) -> Iterator[str]:
    for line in texts:
        yield "".join(map(replace_non_chinese_char_with_space, line))


def segment(texts: Iterable[str], split_symbol: str = " ") -> Iterator[str]:
    for text in texts:
        yield split_symbol.join((word for word in jieba.cut(text, cut_all=False)
                                 if word != " "))
