from pathlib import Path
import asyncio
import aiopath
import shutil
import sys


AVI = []
AMR = []
DOC = []
DOCX = []
JPEG = []
JPG = []
MP4 = []
MOV = []
MKV = []
MP3 = []
OGG = []
OTHER = []
PPTX = []
PDF = []
PNG = []
RAR = []
SVG = []
TAR = []
WAV = []
XLSX = []
ZIP = []


REGISTERED_EXT = {
    'AVI': AVI,
    'AMR': AMR,
    'DOC': DOC,
    'DOCX': DOCX,
    'JPEG': JPEG,
    'JPG': JPG,
    'MP4': MP4,
    'MOV': MOV,
    'MKV': MKV,
    'MP3': MP3,
    'OTHER': OTHER,
    'OGG': OGG,
    'PNG': PNG,
    'PPTX': PPTX,
    'PDF': PDF,
    'RAR': RAR,
    'SVG': SVG,
    'TAR': TAR,
    'WAV': WAV,
    'XLSX': XLSX,
    'ZIP': ZIP,
}

ARCH = [TAR, ZIP, RAR]
DOCS = [DOC, DOCX, PPTX, PDF, XLSX]
IMAGES = [JPG, JPG, PNG, SVG]
VIDEO = [MKV, MOV, MP4]
MUSIC = [AMR, MP3, WAV, OGG]
OTHER = [OTHER]


async def parse_folder(path: Path):
    path = aiopath.AsyncPath(path)
    async for folder_item in path.iterdir():
        is_folder = await folder_item.is_dir()
        if is_folder:
            if folder_item.name not in ['ARCH', 'DOCS', 'IMAGES', 'VIDEO', 'MUSIC', 'OTHER']:
                await parse_folder(folder_item)
                continue
        else:
            ext = folder_item.suffix[1:]
            if ext.upper() in REGISTERED_EXT.keys():
                REGISTERED_EXT[ext.upper()].append(folder_item)


async def handle_file(root_path, file_path: Path):
    ext = file_path.suffix[1:].upper()
    if ext in ['JPG', 'SVG', 'PNG', 'JPEG']:
        category_folder = root_path / 'IMAGES'
    elif ext in ['DOC', 'DOCX', 'PPTX', 'PDF', 'XLSX']:
        category_folder = root_path / 'DOCS'
    elif ext in ['TAR', 'ZIP', 'RAR']:
        category_folder = root_path / 'ARCH'
    elif ext in ['MP3', 'OGG', 'WAV', 'AMR']:
        category_folder = root_path / 'MUSIC'
    elif ext in ['MP4', 'AVI', 'MOV', 'MKV']:
        category_folder = root_path / 'VIDEO'
    else:
        category_folder = root_path / 'OTHER'
    category_folder.mkdir(exist_ok=True)
    type_folder = category_folder / ext
    type_folder.mkdir(exist_ok=True)
    await file_path.replace(type_folder / file_path.name)


async def del_empty_folders(path_file: Path):
    async for folder in path_file.iterdir():
        if folder.name not in ['IMAGES', 'DOCS', 'ARCH', 'OTHER', 'VIDEO', 'MUSIC'] and folder.is_dir():
            shutil.rmtree(folder)


async def sort_folder_command(file_path):
    async for item in REGISTERED_EXT.values():
        print(item)


async def main(path):
    await parse_folder(path)

    for items in REGISTERED_EXT.values():
        for item in items:
            await handle_file(path, item)


if __name__ == '__main__':
    path = sys.argv[1]
    sort_folder = Path(path)
    asyncio.run(main(sort_folder.resolve()))
