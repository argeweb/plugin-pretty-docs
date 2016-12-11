#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
from argeweb import Controller, scaffold, route_menu, Fields, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search
from ..models.pretty_docs_model import get_page
from ..models.pretty_docs_config_model import PrettyDocsConfigModel
import time
import random


class PrettyDocs(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 1000

    class Scaffold:
        display_properties_in_list = ["name", "title", "title_lang_zhtw", "is_enable", "category"]
        hidden_properties_in_edit = []
        excluded_properties_in_from = ()

    @route_with(template='/docs/<:(.*)>')
    def doc_path(self, path):
        self.context["config"], self.context["page"], self.context["list"], self.meta.view.template_name = \
            get_page(self.namespace, path)
        self.meta.view.theme = self.context["config"].theme

    @route_menu(list_name=u"backend", text=u"說明文件", sort=331, group=u"內容管理", need_hr=True)
    def admin_list(self):
        self.context["config"] = PrettyDocsConfigModel.find_or_create_by_name(self.namespace)
        self.check_field_config(self.context["config"], self.Scaffold)
        return scaffold.list(self)

    @route
    def admin_add(self):
        self.context["config"] = PrettyDocsConfigModel.find_or_create_by_name(self.namespace)
        self.check_field_config(self.context["config"], self.Scaffold)
        return scaffold.add(self)

    @route
    def admin_edit(self, key):
        self.context["config"] = PrettyDocsConfigModel.find_or_create_by_name(self.namespace)
        self.check_field_config(self.context["config"], self.Scaffold)
        return scaffold.edit(self, key)

    @staticmethod
    def check_field_config(config, scaffold, *args, **kwargs):
        if config.custom_url_name is False:
            if "name" in scaffold.display_properties_in_list:
                scaffold.display_properties_in_list.remove("name")
            if hasattr(scaffold, "display_properties") and "name" in scaffold.display_properties:
                scaffold.display_properties.remove("name")
            scaffold.hidden_properties_in_edit.append("name")

    @route
    def admin_change_parent(self):
        parent = self.params.get_ndb_record("parent")
        target = self.params.get_ndb_record("target")
        if parent is not None:
            if parent.key != target.key:
                target.category = parent.key
        else:
            target.category = None
        target.must_update_product = True
        target.must_update_timestamp = time.time()
        target.put()

        self.meta.change_view("json")
        self.context["data"] = {
            "move": "done"
        }

    @route
    def admin_change_sort(self):
        sort = self.params.get_ndb_record("sort")
        sort_before = self.params.get_ndb_record("sort_before")
        target = self.params.get_ndb_record("target")
        s = [target.sort]
        if sort is not None:
            s.append(sort.sort)
        else:
            s = [time.time()]
        if sort_before is not None:
            s.append(sort_before.sort)
        s = sorted(s, reverse=True)
        if len(s) == 1:
            target.sort = s[0]
            target.put_async()
        if len(s) == 2:
            if sort is not None:
                sort.sort = s[0]
                sort.put_async()
                target.sort = s[1]
                target.put_async()
            else:
                target.sort = s[0]
                target.put_async()
                sort_before.sort = s[1]
                sort_before.put_async()
        if len(s) == 3:
            sort.sort = s[0]
            sort.put_async()
            target.sort = s[1]
            target.put_async()
            sort_before.sort = s[2]
            sort_before.put_async()

        self.meta.change_view("json")
        self.context["data"] = {
            "sort": "done"
        }
