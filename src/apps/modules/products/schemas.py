from src.config.ma import ma

# Products Schemas
class ProductsSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'image', 'created_at', 'categories')
        include_fk = True  
        