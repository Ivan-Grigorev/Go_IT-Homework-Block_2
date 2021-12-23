import concurrent.futures
from pathlib import Path
import threading
import shutil


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


def parse_folder(path: Path):
    for folder_item in path.iterdir():
        if folder_item.is_dir():
            if folder_item.name not in ['ARCH', 'DOCS', 'IMAGES', 'VIDEO', 'MUSIC', 'OTHER']:
                parse_folder(folder_item)
                continue
        else:
            ext = folder_item.suffix[1:]
            if ext.upper() in REGISTERED_EXT.keys():
                REGISTERED_EXT[ext.upper()].append(folder_item)
            else:
                REGISTERED_EXT['OTHER'].append(folder_item)
    return REGISTERED_EXT


def handle_file(root_path, paths_list):
    for file_type in paths_list:
        for file_path in file_type:
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
            file_path.replace(type_folder / file_path.name)


def del_empty_folders(path_file: Path):
    for folder in path_file.iterdir():
        if folder.name not in ['IMAGES', 'DOCS', 'ARCH', 'OTHER', 'VIDEO', 'MUSIC'] and folder.is_dir():
            shutil.rmtree(folder)


if __name__ == "__main__":
    path = Path('trash')
    parse_folder(path)
    del_empty_folders(path)

    print(f"Sorting folder {path}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        executor.map(handle_file, (path for i in range(6)), (ARCH, DOCS, IMAGES, VIDEO, MUSIC, OTHER))
