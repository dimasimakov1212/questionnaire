from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from business.forms import BusinessForm
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

    # def get_queryset(self, *args, **kwargs):
    #     """ Определяем порядок вывода объектов """
    #
    #     queryset = super().get_queryset(*args, **kwargs)
    #
    #     try:
    #         user = self.request.user
    #         queryset = queryset.filter(category_owner=user)
    #
    #         return queryset
    #
    #     except TypeError:
    #         pass


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
