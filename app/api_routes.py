from flask import jsonify
from flask_restful import Resource, reqparse
from .models import Book, Member
from . import db

class BookListAPI(Resource):
    def get(self):
        books = Book.query.all()
        return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description} for book in books])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('author', type=str, required=True)
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        new_book = Book(title=args['title'], author=args['author'], description=args.get('description'))
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'id': new_book.id, 'title': new_book.title, 'author': new_book.author, 'description': new_book.description}), 201

class BookAPI(Resource):
    def get(self, book_id):
        book = Book.query.get_or_404(book_id)
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description})

    def put(self, book_id):
        book = Book.query.get_or_404(book_id)
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True)
        parser.add_argument('author', type=str, required=True)
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        book.title = args['title']
        book.author = args['author']
        book.description = args.get('description', book.description)
        db.session.commit()
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description})

    def delete(self, book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return '', 204

class MemberListAPI(Resource):
    def get(self):
        members = Member.query.all()
        return jsonify([{'id': member.id, 'name': member.name, 'email': member.email, 'phone': member.phone} for member in members])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('phone', type=str)
        args = parser.parse_args()

        new_member = Member(name=args['name'], email=args['email'], phone=args.get('phone'))
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'id': new_member.id, 'name': new_member.name, 'email': new_member.email, 'phone': new_member.phone}), 201

class MemberAPI(Resource):
    def get(self, member_id):
        member = Member.query.get_or_404(member_id)
        return jsonify({'id': member.id, 'name': member.name, 'email': member.email, 'phone': member.phone})

    def put(self, member_id):
        member = Member.query.get_or_404(member_id)
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('phone', type=str)
        args = parser.parse_args()

        member.name = args['name']
        member.email = args['email']
        member.phone = args.get('phone', member.phone)
        db.session.commit()
        return jsonify({'id': member.id, 'name': member.name, 'email': member.email, 'phone': member.phone})

    def delete(self, member_id):
        member = Member.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        return '', 204

def init_api(api):
    api.add_resource(BookListAPI, '/api/books', '/api/book')
    api.add_resource(BookAPI, '/api/books/<int:book_id>', '/api/book/<int:book_id>')
    api.add_resource(MemberListAPI, '/api/members', '/api/member')
    api.add_resource(MemberAPI, '/api/members/<int:member_id>', '/api/member/<int:member_id>')