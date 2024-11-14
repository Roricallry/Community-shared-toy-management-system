from django import forms
from .models import Toy_type


#搜索表单
class ToySearchForm(forms.Form):
    query = forms.CharField(label='搜索玩具类型', max_length=100, required=False)

#用来输入修改name表值
class ToyTypeForm(forms.ModelForm):
    class Meta:
        model = Toy_type
        fields = ['name']
