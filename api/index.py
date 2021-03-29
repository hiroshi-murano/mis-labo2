from flask import Flask, render_template, jsonify, request
from pprint import PrettyPrinter, pprint
import json
import requests
import random

# app = Flask(__name__)
app = Flask(__name__, static_folder='../static', template_folder='../')
app.config['JSON_AS_ASCII'] = False  # jsonを文字化けせずに返すため
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # キャッシュ無効にするため


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

    svg = ''

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



    # # f = open('../static/images/test.svg', 'w', encoding='utf8')
    # f = open('test.svg', 'w', encoding='utf8')
    # f.write(svg)
    # f.close()

    img_base64 = 'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4NCjwhLS0gR2VuZXJhdG9yOiBBZG9iZSBJbGx1c3RyYXRvciAxNi4wLjAsIFNWRyBFeHBvcnQgUGx1Zy1JbiAuIFNWRyBWZXJzaW9uOiA2LjAwIEJ1aWxkIDApICAtLT4NCjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+DQo8c3ZnIHZlcnNpb249IjEuMSIgaWQ9IkxheWVyXzEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiIHg9IjBweCIgeT0iMHB4Ig0KCSB3aWR0aD0iMTI2cHgiIGhlaWdodD0iMTI2cHgiIHZpZXdCb3g9IjAgMCAxMjYgMTI2IiBlbmFibGUtYmFja2dyb3VuZD0ibmV3IDAgMCAxMjYgMTI2IiB4bWw6c3BhY2U9InByZXNlcnZlIj4NCjxnPg0KCTxyZWN0IHg9IjEuMDk1IiB5PSI5OC4yMjQiIHdpZHRoPSIxMjMuODEiIGhlaWdodD0iMTkuMjc1Ii8+DQoJPHJlY3QgeD0iMS4wOTUiIHk9Ijg1Ljc0IiB3aWR0aD0iMTIzLjgxIiBoZWlnaHQ9IjUuMjA1Ii8+DQoJPHBhdGggZD0iTTE4LjQwNCw5NS43MjFjMC43NjcsMCwxLjM4OS0wLjYyMywxLjM4OS0xLjM5cy0wLjYyMi0xLjM4OC0xLjM4OS0xLjM4OEgzLjQ4MWMtMC43NjcsMC0xLjM4OCwwLjYyMS0xLjM4OCwxLjM4OA0KCQlzMC42MjIsMS4zOSwxLjM4OCwxLjM5SDE4LjQwNHoiLz4NCgk8cGF0aCBkPSJNNDQuNDMzLDk1LjcyMWMwLjc2NywwLDEuMzg4LTAuNjIzLDEuMzg4LTEuMzlzLTAuNjIyLTEuMzg4LTEuMzg4LTEuMzg4SDI5LjUxYy0wLjc2NywwLTEuMzg5LDAuNjIxLTEuMzg5LDEuMzg4DQoJCXMwLjYyMiwxLjM5LDEuMzg5LDEuMzlINDQuNDMzeiIvPg0KCTxwYXRoIGQ9Ik03MC40NjEsOTUuNzIxYzAuNzY3LDAsMS4zODgtMC42MjMsMS4zODgtMS4zOXMtMC42MjItMS4zODgtMS4zODgtMS4zODhINTUuNTM5Yy0wLjc2NywwLTEuMzg4LDAuNjIxLTEuMzg4LDEuMzg4DQoJCXMwLjYyMiwxLjM5LDEuMzg4LDEuMzlINzAuNDYxeiIvPg0KCTxwYXRoIGQ9Ik05Ni40OSw5NS43MjFjMC43NjcsMCwxLjM4OS0wLjYyMywxLjM4OS0xLjM5cy0wLjYyMi0xLjM4OC0xLjM4OS0xLjM4OEg4MS41NjdjLTAuNzY3LDAtMS4zODgsMC42MjEtMS4zODgsMS4zODgNCgkJczAuNjIyLDEuMzksMS4zODgsMS4zOUg5Ni40OXoiLz4NCgk8cGF0aCBkPSJNMTIyLjUxOSw5NS43MjFjMC43NjcsMCwxLjM4OS0wLjYyMywxLjM4OS0xLjM5cy0wLjYyMi0xLjM4OC0xLjM4OS0xLjM4OGgtMTQuOTIzYy0wLjc2NywwLTEuMzg4LDAuNjIxLTEuMzg4LDEuMzg4DQoJCXMwLjYyMiwxLjM5LDEuMzg4LDEuMzlIMTIyLjUxOXoiLz4NCgk8cGF0aCBkPSJNNy40MSw4MC45aDUzLjQ0MmMwLjg2MywwLDEuNTYyLTAuNjk5LDEuNTYyLTEuNTYyVjM5LjU0M2MwLTAuODYyLTAuNjk5LTEuNTYzLTEuNTYyLTEuNTYzSDQ1LjMxNHYtNi41MzkNCgkJYzAtMC44NjEtMC42OTgtMS41NjItMS41NjEtMS41NjJIMjMuNDI4Yy0wLjg2MywwLTEuNTYyLDAuNy0xLjU2MiwxLjU2MnY2LjU0SDcuNDFjLTAuODYyLDAtMS41NjIsMC43LTEuNTYyLDEuNTYzdjM5Ljc5NQ0KCQlDNS44NDgsODAuMjAxLDYuNTQ3LDgwLjksNy40MSw4MC45eiBNMzQuNDkyLDU3Ljg3NGgtMS43OTZ2LTYuNzY4aDEuNzk2VjU3Ljg3NHogTTI2LjU2MywzNC41NzRoMTQuMDU1djMuNDA2SDI2LjU2M1YzNC41NzR6DQoJCSBNMTAuNTQ0LDQyLjY3OGg0Ny4xNzN2MTEuOThIMzYuOTQydi00LjAwNmMwLTAuODYzLTAuNjk5LTEuNTYzLTEuNTYyLTEuNTYzaC0zLjU4MmMtMC44NjMsMC0xLjU2MiwwLjY5OS0xLjU2MiwxLjU2M3Y0LjAwNg0KCQlIMTAuNTQ0VjQyLjY3OHoiLz4NCgk8cGF0aCBkPSJNNjguNzM0LDgwLjloNDkuOTU4YzAuODA3LDAsMS40Ni0wLjY1MywxLjQ2LTEuNDZWMTcuNTM0YzAtMC44MDYtMC42NTMtMS40NTktMS40Ni0xLjQ1OWgtMTQuNTI0VjkuOTYxDQoJCWMwLTAuODA3LTAuNjUzLTEuNDYtMS40Ni0xLjQ2aC0xOWMtMC44MDcsMC0xLjQ2LDAuNjUzLTEuNDYsMS40NnY2LjExNUg2OC43MzRjLTAuODA3LDAtMS40NiwwLjY1My0xLjQ2LDEuNDU5Vjc5LjQ0DQoJCUM2Ny4yNzQsODAuMjQ3LDY3LjkyNyw4MC45LDY4LjczNCw4MC45eiBNODYuNjM4LDEyLjg5aDEzLjEzOXYzLjE4Nkg4Ni42MzhWMTIuODl6Ii8+DQo8L2c+DQo8L3N2Zz4NCg=='

    dictTemp = {'svg': svg}
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
