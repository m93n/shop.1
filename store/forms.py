from django import forms

from store.models import Review, Product


class AddReviewForm(forms.ModelForm):
    product=forms.ModelChoiceField(queryset=Product.objects.all(), to_field_name='name')
    
    class Meta:
        model = Review
        fields = '__all__'

    