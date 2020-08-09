"""
Definition of forms.
"""
from PIL import Image
from django import forms
from django.core.files import File
from .models import BasicModel

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class HomeForm(forms.ModelForm):
        #post = forms.CharField(required =False)
        #img = forms.FileField()
        id_name = forms.CharField(widget=forms.HiddenInput)
        image_resend = forms.CharField(widget=forms.HiddenInput)
        image_to_process = forms.CharField(widget=forms.HiddenInput)
        thresh  = forms.FloatField(initial=0)
        scale = forms.FloatField(initial=30)
        length_dangling_arc = forms.FloatField(initial=100)
        section_size = forms.FloatField(initial=100,label='Size of the section (in m)')


        class Meta:
            model = BasicModel
            fields = ('image_resend','image_to_process','thresh', 'scale', 'length_dangling_arc', ) #removed 'uploadedImage'
            # widgets = {
            # 'uploadedImage': forms.FileInput(attrs={
            #     'accept': 'image/*'  # this is not an actual validation! don't rely on that!
            #    })
            # }
            def __init__(self, *args, **kwargs):
                    super(HomeForm, self).__init__(*args, **kwargs)
                    self.fields['image_to_process'].widget = HiddenInput()
            # def __init__(self, *args, **kwargs):
            #     super(HomeForm, self).__init__(*args, **kwargs)
            #     self.fields['x'].widget = FloatField(attrs={
            #         'id': 'x_coordinate',
            #         'class': 'coordinate',
            #         'name':'x_coordinate',
            #             })
            #     self.fields['y'].widget = TextInput(attrs={
            #         'id': 'y_coordinate',
            #         'class': 'coordinate',
            #         'name':'y_coordinate',
            #             })
            #     self.fields['width'].widget = TextInput(attrs={
            #         'id': 'width',
            #         'class': 'length',
            #         'name':'width',
            #             })
            #     self.fields['height'].widget = TextInput(attrs={
            #         'id': 'height',
            #         'class': 'length',
            #         'name':'height',
            #             })

            # def save(self):
            #     uploaded_file = super(HomeForm, self).save()

            #     x = self.cleaned_data.get('x')
            #     y = self.cleaned_data.get('y')
            #     w = self.cleaned_data.get('width')
            #     h = self.cleaned_data.get('height')

            #     image = Image.open(uploaded_file.file)
            #     cropped_image = image.crop((x, y, w+x, h+y))
            #     resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            #     resized_image.save(uploaded_file.file.path)

            #     return uploaded_file

class image_form(forms.Form):
    uploaded_image = forms.ImageField(widget=forms.HiddenInput)
