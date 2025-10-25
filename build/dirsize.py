import os


class Size:
    def __init__(self):
        self.volume = 0
        self.count_files = 0
        self.count_dirs = 0

    @staticmethod
    def get_size(bts, ending='B'):
        for item in ["", "K", "M", "G", "T", "P"]:
            if bts < 1024:
                return f"{bts:.2f} {item}{ending}"
            bts /= 1024
        return None

    def counting(self, size):
        self.volume += size

    def size_recurse(self, path):
        try:
            for file in os.scandir(path):
                if not file.is_dir(follow_symlinks=False):
                    self.count_files += 1
                    try:
                        self.counting(file.stat().st_size)
                    except:
                        continue
                else:
                    self.count_dirs += 1
                    self.counting(file.stat(follow_symlinks=False).st_size)
                    self.size_recurse(file.path)
            # print(f'\r{self.get_size(self.volume)} total, {self.count_dirs} directories and {self.count_files} '
            #       f'files...', end='')
            return self.volume
        except OSError:
            return None