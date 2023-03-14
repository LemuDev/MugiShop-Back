from src.config.ma import ma
from src.apps.products.models import Products


class ProductsSchemas(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'price', 'image', 'is_shell', 'created_at')