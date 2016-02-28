
# -*- coding: utf-8 -*-

import os
import csv
import requests
from flask import session, render_template, Blueprint, request, jsonify, abort,\
    current_app, redirect, url_for
from config import *

from flask import Flask, redirect, url_for
from werkzeug import secure_filename

from db import *
from utils import parse_request, jsonify_list
from maps import *
api = Blueprint('APIs', __name__)


# query an entity
# =/<:entity>s?query_param1=val1&query_param2=val2&..query_paramn=valn=
@api.route('/<entity>', methods=['GET'])
def query_an_entity(entity):
    if entity not in entity_pairs:
        abort(400, 'Entity %s is not valid.' % entity)

    curr_entity = entity_pairs[entity]['entity_class']
    arg_tuple_list = request.args.lists()
    if not arg_tuple_list:
        print "data: %s" % [i.to_client() for i in curr_entity.get_all()]
        return jsonify_list([i.to_client() for i in curr_entity.get_all()])
    else:
        query = curr_entity.query
        filters = []
        for arg_tuple in arg_tuple_list:
            args = arg_tuple[0].split('.')
            values = arg_tuple[1][0].split(',')
            filters.append(create_filters(entity_pairs[entity], \
                                          curr_entity, args, values))
        for filter in filters:
            query = query.filter(filter)
        entities = query.all()
        print "data: %s" % [ent.to_client() for ent in entities]
        return jsonify_list([ent.to_client() for ent in entities])


def create_filters(entity_map, curr_entity, args, values):
    if len(args) == 1:
        try:
            return getattr(curr_entity, args[0]).in_(values)
        except Exception, e:
            abort(400, 'error is %s' % (str(e)))
    else:
        result = filter(lambda item: item['name'] == args[0],
                        entity_map['attributes'])
        if not result:
            abort(400, '%s is not attribute of %s' %
                  (args[0], str(entity_map['entity_class'])))

        entity_map = args[0]
        if result[0]['relationship'] == 'one':
            try:
                return getattr(curr_entity, args[0]).has(
                    create_filters(entity_map, result[0]['class'], \
                                   args[1:], values))
            except Exception, e:
                abort(400, 'error is %s' % (str(e)))
        else:
            try:
                return getattr(curr_entity, args[0]).any(
                    create_filters(entity_map, result[0]['class'], \
                                   args[1:], values))
            except Exception, e:
                abort(400, 'error is %s' % (str(e)))


@api.route('/<entity>/<id>', methods=['GET'])
def get_specific_entity(entity, id):
    if entity not in entity_pairs:
        abort(400, 'Entity %s is not valid.' % entity)
    curr_entity = entity_pairs[entity]['entity_class']
    record = curr_entity.get_by_id(id)
    if not record:
        abort(404, "No entry for %s with id: %s found." % (entity, id))

    return jsonify(record.to_client())

entity_map_types = {
    'roles': {
        'entity': Role,
        'types': {
            'name': Name
        }
    }
}


def delete_record(entity, id):
    record = entity.get_by_id(id)
    if not record:
        abort(404, 'No %s with id %s' % (entity, id))
    else:
        try:
            record.delete()
            #db.session.delete(record)
            #db.session.commit()
        except Exception, e:
            print e
            abort(500, str(e))

    return jsonify(id=id, status="success")


# take a constructor, and attr name and the actual attribute and convert the
# attribute value to its actual type
def typecast_compound_item(const, attr, val):
    if 'id' not in val:
        abort(400, "id attr has to be present in %s:%s" % (attr,
                                                           val))
    try:
        new_val = const.get_by_id(val['id'])
    except TypeError:
        abort(400, '%s is not a valid %s' % (val, attr))

    if not new_val:
        abort(404, 'id %s of %s is not found' % (val['id'], attr))
    print "new val after const: %s" % new_val
    return new_val


# take a constructor, and attr name and the actual attribute and convert the
# attribute value to its actual type
def typecast_item(const, attr, val):
    if type(val) is dict:
        new_val = typecast_compound_item(const, attr, val)
        return new_val

    try:
        new_val = const(val)
    except TypeError:
        abort(400, '%s is not a valid %s' % (val, attr))

    print "new val after const: %s" % new_val
    return new_val


def typecast_data(entity, data):
    updated_data = {}
    for attr, val in data.iteritems():
        print "attr: %s, val: %s" % (attr, val)
        if attr not in entity_map_types[entity]['types']:
            abort(400, '%s attribute not in %s' % (attr, entity))
        const = entity_map_types[entity]['types'][attr]
        print "const for %s is %s" % (attr, const)

        if type(val) is list:
            new_val = map(lambda item: typecast_item(const, attr, item), val)
        else:
            new_val = typecast_item(const, attr, val)

        updated_data[attr] = new_val

    return updated_data


def update_record(entity_name, entity, id):
    record = entity.get_by_id(id)

    if not record:
        abort(404, 'No %s with id %s' % (entity_name, id))

    data = parse_request(request)
    if not data or type(data) is not dict:
        abort(400, "The data should be in JSON format")

    data = typecast_data(entity_name, data)
    print "typecasted data: %s" % data

    try:
        print "Updating record: %s with data: %s" % (record, data)
        record.update(**data)
    except Exception, e:
        print e
        abort(500, str(e))

    return jsonify(record.to_client())


@api.route('/<entity>/<id>', methods=['PUT', 'DELETE'])
def modify_entity(entity, id):
    if entity not in entity_map_types:
        abort(400, 'Entity %s is not valid.' % entity)

    curr_entity = entity_map_types[entity]['entity']

    if request.method == 'DELETE':
        status = delete_record(curr_entity, id)
        return status

    if request.method == 'PUT':
        status = update_record(entity, curr_entity, id)
        return status


def create_record(entity_name, entity):

    data = parse_request(request)
    if not data or type(data) is not dict:
        abort(400, "The data should be in JSON format")

    data = typecast_data(entity_name, data)
    print "creating new, typecasted data: %s" % data

    try:
        print "Creating record: %s with data: %s" % (entity_name, data)
        new_record = entity(**data)
        new_record.save()
    except Exception, e:
        print e
        abort(500, str(e))

    return jsonify(new_record.to_client())

@api.route('/<entity>', methods=['POST'])
def create_entity(entity):
    if entity not in entity_map_types:
        abort(400, 'Entity %s is not valid.' % entity)

    curr_entity = entity_map_types[entity]['entity']

    status = create_record(entity, curr_entity)
    return status
