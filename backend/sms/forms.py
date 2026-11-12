
from django import forms
from .models import IssuedItem, Items, Faculty, Department


class IssuedForm(forms.ModelForm):
    class Meta:
        model = IssuedItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['ItemName'].queryset = Items.objects.filter(
            is_active=True
        )

        self.fields['Name_of_Employee'].queryset = Faculty.objects.filter(
            is_active=True
        )
