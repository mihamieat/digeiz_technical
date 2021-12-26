# -*- coding: utf-8 -*-
"""Mall model."""
from app.db import db


class MallModel(db.Model):
    """Mall model."""

    __tablename__ = "mall"

    mall_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    place_number = db.Column(db.String)
    uuid = db.Column(db.String)

    account_uuid = db.Column(db.String, db.ForeignKey("account.uuid"))
    account = db.relationship("AccountModel")

    def __init__(self, name, place_number, uuid, account_uuid):
        """Init mall with name, place number and account uuid."""
        self.name = name
        self.place_number = place_number
        self.uuid = uuid
        self.account_uuid = account_uuid

    def json(self):
        """Return mall json."""
        return {
            "name": self.name,
            "place_number": self.place_number,
            "uuid": self.uuid,
            "account_uuid": self.account_uuid,
        }

    @classmethod
    def get_all(cls):
        """Return all malls."""
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        """Find a mall in table by its name."""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        """Find a mall in table by its id."""
        return cls.query.filter_by(uuid=uuid).first()

    @classmethod
    def find_by_place_number(cls, place_number):
        """Find a mall in the table by its place numbver."""
        return cls.query.filter_by(place_number=place_number).first()

    def save_to_db(self):
        """Save malls properties to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete a mall from the database."""
        db.session.delete(self)
        db.session.commit()
    
    def bulk_insert(mall_obj_list):
        """Bulk inster mall oject list."""
        db.session.bulk_save_objects(mall_obj_list)
        db.session.commit()
