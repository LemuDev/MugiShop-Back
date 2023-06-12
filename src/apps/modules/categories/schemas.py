from src.config.ma import ma

# Categories Schemas
class CategoriesSchemas(ma.Schema):

    class Meta:
        fields = ('id', 'name')
     