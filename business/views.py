from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from business.forms import BusinessForm, BusinessAreaForm
from business.models import Business, BusinessArea


class BusinessCreate(CreateView):
    """ Создание объекта тип бизнеса """

    model = Business
    form_class = BusinessForm
    template_name = 'business/business_form.html'

    def form_valid(self, form):
        """ Проверка и сохранение данных """

        self.object = form.save(commit=False)
        self.object.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('business:business_list')


class BusinessList(ListView):
    """ Список объектов тип бизнеса """

    model = Business
    template_name = 'business/business_list.html'
    context_object_name = 'businesses'


class BusinessDetail(DetailView):
    """ Просмотр деталей объекта тип бизнеса """

    model = Business
    context_object_name = 'business'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = self.get_object()
        context['business_areas'] = BusinessArea.objects.filter(business=business)

        return context


class BusinessUpdate(UpdateView):
    """ Изменение объекта тип бизнеса """

    model = Business
    form_class = BusinessForm
    success_url = reverse_lazy('business:business_list')

    def form_valid(self, form):
        """ Проверка и сохранение данных """

        if form.is_valid():
            new_business = form.save()
            new_business.save()

        return super().form_valid(form)


class BusinessDeleteView(DeleteView):
    """ Удаление объекта тип бизнеса """

    model = Business
    success_url = reverse_lazy('business:business_list')


def business_area_create(request, pk):
    """ Создание объекта сфера деятельности """

    business = Business.objects.get(id=pk)  # получаем объект тип бизнеса

    form = BusinessAreaForm(request.POST)  # класс-метод формы создания объекта
    data = {'form': form, 'business': business}  # контекстная информация

    # получаем данные формы
    if request.method == 'POST':

        if form.is_valid():
            business_area = form.save(commit=False)  # получаем данные из формы

            business_area.business = business  # присваиваем сфере деятельности тип бизнеса

            business_area.save()  # сохраняем объект

            pk = business.id  # получаем id типа бизнеса

            # перенаправляем на форму сферы деятельности
            return redirect('business:business_detail', pk)

    return render(request, 'business/businessarea_form.html', context=data)  # шаблон сферы деятельности


class BusinessAreaDetail(DetailView):
    """ Просмотр объекта сфера деятельности """

    model = BusinessArea
    context_object_name = 'business_area'


class BusinessAreaListView(ListView):
    """ Список объектов сфера деятельности """

    model = BusinessArea


class BusinessAreaUpdate(UpdateView):
    """ Изменение объекта сфера деятельности """

    model = BusinessArea
    form_class = BusinessAreaForm
    context_object_name = 'business_area'

    def form_valid(self, form):
        """ Проверка и сохранение данных """

        if form.is_valid():
            new_business_area = form.save()
            new_business_area.save()

        return super().form_valid(form)

    def get_success_url(self):
        business = self.object.business
        return reverse_lazy('business:business_detail', kwargs={'pk': business.pk})


class BusinessAreaDelete(DeleteView):
    """ Удаление объекта сфера деятельности """

    model = BusinessArea

    def get_context_data(self, **kwargs):
        """ Определяем контекстную информацию """

        context = super().get_context_data(**kwargs)
        business_area = self.get_object()  # получаем текущий объект сфера деятельности
        context['business'] = business_area.business  # объект тип бизнеса
        context['business_area'] = business_area  # объект сфера деятельности

        return context

    def get_success_url(self):
        business = self.object.business
        return reverse_lazy('business:business_detail', kwargs={'pk': business.pk})
