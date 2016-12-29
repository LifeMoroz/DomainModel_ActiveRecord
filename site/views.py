from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View

from hometask.models import Document, Element, FieldSubstitution, DE, DFS, TEMPLATE_CHOICES


# миксин, который говорит нам о том, что класс опирается на модель Шаблона (Document)
class DocumentBased:
    # Статический атрибут класса
    model = Document


class DocumentList(DocumentBased, View):
    """
    Domain Model списка объектов типа Document.
    """
    def get(self, request, *args, **kwargs):
        """
        Обработчик HTTP запроса GET
        :param request: HttpRequest объект запроса
        :param args: неименованные параметры
        :param kwargs: именованые параметры
        :return: HttpResponse данные для страницы списка объектов
        """
        return render(request, 'list.html', {'object_list': self.model.find()})


class DocumentAdd(DocumentBased, View):
    """
    Domain Model добавления объекта типа Document.
    """
    def get(self, request, *args, **kwargs):
        """
        Обработчик HTTP запроса GET
        :param request: HttpRequest объект запроса
        :param args: неименованные параметры
        :param kwargs: именованые параметры
        :return: HttpResponseRedirect редирект на страницу редактирования нового объекта
        """
        new = self.model(title='New template', template='doc').save()  # Вызывает конструктор класса Document с дефолтным title. Сразу после создания записывает в базу
        return HttpResponseRedirect(reverse('edit', kwargs={'id': new.id}))


class DocumentDelete(DocumentBased, View):
    """
    Domain Model удаления объекта типа Document.
    """
    def get(self, request, *args, **kwargs):
        """
        Обработчик HTTP запроса GET
        :param request: HttpRequest объект запроса
        :param args: неименованные параметры
        :param kwargs: именованые параметры
        :return: HttpResponseRedirect редирект на главную страницу
        """
        obj = self.model.find(id=kwargs['id'])[0]  # Находим объект, который хотим удалить, в базе
        obj.clear_template()  # Удаляем все связи с элементами и подстановками
        obj.delete()  # Удаляем объект
        return HttpResponseRedirect(reverse('list'))


class DocumentEdit(DocumentBased, View):
    """
    Domain Model редактирования объекта типа Document.
    """
    def get(self, request, *args, **kwargs):
        """
        Обработчик HTTP запроса GET
        :param request: HttpRequest объект запроса
        :param args: неименованные параметры
        :param kwargs: именованые параметры
        :return: HttpResponseRedirect редирект на главную страницу
        """
        obj = self.model.find(id=kwargs['id'])[0]  # Находим объект, который хотим редактировать, в базе
        elems_list = Element.find()  # Получаем список связанных элементов
        fs = FieldSubstitution.find()  # Получаем список связанных подстановок
        return render(request, 'edit.html', {'object': obj, 'elems': elems_list, 'fs': fs, 'tformats': TEMPLATE_CHOICES})

    def post(self, request, *args, **kwargs):
        """
        Обработчик HTTP запроса POST
        :param request: HttpRequest объект запроса
        :param args: неименованные параметры
        :param kwargs: именованые параметры
        :return: HttpResponseRedirect редирект на главную страницу
        """
        elems = self.request.POST.getlist('elem')  # Получаем из запроса новые элементны
        if not isinstance(elems, list):
            elems = [elems]

        fs = self.request.POST.getlist('fs')  # Получаем из запроса новые подстановки
        if not isinstance(fs, list):
            fs = [fs]

        obj = self.model.find(id=kwargs['id'])[0]  # Находим в базе объект, который будем перезаписывать
        obj.clear_template()  # Очищаем текущие связи объекта
        for elem in elems:  # Цикл по элементам
            position, _id = elem.split('_')  # Из условного обозначения в запросе определеяем позицию элемента в шаблоне и id элемента
            DE(element=_id, document=obj.id, position=position).save()  # Создаем и записываем связь
        for elem in fs:  # Цикл по подстановкам
            position, _id = elem.split('_')  # Из условного обозначения в запросе определеяем позицию подстановки в шаблоне и id подстановки
            DFS(fs=_id, document=obj.id, position=position).save()  # Создаем и записываем связь

        title = self.request.POST['title']  # Получаем новый title
        obj.title = title  # Записываем в экземпляр объекта
        obj.template = self.request.POST['format']  # Получаем новый формат шаблона и записываем в экземпляр
        obj.save()  # Записываем новое состояние объекта в базу
        return HttpResponseRedirect(reverse('list'))
