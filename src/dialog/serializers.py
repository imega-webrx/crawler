from crawler.serializers import BaseSerializer
from dialog.models import Product


class DialogProductSerializer(BaseSerializer):
    class Meta:
        model = Product
