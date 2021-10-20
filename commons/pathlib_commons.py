from pathlib import Path


def get_all_files(relative_path):
    file_list = []
    directory = Path(relative_path)

    for item in directory.iterdir():
        if item.is_file():
            file_list.append(str(item))

    return file_list


def get_filename(relative_path, strip_extension=True):
    filename = str(relative_path).split('\\')[-1]
    if strip_extension:
        return filename.split('.')[0]
    return filename


def delete_file(relative_path):
    Path(relative_path).unlink()
