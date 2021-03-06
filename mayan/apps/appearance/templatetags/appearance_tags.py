from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template import Library
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.module_loading import import_string
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from mayan.apps.appearance.models import Theme
from django.shortcuts import get_object_or_404

from ..literals import COMMENT_APP_TEMPLATE_CACHE_DISABLE

app_templates_cache = {}
register = Library()


@register.simple_tag(takes_context=True)
def appearance_app_templates(context, template_name):
    """
    Fetch the app templates for the requested `template_name`, render it with
    the current `request` from the `context`, and cache it for future use
    unless the template has the no caching comment.
    """
    result = []

    for app in apps.get_app_configs():
        template_id = '{}.{}'.format(app.label, template_name)
        if template_id not in app_templates_cache or settings.DEBUG:
            try:
                app_template = get_template(
                    '{}/app/{}.html'.format(app.label, template_name)
                )
                app_template_output = app_template.render(
                    request=context.get('request')
                )

                if COMMENT_APP_TEMPLATE_CACHE_DISABLE not in app_template.template.source:
                    app_templates_cache[template_id] = app_template_output
            except TemplateDoesNotExist:
                """
                Non fatal just means that the app did not defined an app
                template of this name and purpose.
                """
                app_templates_cache[template_id] = ''
                app_template_output = ''
        else:
            app_template_output = app_templates_cache[template_id]

        result.append(app_template_output)

    return mark_safe(' '.join(result))


@register.filter
def appearance_get_choice_value(field):
    try:
        return dict(field.field.choices)[field.value()]
    except TypeError:
        return ', '.join([subwidget.data['label'] for subwidget in field.subwidgets if subwidget.data['selected']])
    except KeyError:
        return _('None')


@register.filter
def appearance_get_form_media_js(form):
    return [form.media.absolute_path(path) for path in form.media._js]


@register.simple_tag
def appearance_get_icon(icon_path):
    return import_string(dotted_path=icon_path).render()


@register.simple_tag
def appearance_get_user_theme_stylesheet(user):
    User = get_user_model()

    if user and user.is_authenticated:
        try:
            theme = user.theme_settings.theme
        except User.theme_settings.RelatedObjectDoesNotExist:
            # User had a setting assigned which was later deleted.
            return ''
        else:
            if theme:
                return user.theme_settings.theme.stylesheet

    return ''

@register.simple_tag
def appearance_get_user_theme_script():
    try:
        obj = Theme.objects.get(status_theme='On')
        context = obj.brand_name +  "|" + obj.logo_path + "|" + obj.color_font_header + "|" + obj.background_color_header + "|" + obj.background_color_menu + "|" + obj.background_color_header_panel + "|" + obj.background_website + "|" + obj.background_menu_dropdown + "|" + obj.btn_color_primary + "|" + obj.btn_color_danger + "|" + obj.btn_color_success + "|" + obj.btn_color_default + "|" + str(obj.font_size_header) + "|" + str(obj.font_size_menu) + "|" + str(obj.font_size_content_title)+ "|" + obj.menu_text_color
    except Theme.DoesNotExist:
        context = "Mayan-EDMS||#ffffff|#2f3c4f|#2f3c4f|#2f3c4f|#ffffff|#2f3c4f|#1b232e|#fe0000|#4aaa97|#95a5a6|19|15|50|#ffffff"    
    
    return context


@register.simple_tag
def color_background_nav():
    try:
        obj = Theme.objects.get(status_theme='On')
        context = obj.background_color_header
    except Theme.DoesNotExist:
        return '#2f3c4f'
    return context


@register.simple_tag
def get_fontraw():
    try:
        obj = Theme.objects.get(status_theme='On')
        if obj.font_other:
            fontname = obj.font_other
        else:
            fontname = obj.font
        
        context = fontname
        return context
    except Theme.DoesNotExist:
        return 'Roboto'


@register.simple_tag
def get_font_link():
    try:
        obj = Theme.objects.get(status_theme='On')
        if obj.font_other:
            fontname = obj.font_other
        else:
            fontname = obj.font
        
        fontRaw = fontname
        fontLink = fontRaw.replace(" ", "+")
        return fontLink
    except Theme.DoesNotExist:
        fontRaw = "Roboto"
    
    fontLink = fontRaw.replace(" ", "+")
    return fontLink
    

@register.simple_tag
def theme_stylesheet():
    try:
        obj = Theme.objects.get(status_theme='On')
    except Theme.DoesNotExist:
        return ''
    
    return obj.stylesheet

@register.simple_tag
def theme_javascript_data():
    try:
        obj = Theme.objects.get(status_theme='On')
    except Theme.DoesNotExist:
        return ''
    
    return obj.javascript_data

@register.simple_tag
def appearance_icon_render(icon, enable_shadow=False):
    return icon.render(extra_context={'enable_shadow': enable_shadow})


@register.filter
def appearance_object_list_count(object_list):
    try:
        return object_list.count()
    except TypeError:
        return len(object_list)
