def reInterpreter(name):
    import os
    os.system('python -m PyQt5.uic.pyuic ' + name + '.ui -o ' + name + '.py')


if __name__ == '__main__':
    reInterpreter('untitled')  # ui文件名，不包括后缀s
