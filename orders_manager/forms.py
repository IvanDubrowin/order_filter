from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Agent, Order

# форма создания агента
class AgentCreationForm(UserCreationForm):
    class Meta:
        model = Agent
        fields = ("username", "number_inn", "password1", "password2")

    # делаем ИНН обязательным
    def __init__(self, *args, **kwargs):
        super(AgentCreationForm, self).__init__(*args, **kwargs)
        self.fields['number_inn'].required = True


# создаем список ИНН по модели Agent и передаем их в выбор форм
class AdminFilterForm(forms.Form):
    query = Agent.objects.values_list('number_inn',flat=True)
    query_choices = [('all', 'Все записи')] + [(id, id) for id in query]
    number_inn = forms.ChoiceField(
                            choices=query_choices,
                            required=False,
                            widget=forms.Select()
                            )

# форма выбора даты
class AgentFilterForm(forms.Form):
    start_date = forms.DateField(label='от', widget = forms.SelectDateWidget())
    end_date = forms.DateField(label='до', widget = forms.SelectDateWidget())
