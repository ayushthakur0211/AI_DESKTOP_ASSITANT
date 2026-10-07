import os


def list_directory(path):
    try:
        items = []

        for item in sorted(os.listdir(path)):
            full_path = os.path.join(path, item)

            if os.path.isdir(full_path):
                items.append(("Folder", item, full_path))
            else:
                size = os.path.getsize(full_path)
                items.append(("File", item, size))

        return items

    except Exception as e:
        return [("Error", str(e), "")]


def open_file(path):
    try:
        os.startfile(os.path.abspath(path))
    except Exception as e:
        print(f"Error opening file: {e}")