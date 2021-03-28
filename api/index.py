from flask import Flask, render_template, jsonify, request
from pprint import PrettyPrinter, pprint
import json
import requests
import random

# app = Flask(__name__)
app = Flask(__name__, static_folder='../static', template_folder='../')
app.config['JSON_AS_ASCII'] = False  # jsonを文字化けせずに返すため
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 #キャッシュ無効にするため


@app.after_request
def add_header(r):
    """
    staticのsvgを変更してもキャッシュで画面が更新されないので、
    強制的にキャッシュを無効にする処理
    """

    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api_01')
def api_01():

    # print(request.args)

    # name = request.args.get('name', '')
    # print(name)


    svg = '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" >\n'

    xpos = 400
    for cnt in range(100):
        bar_length = random.randint(5, 80)

        svg += '<rect x="10" y="{}" width="390" height="50" stroke="black" fill="#FFFFAA" />\n'.format(
            cnt*50+50)
        svg += '<text x="20" y="{}" font-family="sans-serif"  font-size="24" >{} 北海道こんにちはabc123XYZ</text>\n'.format(
            cnt*50+90, bar_length)
        svg += '<rect x="{0}" y="{1}" width="{2}" height="30" stroke="black" fill="#AAFFFF" />\n'.format(
            xpos, cnt*50+60, bar_length)
        svg += '<line id="line1" x1="{0}" y1="{1}" x2="{2}" y2="{1}"  stroke="black"  stroke-width="1" stroke-dasharray="4 4"/>\n'.format(
            xpos, cnt*50+60, xpos + bar_length + 100)

        xpos += bar_length

    svg += '</svg>\n'


    # f = open('../static/images/test.svg', 'w', encoding='utf8')
    f = open('test.svg', 'w', encoding='utf8')
    f.write(svg)
    f.close()



    dictTemp = {}
    # dictTemp['data'] = 'データは{}です'.format(name)

    return jsonify(dictTemp)


def data_insert(listData, domain, app_id, api_token):
    """
    kintoneへのデータ挿入
    """

    url = "https://{}.cybozu.com/k/v1/records.json".format(domain)

    headers = {"X-Cybozu-API-Token": api_token,
               "Content-Type": "application/json"}

    listRecords = []
    for dictTemp in listData:
        dictData = {}
        for key, val in dictTemp.items():
            dictData[key] = {"value": val}

        listRecords.append(dictData)

    params = {
        "app": app_id,
        "records": listRecords
    }

    # pprint(params)
    resp = requests.post(url, json=params, headers=headers)
    # print(resp.text)


@app.route('/api_02', methods=["POST"])
def api_02():

    request_data = json.loads(request.data)

    # pprint(request_data)

    listData = []
    for row in request_data['rows']:
        # pprint(row)
        for cnt in range(5):
            if row[cnt+2] != "":
                sag = '{:02d}_{}'.format(row[0], row[1])
                dictTemp = {'作業NO': 1,
                            '作業': sag, '測定回': cnt+1, '時間': float(row[cnt+2])}
                listData.append(dictTemp)

    app_id = int(request_data['app_id'])
    domain = request_data['domain']
    api_token = request_data['api_token']

    data_insert(listData, domain, app_id, api_token)

    # print(request_data)

    dctData = {}
    # dctData['初期値'] = 'なし'
    # dctData['データ'] = request_data

    return jsonify({})


@app.route('/api_03', methods=["POST"])
def api_03():

    request_data = json.loads(request.data)

    pprint(request_data)

    request_data['追加データ'] = 'api_03で追加したデータ'

    return jsonify(request_data)


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
