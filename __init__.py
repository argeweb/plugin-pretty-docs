#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2016/07/08.

from argeweb import ViewDatastore
from models.pretty_docs_model import PrettyDocsModel, get_page as get_pretty_docs_page


__all__ = (
    'get_pretty_docs_page'
)
ViewDatastore.register('pretty_docs_list', PrettyDocsModel.all_enable)
ViewDatastore.register('pretty_docs', PrettyDocsModel.find_by_properties)

plugins_helper = {
    'title': u'說明文件',
    'desc': u'創建簡單實用的說明文件',
    'controllers': {
        'pretty_docs': {
            'group': u'說明文件',
            'actions': [
                {'action': 'list', 'name': u'說明文件'},
                {'action': 'add', 'name': u'新增文件'},
                {'action': 'edit', 'name': u'編輯文件'},
                {'action': 'view', 'name': u'檢視文件'},
                {'action': 'delete', 'name': u'刪除文件'},
                {'action': 'plugins_check', 'name': u'啟用停用模組'},
            ]
        },
        'config': {
            'group': u'說明文件設定',
            'actions': [
                {'action': 'config', 'name': u'說明文件相關設定'},
            ]
        },
    }
}
