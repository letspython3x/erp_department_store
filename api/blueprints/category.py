import simplejson as json
from flask import request, abort, Response
from flask_restplus import Resource, Api

from api import bp_category, ValidateCategory
from utils.generic_utils import get_logger
from models.category_model import CategoryModel

logger = get_logger(__name__)
api = Api(bp_category)


class CategoryApi(Resource):
    def get(self):
        status = 200
        category_id = request.args.get('category_id', '')
        name = request.args.get('category_name', '')
        print(category_id)

        pm = CategoryModel()

        if category_id not in ['null', '']:
            data = pm.search_by_category_id(int(category_id))
        elif name not in ['null', None, '']:
            data = pm.search_by_name(name)
        else:
            data = pm.get_all_categories()

        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def post(self):
        status = 201
        if not request.json:
            abort(status)
        category = request.json

        category_id = None
        vc = ValidateCategory(category)
        if vc.validate():
            cm = CategoryModel()
            category_id = cm.insert(category)
            message = "Category added Successfully"
        else:
            message = "Invalid category details"

        data = dict(category_id=category_id,
                    message=message)
        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")

    def put(self):
        """
        Will update the details of a category
        :return: response
        """
        status = 400
        category = request.json
        category_id = category.get('category_id')
        if category_id:
            pm = CategoryModel()
            is_updated = pm.update_category(category_id, category)
            if is_updated:
                status = 200
                data = dict(message=f"UPDATE category SUCCESS, ID: {category_id}")
            else:
                data = dict(message=f"UPDATE category FAILURE, ID: {category_id}")
        else:
            data = dict(message='Invalid category ID')

        payload = json.dumps(data)
        # logger.info("PAYLOAD SENT: %s" % payload)
        return Response(payload, status=status, mimetype="application/json")


api.add_resource(CategoryApi, "/")
