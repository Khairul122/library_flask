from flask import render_template, redirect, url_for, request, jsonify
from . import db
from .models import Book, Member

def init_routes(app):
    @app.route('/')
    def index():
        books = Book.query.all()
        return render_template('index.html', books=books)
    
    # API Book
    @app.route('/api/books', methods=['GET'])
    def get_books():
        books = Book.query.all()
        return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description} for book in books])

    @app.route('/api/books', methods=['POST'])
    def add_book_api():
        data = request.json
        new_book = Book(title=data['title'], author=data['author'], description=data.get('description', ''))
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'id': new_book.id, 'title': new_book.title, 'author': new_book.author, 'description': new_book.description}), 201

    @app.route('/api/books/<int:book_id>', methods=['GET'])
    def get_book(book_id):
        book = Book.query.get_or_404(book_id)
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description})

    @app.route('/api/books/<int:book_id>', methods=['PUT'])
    def update_book(book_id):
        book = Book.query.get_or_404(book_id)
        data = request.json
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        db.session.commit()
        return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description})

    @app.route('/api/books/<int:book_id>', methods=['DELETE'])
    def delete_book_api(book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return '', 204
    
    # API Member
    @app.route('/api/members', methods=['GET'])
    def get_members():
        members = Member.query.all()
        return jsonify([{'id': member.id, 'name': member.name, 'email': member.email, 'phone': member.phone} for member in members])

    @app.route('/api/members', methods=['POST'])
    def add_member_api():
        data = request.json
        new_member = Member(name=data['name'], email=data['email'], phone=data.get('phone', ''))
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'id': new_member.id, 'name': new_member.name, 'email': new_member.email, 'phone': new_member.phone}), 201

    @app.route('/api/members/<int:member_id>', methods=['GET'])
    def get_member(member_id):
        member = Member.query.get_or_404(member_id)
        return jsonify({'id': member.id, 'name': member.name, 'email': member.email, 'phone': member.phone})

    @app.route('/api/members/<int:member_id>', methods=['PUT'])
    def update_member(member_id):
        member = Member.query.get_or_404(member_id)
        data = request.json
        member.name = data.get('name', member.name)
        member.email = data.get('email', member.email)
        member.phone = data.get('phone', member.phone)
        db.session.commit()
        return jsonify({'id': member.id, 'name': member.name, 'email': member.email, 'phone': member.phone})

    @app.route('/api/members/<int:member_id>', methods=['DELETE'])
    def delete_member_api(member_id):
        member = Member.query.get_or_404(member_id)
        db.session.delete(member)
        db.session.commit()
        return '', 204
    
    @app.route('/add', methods=['GET', 'POST'])
    def add_book():
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            description = request.form['description']
            new_book = Book(title=title, author=author, description=description)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('add_book.html')

    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit_book(id):
        book = Book.query.get_or_404(id)
        if request.method == 'POST':
            book.title = request.form['title']
            book.author = request.form['author']
            book.description = request.form['description']
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('edit_book.html', book=book)

    @app.route('/delete/<int:id>', methods=['POST'])
    def delete_book(id):
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('index'))

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/member')
    def index_member():
        members = Member.query.all()
        return render_template('index_member.html', members=members)

    @app.route('/add_member', methods=['GET', 'POST'])
    def add_member():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            new_member = Member(name=name, email=email, phone=phone)
            db.session.add(new_member)
            db.session.commit()
            return redirect(url_for('index_member'))
        return render_template('add_member.html')

    @app.route('/edit_member/<int:id>', methods=['GET', 'POST'])
    def edit_member(id):
        member = Member.query.get_or_404(id)
        if request.method == 'POST':
            member.name = request.form['name']
            member.email = request.form['email']
            member.phone = request.form['phone']
            db.session.commit()
            return redirect(url_for('index_member'))
        return render_template('edit_member.html', member=member)

    @app.route('/delete_member/<int:id>', methods=['POST'])
    def delete_member(id):
        member = Member.query.get_or_404(id)
        db.session.delete(member)
        db.session.commit()
        return redirect(url_for('index_member'))

    @app.route('/debug-routes')
    def debug_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                "endpoint": rule.endpoint,
                "methods": list(rule.methods),
                "rule": str(rule)
            })
        return jsonify(routes)