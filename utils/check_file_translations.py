from os import walk
from os.path import join
from app import translate

root = 'C:\\Temp\\210620\\1\\www'

if __name__ == '__main__':
    file_list = []
    for path, subdirs, files in walk(root):
        for name in files:
            file_list.append(join(path, name))
    # print(file_list)

    for file_name in file_list:
        if file_name.endswith('.ico') or \
                file_name.endswith('.png') or \
                file_name.endswith('.jpg') or \
                file_name.endswith('.gif') or \
                file_name.endswith('.eot') or \
                file_name.endswith('.woff') or \
                file_name.endswith('.ttf') or \
                file_name.endswith('.woff2') or \
                file_name.endswith('.css') or \
                file_name.endswith('28.6bcc3380c67338da872d.js') or \
                file_name.endswith('26.4f6ae9841eb539c68754.js') or \
                file_name.endswith('24.5c04087d063557ee2c1c.js'):
            continue
        # print(f"File name: {file_name}")
        file = open(file_name, 'rb')
        file_read = file.read()
        file.close()
        if file_read.decode('UTF8').isascii():
            continue
            # print("File is fully in ascii, skipping")
        else:
            for ind, s in enumerate(file_read.splitlines()):
                line_original = s.decode('UTF8')
                line_translated = translate(s, 'upgrade')[0]
                if not line_translated.isascii() and not line_translated.decode('UTF8').lstrip().startswith('//'):
                    print(f"File {file_name}, Line {ind + 1} is not fully translated:")
                    #print(line_original)
                    together = False
                    for sym in line_translated.decode('UTF8'):
                        if sym.isascii() or sym == ' ':
                            if together:
                                print(end='\n', flush=True)
                            together = False
                            continue
                        else:
                            print(sym, end='')
                            together = True
                    #print(line_translated.decode('UTF8'))

