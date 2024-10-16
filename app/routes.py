from flask import render_template, redirect, url_for, request, jsonify
from . import db
from .models import Book, Member
from flask import jsonify

def init_routes(app):
    @app.route('/')
    def index():
        books = Book.query.all()
        return render_template('index.html', books=books)

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

    @app.route('/debug-api')
    def debug_api():
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                "endpoint": rule.endpoint,
                "methods": list(rule.methods),
                "rule": str(rule)
            })
        return jsonify(routes)
    
    @app.route('/api-routes')
    def api_routes():
        routes = []
        for resource, _ in api.resources:
             routes.append(str(resource))
        return jsonify(routes)