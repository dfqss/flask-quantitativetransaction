"""
    a standard CRUD template of book
    通过 图书 来实现一套标准的 CRUD 功能，供学习
    :copyright: © 2020 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from app.lin import group_required, login_required, route_meta
from app.lin.exception import Success
from app.lin.interface import ViewModel
from app.lin.jwt import login_required
from app.lin.redprint import Redprint
from app.models.v1.book import Book
from app.validators.forms import BookSearchForm, CreateOrUpdateBookForm


book_api = Redprint('book')


class BookViewModel(ViewModel):
    '''
    继承ViewModel类可以自动序列化
    '''

    def __init__(self, book):
        self.title = book.title
        self.author = book.author
        self.summary = book.summary


@book_api.route('/<bid>/base', methods=['GET'])
def get_book_base(bid):
    book = Book.get_detail(bid)
    return BookViewModel(book)


@book_api.route('/<bid>', methods=['GET'])
@login_required
def get_book(bid):
    book = Book.get_detail(bid)
    return book


@book_api.route('', methods=['GET'])
@login_required
def get_books():
    books = Book.get_all()
    return books


@book_api.route('/search', methods=['GET'])
def search():
    form = BookSearchForm().validate_for_api()
    books = Book.search_by_keywords(form.q.data)
    return books


@book_api.route('', methods=['POST'])
def create_book():
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.new_book(form)
    return Success(msg='新建图书成功')


@book_api.route('/<bid>', methods=['PUT'])
def update_book(bid):
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.edit_book(bid, form)
    return Success(msg='更新图书成功')


@book_api.route('/<bid>', methods=['DELETE'])
@route_meta(auth='删除图书', module='图书')
@group_required
def delete_book(bid):
    print(Book.get_detail(bid))
    Book.remove_book(bid)
    return Success(msg='删除图书成功')
