#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import BasicModel
from argeweb import Fields


class PrettyDocsConfigModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u'識別名稱')
    title = Fields.StringProperty(default=u'ArgeWeb', verbose_name=u'標題')
    theme = Fields.StringProperty(default=u'pretty_docs', verbose_name=u'主題樣式')
    category_depth = Fields.IntegerProperty(default=6, verbose_name=u'文件深度')
    custom_url_name = Fields.BooleanProperty(default=True, verbose_name=u'自定義文件網址名稱')
    index_tagline = Fields.RichTextProperty(default=u'', verbose_name=u'首頁簡介')
    index_content = Fields.RichTextProperty(default=u'', verbose_name=u'首頁內容')
    footer_content = Fields.RichTextProperty(default=u'', verbose_name=u'頁尾內容')
    social_container = Fields.RichTextProperty(default=u'', verbose_name=u'社群分享區塊')
