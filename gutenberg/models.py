from gutenberg import db
from gutenberg.support.helpers import CustomSerializerMixin


book_authors = db.Table('books_book_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('books_book.gutenberg_id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('books_author.id'), primary_key=True)
)

book_bookshelves = db.Table('books_book_bookshelves',
    db.Column('book_id', db.Integer, db.ForeignKey('books_book.gutenberg_id'), primary_key=True),
    db.Column('bookshelf_id', db.Integer, db.ForeignKey('books_bookshelf.id'), primary_key=True)
)


book_languages = db.Table('books_book_languages',
    db.Column('book_id', db.Integer, db.ForeignKey('books_book.gutenberg_id'), primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey('books_language.id'), primary_key=True)
)


book_subjects = db.Table('books_book_subjects',
    db.Column('book_id', db.Integer, db.ForeignKey('books_book.gutenberg_id'), primary_key=True),
    db.Column('subject_id', db.Integer, db.ForeignKey('books_subject.id'), primary_key=True)
)


class Book(db.Model, CustomSerializerMixin):
    __tablename__ = 'books_book'

    serialize_only = ('title', 'author.name', 'author.death_year', 'author.birth_year', 'formats.url', 'formats.mime_type', 'language.code', 'bookshelf.name', 'subject.name')
    serialize_rules = ('-author.books', '-formats.books', '-language.books', '-bookshelf.books', '-subject.books')

    id = db.Column(db.Integer, primary_key=True)
    download_count = db.Column(db.Integer, nullable=True)
    gutenberg_id = db.Column(db.Integer, nullable=False)
    media_type = db.Column(db.String(16), nullable=False)
    title = db.Column(db.Text, nullable=True)
    formats = db.relationship('Format', backref='books', lazy=True)

    def __repr__(self):
        return "<Book(id={}, title='{}')>".format(self.id, self.title)


class Author(db.Model, CustomSerializerMixin):
    __tablename__ = 'books_author'
    id = db.Column(db.Integer, primary_key=True)
    birth_year = db.Column(db.Integer, nullable=True)
    death_year = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(128), nullable=False)
    books = db.relationship('Book', secondary=book_authors, lazy='dynamic',
                             backref=db.backref('author', lazy=True))

    def __repr__(self):
        return "<Author(id={}, name='{}')>".format(self.id, self.name)


class Bookshelf(db.Model, CustomSerializerMixin):
    __tablename__ = 'books_bookshelf'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    books = db.relationship('Book', secondary=book_bookshelves, lazy='dynamic',
                            backref=db.backref('bookshelf', lazy=True))

    def __repr__(self):
        return "<Bookshelf(id={}, name='{}')>".format(self.id, self.name)


class Format(db.Model, CustomSerializerMixin):
    __tablename__ = 'books_format'
    id = db.Column(db.Integer, primary_key=True)
    mime_type = db.Column(db.String(32), nullable=False)
    url = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books_book.gutenberg_id'),
        nullable=False)

    def __repr__(self):
        return "<Format(id={}, mime_type='{}')>".format(self.id, self.mime_type)


class Subject(db.Model, CustomSerializerMixin):
    __tablename__ = 'books_subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    books = db.relationship('Book', secondary=book_subjects, lazy='dynamic',
                            backref=db.backref('subject', lazy=True))

    def __repr__(self):
        return "<Subject(id={}, name='{}')>".format(self.id, self.name)


class Language(db.Model, CustomSerializerMixin):
    __tablename__ = 'books_language'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(4), nullable=False)
    books = db.relationship('Book', secondary=book_languages, lazy='dynamic',
                            backref=db.backref('language', lazy=True))

    def __repr__(self):
        return "<Language(id={}, code='{}')>".format(self.id, self.code)