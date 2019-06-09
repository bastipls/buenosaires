from django import forms
from .models import Producto
class ProductoForm (forms.ModelForm):#Y29waW9u 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['hora_inicio_folio'].widget.attrs.update({'readonly':'True'})
     

 
    class Meta:
        model = Producto
       
        fields = ('imagen',)
                