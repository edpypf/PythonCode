class FileWithLogging:
    def __init__(self, file):
        self.file = file

    def writelines(self, strings):
        self.file.writelines(strings)
        print(f'wrote {len(strings)} lines')

    def __iter__(self):
        return iter(self.file)

    def __next__(self):
        return next(self.file)

    def __getattr__(self, item):
        return getattr(self.file, item)

    def __setattr__(self, key, value):
        if key == 'file':
            super().__setattr__(key, value)
        else:
            setattr(self.file, key, value)

    def __delattr__(self, item):
        delattr(self.file, item)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()


if __name__ == '__main__':
    with open('hello.txt', 'w') as f:
        file = FileWithLogging(f)
        file.writelines(['hello\n', 'world\n'])
        file.write('testing\n')
