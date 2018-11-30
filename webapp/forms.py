from django import forms
###
from django.db import models

from crispy_forms.bootstrap import Field, TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

from webapp.models import Technology
##

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur", "required": "required",}),
                              max_length=50,error_messages={"required": "Nom d'utilisateur ne peut pas être vide.",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe", "required": "required",}),
                              max_length=20,error_messages={"required": "Mot de passe ne peut pas être vide.",})

class RegForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur", "required": "required",}),
                              max_length=50,error_messages={"required": "Nom d'utilisateur ne peut pas être vide.",})
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeholder": "E-mail", "required": "required",}),
                              max_length=50,error_messages={"required": "E-mail ne peut pas être vide.",})
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe", "required": "required",}),
                              max_length=20,error_messages={"required": "Mot de passe ne peut pas être vide.",})
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirmer le mot de passe", "required": "required",}),
                              max_length=20,error_messages={"required": "Mot de passe ne peut pas être vide.",})

    def clean(self):
        if not self.is_valid():
             raise forms.ValidationError('Tous les articles sont obligatoires.')
        elif self.cleaned_data['confirm_password'] != self.cleaned_data['password']:
            raise forms.ValidationError('Mot de passe d\'entrée incohérent')
        else:
            cleaned_data = super(RegForm,self).clean()
        return cleaned_data

class CommentForm(forms.Form):
    author = forms.CharField(widget=forms.TextInput(attrs={"id":"author","class":"comment_input",
                                                           "required":"required","size":"25",
                                                           "tabindex":"1"}),
                             max_length=50,error_messages={"required":"Nom d'utilisateur ne peut pas être vide.",})

    email = forms.EmailField(widget=forms.TextInput(attrs={"id":"email","type":"email",
                                                           "class": "comment_input",
                                                           "required":"required","size":"25",
                                                           "tabindex":"2"}),
                                 max_length=50, error_messages={"required":"E-mail ne peut pas être vide.",})

    url = forms.URLField(widget=forms.TextInput(attrs={"id":"url","type":"url","class": "comment_input",
                                                       "size":"25", "tabindex":"3"}),
                              max_length=100, required=False)

    comment = forms.CharField(widget=forms.Textarea(attrs={"id":"comment","class": "message_input",
                                                           "required": "required", "cols": "25",
                                                           "rows": "5", "tabindex": "4"}),
                                                    error_messages={"required":"Le commentaire ne peut pas être vide.",})

    article = forms.CharField(widget=forms.HiddenInput())

#####################################################################################################
class SubmissionForm(forms.Form):

    error_css_class = 'has-error'

    username = forms.CharField(
        max_length=30,
        label="Votre nom",
        required=False
    )

    email = forms.EmailField(
        max_length=254,
        label="Votre email",
        required=True
    )

    name = forms.CharField(
        max_length=100,
        label="Nom de la technologie",
        required=True
    )

    price = forms.DecimalField(
        label="Prix de la technologie", 
        required=False
    )

    age = forms.ChoiceField(
        widget=forms.Select,
        choices=[
         ('Tous âges', 'Tous âges'),
         ('Enfants', 'Enfants'),
         ('Adultes', 'Adultes'),
         ('Personnes âgées', 'Personnes âgées')
        ],
        label="Tranche d'âge concernée",
        required=True
    )

#    cif = forms.ChoiceField(
#        choices=[
#            ('Organisation', 'Organisation'),
#            ('Déplacement',' Déplacement'),
#            ('Santé', 'Santé'),
#            ('Vie domestique', 'Vie domestique'),
#            ('Loisirs', 'Loisirs'),
#            ('Vie sociale', 'Vie sociale'),
#            ('Travail', 'Travail'),
#            ('Apprentissage', 'Apprentissage')
#        ],
#        label="Classification",
#        required=True
#    )

    type_techno = forms.CharField(max_length=100, label="Type de technologie", required=False)
    activite = forms.CharField(max_length=100, label="Activité", required=False)
    source = forms.CharField(max_length=100, label="Source", required=False)
    article = forms.CharField(max_length=None, label="Article", required=False)
    company = forms.CharField(max_length=100, label="Entreprise", required=False)

    fonction = forms.CharField(max_length=100, label="Fonction", required=False)

    desc = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='',
        required=True
    )
    
    video = forms.CharField(max_length=None, required=False)

    image_url_i = forms.ImageField(required=False)

    required_fields = [ 'email','name','desc','company'] 

    def __init__(self, *args):

        super().__init__(*args)

        self.helper = FormHelper()
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Fieldset('Vos informations',
                Field('username', placeholder='Votre nom ici'),
                Field('email', placeholder='Votre email ici')
            ), Fieldset('Informations concernant la technologie',
                Tab('Informations obligatoires','name','desc','company'),
                Tab('Informations complémentaires', 'prix', 'source', 'image')
            )
        )

    def clean(self):

        """
        called by is_valid method
        when the form is going 
        to be validated
        """

        cleaned_data = super(SubmissionForm, self).clean()

        if not all(cleaned_data.get(field) for field in self.required_fields):

            raise forms.ValidationError(
                message="Vous devez remplir les champs marqués d'une étoile !",
            )

        else:

            # instantiate a new technoloy
            new = Technology()

            # don't show img on the website when added by form
            # (wait for an admin validation)
            new.show = False

            # set all forms attributes to 
            # technology model 
            for key in cleaned_data.keys():
                setattr(new, key, cleaned_data.get(key))
            
            new.save(force_insert=True)
