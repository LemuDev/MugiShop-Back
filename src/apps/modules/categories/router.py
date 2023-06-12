from flask import Blueprint
from flask import jsonify

from src.apps.modules.categories.model import Categories
from .schemas import CategoriesSchemas


bp = Blueprint("categories", __name__, url_prefix="/api")

# Endpoint for see all categories
@bp.route("/categories", methods=["GET"])
def categories_list():
    categories_schema = CategoriesSchemas(many=True)
    
    
    categories = Categories.query.all()

    return jsonify(categories_schema.dump(categories))

