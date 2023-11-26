from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    media_type = "application/json"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        results_length = len(data.get("results", []))
        status_code = renderer_context["response"].status_code
        modified_data = {
            "status": status_code,
            "resources_length": results_length,
            "result": data 
        }
        return super().render(modified_data, accepted_media_type, renderer_context)


