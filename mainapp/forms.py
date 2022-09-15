from django import forms
import datetime
from . import models
from django.contrib.auth.models import User
from .core import common_functions


class LeaderBoardForm(forms.Form):
    start_date = forms.DateField(initial=datetime.date(2000, 1, 30).strftime("%d/%m/%Y"),
                                 input_formats=['%d/%m/%Y'],
                                 label="Start date ",
                                 widget=forms.TextInput(attrs={
                                     'placeholder': '30/01/2000',
                                     'class': 'formEntry dateEntry'})
                                 )
    end_date = forms.DateField(initial=datetime.date(2023, 1, 30).strftime("%d/%m/%Y"),
                               input_formats=['%d/%m/%Y'],
                               label="End date ",
                               widget=forms.TextInput(attrs={
                                   'placeholder': '30/01/2023',
                                   'class': 'formEntry dateEntry'})
                               )

    top_best = forms.IntegerField(min_value=1,
                                  required=False,
                                  widget=forms.TextInput(attrs={
                                      'class': 'formEntry integerEntry'}),
                                  label="See only x best "
                                  )

    top_worst = forms.IntegerField(min_value=1,
                                   required=False,
                                   widget=forms.TextInput(attrs={
                                       'class': 'formEntry integerEntry'}),
                                   label="See only x worst "
                                   )

    graph_type = forms.ChoiceField(choices=[('number', 'Message count'), ('avg length', 'Average message length'),
                                            ('total chars', 'Total characters')],
                                   label="Value compared ",
                                   widget=forms.Select(attrs={
                                       'class': 'formEntry dateEntry'})
                                   )


class PersonalStatsForm(forms.Form):
    names = common_functions.get_all_names()
    name = forms.ChoiceField(choices=[(n, n) for n in names],
                             label="Nom ",
                             widget=forms.Select(attrs={
                                 'class': 'formEntry dateEntry'})
                             )
    start_date = forms.DateField(initial=datetime.date(2000, 1, 30).strftime("%d/%m/%Y"),
                                 input_formats=['%d/%m/%Y'],
                                 label="Start date ",
                                 widget=forms.TextInput(attrs={
                                     'placeholder': '30/01/2000',
                                     'class': 'formEntry dateEntry'})
                                 )
    end_date = forms.DateField(initial=datetime.date(2023, 1, 30).strftime("%d/%m/%Y"),
                               input_formats=['%d/%m/%Y'],
                               label="End date ",
                               widget=forms.TextInput(attrs={
                                   'placeholder': '30/01/2023',
                                   'class': 'formEntry dateEntry'})
                               )
    word = forms.CharField(initial='hello', label='Word Search')


class ProgressForm(forms.Form):
    names = common_functions.get_all_names()
    names.append('all')
    name = forms.ChoiceField(choices=[(n, n) for n in names],
                             label="Nom ",
                             widget=forms.Select(attrs={
                                 'class': 'formEntry dateEntry'})
                             )

    mode = forms.ChoiceField(choices=[('per', 'change per month'), ('total', 'total messages at month')])

    graph_type = forms.ChoiceField(choices=[('bar', 'bar'), ('curve', 'curve')])


class ProgressFormVersus(forms.Form):
    names_list = common_functions.get_all_names()
    names = forms.MultipleChoiceField(choices=[(n, n) for n in names_list],
                                      label="Names to compare : (ctrl + click)"
                                      )


class BestMessageForm(forms.Form):
    react_list = ['❤', '😆', '👍', '😮', '😂', '👎', '🤡', '🗿', 'all']

    react = forms.ChoiceField(choices=[(n, n) for n in react_list])
    n_msg = forms.IntegerField(initial=1, min_value=1, max_value=100, label='Top : ')


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.FeedbackModel
        fields = ['body']
