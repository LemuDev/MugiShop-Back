from src.config.ma import ma

# Categories Items Schemas   
class CartItemSchemas(ma.Schema):
    class Meta:
        fields = ('id', 'product', 'price', 'product_img')
    