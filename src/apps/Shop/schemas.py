from src.config.ma import ma
from src.apps.Shop.models import Products



# Products Schemas
class ProductsSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'image', 'created_at', 'categories')
        include_fk = True  
        
class ProductSellSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'image', 'imagehd', 'created_at', 'categories')
        include_fk = True  



# Categories Schemas
class CategoriesSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name')
     
     
     
# Categories Items Schemas   
class CartItemSchemas(ma.Schema):
    class Meta:
        fields = ('id', 'product', 'price', 'product_img')
    