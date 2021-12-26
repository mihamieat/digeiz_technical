# -*- coding: utf-8 -*-
"""Unit model."""
from app.db import db


class UnitModel(db.Model):
    """Unit model."""

    __tablename__ = "unit"

    unit_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float(precision=2))
    uuid = db.Column(db.String)

    mall_uuid = db.Column(db.String, db.ForeignKey("mall.uuid"))
    mall = db.relationship("MallModel")

    def __init__(self, name, price, uuid, mall_uuid):
        """Init unit with name, place number and mall uuid."""
        self.name = name
        self.price = price
        self.uuid = uuid
        self.mall_uuid = mall_uuid

    def json(self):
        """Return unit json."""
        return {
            "name": self.name,
            "price": self.price,
            "uuid": self.uuid,
            "mall_uuid": self.mall_uuid,
        }

    @classmethod
    def get_all(cls):
        """Return all units."""
        return cls.query.all()

    @classmethod
    def find_by_name(cls, name):
        """Find a unit in table by its name."""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_uuid(cls, uuid):
        """Find a unit in table by its id."""
        return cls.query.filter_by(uuid=uuid).first()

    def save_to_db(self):
        """Save units properties to the database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete a unit from the database."""
        db.session.delete(self)
        db.session.commit()
    
    def bulk_insert(unit_obj_list):
        """Bulk inster unit object list."""
        db.session.bulk_save_objects(unit_obj_list)
        db.session.commit()
