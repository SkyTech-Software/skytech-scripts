import os
import pandas as pd
import requests
from fontTools.ttLib import TTFont
import subprocess
from io import BytesIO
import zipfile
import shutil
from typing import Any


def run_extractor(urls: list[str]) -> bytes:
    fonts_save_path = "./fonts"
    list_of_paths = download_all_apk(urls)
    data_to_save = [
        process_apk(path_to_apk, fonts_save_path) for path_to_apk in list_of_paths
    ]
    create_csv_file(data_to_save)
    zip_file = create_zip_file()
    remove_files()
    return zip_file


def remove_files() -> None:
    for file in os.listdir("."):
        if file.endswith(".apk"):
            os.remove(file)
    shutil.rmtree("./fonts")


def process_apk(path_to_apk: str, fonts_save_path: str) -> list[dict[str, Any]]:
    fonts = find_and_save_fonts(path_to_apk, fonts_save_path)
    return [
        {
            "Name": path_to_apk,
            "File Name": font[0],
            "Font Name": font[1],
            "Location": font[2],
        }
        for font in fonts
    ]


def download_all_apk(urls: list[str]) -> list[str]:
    list_of_app_paths = [download_apk_file(url) for url in urls]
    return list_of_app_paths


def download_apk_file(url: str) -> str:
    url = transform_link_to_apkpure(url)
    file_name = url.split("/")[-1] + ".apk"
    full_path = os.path.join("./", file_name)

    response = requests.get(url)
    with open(full_path, "wb") as file:
        file.write(response.content)
    return full_path


def transform_link_to_apkpure(google_play_link: str) -> str:
    if "https://d.apkpure.net/b/APK/" in google_play_link:
        return google_play_link
    app_id = google_play_link.split("id=")[-1]
    return f"https://d.apkpure.net/b/APK/{app_id}?version=latest"


def find_and_save_fonts(
    apk_path: str, fonts_save_path: str
) -> list[tuple[str, str, str]]:
    apk_name = os.path.splitext(os.path.basename(apk_path))[0]
    specific_font_path = os.path.join(fonts_save_path, apk_name)
    os.makedirs(specific_font_path, exist_ok=True)

    font_data = []
    cmd = ["aapt", "list", apk_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    lines = result.stdout.splitlines()
    font_files = [
        line
        for line in lines
        if line.endswith(".ttf")
        or line.endswith(".otf")
        or line.endswith(".woff")
        or line.endswith(".woff2")
        or line.endswith(".eot")
        or line.endswith(".svg")
    ]

    for font_file in font_files:
        original_location = font_file
        temp_font_path = os.path.join(specific_font_path, os.path.basename(font_file))
        unzip_cmd = [
            "unzip",
            "-j",
            "-qq",
            "-n",
            apk_path,
            font_file,
            "-d",
            specific_font_path,
        ]
        subprocess.run(unzip_cmd)

        font_name = get_font_name(temp_font_path)
        font_data.append((os.path.basename(font_file), font_name, original_location))

    return font_data


def get_font_name(font_path: str) -> str:
    name = ""
    try:
        font = TTFont(font_path)
        for record in font["name"].names:
            if record.nameID == 4 and not name:
                if b"\x00" in record.string:
                    name = record.string.decode("utf-16-be")
                else:
                    name = record.string.decode("latin-1")
                break
    except Exception:
        name = "NOT FOUND."
        pass
    return name


def create_csv_file(data: list[list[dict[str, Any]]]) -> None:
    merged_list: list[dict[str, Any]] = []
    for sublist in data:
        merged_list.extend(sublist)
    df = pd.DataFrame(merged_list)
    df.to_csv("fonts/summary.csv", index=False)


def create_zip_file() -> bytes:
    folder_path = "fonts"
    buffer = BytesIO()
    with zipfile.ZipFile(
        buffer, "w", compression=zipfile.ZIP_DEFLATED, strict_timestamps=False
    ) as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(
                    file_path,
                    arcname=os.path.relpath(file_path, folder_path),
                )
    return buffer.getvalue()


def collect_links_by_author(keywords: list[str]) -> list[str]:
    result = []
    for keyword in keywords:
        out = subprocess.check_output(
            ["node", "/app/wrappers/google-play-scraper-wrapper/src/index.js", keyword]
        )

        for line in out.decode("utf-8").split("\n"):
            if line != "":
                result.append(f"https://d.apkpure.net/b/APK/{line}?version=latest")

    return result
