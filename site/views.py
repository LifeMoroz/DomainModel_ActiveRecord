from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View

from hometask.models import Document, Element, Template, FieldSubstitution, DE, DFS


class DocumentBased:
    model = Document


class DocumentList(DocumentBased, View):
    def get(self, request, *args, **kwargs):
        print(self.model.find()[0].title)
        return render(request, 'list.html', {'object_list': self.model.find()})


class DocumentAdd(DocumentBased, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'add.html', {})

    def post(self, request, *args, **kwargs):
        self.model.find(id=id)[0].delete()


class DocumentDelete(DocumentBased, View):
    def get(self, request, *args, **kwargs):
        self.model.find(id=kwargs['id'])[0].delete()


class DocumentEdit(DocumentBased, View):
    def get(self, request, *args, **kwargs):
        obj = self.model.find(id=kwargs['id'])[0]
        elems_list = Element.find()
        fs = FieldSubstitution.find()
        return render(request, 'edit.html', {'object': obj, 'elems': elems_list, 'fs': fs})

    def post(self, request, *args, **kwargs):
        elems = self.request.POST.getlist('elem')
        if not isinstance(elems, list):
            elems = [elems]

        fs = self.request.POST.getlist('fs')
        if not isinstance(fs, list):
            fs = [fs]

        obj = self.model.find(id=kwargs['id'])[0]
        obj.clear_template()
        for elem in elems:
            position, _id = elem.split('_')
            DE(element=_id, document=obj.id, position=position).save()
        for elem in fs:
            position, _id = elem.split('_')
            DFS(fs=_id, document=obj.id, position=position).save()
        return HttpResponseRedirect('/list/')
