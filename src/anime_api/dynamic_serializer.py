from rest_framework import serializers
from .models import Season


class SeasonSerializer(serializers.ModelSerializer):
    # Define fields dynamically based on the related models passed to the serializer
    def __init__(self, *args, **kwargs):
        # Retrieve the related models passed to the serializer
        related_models = kwargs.pop("related_models", [])

        # Define serializer fields dynamically for each related model
        for related_model in related_models:
            field_name = related_model.__name__.lower()  # Use model name as field name
            field = serializers.PrimaryKeyRelatedField(
                queryset=related_model.objects.all(), many=True, read_only=True
            )
            self.fields[field_name] = field

        super().__init__(*args, **kwargs)

    class Meta:
        model = Season
        fields = "__all__"
