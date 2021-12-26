# -*- coding: utf-8 -*-
"""Account model."""
from app.db import db


class AccountModel(db.Model):
    """Account model."""

    __tablename__ = "account"

    acc_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    location = db.Column(db.String)
    uuid = db.Column(db.String)

    def __init__(self, name, location, uuid):
        """Init Acount with name, id and location."""
        self.name = name
        self.location = location
        self.uuid = uuid

    def json(self):
        """Return account json."""
        return {"name": self.name, "location": self.location, "uuid": self.uuid}

    @classmethod
    def get_all(cls):
        """Return all accounts."""
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        """Find an account in table by its name."""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        """Find an account in table by its id."""
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        """Save account properties to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete account from the database."""
        db.session.delete(self)
        db.session.commit()

    def bulk_insert(account_obj_list):
        """Bulk inster account object list."""
        db.session.bulk_save_objects(account_obj_list)
        db.session.commit()
