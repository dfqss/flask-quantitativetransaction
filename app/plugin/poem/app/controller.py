from flask import jsonify
from app.lin.redprint import Redprint

from app.plugin.poem.app.form import PoemListForm, PoemSearchForm
from .model import Poem

api = Redprint('poem')


@api.route('/all', methods=['GET'])
def get_list():
    form = PoemListForm().validate_for_api()
    poems = Poem().get_all(form)
    return jsonify(poems)


@api.route('/search', methods=['GET'])
def search():
    form = PoemSearchForm().validate_for_api()
    poems = Poem().search(form.q.data)
    return jsonify(poems)


@api.route('/authors', methods=['GET'])
def get_authors():
    authors = Poem.get_authors()
    return jsonify(authors)