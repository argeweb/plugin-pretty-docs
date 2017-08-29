#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import BasicModel
from argeweb import Fields


class ConfigModel(BasicModel):
    title = Fields.StringProperty(verbose_name=u'設定名稱', default=u'說明文件相關設定')
    theme = Fields.StringProperty(verbose_name=u'主題樣式', default=u'pretty_docs')
    category_depth = Fields.IntegerProperty(verbose_name=u'文件深度', default=6)
    custom_url_name = Fields.BooleanProperty(verbose_name=u'自定義文件網址名稱', default=True)
    index_tagline = Fields.RichTextProperty(verbose_name=u'首頁簡介', default=u'')
    index_content = Fields.RichTextProperty(verbose_name=u'首頁內容', default=u'')
    footer_content = Fields.RichTextProperty(verbose_name=u'頁尾內容', default=u'')
    social_container = Fields.RichTextProperty(verbose_name=u'社群分享區塊', default=u'')
