from app import db, login
from sqlalchemy import JSON
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

reference = db.Table('reference',
    db.Column('document', db.Integer, db.ForeignKey('document.id'), primary_key=True),
    db.Column('reference', db.Integer, db.ForeignKey('document.id'), primary_key=True)
)
 
 
class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    doi = db.Column(db.String(64), index=True, unique=True)
    references = db.relationship('Document', \
            secondary=reference, \
            backref=db.backref('referenced_by', lazy=True), \
            primaryjoin=id==reference.c.document,
            secondaryjoin=id==reference.c.reference
        )
    queried = db.Column(db.Boolean, default=False)
    meta = db.Column(JSON, default=None)

    def __getitem__(self, key):
        return self.meta[key]

    def __hash__(self):
        return self.id.__hash__()

    def __str__(self):
        try:
            if isinstance(self['title'], list):
                return self['title'][0]
            else:
                return self['title']
        except (KeyError, IndexError):
            pass
        try:
            if isinstance(self['DOI'], list):
                return self['DOI'][0]
            else:
                return self['DOI']
        except (KeyError, IndexError):
            pass
        return '<Document {}>'.format(self.id)

    def __repr__(self):
        try:
            if isinstance(self['DOI'], list):
                return self['DOI'][0]
            else:
                return self['DOI']
        except (KeyError, IndexError):
            pass
        return '<Document {}>'.format(self.id)
