"""
Bad and dirty translation scrapper, takes source files and tries to translate them
Strings extraction is about 80% effective. Besides, Google translate API (free one?) makes worse translations
in comparison to web ui. So manual work is still needed, but way less than fully manual
How to use:
Manually install googletrans==4.0.0rc1 in requirements
Scroll to the bottom and run 3 times:
- with check_translation_v1, check if the translation is needed
- with check_translation_v2, to translate, then copy-paste stdout to translate.py
- with check_translation_v1 again to check if everything is translated - add strings manually if needed
"""

from googletrans import Translator

from os import walk
from os.path import join
from app import translate

from translation_tz import timezone_translation
from translation import translation

root = 'C:\\Temp\\210620\\AC2100_Not_translated'


got_translations = set()


def check_translation_v1(file_read_loc):
    not_translated = True
    for ind, s in enumerate(file_read_loc.splitlines()):
        line_original = s.decode('UTF8')
        line_translated = translate(s, 'upgrade')[0]
        if not line_translated.isascii() and not line_translated.decode('UTF8').lstrip().startswith('//'):
            print(f"File {file_name}, Line {ind + 1} is not fully translated:")
            not_translated = False
            # print(line_original)
            together = False
            for sym in line_translated.decode('UTF8'):
                if sym.isascii() or sym == ' ':
                    if together:
                        i = 1
                        print(end='\n', flush=True)
                    together = False
                    continue
                else:
                    print(sym, end='')
                    together = True
            # print(line_translated.decode('UTF8'))
    if not_translated:
        print(f"File is {file_name} fully translated, skipping")


def print_translation(phrase):
    translator = Translator()
    result_en = translator.translate(phrase, dest='en', src='zh-cn')
    result_ru = translator.translate(result_en.text, dest='ru', src='en')
    print(f"'{phrase}': " + "{'en': '" + result_en.text + "', 'ru': '" + result_ru.text + "'},")


def check_translation_v2(file_read_loc):
    for ind, s in enumerate(file_read_loc.splitlines()):
        if not s.isascii() and not s.decode('UTF8').lstrip().startswith('//'):
            line = s.decode('UTF8')
            if '%:' in line:
                phrases = [ph.split('%')[0].strip() for ph in line.split('%:')[0::1]]
            elif '\'' in line:
                phrases = [ph.split('\'')[0].strip() for ph in line.split('\'')[0::1]]
            else:
                phrases = [ph.split('<')[0].strip() for ph in line.split('>')[0::1]]
            for phrase in phrases:
                if not phrase.isascii():
                    translated = False
                    if phrase.endswith('。') or phrase.endswith('：'):
                        phrase = phrase[0:-1]
                    if phrase.startswith('*'):
                        phrase = phrase[1:]
                    if phrase.isascii() or phrase in translation or phrase in timezone_translation:
                        translated = True
                    if not translated and phrase[0].isascii():
                        i = 0
                        while phrase[i].isascii():
                            i += 1
                        if phrase[i:] in translation or phrase[i:] in timezone_translation:
                            translated = True
                    if not translated and phrase[-1].isascii():
                        i = -1
                        while phrase[i].isascii():
                            i -= 1
                        i += 1
                        if phrase[:i] in translation or phrase[:i] in timezone_translation:
                            translated = True
                    if not translated:
                        i = 0
                        while phrase[i].isascii():
                            i += 1
                        j = -1
                        while phrase[j].isascii():
                            j -= 1
                        if j < -1:
                            phrase = phrase[i:j + 1]
                        else:
                            phrase = phrase[i:]
                    if phrase in translation or phrase in timezone_translation:
                        translated = True
                    global got_translations
                    if not translated and phrase not in got_translations:
                        #print(f"File {file_name}, string in Line {ind + 1} is not translated:")
                        #print(phrase)
                        print_translation(phrase)
                        got_translations.add(phrase)


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
            print(f"File is {file_name} fully in ascii, skipping")
            continue
        else:
            # run with check_translation_v1 first, then run with check_translation_v2 and again check_translation_v1
            check_translation_v1(file_read)


