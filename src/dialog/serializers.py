from crawler.serializers import BaseSerializer
from dialog.models import Category, Product


class DialogCategorySerializer(BaseSerializer):
    class Meta:
        model = Category


class DialogProductSerializer(BaseSerializer):
    class Meta:
        model = Product
