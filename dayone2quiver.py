# -*- coding: utf-8 -*-
"""DayOne2 の JSON ファイルを Quiver のノートブックを生成

Quiver ファイル構成

- ノートブック.qvnotebook/
    - meta.json
    - ノート1.qvnote/
        - meta.json
        - content.json
    - ノート2.qvnote/
        - meta.json
        - content.json
    - ...
"""
import os
import json
from datetime import datetime, timedelta

from conf import (
    BASE_PATH,
    DAYONE_JSON_PATH,
)


def gen_note(notebook_path, uuid, title, body, created_at):
    """ノートの生成
    """
    note_path = os.path.join(notebook_path, '{}.qvnote'.format(uuid))
    if not os.path.exists(note_path):
        os.makedirs(note_path)

    meta_path = os.path.join(note_path, 'meta.json')
    meta = {
        'created_at' : created_at,
        'tags' : [],
        'title' : title,
        'updated_at' : created_at,
        'uuid': uuid,
    }
    with open(meta_path, 'w') as f:
        data = json.dumps(meta)
        f.write(data)

    content_path = os.path.join(note_path, 'content.json')
    content = {
        'title' : title,
        'cells': [{
            'type': 'markdown',
            'data': body
        }]
    }
    with open(content_path, 'w') as f:
        data = json.dumps(content)
        f.write(data)

def gen_all_note(notebook_path):
    """全ノート情報を読み込み、ノートを生成する
    """
    with open(DAYONE_JSON_PATH, 'r') as f:
        json_data = f.read()
    data = json.loads(json_data)
    for i, entry in enumerate(data['entries'], 1):
        uuid = entry['uuid']
        body = entry['text']
        title = body.split('\n')[0]
        date_str = entry['creationDate']
        created_at = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ') + timedelta(hours=9)
        created_at = int(created_at.timestamp())

        print('{}: "{}" ({})'.format(i, title, created_at))
        gen_note(notebook_path, uuid, title, body, created_at)

def gen_notebook(uuid, name):
    """ノートブックの生成
    """
    notebook_path = os.path.join(BASE_PATH, '{}.qvnotebook'.format(uuid))
    if not os.path.exists(notebook_path):
        os.makedirs(notebook_path)

    meta_path = os.path.join(notebook_path, 'meta.json')
    meta = {
        'name': name,
        'uuid': uuid,
    }
    with open(meta_path, 'w') as f:
        data = json.dumps(meta)
        f.write(data)

    return notebook_path

def main(uuid, name):
    notebook_path = gen_notebook()
    gen_all_note(notebook_path)

if __name__ == '__main__':
    main('SampleNotebook1', 'Sample Notebook 1')
