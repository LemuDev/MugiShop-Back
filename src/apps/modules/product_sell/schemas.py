from src.config.ma import ma

class ProductSellSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name', 'description', 'price', 'image', 'imagehd', 'created_at', 'categories')
        include_fk = True  

