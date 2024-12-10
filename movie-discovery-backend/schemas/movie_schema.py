# schemas/movie_schema.py

from marshmallow import Schema, fields, validate

class MovieSchema(Schema):
    title = fields.String(required=False)  # Corresponds to the "name" in the document
    genres = fields.List(fields.String(), required=False)  # "genre" in the document
    runtime = fields.Integer(required=False, validate=validate.Range(min=1))  # "duration" in the document
    actors = fields.List(fields.String(), required=False)  # Corresponds to "cast_name" in the document
    director = fields.String(required=False)  # Corresponds to "director_name" in the document
    release_year = fields.Integer(required=False, validate=validate.Range(min=1888))  # "year" in the document
    description = fields.String(required=False)  # Assuming you have a description field
    rating = fields.Float(required=False, validate=validate.Range(min=0, max=10))  # "imdb_rating" in the document
