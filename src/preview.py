# -------------------------------------------------
# preview.py
# This program for previewing the output results of structure processing programs in RDE in a browser.
# 
# Copyright (c) 2025, MDPF(Materials Data Platform), NIMS
#
# This software is released under the MIT License.
# -------------------------------------------------

import sys
import shutil
import traceback
from datetime import datetime
from pathlib import Path
import json
import itertools
import webbrowser

# 出力ファイルを極力圧縮したい場合はTrueにする
COMPRESS = False

class Terms:
    """ 試料用語の定義 """

    def __init__(self):
        self.general_sample_term = {
            "0aadfff2-37de-411f-883a-38b62b2abbce":{"ja":"化学組成","en":"Chemical composition"},
            "5e166ac4-bfcd-457a-84bc-8626abe9188f":{"ja":"購入元","en":"Supplier"},
            "33c6e9dc-5787-0f96-7683-f39281c60419":{"ja":"化学式、組成式、分子式など","en":"Chemical formula, composition formula, molecular formula, etc."},
            "f2d5e89e-01f0-66a2-5d8e-623a4fc31698":{"ja":"物質名","en":"Material name"},
            "a7a6fc7b-ed46-88b0-bba8-a1e34857a049":{"ja":"試料別名","en":"Another sample name"},
            "0d0417a3-3c3b-496a-b0fb-5a26f8a74166":{"ja":"ロット番号、製造番号など","en":"Lot number or product number etc"},
            "e2d20d02-2e38-2cd3-b1b3-66fdb8a11057":{"ja":"CAS番号","en":"CAS Number"},
            "1e70d11d-cbdd-bfd1-9301-9612c29b4060":{"ja":"試料購入日","en":"Purchase date"},
            "1d3cab05-3eaa-cb9b-9a3f-20eb0ca26963":{"ja":"結晶状態","en":"Crystalline state"},
            "efcf34e7-4308-c195-6691-6f4d28ffc9bb":{"ja":"結晶構造","en":"Crystal structure"},
            "e9617207-7f74-ef45-9b05-74eef6e4ecbb":{"ja":"ピアソン記号","en":"Pearson symbol"},
            "f63149a4-e57c-4273-4c1e-dffa41356d28":{"ja":"空間群","en":"Space group"},
            "7cc57dfb-8b70-4b3a-5315-fbce4cbf73d0":{"ja":"試料形状","en":"Sample shape"},
            "dc27a956-263e-f920-e574-5beec912a247":{"ja":"分子量","en":"molecular weight"},
            "efc6a0d5-313e-1871-190c-baaff7d1bf6c":{"ja":"SMILES String","en":"SMILES String"},
            "3edadcff-8a85-51d9-708f-8f76bf055377":{"ja":"InChI key","en":"InChI key"},
            "0444cf53-db47-b208-7b5f-54429291a140":{"ja":"試料分類","en":"Sample type"},
            "fc30c31d-12a3-591a-c837-4f06ab458de0":{"ja":"生物種","en":"Taxonomy"},
            "9a23002a-c398-e521-081a-24b6cd32dbbd":{"ja":"細胞株","en":"Cell line"},
            "b4ce4016-e2bf-e5a1-7cae-ed496c7a776f":{"ja":"タンパク名","en":"Protein name"},
            "8c9b1a88-1530-24d3-4b2e-5441eee5c24f":{"ja":"遺伝子名","en":"Gene name"},
            "047e30f3-f294-e58d-cbe4-6bb588bf4cf8":{"ja":"NCBIアクセッション番号","en":"NCBI accession number"},
            "3adf9874-7bcb-e5f8-99cb-3d6fd9d7b55e":{"ja":"一般名称","en":"General name"},
            "9270879d-d94e-4d3f-2d5c-19568e040004":{"ja":"InChI","en":"InChI"}
        }

        self.sample_class = {
            "01cb3c01-37a4-5a43-d8ca-f523ca99a75b":{"ja":"有機材料","en":"organic material"},
            "932e4fe1-9724-305f-ffc5-1908c31c83e5":{"ja":"無機材料","en":"inorganic material"},
            "a674a8ef-efa8-9497-4ed4-74de55fafddb":{"ja":"金属・合金","en":"metals and alloys"},
            "342ba516-4d02-171c-9bc4-70a3134b47a8":{"ja":"ポリマー","en":"polymers"},
            "52148afb-6759-23e8-c8b8-33912ec5bfcf":{"ja":"半導体","en":"semiconductors"},
            "961c9637-9b83-0e9d-e60e-ffc1e2517afd":{"ja":"セラミックス","en":"ceramics"},
            "0dde5969-3039-739b-b33b-97df40450790":{"ja":"生物学的物質","en":"biological"}
        }

        self.specific_sample_term = {
            "3a775d54-5c13-fe66-6405-29c05bc931ce":{"ja":"粘度","en":"viscosity"},
            "3edadcff-8a85-51d9-708f-8f76bf055377":{"ja":"InChI key","en":"InChI key"},
            "b4ce4016-e2bf-e5a1-7cae-ed496c7a776f":{"ja":"タンパク名","en":"Protein name"},
            "047e30f3-f294-e58d-cbe4-6bb588bf4cf8":{"ja":"NCBIアクセッション番号","en":"NCBI accession number"},
            "70c2c751-5404-19b7-4a5e-981e6cebbb15":{"ja":"名称","en":"Name"},
            "659da80e-c2ee-2986-41ce-68201b3bc4dd":{"ja":"沸点","en":"boiling point"},
            "3250c45d-0ed6-1438-43b5-eb679918604a":{"ja":"化学式","en":"Chemical formula"},
            "8c9b1a88-1530-24d3-4b2e-5441eee5c24f":{"ja":"遺伝子名","en":"Gene name"},
            "efcf34e7-4308-c195-6691-6f4d28ffc9bb":{"ja":"結晶構造","en":"Crystal structure"},
            "4efc4c3b-727c-c752-cf28-701b55dba1af":{"ja":"融点","en":"Melting temperature"},
            "0444cf53-db47-b208-7b5f-54429291a140":{"ja":"試料分類","en":"Sample type"},
            "efc6a0d5-313e-1871-190c-baaff7d1bf6c":{"ja":"SMILES String","en":"SMILES String"},
            "518e26a0-4262-86f5-3598-80e18e6ff2af":{"ja":"PubChem","en":"PubChem"},
            "f63149a4-e57c-4273-4c1e-dffa41356d28":{"ja":"空間群","en":"Space group"},
            "9270879d-d94e-4d3f-2d5c-19568e040004":{"ja":"InChI","en":"InChI"},
            "9a23002a-c398-e521-081a-24b6cd32dbbd":{"ja":"細胞株","en":"Cell line"},
            "dc27a956-263e-f920-e574-5beec912a247":{"ja":"分子量","en":"molecular weight"},
            "fc30c31d-12a3-591a-c837-4f06ab458de0":{"ja":"生物種","en":"Taxonomy"},
            "e2d20d02-2e38-2cd3-b1b3-66fdb8a11057":{"ja":"CAS番号","en":"CAS Number"}
        }

class OneTimeUse:
    """ 一度だけ使う値 """

    def __init__(self, value):
        self.value = value
        self.used = False

    def __str__(self):
        if self.used:
            return ""
        self.used = True
        return str(self.value)

def get_file_size(ifile):
    """ ファイルサイズの取得 """

    units = ["B", "kB", "MB", "GB", "TB"]
    file_size = ifile.stat().st_size
    index = 0
    for i in range(len(units)):
        if file_size < 1024:
            index = i
            break
        file_size /= 1024
    return f"{file_size:.2f} {units[index]}"

def get_value(data, default=""):
    """ デフォルト値指定で値の取得 """

    if data is not None:
        value = data
    else:
        value = default

    return value

def get_thumbnail(data):
    """ サムネイル画像の取得 """

    img_path = ""
    thumb = data["files"].get("thumbnail", [])
    if len(thumb) > 0:
        img_path = f"./images/{data['id']}/thumbnail/{thumb[0]['name']}"
    return img_path

def get_file_len(data, dirs):
    """ ファイル数の取得 """

    file_len = 0
    for d in dirs:
        file_len += len(data["files"].get(d, []))
    return file_len

def get_data_info(input_dir):
    """ データ情報の取得 """

    data_info = []
    # トップのフォルダ情報
    info = {"id":"0001", "files":{},
            "invoice":read_json(input_dir.joinpath("invoice", "invoice.json"), invoice=True),
            "metadata":read_json(input_dir.joinpath("meta", "metadata.json"))}
    for d in input_dir.iterdir():
        if d.is_dir():
            info["files"][d.name] = [{"name":f.name, "size":get_file_size(f)} for f in d.iterdir()]
    data_info.append(info)

    # dividedフォルダの情報
    divided_dir = input_dir.joinpath("divided")
    if divided_dir.exists():
        # 数値が大きい方がデータ一覧ページの上にくるようにソートする
        for div in sorted(divided_dir.iterdir(), reverse=True):
            info = {"id":div.name, "files":{},
                    "invoice":read_json(div.joinpath("invoice", "invoice.json"), invoice=True),
                    "metadata":read_json(div.joinpath("meta", "metadata.json"))}
            for d in div.iterdir():
                if d.is_dir():
                    info["files"][d.name] = [{"name":f.name, "size":get_file_size(f)} for f in d.iterdir()]

            data_info.append(info)

    # データ一覧ページの並び順の関係でdividedがあればトップを最後のデータIDにする
    if len(data_info) > 1:
        data_info[0]["id"] = f"{int(data_info[1]['id'])+1:04d}"

    return data_info


def hd_update(tgtDict, patchDict):
    ret = {}
    for k in itertools.chain(tgtDict.keys(), patchDict.keys()):
        if k in ret:
            continue
        if k not in patchDict:
            ret[k] = tgtDict[k]
        elif k not in tgtDict:
            ret[k] = patchDict[k]
        else:
            if isinstance(patchDict[k], dict):
                ret[k] = hd_update(tgtDict[k], patchDict[k])
            else:
                ret[k] = patchDict[k]
    return ret


def read_json(ifile, invoice=False):
    """ jsonファイルの読み込み """

    if ifile.exists():
        with open(ifile, "r", encoding="utf_8") as f:
            data = json.load(f)
    else:
        data = {}

    if invoice:
        default = {"datasetId": "",
                   "basic": {
                     "dateSubmitted": datetime.now().strftime("%Y-%m-%d"),
                     "dataOwnerId": "プレビューユーザ",
                     "dataName": "",
                     "instrumentId": "",
                     "experimentId": "",
                     "description": ""
                   },
                   "sample": {
                     "sampleId": "",
                     "names": [],
                     "ownerId": "",
                     "composition": "",
                     "referenceUrl": "",
                     "description": ""
                   }
                  }

        data = hd_update(default, data)
    return data

def sort_meta(metadef_data, metakeys):
    """ medakeysのソート """

    new_metakeys = []
    sorted_metadef = dict(sorted(metadef_data.items(), key=lambda x: x[1].get("order", float("inf"))))
    for key in sorted_metadef:
        if key in metakeys:
            new_metakeys.append(key)

    return new_metakeys

def create_dataDetail(input_dir, out_root_dir, data_info, metadef_data, invsche_data):
    """ dataDetailのhtml作成 """

    filedirs = {"raw":"rawデータファイル",
                "nonshared_raw":"非共有rawデータファイル",
                "meta":"主要パラメータメタ情報ファイル",
                "structured":"構造化ファイル",
                "main_image":"代表画像ファイル",
                "other_image":"画像ファイル"}

    terms = Terms()

    base_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
          <title>RDE/Dataset View</title>
          <meta http-equiv="X-UA-Compatible" content="IE=edge">
          <meta http-equiv="Cache-Control" content="no-cache">
          <meta http-equiv="Cache-Control" content="no-store">
          <meta http-equiv="Cache-Control" content="must-revalidate">
          <meta data-hid="description" name="description" content="">
          <meta name="format-detection" content="telephone=no">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet" href="style.css">
          <script defer>
            function switchTab(tabName) {
              var tabs = ['summary', 'files', 'attachments'];
              tabs.forEach(function (tab) {
                var tabElement = document.getElementById(`${tab}_tab`);
                var tabContent = document.getElementById(tab);
                if (tab === tabName) {
                  tabElement.classList.remove('pointer');
                  tabElement.classList.add('active');
                  tabContent.style.display = 'block';
                } else {
                  tabElement.classList.remove('active');
                  tabElement.classList.add('pointer');
                  tabContent.style.display = 'none';
                }
              });
            }

            function changeImg(imgPath) {
              document.getElementById('topImg').src = imgPath;
              document.getElementById('topImg_title').innerText = imgPath.split('/').pop();
            }
          </script>
        </head>
        <body>
          <div>
            <div>
              <header class="header container px-0">
                <h1 class="logo"><img src="https://rde.nims.go.jp/images/logo/RDE_logo.png"></h1>
                <div class="menu">
                  <a class="dicehome"><img src="https://rde.nims.go.jp/external/dice.png"></a>
                  <a class="register ban">ログアウト</a>
                </div>
              </header>
              <div class="container row container-fix">
                <div class="col-4"></div>
                <nav class="navi col-8 navi-fix">
                  <ul class="d-flex align-items-center justify-content-end pb-1 row">
                    <li class="navilink usage col-2 text-right"><a>利用方法</a></li>
                    <li class="naviitem col-auto naviitem-width"><a class="break-word white-space-pre-line">プレビューユーザ</a></li>
                  </ul>
                </nav>
              </div>
              <div class="topline topline-width"></div>
            </div>
            <main class="contents">
              <div class="container page-content">
                <div>
                  <h2>
                    データ詳細 : プレビューデータセット
                    <span class="small badge rounded-pill bg-success white-space-pre-line break-word text-left"></span>
                    : {{データ名}}
                  </h2>
                  <div class="form-buttons mt-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-danger btn-144px ml-2 ban" disabled>データ削除</button>
                    <button type="button" class="btn btn-primary btn-144px ml-2 ban" disabled><span>データダウンロード</span></button>
                    <a target="_blank" style="display: none;"></a>
                    <a href="./index.html"><button type="button" class="btn btn-secondary btn-144px ml-2">データ一覧へ戻る</button></a>
                  </div>
                  <div>
                    <div class="alert text-danger py-0 mb-3" style="display: none;"></div>
                  </div>
                  <ul class="nav nav-tabs mt-3">
                    <li class="nav-item">
                      <a id="summary_tab" class="nav-link active" onclick="switchTab('summary')">概要</a>
                    </li>
                    <li class="nav-item">
                      <a id="files_tab" class="nav-link pointer" onclick="switchTab('files')">ファイル
                        <span class="badge badge-pill badge-secondary">{{All_File_Num}}</span>
                      </a>
                    </li>
                    <li class="nav-item">
                      <a id="attachments_tab" class="nav-link pointer" onclick="switchTab('attachments')">添付ファイル
                        <span class="badge badge-pill badge-secondary">{{Attachment_Num}}</span>
                      </a>
                    </li>
                  </ul>
                  <div id="summary">
                    <div>
                      <div class="row ml-2">
                        <div class="col-12 text-right">
                          <button type="button" class="btn btn-primary ml-3 btn-144px mr-3 mt-3 ban" disabled>送り状編集</button>
                        </div>
                      </div>
                      <div class="card mt-3">
                        <div class="card-body">
                          <div class="row">
                            <div class="mx-auto">
                              {{TOP画像}}
                            </div>
                          </div>
                        </div>
                        <div class="row form-group">
                          <div class="ml-5">
                            サムネイルをクリックすると画像が表示されます。
                            <span class="badge badge-pill badge-secondary">{{Images_Num}}</span>
                          </div>
                        </div>
                        <div class="row form-group mx-3 thumbnail-scroll">
                          {{カルーセル}}
                        </div>
                      </div>
                      <div class="card mt-3">
                        <div class="card-body px-4">
                          <h5 class="card-title">メタ情報</h5>
                          <div class="table-responsive">
                            <table id="primary-terms-table" class="table table-sm mt-4">
                              <thead>
                                <tr>
                                  <th class="w-200px">分類</th>
                                  <th class="w-200px">日本語名</th>
                                  <th class="w-200px">英語名</th>
                                  <th class="w-75px">単位</th>
                                  {{Table_Column_Value}}
                                </tr>
                              </thead>
                              <tbody>
                                {{Table_Basic}}
                                {{Table_Instrument}}
                                {{Table_Sample}}
                                {{Table_Meta}}
                              </tbody>
                            </table>
                          </div>
                          <div class="row form-group mt-3 ml-3">
                            <span>
                              <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="file earmark text fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-file-earmark-text-fill b-icon bi">
                                <g>
                                  <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0zM9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1zM4.5 9a.5.5 0 0 1 0-1h7a.5.5 0 0 1 0 1h-7zM4 10.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm.5 2.5a.5.5 0 0 1 0-1h4a.5.5 0 0 1 0 1h-4z"></path>
                                </g>
                              </svg>
                              送り状で登録されたメタ情報を示す
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div id="files" style="display: none;">
                    <div class="row px-3">
                      <div class="col-12">
                        <div>
                          <div>
                            <table class="table table-sm mt-4 table-hover tableFixed">
                              <thead>
                                <tr>
                                  <th class="align-middle" style="width: 6%;">
                                    <div class="d-flex align-items-center">
                                      <div>No.</div>
                                      <div class="ml-auto h-100"></div>
                                    </div>
                                  </th>
                                  <th class="align-middle" style="width: 25%;">
                                    <div class="d-flex align-items-center ban">
                                      <div>ファイル種別</div>
                                      <div class="ml-auto h-100">
                                        <div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret up fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-up-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -23)">
                                                <g>
                                                  <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret down fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-down-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -13)">
                                                <g>
                                                  <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </th>
                                  <th class="align-middle" style="width: 34%;">
                                    <div class="d-flex align-items-center ban">
                                      <div>ファイル名</div>
                                      <div class="ml-auto h-100">
                                        <div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret up fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-up-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -23)">
                                                <g>
                                                  <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret down fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-down-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -13)">
                                                <g>
                                                  <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </th>
                                  <th class="align-middle" style="width: 20%;">
                                    <div class="d-flex align-items-center ban">
                                      <div>ファイル登録日(JST)</div>
                                      <div class="ml-auto h-100">
                                        <div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret up fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-up-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -23)">
                                                <g>
                                                  <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret down fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-down-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -13)">
                                                <g>
                                                  <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </th>
                                  <th class="align-middle" style="width: 15%;">
                                    <div class="d-flex align-items-center ban">
                                      <div>サイズ</div>
                                      <div class="ml-auto h-100">
                                        <div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret up fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-up-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -23)">
                                                <g>
                                                  <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret down fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-down-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -13)">
                                                <g>
                                                  <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </th>
                                </tr>
                              </thead>
                              <tbody>
                                {{Table_Files}}
                              </tbody>
                            </table>
                          </div>
                          <div class="pager container">
                            <div class="row">
                              <div class="col-6">
                                <span> Showing 1 to {{All_File_Num}} of {{All_File_Num}} entries</span>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div id="attachments" style="display: none;">
                    <div class="row px-3">
                      <div class="col-12">
                        <div {{Table_Attachments_Display}}>
                          <div>
                            <table class="table table-sm mt-4 table-hover tableFixed">
                              <thead>
                                <tr>
                                  <th class="align-middle" style="width: 6%;">
                                    <div class="d-flex align-items-center">
                                      <div>No.</div>
                                      <div class="ml-auto h-100"></div>
                                    </div>
                                  </th>
                                  <th class="align-middle" style="width: 34%;">
                                    <div class="d-flex align-items-center ban">
                                      <div>ファイル名</div>
                                      <div class="ml-auto h-100">
                                        <div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret up fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-up-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -23)">
                                                <g>
                                                  <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg></div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false"  role="img" aria-label="caret down fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-down-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -13)">
                                                <g>
                                                  <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </th>
                                  <th class="align-middle" style="width: 20%;">
                                    <div class="d-flex align-items-center ban">
                                      <div>ファイル登録日(JST)</div>
                                      <div class="ml-auto h-100">
                                        <div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret up fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-up-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -23)">
                                                <g>
                                                  <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret down fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-down-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -13)">
                                                <g>
                                                  <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </th>
                                  <th class="align-middle" style="width: 15%;">
                                    <div class="d-flex align-items-center ban">
                                      <div>サイズ</div>
                                      <div class="ml-auto h-100">
                                        <div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret up fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-up-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -23)">
                                                <g>
                                                  <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret down fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-down-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -13)">
                                                <g>
                                                  <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </th>
                                  <th class="align-middle" style="width: 25%;">
                                    <div class="d-flex align-items-center ban">
                                      <div>説明</div>
                                      <div class="ml-auto h-100">
                                        <div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret up fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-up-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -23)">
                                                <g>
                                                  <path d="M7.247 4.86l-4.796 5.481c-.566.647-.106 1.659.753 1.659h9.592a1 1 0 0 0 .753-1.659l-4.796-5.48a1 1 0 0 0-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                          <div class="h-0px">
                                            <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="caret down fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-caret-down-fill b-icon bi" style="font-size: 70%;">
                                              <g transform="translate(0 -13)">
                                                <g>
                                                  <path d="M7.247 11.14L2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z"></path>
                                                </g>
                                              </g>
                                            </svg>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </th>
                                  <th style="width: 100px;"></th>
                                </tr>
                              </thead>
                              <tbody>
                                {{Table_Attachments}}
                              </tbody>
                            </table>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="py-5">
                  <h3>お問い合わせ</h3>
                  <div class="container">
                    <div class="row">
                      <div class="col-5 p-2">
                        <div><span class="font-weight-bold">マテリアル先端リサーチインフラ事業 (ARIM) の利用者は</span></div>
                        <div><a>こちら</a></div>
                      </div>
                    </div>
                    <div class="row">
                      <a><img src="https://rde.nims.go.jp/sample_files/dice399-46.png" alt="国立研究開発法人物質・材料研究機構"></a>
                      <a><img src="https://rde.nims.go.jp/sample_files/rde2_logo_arim.png" alt="マテリアル先端リサーチインフラ事業"></a>
                    </div>
                  </div>
                </div>
              </div>
            </main>
            <footer class="footer footer_fix">
              <div class="footer_bg footer_bg_fix"></div>
              <div class="footerBlock">
                <div class="leftBlock">
                  <p class="sitename"><a>国立研究開発法人物質・材料研究機構</a></p>
                  <p class="address"><a>技術開発・共用部門</a> <br> <a>材料データプラットフォーム</a></p>
                  <p class="copyright">Copyright © 2022-2023 National Institute for Materials Science. All rights Reserved.</p>
                </div>
                <div class="rightBlock">
                  <ul class="footerLink">
                    <li><a>プライバシーポリシー</a></li>
                    <li><a>GDPR対応について</a></li>
                    <li><a>お問い合わせ</a></li>
                  </ul>
                </div>
              </div>
            </footer>
          </div>
        </body>
        </html>
    """

    for d in data_info:
        # 出力ファイル名
        out_html_file = out_root_dir.joinpath(f"{d['id']}.html")

        # 試料ID
        if len(d["invoice"]["sample"]["names"]) > 0:
            sample_id = d["invoice"]["sample"]["names"][0]
        else:
            sample_id = d["invoice"]["sample"]["sampleId"]

        # データ名
        if d["invoice"]["basic"]["dataName"]:
            dataname = d["invoice"]["basic"]["dataName"]
        else:
            dataname = f"プレビュー_{d['id']}"

        # 出現するメタデータの全項目
        metakeys  = list(d["metadata"]["constant"].keys())
        metakeys += list(set([key for v in d["metadata"]["variable"] for key in v.keys()]))
        metakeys  = sort_meta(metadef_data, metakeys)

        # variableメタの数(テーブルの値の列数)
        metalen = len(d["metadata"]["variable"])
        if metalen == 0:
            metalen = 1

        # テーブルの値の列数
        column_value = "\n".join([f'<th class="w-200px">値{i}</th>' for i in range(1, metalen+1)])

        if (len(d["files"].get("main_image", [])) + len(d["files"].get("other_image", []))) == 0:
            top_img = """
                <div class="border d-flex align-items-center justify-content-center no-image gray" style="width: 500px; height: 350px;">
                  <div class="text-left" style="font-size: 5rem; line-height: 6rem;">
                    <div>No</div>
                    <div>Image</div>
                  </div>
                </div>
                <div class="text-center main-image-box-width break-word"><span id="topImg_title"></span></div>
            """

            carousel = """
                <div class="thumbnail-position px-1">
                  <div class="border d-flex align-items-center justify-content-center no-image gray" style="width: 120px; height: 80px;">
                    <div class="text-left" style="font-size: 1.2rem; line-height: 1.44rem;">
                      <div>No</div>
                      <div>Image</div>
                    </div>
                  </div>
                </div>
            """
        else:
            top_img  = ""
            carousel = ""
            for m in ["main_image", "other_image"]:
                for img in d["files"].get(m, []):
                    img_path = f"./images/{d['id']}/{m}/{img['name']}"

                    if top_img == "":
                        top_img = f"""
                            <div class="border p-2">
                              <div class="d-flex align-items-center justify-content-center main-image-box">
                                <img id="topImg" class="main-image" src="{img_path}">
                              </div>
                            </div>
                            <div class="text-center main-image-box-width break-word"><span id="topImg_title">{img['name']}</span></div>
                        """

                    carousel += f"""
                        <div class="thumbnail-position px-1 pointer">
                          <div class="text-center d-flex align-items-center justify-content-center image-box" onclick="changeImg('{img_path}')">
                            <img id="thumbImg" class="image2" src="{img_path}">
                          </div>
                          <div class="text-center image-box-width break-word">{img['name']}</div>
                        </div>
                    """

        basic = f"""
            <tr>
              <td>基本情報</td>
              <td>記入年月日</td>
              <td>Date of Data Entry</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">{d['invoice']['basic']['dateSubmitted']} JST</td>
            </tr>
            <tr>
              <td></td>
              <td>データ所有者(所属)</td>
              <td>Data Owner (Affiliation)</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">プレビューユーザ</td>
            </tr>
            <tr>
              <td></td>
              <td>データ名</td>
              <td>Data Name</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">{dataname}</td>
            </tr>
            <tr>
              <td></td>
              <td>実験ID</td>
              <td>Experiment ID</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">{get_value(d['invoice']['basic']['experimentId'])}</td>
            </tr>
            <tr>
              <td></td>
              <td>説明</td>
              <td>Description</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">{get_value(d['invoice']['basic']['description'])}</td>
            </tr>
        """

        instrument = f"""
            <tr>
              <td>装置情報</td>
              <td>登録名</td>
              <td>Registration Name</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">**プレビューでは非表示**</td>
            </tr>
            <tr>
              <td></td>
              <td>機関</td>
              <td>Organization</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">**プレビューでは非表示**</td>
            </tr>
            <tr>
              <td></td>
              <td>説明</td>
              <td>Description</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">**プレビューでは非表示**</td>
            </tr>
        """

        sample = f"""
            <tr>
              <td>試料情報</td>
              <td>試料名(ローカルID)</td>
              <td>Sample Name (Local ID)</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">{sample_id}</td>
            </tr>
            <tr>
              <td></td>
              <td>化学式・組成式・分子式など</td>
              <td>Chemical Formula etc.</td>
              <td></td>
              <td colspan="{metalen}" class="break-word white-space-pre-line">{get_value(d['invoice']['sample']['composition'])}</td>
            </tr>
            <tr>
              <td></td>
              <td>試料の説明</td>
              <td>Description</td>
              <td></td>
              <td colspan="{metalen}" class=""><div class="css-reset">{get_value(d['invoice']['sample']['description'])}</div></td>
            </tr>
        """

        label = OneTimeUse("固有情報")
        meta = ""
        for k in metakeys:
            if metadef_data[k].get("variable", 2) == 2:
                if d['metadata']['constant'].get(k, False):
                    meta += f"""
                        <tr>
                          <td>{label}</td>
                          <td>{get_value(metadef_data[k]['name']['ja'])}</td>
                          <td>{get_value(metadef_data[k]['name']['en'])}</td>
                          <td>{get_value(d['metadata']['constant'][k].get('unit'), metadef_data[k].get('unit', ''))}</td>
                          <td colspan="{metalen}" class="break-word white-space-pre-line">{get_value(d['metadata']['constant'][k]["value"])}</td>
                        </tr>
                    """
            else:
                unit = metadef_data[k].get('unit', '')
                for v in d['metadata']['variable']:
                    kunit = v.get(k, {'unit':None}).get('unit', None)
                    if kunit:
                        unit = kunit
                        break

                meta += f"""
                    <tr>
                      <td>{label}</td>
                      <td>{get_value(metadef_data[k]['name']['ja'])}</td>
                      <td>{get_value(metadef_data[k]['name']['en'])}</td>
                      <td>{unit}</td>
                """
                for v in d['metadata']['variable']:
                    meta += f"<td colspan='1' class='break-word white-space-pre-line'>{get_value(v.get(k, {'value':None})['value'])}</td>"

                meta += "</tr>"

        for k in d["invoice"].get("custom", []):
            if d["invoice"]["custom"][k]:
                meta += f"""
                    <tr>
                      <td>{label}</td>
                      <td>{invsche_data['properties']['custom']['properties'][k]['label']['ja']}
                        <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="file earmark text fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-file-earmark-text-fill b-icon bi">
                          <g>
                            <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0zM9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1zM4.5 9a.5.5 0 0 1 0-1h7a.5.5 0 0 1 0 1h-7zM4 10.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm.5 2.5a.5.5 0 0 1 0-1h4a.5.5 0 0 1 0 1h-4z"></path>
                          </g>
                        </svg>
                      </td>
                      <td>{invsche_data['properties']['custom']['properties'][k]['label']['en']}</td>
                      <td>{invsche_data['properties']['custom']['properties'][k].get('options', {}).get('unit', "")}</td>
                      <td colspan="{metalen}" class="break-word white-space-pre-line">{get_value(d["invoice"]["custom"][k])}</td>
                    </tr>
                """

        for k in d["invoice"].get("sample", {}).get("generalAttributes", []):
            if k["value"]:
                meta += f"""
                    <tr>
                      <td>{label}</td>
                      <td>{terms.general_sample_term.get(k['termId'], {}).get('ja', '')}
                        <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="file earmark text fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-file-earmark-text-fill b-icon bi">
                          <g>
                            <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0zM9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1zM4.5 9a.5.5 0 0 1 0-1h7a.5.5 0 0 1 0 1h-7zM4 10.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm.5 2.5a.5.5 0 0 1 0-1h4a.5.5 0 0 1 0 1h-4z"></path>
                          </g>
                        </svg>
                      </td>
                      <td>{terms.general_sample_term.get(k['termId'], {}).get('en', '')}</td>
                      <td></td>
                      <td colspan="{metalen}" class="break-word white-space-pre-line">{get_value(k["value"])}</td>
                    </tr>
                """

        for k in d["invoice"].get("sample", {}).get("specificAttributes",[]):
            if k["value"]:
                meta += f"""
                    <tr>
                      <td>{label}</td>
                      <td>{terms.sample_class.get(k['classId'], {}).get('ja', k['classId'])} / {terms.specific_sample_term.get(k['termId'], {}).get('ja', k['termId'])}
                        <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="file earmark text fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-file-earmark-text-fill b-icon bi">
                          <g>
                            <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0zM9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1zM4.5 9a.5.5 0 0 1 0-1h7a.5.5 0 0 1 0 1h-7zM4 10.5a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7a.5.5 0 0 1-.5-.5zm.5 2.5a.5.5 0 0 1 0-1h4a.5.5 0 0 1 0 1h-4z"></path>
                          </g>
                        </svg>
                      </td>
                      <td>{terms.sample_class.get(k['classId'], {}).get('en', k['classId'])} / {terms.specific_sample_term.get(k['termId'], {}).get('en', k['termId'])}</td>
                      <td></td>
                      <td colspan="{metalen}" class="break-word white-space-pre-line">{get_value(k["value"])}</td>
                    </tr>
                """

        counter_files = 0
        files = ""
        for dr in filedirs:
            if dr in ["main_image", "other_image"]:
                eye = """
                    <button type="button" class="btn p-0 btn-link">
                      <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="eye fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-eye-fill b-icon bi ban">
                        <g>
                          <path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"></path>
                          <path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"></path>
                        </g>
                      </svg>
                    </button>
                """
            else:
                eye = ""
            for f in d["files"].get(dr, []):
                counter_files += 1
                files += f"""
                    <tr>
                      <td><div class="word-break m-0">{counter_files}</div></td>
                      <td><div class="word-break m-0">{filedirs[dr]}</div></td>
                      <td>
                        <div>
                          <div class="d-flex">
                            <div class="break-word">{f['name']}</div>
                            <div class="text-right ml-auto"></div>
                            {eye}
                            <div class="ml-2 mt-1">
                              <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="download" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-download p-0 pointer b-icon bi ban">
                                <g>
                                  <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"></path>
                                  <path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"></path>
                                </g>
                              </svg>
                              <a target="_blank" style="display: none;"></a>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td class=""><div class="word-break m-0">{d['invoice']['basic']['dateSubmitted']}</div></td>
                      <td class=""><div class="word-break m-0">{f['size']}</div></td>
                    </tr>
                """

        counter_attachments = 0
        attachments = ""
        for f in d["files"].get("attachment", []):
            counter_attachments += 1
            attachments += f"""
              <tr>
                <td><div class="word-break m-0">{counter_attachments}</div></td>
                <td>
                  <div>
                    <div class="d-flex">
                      <div class="break-word">{f['name']}</div>
                      <div class="text-right ml-auto"></div>
                      <div class="ml-2 mt-1">
                        <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="download" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-download p-0 pointer b-icon bi ban">
                          <g>
                            <path d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z"></path><path d="M7.646 11.854a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 10.293V1.5a.5.5 0 0 0-1 0v8.793L5.354 8.146a.5.5 0 1 0-.708.708l3 3z"></path>
                          </g>
                        </svg>
                      </div>
                    </div>
                  </div>
                </td>
                <td><div class="word-break m-0">{d['invoice']['basic']['dateSubmitted']}</div></td>
                <td><div class="word-break m-0">{f['size']}</div></td>
                <td><div class="word-break m-0"></div></td>
                <td class="text-center">
                  <svg viewBox="0 0 16 16" width="1em" height="1em" focusable="false" role="img" aria-label="trash fill" xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi-trash-fill pointer b-icon bi ban" style="font-size: 150%;">
                    <g>
                      <path d="M2.5 1a1 1 0 0 0-1 1v1a1 1 0 0 0 1 1H3v9a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V4h.5a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1H10a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1H2.5zm3 4a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 .5-.5zM8 5a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-1 0v-7A.5.5 0 0 1 8 5zm3 .5v7a.5.5 0 0 1-1 0v-7a.5.5 0 0 1 1 0z"></path>
                    </g>
                  </svg>
                </td>
              </tr>
              """

        if counter_attachments == 0:
            attachments_display = 'style="display: none;"'
        else:
            attachments_display = ""

        html = base_template.replace("{{データ名}}", dataname)
        html = html.replace("{{TOP画像}}", top_img)
        html = html.replace("{{カルーセル}}", carousel)
        html = html.replace("{{Images_Num}}", str(get_file_len(d, ["main_image","other_image"])))
        html = html.replace("{{Table_Column_Value}}", column_value)
        html = html.replace("{{Table_Instrument}}", instrument)
        html = html.replace("{{Table_Basic}}", basic)
        html = html.replace("{{Table_Sample}}", sample)
        html = html.replace("{{Table_Meta}}", meta)
        html = html.replace("{{Table_Files}}", files)
        html = html.replace("{{All_File_Num}}", str(counter_files))
        html = html.replace("{{Attachment_Num}}", str(counter_attachments))
        html = html.replace("{{Table_Attachments_Display}}", attachments_display)
        html = html.replace("{{Table_Attachments}}", attachments)

        # 圧縮する場合
        if COMPRESS:
          html = html.replace("\n", "").replace("  ", "")

        with open(out_html_file, "w", encoding="utf_8") as f:
            f.write(html)

def create_dataList(input_dir, out_root_dir, data_info):
    """ index.htmlの作成 """

    out_html_file = out_root_dir.joinpath("index.html")

    base_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
          <title>RDE/Dataset View</title>
          <meta http-equiv="X-UA-Compatible" content="IE=edge">
          <meta http-equiv="Cache-Control" content="no-cache">
          <meta http-equiv="Cache-Control" content="no-store">
          <meta http-equiv="Cache-Control" content="must-revalidate">
          <meta data-hid="description" name="description" content="">
          <meta name="format-detection" content="telephone=no">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet" href="style.css">
        </head>
        <body>
          <div>
            <div>
              <header class="header container px-0">
                <h1 class="logo"><img src="https://rde.nims.go.jp/images/logo/RDE_logo.png"></h1>
                <div class="menu">
                  <a class="dicehome"><img src="https://rde.nims.go.jp/external/dice.png"></a>
                  <a class="register ban">ログアウト</a>
                </div>
              </header>
              <div class="container row container-fix">
                <div class="col-4"></div>
                <nav class="navi col-8 navi-fix">
                  <ul class="d-flex align-items-center justify-content-end pb-1 row">
                    <li class="navilink usage col-2 text-right"><a>利用方法</a></li>
                    <li class="naviitem col-auto naviitem-width"><a class="break-word white-space-pre-line">プレビューユーザ</a></li>
                  </ul>
                </nav>
              </div>
              <div class="topline topline-width"></div>
            </div>
            <main class="contents">
              <div class="container page-content">
                <div>
                  <h2>
                    データ一覧: プレビューデータセット
                    <span class="badge badge-pill badge-success white-space-pre-line break-word text-left"></span>
                  </h2>
                  <div class="form-buttons mt-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-144px btn-primary ml-2 ban" disabled>データセット詳細</button>
                    <button type="button" class="btn btn-144px btn-secondary ml-2 ban" disabled>データセット一覧へ戻る</button>
                  </div>
                  <div>
                    <div class="alert text-danger py-0 mb-3" style="display: none;"></div>
                  </div>
                  <div class="card mt-3">
                    <div class="card-body">
                      <div class="row form-group">
                        <div class="col-12 break-word white-space-pre-line"></div>
                      </div>
                    </div>
                  </div>
                  <ul class="nav nav-tabs mt-3">
                    <li class="nav-item">
                      <a class="nav-link active">ギャラリー表示</a>
                    </li>
                  </ul>
                  <div>
                    <div class="row form-group">
                      {{カード}}
                    </div>
                    <div class="col d-flex justify-content-end">
                      <div class="pager container">
                        <div class="row">
                          <div class="col-6">
                            <span> Showing 1 to {{Data_Num}} of {{Data_Num}} entries</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="py-5">
                  <h3>お問い合わせ</h3>
                  <div class="container">
                    <div class="row">
                      <div class="col-5 p-2">
                        <div><span class="font-weight-bold">マテリアル先端リサーチインフラ事業 (ARIM) の利用者は</span></div>
                        <div><a>こちら</a></div>
                      </div>
                    </div>
                    <div class="row">
                      <a><img src="https://rde.nims.go.jp/sample_files/dice399-46.png" alt="国立研究開発法人物質・材料研究機構"></a>
                      <a><img src="https://rde.nims.go.jp/sample_files/rde2_logo_arim.png" alt="マテリアル先端リサーチインフラ事業"></a>
                    </div>
                  </div>
                </div>
              </div>
            </main>
            <footer class="footer footer_fix">
              <div class="footer_bg footer_bg_fix"></div>
              <div class="footerBlock">
                <div class="leftBlock">
                  <p class="sitename"><a>国立研究開発法人物質・材料研究機構</a></p>
                  <p class="address"><a>技術開発・共用部門</a> <br> <a>材料データプラットフォーム</a></p>
                  <p class="copyright">Copyright © 2022-2023 National Institute for Materials Science. All rights Reserved.</p>
                </div>
                <div class="rightBlock">
                  <ul class="footerLink">
                    <li><a>プライバシーポリシー</a></li>
                    <li><a>GDPR対応について</a></li>
                    <li><a>お問い合わせ</a></li>
                  </ul>
                </div>
              </div>
            </footer>
          </div>
        </body>
        </html>
    """

    card_template = """
        <div class="col-4 mt-3">
          <div class="card h-100">
            <div class="card-header bg-transparent">
              <a href="{{HTMLファイル}}">{{データ名}}</a>
              <div class="badge rounded-pill badge-secondary">{{ファイル数}}</div>
              <span class="float-right">{{データ番号}}</span>
            </div>
            <div class="card-body">
              <div class="row form-group d-flex align-items-center justify-content-center mx-2 imageBox">{{サムネイル画像}}</div>
              <div class="form-group">
                <div class="col-12 pl-0">データ所有者(所属)</div>
                <span><a>プレビューユーザ</a></span>
              </div>
              <div class="row form-group">
                <div class="col-12">試料名(ローカルID)</div>
                <div class="col-12"><a>{{試料ID}}</a></div>
              </div>
              <div class="row form-group">
                <div class="col-12">説明</div>
                <div class="col-12 white-space-pre-line">{{データ説明}}</div>
              </div>
              <div class="row form-group">
                <div class="col-12">タクソノミー</div>
              </div>
            </div>
            <div class="card-footer bg-transparent">
              <p class="card-text text-right mb-2"><small class="text-muted">登録日時 {{登録日時}}</small></p>
              <p class="card-text text-right"><small class="text-muted">データID N/A</small></p>
            </div>
          </div>
        </div>
    """

    card = ""
    for d in data_info:
        if len(d["invoice"]["sample"]["names"]) > 0:
            sample_id = d["invoice"]["sample"]["names"][0]
        else:
            sample_id = d["invoice"]["sample"]["sampleId"]

        card += card_template.replace("{{HTMLファイル}}", f"./{d['id']}.html")
        card = card.replace("{{データ名}}", d["invoice"]["basic"]["dataName"] if d["invoice"]["basic"]["dataName"] else f"プレビュー_{d['id']}")
        card = card.replace("{{ファイル数}}", str(get_file_len(d, ["raw","nonshared_raw","meta","structured","main_image","other_image"])))
        card = card.replace("{{データ番号}}", f"{int(d['id'])}")
        card = card.replace("{{試料ID}}", sample_id)
        card = card.replace("{{データ説明}}", get_value(d["invoice"]["basic"]["description"]))
        card = card.replace("{{登録日時}}", datetime.strptime(d["invoice"]["basic"]["dateSubmitted"], "%Y-%m-%d").strftime("%Y-%m-%d 0:00:00 JST"))
        thumb_img = get_thumbnail(d)
        if thumb_img == "":
            thumbnail = """
                <div class="border d-flex align-items-center justify-content-center no-image white" style="width: 250px; height: 250px;">
                  <div class="text-left" style="font-size: 2.5rem; line-height: 3rem;">
                    <div>No</div>
                    <div>Image</div>
                  </div>
                </div>
            """
        else:
            thumbnail = f"""
                <span>
                  <img id="thumbnailImg" class="image" src="{thumb_img}">
                </span>
            """
        card = card.replace("{{サムネイル画像}}", thumbnail)

    html = base_template.replace("{{カード}}", card)
    html = html.replace("{{Data_Num}}", str(len(data_info)))

    # 圧縮する場合
    if COMPRESS:
        html = html.replace("\n", "").replace("  ", "")

    with open(out_html_file, "w", encoding="utf_8") as f:
        f.write(html)

def create_css(out_root_dir):
    """ CSSファイルの作成 """

    out_css_file = out_root_dir.joinpath("style.css")
    css = """
    :root {
        --blue: #007bff;
        --indigo: #6610f2;
        --purple: #6f42c1;
        --pink: #e83e8c;
        --red: #dc3545;
        --orange: #fd7e14;
        --yellow: #ffc107;
        --green: #28a745;
        --teal: #20c997;
        --cyan: #17a2b8;
        --white: #fff;
        --gray: #6c757d;
        --gray-dark: #343a40;
        --primary: #007bff;
        --secondary: #6c757d;
        --success: #28a745;
        --info: #17a2b8;
        --warning: #ffc107;
        --danger: #dc3545;
        --light: #f8f9fa;
        --dark: #343a40;
        --breakpoint-xs: 0;
        --breakpoint-sm: 576px;
        --breakpoint-md: 768px;
        --breakpoint-lg: 992px;
        --breakpoint-xl: 1200px;
        --font-family-sans-serif: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans",
            "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
        --font-family-monospace: SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
    }
    
    *,
    ::after,
    ::before {
        box-sizing: border-box;
    }
    
    html {
        font-family: sans-serif;
        line-height: 1.15;
        text-size-adjust: 100%;
        -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    }
    
    article,
    aside,
    figcaption,
    figure,
    footer,
    header,
    hgroup,
    main,
    nav,
    section {
        display: block;
    }
    
    body {
        margin: 0px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans",
            "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.5;
        color: rgb(33, 37, 41);
        text-align: left;
        background-color: rgb(255, 255, 255);
        line-height: 1;
        background: rgb(255, 255, 255);
        font-family: "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro", メイリオ, Meiryo, Osaka, "ＭＳ Ｐゴシック",
            "MS PGothic", "sans-serif";
    }
    
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        margin-top: 0px;
        margin-bottom: 0.5rem;
    }
    
    p {
        margin-top: 0px;
        margin-bottom: 1rem;
    }
    
    address,
    dl,
    ol,
    ul {
        margin-bottom: 1rem;
    }
    
    dl,
    ol,
    ul {
        margin-top: 0px;
    }
    
    small {
        font-size: 80%;
        font-size: smaller;
    }
    
    a {
        color: rgb(0, 123, 255);
        text-decoration: none;
        background-color: transparent;
        color: rgb(0, 0, 153);
    }
    
    img {
        border-style: none;
        width: 100%;
        max-width: inherit;
        vertical-align: bottom;
    }
    
    img,
    svg {
        vertical-align: middle;
    }
    
    svg {
        overflow: hidden;
    }
    
    label {
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    
    button {
        border-radius: 0px;
    }
    
    button,
    input,
    optgroup,
    select,
    textarea {
        margin: 0px;
        font-family: inherit;
        font-size: inherit;
        line-height: inherit;
    }
    
    button,
    input {
        overflow: visible;
    }
    
    button,
    select {
        text-transform: none;
    }
    
    select {
        overflow-wrap: normal;
    }
    
    [type="button"],
    [type="reset"],
    [type="submit"],
    button {
        appearance: button;
    }
    
    [type="button"]:not(:disabled),
    [type="reset"]:not(:disabled),
    [type="submit"]:not(:disabled),
    button:not(:disabled) {
        cursor: pointer;
    }
    
    input[type="checkbox"],
    input[type="radio"] {
        box-sizing: border-box;
        padding: 0px;
    }
    
    .h1,
    .h2,
    .h3,
    .h4,
    .h5,
    .h6,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        margin-bottom: 0.5rem;
        font-weight: 500;
        line-height: 1.2;
    }
    
    .h1,
    h1 {
        font-size: 2.5rem;
    }
    
    .h2,
    h2 {
        font-size: 2rem;
    }
    
    .h3,
    h3 {
        font-size: 1.75rem;
    }
    
    .h5,
    h5 {
        font-size: 1.25rem;
    }
    
    .small,
    small {
        font-size: 80%;
        font-weight: 400;
    }
    
    .container,
    .container-fluid,
    .container-lg,
    .container-md,
    .container-sm,
    .container-xl {
        width: 100%;
        padding-right: 15px;
        padding-left: 15px;
        margin-right: auto;
        margin-left: auto;
    }
    
    .row {
        display: flex;
        flex-wrap: wrap;
        margin-right: -15px;
        margin-left: -15px;
    }
    
    .col,
    .col-1,
    .col-2,
    .col-3,
    .col-4,
    .col-5,
    .col-6,
    .col-7,
    .col-8,
    .col-9,
    .col-10,
    .col-11,
    .col-12,
    .col-auto,
    .col-lg,
    .col-lg-1,
    .col-lg-2,
    .col-lg-3,
    .col-lg-4,
    .col-lg-5,
    .col-lg-6,
    .col-lg-7,
    .col-lg-8,
    .col-lg-9,
    .col-lg-10,
    .col-lg-11,
    .col-lg-12,
    .col-lg-auto,
    .col-md,
    .col-md-1,
    .col-md-2,
    .col-md-3,
    .col-md-4,
    .col-md-5,
    .col-md-6,
    .col-md-7,
    .col-md-8,
    .col-md-9,
    .col-md-10,
    .col-md-11,
    .col-md-12,
    .col-md-auto,
    .col-sm,
    .col-sm-1,
    .col-sm-2,
    .col-sm-3,
    .col-sm-4,
    .col-sm-5,
    .col-sm-6,
    .col-sm-7,
    .col-sm-8,
    .col-sm-9,
    .col-sm-10,
    .col-sm-11,
    .col-sm-12,
    .col-sm-auto,
    .col-xl,
    .col-xl-1,
    .col-xl-2,
    .col-xl-3,
    .col-xl-4,
    .col-xl-5,
    .col-xl-6,
    .col-xl-7,
    .col-xl-8,
    .col-xl-9,
    .col-xl-10,
    .col-xl-11,
    .col-xl-12,
    .col-xl-auto {
        position: relative;
        width: 100%;
        padding-right: 15px;
        padding-left: 15px;
    }
    
    .col {
        flex-basis: 0px;
        flex-grow: 1;
        max-width: 100%;
    }
    
    .col-auto {
        flex: 0 0 auto;
        width: auto;
        max-width: 100%;
    }
    
    .col-2 {
        flex: 0 0 16.6667%;
        max-width: 16.6667%;
    }
    
    .col-4 {
        flex: 0 0 33.3333%;
        max-width: 33.3333%;
    }
    
    .col-5 {
        flex: 0 0 41.6667%;
        max-width: 41.6667%;
    }
    
    .col-6 {
        flex: 0 0 50%;
        max-width: 50%;
    }
    
    .col-8 {
        flex: 0 0 66.6667%;
        max-width: 66.6667%;
    }
    
    .col-12 {
        flex: 0 0 100%;
        max-width: 100%;
    }
    
    .form-control {
        display: block;
        width: 100%;
        height: calc(1.5em + 2px + 0.75rem);
        padding: 0.375rem 0.75rem;
        font-size: 1rem;
        font-weight: 400;
        line-height: 1.5;
        color: rgb(73, 80, 87);
        background-color: rgb(255, 255, 255);
        background-clip: padding-box;
        border: 1px solid rgb(206, 212, 218);
        border-radius: 0.25rem;
        transition:
            border-color 0.15s ease-in-out,
            box-shadow 0.15s ease-in-out;
    }
    
    .form-group {
        margin-bottom: 1rem;
    }
    
    .form-inline {
        display: flex;
        flex-flow: wrap;
        align-items: center;
    }
    
    .btn {
        display: inline-block;
        font-weight: 400;
        color: rgb(33, 37, 41);
        text-align: center;
        vertical-align: middle;
        user-select: none;
        background-color: transparent;
        border: 1px solid transparent;
        padding: 0.375rem 0.75rem;
        font-size: 1rem;
        line-height: 1.5;
        border-radius: 0.25rem;
        transition:
            color 0.15s ease-in-out,
            background-color 0.15s ease-in-out,
            border-color 0.15s ease-in-out,
            box-shadow 0.15s ease-in-out;
    }
    
    .btn:not(:disabled):not(.disabled) {
        cursor: pointer;
    }
    
    .btn-primary {
        color: rgb(255, 255, 255);
        background-color: rgb(0, 123, 255);
        border-color: rgb(0, 123, 255);
    }
    
    .btn-secondary {
        color: rgb(255, 255, 255);
        background-color: rgb(108, 117, 125);
        border-color: rgb(108, 117, 125);
    }
    
    .nav {
        display: flex;
        flex-wrap: wrap;
        padding-left: 0px;
        margin-bottom: 0px;
        list-style: none;
    }
    
    .nav-link {
        display: block;
        padding: 0.5rem 1rem;
    }
    
    .nav-tabs {
        border-bottom: 1px solid rgb(222, 226, 230);
    }
    
    .nav-tabs .nav-link {
        margin-bottom: -1px;
        border: 1px solid transparent;
        border-top-left-radius: 0.25rem;
        border-top-right-radius: 0.25rem;
    }
    
    .nav-tabs .nav-item.show .nav-link,
    .nav-tabs .nav-link.active {
        color: rgb(73, 80, 87);
        background-color: rgb(255, 255, 255);
        border-color: rgb(222, 226, 230) rgb(222, 226, 230) rgb(255, 255, 255);
    }
    
    .card {
        position: relative;
        display: flex;
        flex-direction: column;
        min-width: 0px;
        overflow-wrap: break-word;
        background-color: rgb(255, 255, 255);
        background-clip: border-box;
        border: 1px solid rgba(0, 0, 0, 0.125);
        border-radius: 0.25rem;
    }
    
    .card-body {
        flex: 1 1 auto;
        min-height: 1px;
        padding: 1.25rem;
    }
    
    .card-title {
        margin-bottom: 0.75rem;
    }
    
    .card-subtitle,
    .card-text:last-child {
        margin-bottom: 0px;
    }
    
    .card-header {
        padding: 0.75rem 1.25rem;
        margin-bottom: 0px;
        background-color: rgba(0, 0, 0, 0.03);
        border-bottom: 1px solid rgba(0, 0, 0, 0.125);
    }
    
    .card-header:first-child {
        border-radius: calc(-1px + 0.25rem) calc(-1px + 0.25rem) 0px 0px;
    }
    
    .card-footer {
        padding: 0.75rem 1.25rem;
        background-color: rgba(0, 0, 0, 0.03);
        border-top: 1px solid rgba(0, 0, 0, 0.125);
    }
    
    .card-footer:last-child {
        border-radius: 0px 0px calc(-1px + 0.25rem) calc(-1px + 0.25rem);
    }
    
    .pagination {
        display: flex;
        padding-left: 0px;
        list-style: none;
        border-radius: 0.25rem;
    }
    
    .page-link {
        position: relative;
        display: block;
        padding: 0.5rem 0.75rem;
        margin-left: -1px;
        line-height: 1.25;
        color: rgb(0, 123, 255);
        background-color: rgb(255, 255, 255);
        border: 1px solid rgb(222, 226, 230);
    }
    
    .page-item:first-child .page-link {
        margin-left: 0px;
        border-top-left-radius: 0.25rem;
        border-bottom-left-radius: 0.25rem;
    }
    
    .page-item:last-child .page-link {
        border-top-right-radius: 0.25rem;
        border-bottom-right-radius: 0.25rem;
    }
    
    .page-item.active .page-link {
        z-index: 3;
        color: rgb(255, 255, 255);
        background-color: rgb(0, 123, 255);
        border-color: rgb(0, 123, 255);
    }
    
    .page-item.disabled .page-link {
        color: rgb(108, 117, 125);
        pointer-events: none;
        cursor: auto;
        background-color: rgb(255, 255, 255);
        border-color: rgb(222, 226, 230);
    }
    
    .badge {
        display: inline-block;
        padding: 0.25em 0.4em;
        font-size: 75%;
        font-weight: 700;
        line-height: 1;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border-radius: 0.25rem;
        transition:
            color 0.15s ease-in-out,
            background-color 0.15s ease-in-out,
            border-color 0.15s ease-in-out,
            box-shadow 0.15s ease-in-out;
    }
    
    .badge:empty {
        display: none;
    }
    
    .badge-pill {
        padding-right: 0.6em;
        padding-left: 0.6em;
        border-radius: 10rem;
    }
    
    .badge-secondary {
        color: rgb(255, 255, 255);
        background-color: rgb(108, 117, 125);
    }
    
    .badge-success {
        color: rgb(255, 255, 255);
        background-color: rgb(40, 167, 69);
    }
    
    .alert {
        position: relative;
        padding: 0.75rem 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid transparent;
        border-radius: 0.25rem;
    }
    
    .bg-transparent {
        background-color: transparent !important;
    }
    
    .rounded-pill {
        border-radius: 50rem !important;
    }
    
    .d-flex {
        display: flex !important;
    }
    
    .justify-content-end {
        justify-content: flex-end !important;
    }
    
    .justify-content-center {
        justify-content: center !important;
    }
    
    .align-items-center {
        align-items: center !important;
    }
    
    .align-self-center {
        align-self: center !important;
    }
    
    .float-right {
        float: right !important;
    }
    
    .h-100 {
        height: 100% !important;
    }
    
    .m-0 {
        margin: 0px !important;
    }
    
    .mr-0,
    .mx-0 {
        margin-right: 0px !important;
    }
    
    .ml-1,
    .mx-1 {
        margin-left: 0.25rem !important;
    }
    
    .mt-2,
    .my-2 {
        margin-top: 0.5rem !important;
    }
    
    .mr-2,
    .mx-2 {
        margin-right: 0.5rem !important;
    }
    
    .mb-2,
    .my-2 {
        margin-bottom: 0.5rem !important;
    }
    
    .ml-2,
    .mx-2 {
        margin-left: 0.5rem !important;
    }
    
    .mt-3,
    .my-3 {
        margin-top: 1rem !important;
    }
    
    .mr-3,
    .mx-3 {
        margin-right: 1rem !important;
    }
    
    .mb-3,
    .my-3 {
        margin-bottom: 1rem !important;
    }
    
    .ml-3,
    .mx-3 {
        margin-left: 1rem !important;
    }
    
    .pt-0,
    .py-0 {
        padding-top: 0px !important;
    }
    
    .pr-0,
    .px-0 {
        padding-right: 0px !important;
    }
    
    .pb-0,
    .py-0 {
        padding-bottom: 0px !important;
    }
    
    .pl-0,
    .px-0 {
        padding-left: 0px !important;
    }
    
    .pb-1,
    .py-1 {
        padding-bottom: 0.25rem !important;
    }
    
    .p-2 {
        padding: 0.5rem !important;
    }
    
    .p-3 {
        padding: 1rem !important;
    }
    
    .pl-3,
    .px-3 {
        padding-left: 1rem !important;
    }
    
    .pt-5,
    .py-5 {
        padding-top: 3rem !important;
    }
    
    .pb-5,
    .py-5 {
        padding-bottom: 3rem !important;
    }
    
    .text-left {
        text-align: left !important;
    }
    
    .text-right {
        text-align: right !important;
    }
    
    .font-weight-bold {
        font-weight: 700 !important;
    }
    
    .text-danger {
        color: rgb(220, 53, 69) !important;
    }
    
    .text-muted {
        color: rgb(108, 117, 125) !important;
    }
    
    .invisible {
        visibility: hidden !important;
        visibility: hidden;
    }
    
    .b-icon.bi {
        display: inline-block;
        overflow: visible;
        vertical-align: -0.15em;
    }
    
    a,
    abbr,
    acronym,
    address,
    applet,
    article,
    aside,
    audio,
    b,
    big,
    blockquote,
    body,
    canvas,
    caption,
    center,
    cite,
    code,
    dd,
    del,
    details,
    dfn,
    div,
    dl,
    dt,
    em,
    embed,
    fieldset,
    figcaption,
    figure,
    footer,
    form,
    h1,
    h2,
    h3,
    h4,
    h5,
    h6,
    header,
    hgroup,
    html,
    i,
    iframe,
    img,
    ins,
    kbd,
    label,
    legend,
    li,
    mark,
    menu,
    nav,
    object,
    ol,
    output,
    p,
    pre,
    q,
    ruby,
    s,
    samp,
    section,
    small,
    span,
    strike,
    strong,
    sub,
    summary,
    sup,
    table,
    tbody,
    td,
    tfoot,
    th,
    thead,
    time,
    tr,
    tt,
    u,
    ul,
    var,
    video {
        margin: 0px;
        padding: 0px;
        border: 0px;
        font: inherit;
        vertical-align: baseline;
    }
    
    article,
    aside,
    details,
    figcaption,
    figure,
    footer,
    header,
    hgroup,
    menu,
    nav,
    section {
        display: block;
    }
    
    ol,
    ul {
        list-style: none;
    }
    
    .header {
        width: 1100px;
        margin: 0px auto;
        padding-top: 20px;
        background: rgb(255, 255, 255);
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    
    .header h1 {
        display: inline-block;
        height: 82px;
    }
    
    .header .menu {
        font-size: 14px;
        font-weight: 700;
        line-height: 1;
        display: flex;
    }
    
    .header .menu .help,
    .header .menu .login,
    .header .menu .register {
        padding: 8px 15px;
        border: 1px solid rgb(214, 227, 241);
        color: rgb(73, 109, 144);
        margin: 0px 5px;
    }
    
    .header .menu .dicehome img,
    .header .menu .matnavihome img {
        height: 32px;
        width: auto;
    }
    
    .navi {
        margin: 0px auto;
        font-size: 16px;
        font-weight: 700;
        position: relative;
        height: 40px;
    }
    
    .navi>ul {
        width: 1100px;
        margin: -30px auto 0px;
        display: flex;
        justify-content: flex-end;
        height: 40px;
        width: 100%;
    }
    
    .navi>ul li {
        padding: 0px 8px 0px 5px;
    }
    
    .navi>ul li>a {
        color: rgb(0, 0, 0);
        padding-bottom: 5px;
    }
    
    .contents .page-content {
        width: 1100px;
        margin: 0px auto;
        padding: 0px 0px 30px;
        background: none;
        font-size: 14px;
        line-height: 1.8;
    }
    
    .contents .page-content h2 {
        padding: 0px 25px 10px;
        background-color: rgb(0, 86, 169);
        background-repeat: no-repeat;
        background-position: 10px 3px;
        color: rgb(255, 255, 255);
        margin: 40px auto 20px;
        font-size: 20px;
        font-weight: 700;
        position: relative;
        overflow-wrap: break-word;
    }
    
    .contents .page-content h3 {
        padding: 8px 15px;
        background: 12px center no-repeat rgb(243, 243, 243);
        color: rgb(51, 51, 51);
        margin: 30px auto 10px;
        font-size: 18px;
        font-weight: 700;
        clear: both;
    }
    
    .contents .page-content h5 {
        padding: 0px;
        color: rgb(51, 51, 51);
        margin: 10px auto 5px 5px;
        font-size: 14px;
        font-weight: 700;
        text-decoration: underline;
        margin: 5px auto 5px 5px;
        font-size: 1.2rem;
        font-weight: unset;
        text-decoration: none;
    }
    
    .contents .page-content p {
        margin-bottom: 20px;
        margin-left: 10px;
    }
    
    .contents .page-content img {
        width: auto;
    }
    
    .contents .page-content ul {
        padding-left: 1em;
        margin-bottom: 15px;
    }
    
    .contents .page-content ul li {
        font-size: 14px;
        margin-bottom: 5px;
        background: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABZ0RVh0Q3JlYXRpb24gVGltZQAwMi8yNS8yMPZqN5kAAAAcdEVYdFNvZnR3YXJlAEFkb2JlIEZpcmV3b3JrcyBDUzVxteM2AAABXUlEQVQokZWSP2uTURTGf+fe980bO9iUQkKGorh3EaShoWtL3SLWDPkE2Yqz4uIH6ObmFAuFoEOh0C9QElJc/AKhEiSRUCuKef/cexxCQgJd8lsfHs55znNEVVmk3B6+cUodwApnP16W3i/qMjNsfR7t/k79ifM8VbAAAs4avj4MzfH3F8WrueHxl9HOOPYdpyAso9NJbEam0q8Vu3Z0eBz1xul5ppQMkHglTpXUKSoQiuCB1OvOzd/so/35/PW7P6keAWRe2VqztPY2aDxZ42qU8CvxWBFUKQ3+eQ0mThuz2EmqfKiss1+OAAgq6xxcjgkiQYGJ04ZhRUzeyqdZ0FwoNDt3XAxiLgYxzc4duXCqCpC30pJm5zY67ce9xOu2AWKvZNl0ySAQIjMNHRm+1R89eLbyWQ1Av1bsFnKmGhquBdy8VXChoVfImWq/VuwuNT2j3B6+dcoruP81/gO9MKHH8nUUoQAAAABJRU5ErkJggg==") 0px center no-repeat;
        padding-left: 1.2em;
    }
    
    .footer {
        width: 100%;
        background: rgb(243, 243, 243);
        padding: 50px;
        color: rgb(51, 51, 51);
        position: absolute;
    }
    
    .footerBlock {
        width: 1100px;
        margin: 0px auto;
        display: flex;
        justify-content: space-between;
    }
    
    .footerBlock .leftBlock,
    .footerBlock .rightBlock {
        padding: 0px 20px;
    }
    
    .footerBlock .leftBlock {
        width: 70%;
        border-right: 1px solid rgb(207, 207, 207);
    }
    
    .footerBlock .leftBlock .sitename {
        font-weight: 700;
        font-size: 18px;
        margin-bottom: 15px;
    }
    
    .footerBlock .leftBlock .address {
        font-size: 14px;
        line-height: 1.8;
        margin-bottom: 15px;
    }
    
    .footerBlock .leftBlock .copyright {
        font-size: 14px;
        margin-top: 20px;
    }
    
    .footerBlock .rightBlock {
        width: 30%;
    }
    
    .footerBlock .rightBlock li {
        margin-bottom: 10px;
    }
    
    .footerBlock .rightBlock li>a {
        display: block;
        padding: 8px 10px;
        font-size: 16px;
        color: rgb(51, 51, 51);
    }
    
    .footer_bg {
        position: absolute;
        width: 0px;
        border-top: 15vw solid rgb(255, 255, 255);
        border-left: 15vw solid transparent;
        height: 0px;
        text-align: center;
        line-height: 30px;
        font-weight: 700;
        margin: 0px auto;
        color: rgb(102, 102, 102);
        top: 0px;
        right: 0px;
    }
    
    h1.logo {
        height: 90px;
        width: auto;
    }
    
    .pagetitle,
    .topline {
        width: 100%;
        background: rgb(243, 243, 243);
    }
    
    .topline {
        height: 20px;
    }
    
    .btn-144px {
        min-width: 144px;
        height: 38px;
    }
    
    .pointer {
        cursor: pointer;
    }
    
    .container {
        width: 1100px;
        max-width: none !important;
    }
    
    .contents .page-content ul.nav {
        padding-left: 0px;
        margin-bottom: 0px;
    }
    
    .contents .page-content ul li.nav-item {
        margin-bottom: 0px;
        background: none;
        padding-left: 0px;
    }
    
    .contents .page-content h2:before {
        content: "";
        width: 100%;
        display: block;
        position: absolute;
        border-bottom: 13px solid #0056a9;
        border-left: 13px solid transparent;
        height: 0;
        line-height: 30px;
        top: -13px;
        left: 0;
    }
    
    .white-space-pre-line {
        white-space: pre-line;
    }
    
    .break-word {
        word-break: break-word;
    }
    
    .footer_fix {
        min-width: 1350px;
    }
    
    .footer_bg_fix {
        border-top: 250px solid rgb(255, 255, 255);
        border-left: 250px solid transparent;
    }
    
    .navi>ul li.navilink.usage a:before {
        background-image: url(https://rde.nims.go.jp/_nuxt/img/usage.e57c944.png);
    }
    
    .container-fix {
        margin-left: auto;
        margin-right: auto;
        display: block;
    }
    
    .navi-fix {
        margin-right: 0px;
        padding-right: 0px;
    }
    
    .naviitem-width {
        max-width: 80%;
    }
    
    .topline-width {
        min-width: 1350px;
    }
    
    ul,
    ul.pagination li {
        padding-left: 0px !important;
        margin-bottom: 0px !important;
    }
    
    ul.pagination li {
        background: none !important;
    }
    
    .imageBox {
        height: 250px;
        max-width: 100%;
    }
    
    .image {
        height: 200px;
        object-fit: contain;
        width: 286px !important;
    }
    
    .image2 {
        height: 80px;
        width: 120px !important;
    }
    
    .radioSize {
        width: 13px !important;
    }
    
    .whiteBorder {
        border: 1px solid;
        color: rgb(255, 255, 255);
    }
    
    ul,
    ul li {
        margin-bottom: 0px !important;
    }
    
    ul li {
        list-style: none;
        background: none !important;
        padding-left: 1em;
    }
    
    ul {
        line-height: 1.5em;
        list-style-type: dot;
        padding-left: 0px !important;
        margin-bottom: 0px !important;
    }
    
    a:not([href]):not([class]),
    a:not([href]):not([class]):hover {
        color: inherit;
        text-decoration: none;
    }
    
    table {
        border-collapse: collapse;
        border-collapse: collapse;
        border-spacing: 0px;
    }
    
    th {
        text-align: -webkit-match-parent;
    }
    
    .table {
        width: 100%;
        margin-bottom: 1rem;
        color: rgb(33, 37, 41);
    }
    
    .table td,
    .table th {
        padding: 0.75rem;
        vertical-align: top;
        border-top: 1px solid rgb(222, 226, 230);
    }
    
    .table thead th {
        vertical-align: bottom;
        border-bottom: 2px solid rgb(222, 226, 230);
    }
    
    .table-sm td,
    .table-sm th {
        padding: 0.3rem;
    }
    
    .table-responsive {
        display: block;
        width: 100%;
        overflow-x: auto;
    }
    
    .btn-danger {
        color: rgb(255, 255, 255);
        background-color: rgb(220, 53, 69);
        border-color: rgb(220, 53, 69);
    }
    
    .btn-outline-primary {
        color: rgb(0, 123, 255);
        border-color: rgb(0, 123, 255);
    }
    
    .btn-link {
        font-weight: 400;
        color: rgb(0, 123, 255);
        text-decoration: none;
    }
    
    .align-middle {
        vertical-align: middle !important;
    }
    
    .bg-success {
        background-color: rgb(40, 167, 69) !important;
    }
    
    .border {
        border: 1px solid rgb(222, 226, 230) !important;
    }
    
    .ml-0,
    .mx-0 {
        margin-left: 0px !important;
    }
    
    .mt-1,
    .my-1 {
        margin-top: 0.25rem !important;
    }
    
    .mt-4,
    .my-4 {
        margin-top: 1.5rem !important;
    }
    
    .ml-5,
    .mx-5 {
        margin-left: 3rem !important;
    }
    
    .p-0 {
        padding: 0px !important;
    }
    
    .pr-1,
    .px-1 {
        padding-right: 0.25rem !important;
    }
    
    .pl-1,
    .px-1 {
        padding-left: 0.25rem !important;
    }
    
    .pr-3,
    .px-3 {
        padding-right: 1rem !important;
    }
    
    .pr-4,
    .px-4 {
        padding-right: 1.5rem !important;
    }
    
    .pl-4,
    .px-4 {
        padding-left: 1.5rem !important;
    }
    
    .mr-auto,
    .mx-auto {
        margin-right: auto !important;
    }
    
    .ml-auto,
    .mx-auto {
        margin-left: auto !important;
    }
    
    .text-center {
        text-align: center !important;
    }
    
    .text-primary {
        color: rgb(0, 123, 255) !important;
    }
    
    .b-table-sticky-header,
    .table-responsive,
    [class*="table-responsive-"] {
        margin-bottom: 1rem;
    }
    
    .b-table-sticky-header>.table,
    .table-responsive>.table,
    [class*="table-responsive-"]>.table {
        margin-bottom: 0px;
    }
    
    .btn .b-icon.bi,
    .dropdown-item .b-icon.bi,
    .dropdown-toggle .b-icon.bi,
    .input-group-text .b-icon.bi,
    .nav-link .b-icon.bi {
        font-size: 125%;
        vertical-align: text-bottom;
    }
    
    .contents .page-content table {
        background: rgb(204, 204, 204);
        border: 5px solid rgb(204, 204, 204);
        margin-bottom: 20px;
    }
    
    .contents .page-content table td,
    .contents .page-content table th {
        background: rgb(255, 255, 255);
        padding: 10px;
        font-size: 14px;
        border: 1px solid rgb(204, 204, 204);
    }
    
    .contents .page-content table th {
        background: rgb(243, 243, 243);
    }
    
    table td {
        word-break: break-word;
        overflow-wrap: break-word;
    }
    
    .tableFixed {
        table-layout: fixed;
        width: 100%;
        table-layout: fixed;
        width: 100%;
    }
    
    .word-break {
        word-break: break-word;
    }
    
    .h-0px {
        height: 0px;
    }
    
    .table-responsive>.table {
        width: 100%;
        table-layout: fixed;
        overflow-wrap: break-word;
        background: rgb(255, 255, 255);
    }
    
    .main-image-box-width {
        width: 500px;
    }
    
    .main-image-box {
        height: 350px;
        width: 500px;
    }
    
    .image-box {
        height: 80px;
        background-color: rgb(191, 191, 191);
    }
    
    .image-box,
    .image-box-width {
        width: 120px;
    }
    
    .main-image {
        height: 350px;
        width: 500px !important;
    }
    
    .image,
    .main-image {
        object-fit: contain;
    }
    
    .thumbnail-position {
        display: block;
    }
    
    .thumbnail-scroll {
        overflow-x: auto;
        flex-wrap: nowrap;
    }
    
    .w-200px {
        width: 200px;
    }
    
    .w-75px {
        width: 75px;
    }
    
    .gray {
        background-color: #bfbfbf;
        color: #fff;
    }

    .ban {
        cursor: not-allowed;
    }
    """

    # 圧縮する場合
    if COMPRESS:
        css = css.replace("\n", "").replace("  ", "")
    with open(out_css_file, "w", encoding="utf_8") as f:
        f.write(css)

def copy_images(input_dir, out_root_dir, out_img_dir):
    """ 画像フォルダのコピー """

    dirs = ["main_image", "other_image", "thumbnail"]

    # データ一覧ページの並び順の関係でdividedから処理する
    # dividedフォルダのコピー
    data_id = "0000"
    divided_dir = input_dir.joinpath("divided")
    if divided_dir.exists():
        for div in divided_dir.iterdir():
            data_id = div.name
            for d in dirs:
                in_dir  = div.joinpath(d)
                out_dir = out_img_dir.joinpath(div.name, d)
                if in_dir.exists():
                    if out_dir.exists():
                        shutil.rmtree(out_dir)
                    shutil.copytree(in_dir, out_dir)

    # トップレベルの画像フォルダをコピー
    for d in dirs:
        in_dir  = input_dir.joinpath(d)
        out_dir = out_img_dir.joinpath(f"{int(data_id)+1:04d}", d)
        if in_dir.exists():
            if out_dir.exists():
                shutil.rmtree(out_dir)
            shutil.copytree(in_dir, out_dir)

def write_log(text):
    """ 標準出力とログファイルへの書き込み """

    print(text)
    with open(LOG_FILE, "a", encoding="utf_8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S}\t{text}\n")

def check_idir(input_dir):
    """ 入力フォルダのチェック """

    # flagはエラーがある場合にTrueを返す
    flag = True
    if not input_dir.exists():
        write_log(f"[Error] 指定した入力フォルダ {input_dir} が見つかりません。")
    elif not input_dir.is_dir():
        write_log(f"[Error] 指定した入力フォルダ {input_dir} はフォルダではありません。")
    elif not input_dir.joinpath("meta", "metadata.json").exists():
        write_log(f"[Error] 指定した入力フォルダ {input_dir} にmeta/metadata.jsonが見つかりません。")
    elif not input_dir.joinpath("tasksupport", "metadata-def.json").exists():
        write_log(f"[Error] 指定した入力フォルダ {input_dir} にtasksupport/metadata-def.jsonが見つかりません。")
    elif not input_dir.joinpath("tasksupport", "invoice.schema.json").exists():
        write_log(f"[Error] 指定した入力フォルダ {input_dir} にtasksupport/invoice.schema.jsonが見つかりません。")
    elif input_dir.joinpath("job.failed").exists():
        write_log(f"[Error] 指定した入力フォルダ {input_dir} にjob.failedがあるので構造化が失敗しています。")
    else:
        write_log("[Info] 指定した入力フォルダのチェックが完了しました。")
        flag = False

    return flag

def get_out_root_dir(root_dir):
    """ 出力フォルダの取得 """

    # 1000回までフォルダ名を変えて作成する
    for i in range(1000):
        if i == 0:
            out_root_dir = root_dir.joinpath("output_preview")
        else:
            out_root_dir = root_dir.joinpath(f"output_preview_{i:04d}")

        if not out_root_dir.exists():
            out_root_dir.mkdir(parents=True)
            write_log(f"[Info] 出力フォルダ {out_root_dir} を作成しました。")
            break
    else:
        write_log(f"[Error] 出力フォルダを作成できませんでした。")
        sys.exit(1)

    return out_root_dir

def help_msg():
    """ ヘルプメッセージ """
    print("""
    usage: preview.py [-h] [input-data-dir]

    positional arguments:
      input-data-dir  input data directory after structured

    optional arguments:
      -h, --help  show this help message and exit
    """)

def main():
    global LOG_FILE

    # 入力ファイルが指定されていない場合は直下のdataディレクトリを処理対象とする
    if len(sys.argv) > 1:
        input_dir  = Path(sys.argv[1]).resolve()
        root_dir   = input_dir.parent
    else:
        root_dir  = Path(sys.argv[0]).resolve().parent
        input_dir = root_dir.joinpath("data")
    LOG_FILE = root_dir.joinpath("preview.log")
    out_root_dir = get_out_root_dir(root_dir)
    out_img_dir  = out_root_dir.joinpath("images")

    flag_idir = check_idir(input_dir)
    if flag_idir:
        input("エラーが発生したため、処理を中止します。Enterを押してください。")
        sys.exit(1)

    try:
        metadef_data = read_json(input_dir.joinpath("tasksupport", "metadata-def.json"))
        invsche_data = read_json(input_dir.joinpath("tasksupport", "invoice.schema.json"))
        data_info = get_data_info(input_dir)

        write_log("[Info] 画像ファイルのコピーを開始します。")
        copy_images(input_dir, out_root_dir, out_img_dir)
        write_log("[Info] 画像ファイルのコピーが完了しました。")

        write_log("[Info] style.cssの作成を開始します。")
        create_css(out_root_dir)
        write_log("[Info] style.cssの作成が完了しました。")

        write_log("[Info] index.htmlの作成を開始します。")
        create_dataList(input_dir, out_root_dir, data_info)
        write_log("[Info] index.htmlの作成が完了しました。")

        write_log("[Info] dataDetailの作成を開始します。")
        create_dataDetail(input_dir, out_root_dir, data_info, metadef_data, invsche_data)
        write_log("[Info] dataDetailの作成が完了しました。")

        input("正常に完了しました。プログラムを終了し、ブラウザで開きますのでEnterを押してください。")
        browser = webbrowser.get()
        browser.open_new_tab(f"{out_root_dir.joinpath('index.html').absolute()}")
    except:
        write_log(f"[Error] 予期せぬエラーが発生しました。\n{traceback.format_exc()}")
        input("エラーが発生したため、処理を中止します。Enterを押してください。")


if __name__ == "__main__":
    if "-h" in sys.argv:
        help_msg()
    else:
        main()
