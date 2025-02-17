# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.core.serializers import serialize

import hashlib
import uuid
import os
import datetime
import decimal

from collections import OrderedDict
from itertools import chain

from django.contrib.admin.utils import (
    lookup_field, NestedObjects
)
from django.contrib.auth import get_permission_codename
from django.db import models, router
from django.conf import settings
from django.utils import formats, six, timezone
from django.utils.encoding import force_text
from django.utils.module_loading import import_string
from django.utils.html import format_html
from django.utils.http import urlencode
from django.utils.text import capfirst
from django.utils.safestring import mark_safe

# from django.views.generic.base import logger

from idcops.models import Option


COLOR_TAGS = getattr(settings, 'COLOR_TAGS', True)

COLOR_FK_FIELD = getattr(settings, 'COLOR_FK_FIELD', False)


def get_deleted_objects(objs, request, admin_site):
    """
    Find all objects related to ``objs`` that should also be deleted. ``objs``
    must be a homogeneous iterable of objects (e.g. a QuerySet).

    Return a nested list of strings suitable for display in the
    template with the ``unordered_list`` filter.
    """
    try:
        obj = objs[0]
    except IndexError:
        return [], {}, set(), []
    else:
        using = router.db_for_write(obj._meta.model)
    collector = NestedObjects(using=using)
    collector.collect(objs)
    perms_needed = set()

    def format_callback(obj):
        model = obj.__class__
        has_admin = model in admin_site._registry
        opts = obj._meta

        no_edit_link = '%s: %s' % (capfirst(opts.verbose_name), obj)

        if has_admin:
            # Display a link to the admin page.
            return format_html('{}: <a href="{}">{}</a>',
                               capfirst(opts.verbose_name),
                               obj.get_absolute_url,
                               obj)
        else:
            # Don't display link to edit, because it either has no
            # admin or is edited inline.
            return no_edit_link

    to_delete = collector.nested(format_callback)

    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {model._meta.verbose_name_plural: len(
        objs) for model, objs in collector.model_objs.items()}

    return to_delete, model_count, perms_needed, protected


def get_content_type_for_model(obj, fcm=False):
    # Since this module gets imported in the application's root package,
    # it cannot import models from other applications at the module level.
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(obj, for_concrete_model=fcm)


# def make_cache_key(key):
#     return cache_key.make_template_fragment_key(key)


# def user_cache_key(user, mark):
#     key = '{}.user{}'.format(mark, user.id)
#     return make_cache_key(key)


def has_form_class(model_name):
    from idcops import forms
    name = model_name.capitalize()
    has_add_form = "{}NewForm".format(name) in dir(forms)
    has_edit_form = "{}Form".format(name) in dir(forms)
    return has_add_form or has_edit_form


def shared_queryset(queryset, onidc_id):
    effective = {'deleted': False, 'actived': True}
    _shared = queryset.filter(**effective).filter(mark='shared')
    effective.update({'onidc_id': onidc_id})
    _private = queryset.filter(**effective)
    data = _shared | _private
    return data


def nature_field_name(model):
    """ Return model CharField , SlugField Field name use nature field."""
    opts = model._meta
    fields = [
        f.name for f in opts.fields if (
            isinstance(f, (models.CharField, models.GenericIPAddressField))
            and not getattr(f, 'blank', False)
        )
    ]
    if fields:
        if 'name' in fields:
            return 'name'
        elif 'text' in fields:
            return 'text'
        elif 'title' in fields:
            return 'title'
        elif 'username' in fields:
            return 'username'
        elif 'linenum' in fields:
            return 'linenum'
        elif 'kcnum' in fields:
            return 'kcnum'
        elif 'address' in fields:
            return 'address'
        else:
            if 'created' in [f.name for f in opts.fields]:
                return 'created'
            else:
                return fields[0]
    else:
        if 'created' in [f.name for f in opts.get_fields()]:
            return 'created'
        else:
            return '{}'.format(opts.pk.attname)


def allow_search_fields(cls, exclude=None):
    opts = cls._meta
    if not exclude:
        exclude = ['onidc', 'slug', 'created', 'modified']
    exclude.extend([f.name for f in opts.fields if getattr(f, 'choices')])
    fields = []
    for f in opts.fields:
        if exclude and f.name in exclude:
            continue
        if isinstance(f, models.ForeignKey):
            submodel = f.related_model
            for sub in submodel._meta.fields:
                if exclude and sub.name in exclude:
                    continue
                if isinstance(sub, models.CharField) \
                        and not getattr(sub, 'choices'):
                    fields.append(f.name + '__' + sub.name + '__icontains')
        if isinstance(f, models.CharField):
            fields.append(f.name + '__icontains')
    return fields


def select_related_fields(cls, exclude=None):
    if exclude is None:
        exclude = ['onidc']
    opts = cls._meta
    rel_fileds = [f.name for f in opts.fields
                  if isinstance(f, models.ForeignKey)
                  and f.name not in exclude]
    return rel_fileds


def fields_for_model(model, fields=None, exclude=None):
    field_list = []
    opts = model._meta
    for f in chain(opts.concrete_fields, opts.many_to_many):
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        else:
            field_list.append((f.name, f))
    field_dict = OrderedDict(field_list)
    return field_dict


def make_boolean_icon(field_val):
    choice = {
        True: 'fa fa-check-circle text-green',
        False: 'fa fa-ban on fa-check-circle text-red',
        None: 'unknown'}[field_val]
    return format_html('<i class="{}"></i>'.format(choice))


def make_color_icon(field_val):
    return format_html('<i class="fa fa-square text-{}"'.format(field_val))


def display_for_value(value):
    if isinstance(value, bool):
        return force_text(value)
    elif isinstance(value, (int, decimal.Decimal, float)):
        return formats.number_format(value)
    elif isinstance(value, (list, tuple)):
        return ', '.join(force_text(v) for v in value)
    elif isinstance(value, six.integer_types + (decimal.Decimal, float)):
        return formats.number_format(value)
    elif isinstance(value, datetime.datetime):
        return formats.localize(timezone.template_localtime(value))
    elif isinstance(value, (datetime.date, datetime.time)):
        return formats.localize(value)
    elif isinstance(value, models.query.QuerySet):
        if value.model is Option and COLOR_TAGS:
            html = ''
            for v in value:
                item = f'<span class="badge bg-{v.color}">{v.text}</span>&nbsp'
                html += item
            return mark_safe(html)
        else:
            value = [force_text(i) for i in value]
            return display_for_value(value)
    else:
        return force_text(value)


def display_for_field(value, field, html=True, only_date=True):
    if getattr(field, 'flatchoices', None):
        if html and field.name == 'color' and value:
            return make_color_icon(value)
        return dict(field.flatchoices).get(value, '')
    elif html and (isinstance(field, (
            models.BooleanField, models.NullBooleanField))):
        return make_boolean_icon(value)
    elif isinstance(field, (models.BooleanField, models.NullBooleanField)):
        boolchoice = {False: "否", True: "是"}
        return boolchoice.get(value)
    elif value is None:
        return ""
    elif isinstance(field, models.DecimalField):
        return formats.number_format(value, field.decimal_places)
    elif isinstance(field, (models.IntegerField, models.FloatField)):
        return formats.number_format(value)
    elif isinstance(field, models.ForeignKey) and value:
        rel_obj = field.related_model.objects.get(pk=value)
        if html and COLOR_FK_FIELD and isinstance(rel_obj, Option):
            text_color = rel_obj.color
            if not text_color:
                text_color = 'text-info'
            safe_value = format_html(
                f'<span class="text-{text_color}">{rel_obj.text}</span>')
            return safe_value
        return force_text(rel_obj)
    elif isinstance(field, models.TextField) and value:
        return force_text(value)
    elif isinstance(field, models.DateTimeField):
        if only_date:
            return formats.date_format(value)
        return formats.localize(timezone.template_localtime(value))
    elif isinstance(field, (models.DateField, models.TimeField)):
        return formats.localize(value)
    elif isinstance(field, models.FileField) and value:
        return format_html('<a href="{}">{}</a>', value.url, value)
    else:
        return display_for_value(value)


def get_query_string(params, new_params=None, remove=None):
    new_params = new_params if new_params else {}
    remove = remove if remove else []
    p = params.copy()
    for r in remove:
        for k in list(p):
            if k.startswith(r):
                del p[k]
    for k, v in new_params.items():
        if v is None:
            if k in p:
                del p[k]
        else:
            p[k] = v
    if p:
        return '?%s' % urlencode(sorted(p.items()))
    else:
        return ''


def make_tbody_tr(
    lmv, obj, row_num, fields, extra_fields, only_date,
    verbose_name, to_field_name
):
    """Return tbody tr items."""
    opts = lmv.opts
    detail_link = obj.get_absolute_url
    update_link = obj.get_edit_url
    rowdata = list()
    for field_name in fields:
        td_format = '<td class="{}">{}</td>'
        td_text = ''
        td_class = "{}".format(field_name)
        if field_name == 'field-first':
            td_text = obj.pk
            td_format = '''<td class="no-print {}">
                <input type="checkbox" name="index" value="{}"></td>'''
        if field_name == 'field-second':
            td_text = row_num
            td_format = '<td class="{}">{}.</td>'
        if field_name == 'field-last':
            _edit = ''
            if can_change(opts, lmv.request.user):
                _edit = f'''
                    <a title="编辑" href="{update_link}">
                    <span class="label label-warning margin-r-5">编辑</span>
                    </a>'''
            _show = f'''
                <a title="弹窗模式进行查看" href="{detail_link}"
                data-toggle="modal" data-target="#modal-lg">
                <span class="label label-info">查看</span>
                </a>'''
            td_text = mark_safe(_edit + _show)
            td_format = '<td class="no-print {}">{}</td>'
        if field_name not in extra_fields:
            td_class = "field-{}".format(field_name)
            td_format = '<td class="{}">{}</td>'
            classes = 'text-info'
            try:
                field = opts.get_field(field_name)
                value = field.value_from_object(obj)
                td_text = display_for_field(value, field, only_date=only_date)
                if field.name == to_field_name:
                    title = f"点击查看 {opts.verbose_name} 为 {force_text(obj)} 的详情信息"
                    td_text = mark_safe(
                        f'<a title="{title}" href="{detail_link}">{td_text}</a>'
                    )
                if getattr(field, 'flatchoices', None) \
                        or isinstance(field,
                                      (models.ForeignKey,
                                       models.BooleanField, models.NullBooleanField)):
                    link = lmv.get_query_string(
                        {'{}'.format(field.name): '{}'.format(value)}, ['page']
                    )
                    td_title = display_for_field(
                        value, field, html=False, only_date=only_date
                    )
                    title = f"点击过滤 {field.verbose_name} 为 {td_title} 的所有 {verbose_name}"
                    td_text = mark_safe(
                        f'<a class="{classes}" title="{title}" href="{link}">{td_text}</a>'
                    )
            except BaseException:
                _, _, _td_text = lookup_field(field_name, obj, obj._meta.model)
                td_text = mark_safe(_td_text)
        tr = format_html(td_format, td_class, td_text)
        rowdata.append(tr)
    return mark_safe(''.join(rowdata))


def make_dict(data_dict):
    data = {}
    for k, v in data_dict.items():
        if isinstance(v, list):
            data[k] = [(i.pk) for i in v]
        # if isinstance(v, (IPv4Network, IPv6Network)):
        #     data[k] = str(v)
        # if isinstance(v, datetime.datetime):
        #     data[k] = str(v)
        else:
            data[k] = str(v)
    return data


def get_forms_names():
    forms = import_string('idcops.forms')
    return dir(forms)


def _has_form(model_name):
    return "{}Form".format(model_name) in get_forms_names()


def _has_add_form(model_name):
    name = model_name.capitalize()
    return _has_form(name) or "{}NewForm".format(name) in get_forms_names()


def _has_edit_form(model_name):
    name = model_name.capitalize()
    return _has_form(name) or "{}EditForm".format(name) in get_forms_names()


def has_permission(opts, user, perm):
    codename = get_permission_codename(perm, opts)
    return user.has_perm("%s.%s" % (opts.app_label, codename))


def can_create(opts, user):
    # from idcops import forms
    name = opts.model_name.capitalize()
    return has_permission(opts, user, 'add') and _has_add_form(name)


def can_change(opts, user):
    # from idcops import forms
    name = opts.model_name.capitalize()
    return has_permission(opts, user, 'change') and _has_edit_form(name)


def diff_dict(d1, d2, exclude=None):
    if exclude is None:
        exclude = ['operator', 'creator', 'modified', 'created']
    diffs = [(k, (v, d2[k]))
             for k, v in d1.items() if v != d2[k] and k not in exclude]
    return dict(diffs)


def get_actions(opts, user):
    actions = []
    name = opts.model_name.lower()
    ACTION_PATH = 'idcops.actions'
    try:
        action_list = import_string("{}.{}".format(ACTION_PATH, name))
    except BaseException:
        action_list = import_string("{}.general".format(ACTION_PATH))
    for a in action_list:
        action = get_action(import_string("{}.{}".format(ACTION_PATH, a)))
        perm, _, _, _ = action
        p = '%s.%s' % (opts.app_label, get_permission_codename(perm, opts))
        if user.has_perm(p):
            actions.append(action)
    return actions


def get_action(action):
    func = action
    action = action.__name__
    if hasattr(func, 'description'):
        description = func.description
    else:
        description = action.replace('_', ' ')
    if hasattr(func, 'icon'):
        icon = func.icon
    else:
        icon = 'fa fa-circle-o'
    if hasattr(func, 'required'):
        perm = func.required
    else:
        perm = 'change'
    return perm, action, icon, description


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    today = timezone.datetime.now().strftime(r'%Y/%m/%d')
    return os.path.join('uploads', today, filename)


def get_file_md5(f):
    m = hashlib.md5()
    while True:
        data = f.read(1024)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def serialize_object(obj, extra=None):
    """
    Return a generic JSON representation of an object using Django's built-in serializer. (This is used for things like
    change logging, not the REST API.) Optionally include a dictionary to supplement the object data. A list of keys
    can be provided to exclude them from the returned dictionary. Private fields (prefaced with an underscore) are
    implicitly excluded.
    """
    json_str = serialize('json', [obj])
    data = json.loads(json_str)[0]['fields']
    # Append any extra data
    if extra is not None:
        data.update(extra)
    return data
