import datetime
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.db.models import Q
from .models import Agent, Order
from .forms import AgentCreationForm, AdminFilterForm, AgentFilterForm


# отображение заказов
class OrderView(View):

    template_name = 'order.html'

    def get(self, request):
        # если нет аутенфикации, то редирект на форму авторизации
        if request.user.is_anonymous:
            return redirect('/accounts/login')
        else:
            # если зашли как админ, то отобразить форму фильтрации админа и весь список заказов
            if request.user.is_superuser:
                form = AdminFilterForm()
                orders = Order.objects.all()
            # если зашли как агент, то форма агента и список только наших заказов
            else:
                form = AgentFilterForm()
                orders = Order.objects.filter(agent=request.user)
            args = {"orders": orders, "form": form}
            return render(request, self.template_name, args)

    # post запросы только для авторизованных пользователей
    @method_decorator(login_required)
    def post(self, request):
        if request.user.is_superuser:
            form = AdminFilterForm(request.POST)
            if form.is_valid():
                # показать все записи
                if form.data.get('number_inn' )== 'all':
                    orders = Order.objects.all()
                else:
                    # фильтр по ИНН
                    orders = Order.objects.filter(agent__number_inn=form.data.get('number_inn'))
        else:
            form = AgentFilterForm(request.POST)
            if form.is_valid():
                # форматируем словарь формы
                start_date = datetime.date(int('{}'.format(form.data.get('start_date_year'))),
                                           int('{}'.format(form.data.get('start_date_month'))),
                                           int('{}'.format(form.data.get('start_date_day'))))

                end_date = datetime.date(int('{}'.format(form.data.get('end_date_year'))),
                                         int('{}'.format(form.data.get('end_date_month'))),
                                         int('{}'.format(form.data.get('end_date_day'))))
                # фильтруем по дате заказы агента
                orders = Order.objects.filter(
                                        Q(date__gte=start_date),
                                        Q(date__lte=end_date),
                                        Q(agent=request.user)
                                    )
        # передаем результаты фильтра в контекст
        args = {"orders": orders, "form": form}
        return render(request, self.template_name, args)


# форма создания агента
class RegistrationFormView(FormView):

    form_class = AgentCreationForm
    success_url = "/accounts/login"
    template_name = "registration.html"

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)
