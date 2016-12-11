#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.
import time

from argeweb import BasicModel
from argeweb import Fields
from pretty_docs_self_referential_model import PrettyDocsModel as Category
from pretty_docs_config_model import PrettyDocsConfigModel


def get_page(namespace, page_name):
    config = PrettyDocsConfigModel.find_or_create_by_name(namespace)
    if page_name == "index":
        template_name = u"/index.html"
        page = None
        page_list = PrettyDocsModel.all_enable()
    else:
        template_name = u"/docs.html"
        page = PrettyDocsModel.find_by_name(page_name)
        if page is not None:
            page.modified_time = str(page.modified).split(".")[0]
        page_list = PrettyDocsModel.all_enable(category=page_name)
        for item in page_list:
            item.children = PrettyDocsModel.all_enable(category_key=item.key).fetch()
    return config, page, page_list, template_name


class PrettyDocsModel(BasicModel):
    name = Fields.StringProperty(verbose_name=u"網址名稱")
    title = Fields.StringProperty(verbose_name=u"文件名稱")
    intro = Fields.StringProperty(verbose_name=u"文件簡介")
    icon = Fields.StringProperty(verbose_name=u"圖示名稱")
    page_color = Fields.StringProperty(default=u"", verbose_name=u"文件顏色",
                                       choices=(u"", u"green", u"blue", u"orange", u"red", u"pink", u"purple"))
    category = Fields.CategoryProperty(kind=Category, verbose_name=u"上層文件")
    is_enable = Fields.BooleanProperty(default=True, verbose_name=u"顯示於前台")
    content = Fields.RichTextProperty(verbose_name=u"文件內容")
    footer_content = Fields.RichTextProperty(verbose_name=u"頁尾內容")

    @classmethod
    def all_enable(cls, category=None, category_key=None, *args, **kwargs):
        cat = None
        if category and category_key is None:
            cat = cls.find_by_name(category)
            if cat is not None:
                category_key = cat.key
        if category_key is None:
            return cls.query(cls.category == None, cls.is_enable == True).order(-cls.sort)
        else:
            return cls.query(cls.category == category_key, cls.is_enable == True).order(-cls.sort)

    def before_put(self):
        super(PrettyDocsModel, self).before_put()
        if self.name is None or self.name is u"":
            self.name = str(int(time.time()))
