import os
import pandas as pd
import requests
from fontTools.ttLib import TTFont
import subprocess
from io import BytesIO
import zipfile
from bs4 import BeautifulSoup as bs
import asyncio
import shutil

async def run_extractor(urls: list[str]) -> bytes:
    fonts_save_path = "./fonts"
    list_of_paths = await download_all_apk(urls)
    data_to_save = [await process_apk(path_to_apk, fonts_save_path) for path_to_apk in list_of_paths]
    await create_csv_file(data_to_save)
    zip_file = await create_zip_file()
    shutil.rmtree("./fonts")
    [os.remove(file) for file in os.listdir('.') if file.endswith(".apk")]
    print(os.listdir())
    return zip_file


async def process_apk(path_to_apk: str, fonts_save_path:str) -> list[tuple[str, str, str, str]]:
    fonts = await find_and_save_fonts(path_to_apk, fonts_save_path)
    return [{"Name": path_to_apk, "File Name": font[0], "Font Name":  font[1], "Location": font[2]} for font in fonts]


async def download_all_apk(urls: list[str]) -> str:
    coros = [download_apk_file(url) for url in urls]
    list_of_app_paths = await asyncio.gather(*coros)
    return list_of_app_paths
    

async def download_apk_file(url:str ):
    url = await transform_link_to_apkpure(url)
    file_name = url.split("/")[-1] + ".apk"
    full_path = os.path.join("./", file_name)

    response = requests.get(url)
    with open(full_path, "wb") as file:
        file.write(response.content)
    return full_path

async def transform_link_to_apkpure(google_play_link: str) -> str:
    if "https://d.apkpure.net/b/APK/" in google_play_link:
        return google_play_link
    app_id = google_play_link.split("id=")[-1]
    return f"https://d.apkpure.net/b/APK/{app_id}?version=latest"


async def find_and_save_fonts(
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

        font_name = await get_font_name(temp_font_path)
        font_data.append((os.path.basename(font_file), font_name, original_location))

    return font_data


async def get_font_name(font_path: str) -> str:
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
    except Exception as exc:
        name = "NOT FOUND."
        pass
    return name

async def create_csv_file(data: list[tuple[str, str, str, str]]) -> None:
    merged_list = []
    for sublist in data:
        merged_list.extend(sublist)
    df = pd.DataFrame(merged_list)
    df.to_csv('fonts/summary.csv', index=False)


async def create_zip_file() -> bytes:
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


def __get_html_by_keyword(keyword: str) -> str:
    url = f"http://play.google.com/store/search?q={keyword}&c=apps"

    return requests.get(url).text


def collect_links_by_author(keyword: str) -> list[str]:
    """
    This function returns a list of google play store links of the apps that
    are written by the author

    :param keyword: The author's name
    """
    html = __get_html_by_keyword(keyword)
    parsed = bs(html, "html.parser")
    containers = parsed.select("a.Si6A0c")
    links = []
    for container in containers:
        href = container.get("href")
        if href is None:
            continue
        entries = container.select("div.cXFu1")
        span = entries[0].select("span")
        author = span[1].contents[0]
        if str(author).lower() == keyword.lower():
            id = href.split("id=")[-1]
            links.append(f"https://play.google.com/store/apps/details?id={id}")

    return links
