from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from store.models import AdditionalInformation, AdditionalInformationValue
from account.models import CartItem, Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='eg. example@gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['email'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})

class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-lg text-4'})

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username','email')
    
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs.update({'class': 'form-control text-3 h-auto py-2'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control text-3 h-auto py-2'})
        self.fields['email'].widget.attrs.update({'class': 'form-control text-3 h-auto py-2'})
        self.fields['username'].widget.attrs.update({'class': 'form-control text-3 h-auto py-2'})
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']


class CartItemForm(forms.ModelForm):
    
    class Meta:
        model = CartItem
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        product_stock = self.instance.stock
        self.fields['quantity'] = forms.IntegerField(max_value=product_stock, required=True)

        user_choose_informations = AdditionalInformation.objects.filter(product=self.instance, user_choose=True)

        for info in user_choose_informations:
            field_name = info.name
            self.fields[field_name] = forms.ModelChoiceField(queryset=AdditionalInformationValue.objects.filter(additional_information=info), required=True, empty_label='PLEASE CHOOSE', to_field_name="name")

    def save(self, cart):
        product = self.instance
        cart = cart
        quantity = self.cleaned_data['quantity']
        choosen_informations = make_choosen_inforamtion_dict(product=product, data=self.cleaned_data)
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += quantity
            cart_item.choosen_informations = choosen_informations
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity = quantity,
                choosen_informations = choosen_informations
            )
            cart.save()

def make_choosen_inforamtion_dict(product, data):
    choosen_informations = dict()

    for field_name in data:
        field_value = data[field_name]
        if type(field_value) != int:
            field_value = field_value.name
        choosen_informations[field_name]= field_value

    return choosen_informations
