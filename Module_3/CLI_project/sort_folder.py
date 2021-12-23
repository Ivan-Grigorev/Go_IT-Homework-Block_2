from pathlib import Path
import shutil


AVI_VIDEOS = []
MP4_VIDEOS = []
MOV_VIDEOS = []
MKV_VIDEOS = []
MP3_MUSIC = []
OGG_MUSIC = []
WAV_MUSIC = []
AMR_MUSIC = []
JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
DOC_DOC = []
DOCX_DOC = []
XLSX_DOC = []
PPTX_DOC = []
PDF_DOC = []
ZIP_ARCH = []
TAR_ARCH = []
OTHER = []

REGISTERED_EXT = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    'DOC': DOC_DOC,
    'DOCX': DOCX_DOC,
    'XLSX': XLSX_DOC,
    'PPTX': PPTX_DOC,
    'PDF': PDF_DOC,
    'ZIP': ZIP_ARCH,
    "TAR": TAR_ARCH,
    'MP4': MP4_VIDEOS,
    'AVI': AVI_VIDEOS,
    'MOV': MOV_VIDEOS,
    'MKV': MKV_VIDEOS,
    'MP3': MP3_MUSIC,
    'OGG': OGG_MUSIC,
    'WAV': WAV_MUSIC,
    'AMR': AMR_MUSIC,
    'OTHER': OTHER
}


def parse_folder(path: Path):
    for folder_item in path.iterdir():
        if folder_item.is_dir():
            if folder_item.name not in ['IMAGES', 'VIDEOS', 'DOCS', 'OTHER']:
                parse_folder(folder_item)
                continue
        else:
            ext = folder_item.suffix[1:]
            if ext.upper() in REGISTERED_EXT.keys():
                REGISTERED_EXT[ext.upper()].append(folder_item)
            else:
                REGISTERED_EXT['OTHER'].append(folder_item)
    return REGISTERED_EXT


def handle_file(root_path, file_path: Path):
    ext = file_path.suffix[1:].upper()
    if ext in ['JPG', 'SVG', 'PNG', 'JPEG']:
        category_folder = root_path / 'IMAGES'
    elif ext in ['DOC', 'DOCX', 'PPTX', 'PDF', 'XLSX']:
        category_folder = root_path / 'DOC'
    elif ext in ['TAR', 'ZIP', 'RAR']:
        category_folder = root_path / 'ARCH'
    elif ext in ['MP3', 'OGG', 'WAV', 'AMR']:
        category_folder = root_path / 'MUSIC'
    elif ext in ['MP4', 'AVI', 'MOV', 'MKV']:
        category_folder = root_path / 'VIDEOS'
    else:
        category_folder = root_path / 'OTHER'
    category_folder.mkdir(exist_ok=True)
    type_folder = category_folder / ext
    type_folder.mkdir(exist_ok=True)
    file_path.replace(type_folder / file_path.name)


def del_empty_folders(path: Path):
    for folder in path.iterdir():
        if folder.name not in ['IMAGES', 'DOCS', 'ARCH', 'OTHER', 'VIDEOS', 'MUSIC'] and folder.is_dir():
            shutil.rmtree(folder)


def sort_folder_command(file_path):
    reg_ext = parse_folder(Path(file_path))
    for item in reg_ext.values():
        for file in item:
            handle_file(Path(file_path), file)
        item.clear()
    del_empty_folders(Path(file_path))