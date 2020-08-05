from sqlalchemy_serializer import SerializerMixin
import datetime


class CustomSerializerMixin(SerializerMixin):
    serialize_types = (
        (datetime.datetime, lambda x: str(x)),
        (datetime.date, lambda x: str(x)),
    )