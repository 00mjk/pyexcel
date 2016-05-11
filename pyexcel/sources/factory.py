class SourceFactory:
    """
    The factory method to support multiple datasources in getters and savers
    """
    sources = {
        "sheet-read": [],
        "sheet-write": [],
        "book-read": [],
        "book-write": []
    }

    @classmethod
    def register_sources(self, sources):
        for source in sources:
            for target in source.targets:
                for action in source.actions:
                    self.register_a_source(target, action, source)

    @classmethod
    def register_a_source(self, target, action, source):
        key = "%s-%s" % (target, action)
        self.sources[key].append(source)

    @classmethod
    def _get_generic_source(self, target, action, **keywords):
        key = "%s-%s" % (target, action)
        for source in self.sources[key]:
            if source.is_my_business(action, **keywords):
                s = source(**keywords)
                return s
        return None

    @classmethod
    def get_source(self, **keywords):
        return self._get_generic_source(
            'sheet',
            'read',
            **keywords)

    @classmethod
    def get_book_source(self, **keywords):
        return self._get_generic_source(
            'book',
            'read',
            **keywords)

    @classmethod
    def get_writeable_source(self, **keywords):
        return self._get_generic_source(
            'sheet',
            'write',
            **keywords)

    @classmethod
    def get_writeable_book_source(self, **keywords):
        return self._get_generic_source(
            'book',
            'write',
            **keywords)


class RendererFactory:
    renderer_factories = {}
    book_renderer_factories = {}
    @classmethod
    def get_renderer(self, file_type):
        return self.renderer_factories.get(file_type)

    @classmethod
    def get_book_renderer(self, file_type):
        return self.book_renderer_factories.get(file_type)

    @classmethod
    def register_renderers(self, file_types, renderer):
        for file_type in file_types:
            self.renderer_factories[file_type] = renderer[0]
            if renderer[1]:
                self.book_renderer_factories[file_type] = renderer[1]
