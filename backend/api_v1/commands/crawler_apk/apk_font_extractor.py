import os
import csv
import requests
from fontTools.ttLib import TTFont
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
import zipfile
from fastapi.exceptions import HTTPException


def run_extractor(urls: list[str]) -> bytes:
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(process_apk, url): url for url in urls}
        for future in as_completed(future_to_url):
            try:
                data = future.result()
                create_csv_file(data)
                zip_file = create_zip_file()
            except Exception as exc:
                raise HTTPException(
                    status_code=500, detail=f"Failed to fetch fonts: {str(exc)}"
                )
        return zip_file


def process_apk(target_url: str) -> list[tuple[str, str, str, str]]:
    save_path = "./"
    fonts_save_path = "./fonts"
    apk_file_name = download_apk(target_url, save_path)
    fonts = find_and_save_fonts(apk_file_name, fonts_save_path)
    return [(target_url, font[0], font[1], font[2]) for font in fonts]


def download_apk(url: str, save_path: str) -> str:
    url = transform_link_to_apkpure(url)
    file_name = url.split("/")[-1] + ".apk"
    full_path = os.path.join(save_path, file_name)

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
        unzip_cmd = ["unzip", "-j", "-q", apk_path, font_file, "-d", specific_font_path]
        subprocess.run(unzip_cmd)

        font_name = get_font_name(temp_font_path)
        font_data.append((os.path.basename(font_file), font_name, original_location))

    return font_data


def get_font_name(font_path: str) -> str:
    font = TTFont(font_path)
    name = ""
    for record in font["name"].names:
        if record.nameID == 4 and not name:
            if b"\x00" in record.string:
                name = record.string.decode("utf-16-be")
            else:
                name = record.string.decode("latin-1")
            break
    return name


def create_csv_file(data: list[tuple[str, str, str, str]]) -> None:
    with open("fonts/summary.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL/Name", "File Name", "Font Name", "Location"])
        for row in data:
            writer.writerow(row)


def create_zip_file() -> bytes:
    folder_path = "fonts"
    buffer = BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(
                    file_path, arcname=os.path.relpath(file_path, folder_path)
                )
    return buffer.getvalue()
