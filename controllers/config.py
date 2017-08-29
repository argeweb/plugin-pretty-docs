#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import Controller, scaffold, route_menu, route


class Config(Controller):
    class Scaffold:
        display_in_list = ['title', 'is_enable', 'category']

    @route
    @route_menu(list_name=u'system', group=u'系統設定', text=u'說明文件設定', sort=9981)
    def admin_config(self):
        config_record = self.meta.Model.get_or_create_by_name('pretty_docs_config')
        return scaffold.edit(self, config_record.key)
