#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2015/7/12.

from argeweb import auth, add_authorizations
from argeweb import Controller, scaffold, route_menu, Fields, route_with, route
from ..models.pretty_docs_model import get_page
from ..models.config_model import ConfigModel
import time


class PrettyDocs(Controller):
    class Scaffold:
        display_in_list = ['name', 'title', 'title_lang_zhtw', 'is_enable', 'category']

    @add_authorizations(auth.check_user)
    @route_with(template="/docs/<:(.*)>")
    @route_with(template="/docs/<:(.*)>.html")
    def doc_path(self, path):
        self.meta.pagination_limit = 1000
        self.context['config'], self.context['page'], self.context['list'], self.meta.view.template_name = \
            get_page(path)
        self.meta.view.theme = self.context['config'].theme
        self.context['path'] = u'/docs/' + path
        if self.application_user and self.application_user_level >= 999:
            self.context['editable'] = self.params.get_boolean('edit')

    @route_menu(list_name=u'backend', group=u'內容管理', need_hr=True, text=u'說明文件', sort=331)
    def admin_list(self):
        page_view = self.params.get_header('page_view')
        self.context['config'] = ConfigModel.get_or_create_by_name('pretty_docs_config')
        self.check_field_config(self.context['config'], self.Scaffold)
        if page_view == u'sort':
            self.meta.view.template_name = '/pretty_docs/admin_sort.html'
            self.context['change_view_to_edit_function'] = 'reload'
            self.context['change_view_to_view_function'] = 'reload'
            self.context['change_view_to_delete_function'] = 'reload'
        else:
            self.context['change_view_to_sort_function'] = 'reload'
        return scaffold.list(self)

    @route
    def admin_add(self):
        self.context['config'] = ConfigModel.get_or_create_by_name('pretty_docs_config')
        self.check_field_config(self.context['config'], self.Scaffold)
        return scaffold.add(self)

    @route
    def admin_edit(self, key):
        self.context['config'] = ConfigModel.get_or_create_by_name('pretty_docs_config')
        self.check_field_config(self.context['config'], self.Scaffold)
        return scaffold.edit(self, key)

    @staticmethod
    def check_field_config(config, scaffold, *args, **kwargs):
        if config.custom_url_name is False:
            if 'name' in scaffold.display_in_list:
                scaffold.display_in_list.remove('name')
            if hasattr(scaffold, 'display_in_form') and 'name' in scaffold.display_in_form:
                scaffold.display_in_form.remove('name')
            scaffold.hidden_in_form.append('name')

    @route
    def admin_change_parent(self):
        parent = self.params.get_ndb_record('parent')
        target = self.params.get_ndb_record('target')
        if parent is not None:
            if parent.key != target.key:
                target.category = parent.key
        else:
            target.category = None
        target.must_update_timestamp = time.time()
        target.put()

        self.meta.change_view('json')
        self.context['data'] = {
            'move': 'done'
        }

    @route
    def admin_change_sort(self):
        sort = self.params.get_ndb_record('sort')
        sort_before = self.params.get_ndb_record('sort_before')
        target = self.params.get_ndb_record('target')
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

        self.meta.change_view('json')
        self.context['data'] = {
            'sort': 'done'
        }
