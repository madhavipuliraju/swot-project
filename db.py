
# -*- coding: utf-8 -*-

from collections import OrderedDict

from flask.ext.sqlalchemy import SQLAlchemy
from flask import current_app, request
from sqlalchemy.orm import relationship
import sqlalchemy.types as types

import os
import re
from urlparse import urlparse
from datetime import datetime
import json

from op_exceptions import AttributeRequired
from utils import typecheck


db = SQLAlchemy()


# Abstract class to hold common methods
class Entity(db.Model):

    __abstract__ = True

    # save a db.Model to the database. commit it.
    def save(self):
        db.session.add(self)
        db.session.commit()

    # update the object, and commit to the database
    def update(self, **kwargs):
        for attr, val in kwargs.iteritems():
            setter_method = "set_" + attr
            try:
                self.__getattribute__(setter_method)(val)
            except Exception as e:
                raise e

        self.save()

    #print "Setting new val"
    #print "Calling %s on %s" % (method_to_set, curr_entity)
    #try:
    #    getattr(record, method_to_set)(new_val)
    #except Exception as e:
    #pass

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Name(object):
    def __init__(self, value):
        # if the string contains any non-alphabet and non-space character, raise
        # a type error
        if re.search('[^a-zA-Z. ]+', value):
            raise TypeError('%s is not a Name!' % value)

        self.value = value

class Email(object):
    def __init__(self, value):
        if not re.search('[^@]+@[^@]+\.[^@]+', value):
            raise TypeError('%s is not an email!' % value)
        self.value = value


class Role(Entity):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

#    users = db.relationship('User', backref='role')


    def __init__(self, **kwargs):
        if 'name' not in kwargs:
            raise AttributeRequired("mandatory attribute `name` is missing")
        self.set_name(kwargs['name'])

    @staticmethod
    def get_by_id(id):
        return Role.query.get(id)

    @staticmethod
    def get_all():
        return Role.query.all()

    def get_name(self):
        return self.name

    @typecheck(name=Name)
    def set_name(self, name):
        self.name = name.value

    def to_client(self):
        return {
            'id': self.id,
            'name': self.name
        }
