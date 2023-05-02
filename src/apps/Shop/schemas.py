from src.config.ma import ma
from src.apps.Shop.models import Products



# Products Schemas
class ProductsSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'image', 'is_shell', 'created_at', 'categories')
        include_fk = True  



# Categories Schemas
class CategoriesSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name')
     
     
     
# Categories Items Schemas   
class CartItemSchemas(ma.Schema):
    class Meta:
        fields = ('id', 'product', 'product_img')
    