from django.shortcuts import render
from django.http import HttpResponse


def index(request):
	return render(request, template_name="web_ui/index.html")

# from django.core import serializers
# data = serializers.serialize("xml", SomeModel.objects.all())
# XMLSerializer = serializers.get_serializer("xml")
# xml_serializer = XMLSerializer()
# xml_serializer.serialize(queryset)
# data = xml_serializer.getvalue()
