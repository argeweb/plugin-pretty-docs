#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import Controller, scaffold, route_menu, Fields, route_with, route
from argeweb.components.pagination import Pagination
from argeweb.components.search import Search


class PrettyDocsConfig(Controller):
    class Meta:
        components = (scaffold.Scaffolding, Pagination, Search)
        pagination_limit = 10

    class Scaffold:
        display_properties_in_list = ("title", "is_enable", "category")
        hidden_properties_in_edit = ("name",)

    @route
    def admin_config(self):
        record = self.meta.Model.find_by_name(self.namespace)
        if record is None:
            record = self.meta.Model()
            record.name = self.namespace
            record.put()
        return scaffold.edit(self, record.key)

