from flask import Flask, request, jsonify
from flask.views import MethodView
from db import Shop, Session
from schema import validate_create_ad
from errors import HttpError

app = Flask('server')


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response


class AdsView(MethodView):

    def post(self):
        request_data = validate_create_ad(request.json)
        with Session() as session:
            new_ad = Shop(**request_data)
            session.add(new_ad)
            session.commit()
            return jsonify(
                {
                    'id': new_ad.id,
                    'created_at': int(new_ad.creation_time.timestamp()),
                }
            )

    def get(self, ad_id: int):
        if ad_id is None:
            with Session() as session:
                data = session.query(Shop).all()
                ads = []
                for one in data:
                    ad = {'id': one.id, 'title': one.title, 'created_at': int(one.creation_time.timestamp())}
                    ads.append(ad)
                return ads
        else:
            with Session() as session:
                ad = session.query(Shop).get(ad_id)
                return {'id': ad.id, 'title': ad.title, 'created_at': int(ad.creation_time.timestamp())}

    def delete(self, ad_id: int):
        with Session() as session:
            session.query(Shop).filter(Shop.id == ad_id).delete()
            session.commit()
            return 'Done'


ad_view = AdsView.as_view('shop_id')
app.add_url_rule('/shop', defaults={'shop_id': None}, view_func=ad_view, methods=['GET', ])
app.add_url_rule('/shop', view_func=ad_view, methods=['POST', ])
app.add_url_rule('/shop/<int:ad_id>', view_func=ad_view, methods=['GET', 'DELETE'])

if __name__ == '__main__':
    app.run(debug=True)
