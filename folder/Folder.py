class Folder:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.folders = []

    def add_page(self, page):
        self.files.append(page)

    def add_pages(self, pages):
        self.files.extend(pages)
    
    def add_folder(self, folder):
        self.folders.append(folder)  # Fixed the typo here

    def add_folders(self, folders):
        self.folders.extend(folders)


class File:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content
