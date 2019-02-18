from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField()
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    password_confirmation = forms.CharField(label='Password Again', widget=forms.PasswordInput())

    # fancy magic to add class to input field
    # https: // stackoverflow.com/questions/29716023/add-class-to-form-field-django-modelform
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class CreateNewGameForm(forms.Form):
    name = forms.CharField(label='Name', max_length=50)
    price = forms.FloatField(label='Price')
    url = forms.URLField(label="URL Link", max_length=500)
    game_picture = forms.URLField(label="Game Picture", max_length=500)
    description = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CreateNewGameForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
