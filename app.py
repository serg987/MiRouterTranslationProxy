import requests
import os

from flask import Flask, request, Response

from translation import translation, translation_keys_sorted, timezone_translation_keys_sorted, timezone_translation, \
    available_langs
from css_to_modify import css_to_modify, css_to_modify_keys

app = Flask(__name__, static_folder=None)
app.debug = False

router_ip_from_env = None
lang_from_env = None
if 'MI_ROUTER_IP' in os.environ:
    router_ip_from_env = os.environ['MI_ROUTER_IP']
if 'MI_ROUTER_TRANSLATION_LANG' in os.environ and os.environ['MI_ROUTER_TRANSLATION_LANG'] in available_langs:
    lang_from_env = os.environ['MI_ROUTER_TRANSLATION_LANG']

lang_zh_str = 'lang="zh"'
host = 'miwifi.com' if router_ip_from_env is None else router_ip_from_env
default_lang = 'en'
lang = default_lang if lang_from_env is None else lang_from_env
lang_is_explicitly_set = lang_from_env is not None
lang_from_header = default_lang


def check_path_for_lang(path):
    global lang_is_explicitly_set
    global lang
    path = path[:-1] if len(path) > 0 and path[-1] == '/' else path
    preferred_lang = path.split('/')[-1]
    if preferred_lang == 'resetlang':
        lang = default_lang
        lang_is_explicitly_set = False
        return '/'.join(path.split('/')[:-1])
    if preferred_lang in available_langs:
        lang = preferred_lang
        lang_is_explicitly_set = True
        return '/'.join(path.split('/')[:-1])
    return path


def get_language_from_header(header):
    global lang_from_header
    parsed_header = header.split(';')[0].split(',')[0].split('-')[0]
    if parsed_header in available_langs:
        lang_from_header = parsed_header


def make_post_request(request_l, url):
    data = request_l.form
    r_hdrs = dict(request_l.headers)
    if 'Origin' in r_hdrs:
        r_hdrs['Origin'] = f"http://{host}"
    if 'Referer' in r_hdrs:
        r_hdrs['Referer'] = f"http://{host}/{'/'.join(r_hdrs['Referer'].split('/')[3:])}"
    r_hdrs['Host'] = host
    request_to_router: requests.Response = requests.post(url, headers=r_hdrs, data=data)
    response: Response = Response(response=request_to_router.content, status=request_to_router.status_code)
    for k in request_to_router.headers:
        if k != 'Transfer-Encoding' and k != '{':
            response.headers[k] = request_to_router.headers[k]
    return response


def make_get_request(request_l, url):
    data = request_l.data
    r_hdrs = dict(request_l.headers)
    r_hdrs['Host'] = host
    request_to_router: requests.Response = requests.get(url, headers=r_hdrs, data=data)
    response: Response = Response(response=request_to_router.content, status=request_to_router.status_code)
    for k in request_to_router.headers:
        if k != 'Transfer-Encoding' and k != '{':
            response.headers[k] = request_to_router.headers[k]
    return response


def translate(text_list, url):
    page_name = url.split('/')[-1]
    lang_to_translate = lang if lang_is_explicitly_set else lang_from_header
    text_lines = [s.decode('UTF8') for s in text_list.splitlines()]
    for ind, row in enumerate(text_lines):
        if row.lstrip().startswith('//'):
            continue
        if lang_zh_str in row:
            row = row.replace(lang_zh_str, f'lang="{lang_to_translate}"')
            text_lines[ind] = row
        if row.isascii():
            continue
        if page_name == 'upgrade':
            for w in timezone_translation_keys_sorted:
                if w in row:
                    translation_str = timezone_translation[w][lang_to_translate] if \
                        lang_to_translate in timezone_translation[w] else timezone_translation[w][default_lang]
                    row = row.replace(w, translation_str)
        for w in translation_keys_sorted:
            if w in row:
                translation_str = translation[w][lang_to_translate] \
                    if lang_to_translate in translation[w] else translation[w][default_lang]
                row = row.replace(w, translation_str)
        text_lines[ind] = row
    out = '\n'.join(text_lines).encode('UTF-8')
    return [out]


# some CSS properties do not allow showing long texts. Trying to fix it
def modify_css(css_list, url):
    css_file_to_modify = None
    for k in css_to_modify_keys:
        if k in url:
            css_file_to_modify = k
    if css_file_to_modify is None:
        return [css_list]
    css_modify_list = css_to_modify[css_file_to_modify]
    for i_dict in css_modify_list:
        for k in i_dict:
            k_enc = k.encode("UTF8")
            if k_enc in css_list:
                css_list = css_list.replace(k_enc, i_dict[k].encode("UTF8"))
    return [css_list]


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def consume_request(path):
    path = check_path_for_lang(path)
    get_language_from_header(request.headers['Accept-Language'])
    if request.query_string == b'':
        url = f"http://{host}/{path}"
    else:
        url = f"http://{host}/{path}?{request.query_string.decode()}"
    if request.method == 'POST':
        response_from_router: Response = make_post_request(request, url)
    if request.method == 'GET':
        response_from_router: Response = make_get_request(request, url)
    if 'image' in request.headers['Accept'] and 'text' not in request.headers['Accept']:
        return response_from_router
    response_payload = response_from_router.response[0]
    if not response_payload.isascii() \
            and ('text/html' in response_from_router.content_type
                 or ('application/javascript' in response_from_router.content_type and 'static/js' in path)):
        response_from_router.response = translate(response_payload, url)
        response_from_router.content_length = sum(len(s) for s in response_from_router.response)
    if 'text/css' in response_from_router.content_type:
        response_from_router.response = modify_css(response_payload, url)
        response_from_router.content_length = sum(len(s) for s in response_from_router.response)
    return response_from_router
