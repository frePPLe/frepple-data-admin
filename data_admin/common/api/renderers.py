from rest_framework.renderers import BrowsableAPIRenderer


class freppleBrowsableAPI(BrowsableAPIRenderer):
    """
    Customized rendered for the browsable API:
      - added the 'title' variable to the context to make the breadcrumbs work
    """

    def get_context(self, data, accepted_media_type, renderer_context):
        ctx = super().get_context(data, accepted_media_type, renderer_context)
        ctx["name"] = ctx["view"].serializer_class.Meta.model._meta.model_name
        if hasattr(ctx["view"], "list"):
            ctx["title"] = "List API for %s" % ctx["name"]
        else:
            ctx["title"] = "Detail API for %s" % ctx["name"]
        return ctx

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, list) and renderer_context["request"].method in (
            "POST",
            "PUT",
            "PATCH",
        ):
            # Workaround for a 500-error when posting a list update in the user interface
            data = data[0]
        return super().render(data, accepted_media_type, renderer_context)
