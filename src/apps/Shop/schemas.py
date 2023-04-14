from src.config.ma import ma
from src.apps.Shop.models import Products


class ProductsSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'image', 'is_shell', 'created_at', 'categories')
        include_fk = True  


class CategoriesSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name')
        
class CartItemSchemas(ma.Schema):
    
    class Meta:
        fields = ('id', 'product', 'product_img')