from flask import Blueprint, request, jsonify
from gutenberg.models import (
        Book,
        Bookshelf,
        Author,
        Subject,
        Format,
        Language
    )
from sqlalchemy import or_
import logging

main = Blueprint('main', __name__)
logger = logging.getLogger(__name__)


@main.route('/api/v1/gutenberg', methods=['GET'])
def get_data():
    if request.args.get('offset'):
        page_number = int(request.args.get('offset'))
    else:
        page_number = 1

    logger.info('books requested with offset: {}'.format(page_number))

    count_number = 25
    offset_number = (page_number * count_number) - count_number

    all_books = Book.query.order_by(Book.download_count.desc())

    if request.args.get('topic'):
        topics = request.args.get('topic')
        logger.info('applying filters on subject and bookshelf with topic: "{}"'.format(topics))
        for topic in topics.split(','):
            filter_string = '%{}%'.format(topic)
            all_books = all_books.filter(or_(Book.bookshelf.any(Bookshelf.name.like(filter_string)), Book.subject.any(Subject.name.like(filter_string))))

    if request.args.get('language'):
        language = request.args.get('language')
        logger.info('applying filters on books language with value: "{}"'.format(language))
        all_books = all_books.filter(Book.language.any(Language.code.in_(language.split(','))))

    if request.args.get('title'):
        titles = request.args.get('title')
        logger.info('applying filters on books title with value: "{}"'.format(titles))
        for title in titles.split(','):
            filter_string = '%{}%'.format(title)
            all_books = all_books.filter(Book.title.like(filter_string))

    if request.args.get('author'):
        authors = request.args.get('author')
        logger.info('applying filters on books authors with value: "{}"'.format(authors))
        for author in authors.split(','):
            filter_string = '%{}%'.format(author)
            all_books = all_books.filter(Book.author.any(Author.name.like(filter_string)))

    if request.args.get('mime_type'):
        mime_types = request.args.get('mime_type')
        logger.info('applying filters on books mime types with value: "{}"'.format(mime_types))
        for mime_type in mime_types.split(','):
            filter_string = '%{}%'.format(mime_type)
            all_books = all_books.filter(Book.formats.any(Format.mime_type.like(filter_string)))

    total_records = all_books.count()
    logger.info('total filtered records: {}'.format(total_records))

    selected_books = all_books.offset(offset_number).limit(count_number).all()
    selected_records = len(selected_books)
    logger.info('selected records: {}'.format(selected_records))

    books = [book.to_dict() for book in selected_books]

    result = {
        'records_info': {
            'limit': count_number,
            'offset': page_number,
            'total_records': total_records,
            'selected_records': selected_records,
            'order_by': {
                'download_count': 'DESC'
            }
        },
        'records': books
    }

    return jsonify(result)