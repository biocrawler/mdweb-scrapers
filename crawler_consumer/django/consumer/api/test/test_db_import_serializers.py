from django.test import TestCase
from api.models import Author, ArticleFile, Article, Keyword
from api.serializers import ArticleSerializer
from api.api_lib.serializers import ArticleSerializer as apiserializer
from api.api_lib.validators import ArticleValidator
from api.test.article_test_data_1 import test_data_1, test_data_2
from unittest import skip
import json


class ArticleSerializerTC(TestCase):
    def setUp(self) -> None:
        pass

    def test_serializer_data_1_ok(self):
        validator = ArticleValidator(test_data_1)
        data = validator.get_validated_data()
        print("validated data: " + str(json.dumps(data, indent=4)))
        serializer = ArticleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        a = serializer.save()
        print(Article.objects.get(digital_object_id=a).to_json())

    @skip("test data 2 not used")
    def _test_serializer_data_3_ok(self):
        validator = ArticleValidator(test_data_2)
        data = validator.get_validated_data()
        print("validated data: " + str(json.dumps(data, indent=4)))
        serializer = ArticleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        a = serializer.save()
        print(Article.objects.get(digital_object_id=a).to_json())

    @skip("test data 2 not used")
    def _test_api_serializer_data_2_ok(self):
        validator = ArticleValidator(test_data_2)
        data = validator.get_validated_data()
        print("validated data: " + str(json.dumps(data, indent=4)))
        serializer = apiserializer(data=data)
        # serializer.is_valid(raise_exception=True)
        a = serializer.save()
        print(Article.objects.get(digital_object_id=a).to_json())
