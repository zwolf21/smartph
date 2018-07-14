class ObjectListMixin(object):
    object_list_name = 'object_list'
    filter_kwargs = None
    
    def get_context_data(self, **kwargs):
        context = super(ObjectListMixin, self).get_context_data(**kwargs)
        if self.filter_kwargs:
            context[self.object_list_name] = self.model.objects.filter(**self.filter_kwargs)
        else:
            context[self.object_list_name] = self.model.objects.all()
        return context