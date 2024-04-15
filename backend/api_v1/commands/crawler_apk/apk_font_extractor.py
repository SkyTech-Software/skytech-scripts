import os
import pandas as pd
import requests
from fontTools.ttLib import TTFont
import subprocess
from io import BytesIO, StringIO
import zipfile
import shutil
import re
from typing import Any
from uuid import uuid4
from backend.db.logging import add_log


font_data_mapping = {
    0:'Copyright',
    4 : 'Font Name',
    5 : 'Version',
    8 : 'Manufacturer',
    9 : 'Designer',
    11 : 'Designer URL',
    13 : 'License',
    14 : 'License Info URL',
}


def run_extractor(urls: list[str]) -> tuple[bytes, str]:
    work_dir = f"./{uuid4()}"
    fonts_save_path = f"{work_dir}/fonts"
    os.makedirs(fonts_save_path)
    data_to_save = []
    for url in urls:
        if not isinstance(url, list):
            path_to_apk = download_apk_file(url, work_dir)
            data_to_save.append(process_apk(path_to_apk, fonts_save_path))
            os.remove(path_to_apk) if path_to_apk else None
        else:
            data_to_save.append(url)
    csv_file = create_csv_file(data_to_save, work_dir)
    zip_file = create_zip_file(work_dir)
    shutil.rmtree(work_dir)
    return zip_file, csv_file


def process_apk(path_to_apk: str | None, fonts_save_path: str) -> list[dict[str, Any]]:
    if path_to_apk:
        fonts = find_and_save_fonts(path_to_apk, fonts_save_path)
        return [
            font
            for font in fonts
        ]
    return []


def download_apk_file(url: str, work_dir: str) -> str | None:
    try:
        url = transform_link_to_apkpure(url)
        response = requests.get(url)
        match = re.search(
            r"(?<=filename=\").*?(?=\")", response.headers["Content-Disposition"]
        )
        filename = match.group() if match else ""
        full_path = os.path.join(work_dir, filename)
        with open(full_path, "wb") as file:
            file.write(response.content)
        return full_path
    except Exception as e:
        add_log("filename", "Failed to download/save .apk", url, None, str(e))
        return None


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
    ]

    for font_file in font_files:
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

        font_data.append(extract_additional_data_from_font(temp_font_path, font_file, apk_name))

    return font_data


def extract_additional_data_from_font(temp_font_path: str, font_file: str, apk_name: str):
    data = {}
    data.update({'Name': apk_name, 'File Name': os.path.basename(font_file), 'Location': font_file})
    try:
        font = TTFont(temp_font_path)
        for record in font["name"].names:
            if b"\x00" in record.string:
                data.update({font_data_mapping.get(record.nameID, f"UNKNOW: {record.nameID}"): record.string.decode("utf-16-be")})
            else:
                data.update({font_data_mapping.get(record.nameID, f"UNKNOW: {record.nameID}"): record.string.decode("latin-1")})
    except Exception:
        pass
    return data


def create_csv_file(data: list[list[dict[str, Any]]], work_dir: str) -> str:
    merged_list: list[dict[str, Any]] = []
    for sublist in data:
        merged_list.extend(sublist)
    if not merged_list:
        merged_list.append({"0": "Nie znaleziono czcionek"})
    df = pd.DataFrame(merged_list)
    df.to_csv(f"{work_dir}/fonts/summary.csv", index=False)
    in_memory_csv = StringIO()
    df.to_csv(in_memory_csv, index=False)
    csv_string = in_memory_csv.getvalue()
    return csv_string


def create_zip_file(work_dir: str) -> bytes:
    folder_path = f"{work_dir}/fonts"
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
        apps_by_keyword = []
        out = subprocess.check_output(
            ["node", "/app/wrappers/google-play-scraper-wrapper/src/index.js", keyword]
        )

        for line in out.decode("utf-8").split("\n"):
            if line != "":
                link = f"https://d.apkpure.net/b/APK/{line}?version=latest"
                apps_by_keyword.append(link)
                result.append(link)

        if not apps_by_keyword:
            result.append(
                [
                    {
                        "Name": keyword,
                        "File Name": "Developer Not Found",
                        "Font Name": "Developer Not Found",
                        "Location": "Developer Not Found",
                    }
                ]
            )
    return result
