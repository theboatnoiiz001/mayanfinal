from django import forms

from mayan.apps.views.forms import DetailForm

from .models import Theme, UserThemeSetting


class ThemeForm(forms.ModelForm):
    class Meta:
        fields = ('label','brand_name','logo_path','status_theme','javascript_data','stylesheet','font','font_other','color_font_header','background_color_header','background_color_menu','menu_text_color','background_menu_dropdown','background_website','background_color_header_panel','btn_color_primary','btn_color_danger','btn_color_success','btn_color_default','font_size_header','font_size_menu','font_size_content_title')
        model = Theme


class UserThemeSettingForm(forms.ModelForm):
    class Meta:
        fields = ('theme',)
        model = UserThemeSetting
        widgets = {
            'theme': forms.Select(
                attrs={
                    'class': 'select2'
                }
            ),
        }


class UserThemeSettingForm_view(DetailForm):
    class Meta:
        fields = ('theme',)
        model = UserThemeSetting
