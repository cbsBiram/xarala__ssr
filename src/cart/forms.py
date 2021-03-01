from django import forms
from django.utils.translation import gettext_lazy as _


COURSE_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddCourseForm(forms.Form):
    quantity = forms.TypedChoiceField(
        choices=COURSE_QUANTITY_CHOICES, coerce=int, label=_("Quantité")
    )
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
