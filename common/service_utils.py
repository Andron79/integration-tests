import logging
import os
import pathlib
import time
from pathlib import Path
from typing import Dict, Tuple
import zipfile
from selenium.webdriver.common.keys import Keys
from common.settings import download_default_directory


logger = logging.getLogger(__name__)


def overwrite_input(input_field, value, delay: float = 0.1):
    time.sleep(delay)
    input_field.send_keys(Keys.CONTROL + "a")
    time.sleep(delay)
    input_field.send_keys(Keys.DELETE)
    time.sleep(delay)
    input_field.send_keys(value)


def compare_data(
    local: dict, remote: dict, prefix: str = ""
) -> Dict[str, Tuple[str, str]]:
    """Сравнивает два словаря local и remote с учетом прочитанного префикса.

    :param local:
    :param remote:
    :param prefix:
    :return Возвращается словарь с различающимися ключами:
    """
    diff = {}
    for k in local:
        if (lv := local[k]) != (
            rv := remote.get(f"{f'{prefix}__' if prefix else ''}{k}", "<пусто>")
        ):
            diff[k] = (lv, rv)
    return diff


def file_exist(file: pathlib.Path) -> bool:
    return file.is_file()


def get_folders_from_archive(filepath: Path) -> list:
    """Возвращает список уникальных названий папок в архиве"""
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        return list(set([folder for folder in zip_ref.infolist() if folder.is_dir()]))


def extract_files_from_archive(filepath: pathlib.Path, zip_pass: str = None):
    """Разархивирование архива с файлами диагностики и последующее удаление
    архива.

    :param filepath: Файл архива с абсолютным путем.
    :param zip_pass: Пароль zip архива
    """

    if zip_pass:
        (Path(download_default_directory) / "data").mkdir(exist_ok=True, parents=True)
        os.system(f"7z x {str(filepath)} -p{zip_pass}")
    else:
        with zipfile.ZipFile(filepath, "r") as zip_ref:
            zip_ref.extractall(path=download_default_directory)
    filepath.unlink(missing_ok=True)


def empty_files_in_archive(filepath: pathlib.Path, zip_pass: str = None) -> list[Path]:
    """Проверка всех файлов в папке на нулевой размер.

    :param zip_pass: Пароль архива.
    :param filepath: Файл архива с абсолютным путем.
    :return: Список из пустых файлов.
    """
    folders = get_folders_from_archive(filepath)
    extract_files_from_archive(filepath=filepath, zip_pass=zip_pass)
    for folder_unpacked_result_files in folders:
        extracted_directory = Path(
            download_default_directory, folder_unpacked_result_files
        )
        return [
            entry
            for entry in extracted_directory.iterdir()
            if entry.is_file() and entry.stat().st_size == 0
        ]
