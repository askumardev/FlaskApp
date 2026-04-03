from flask import request, jsonify
from . import api_bp
from models import Category
from db import db

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'description': c.description} for c in categories])

@api_bp.route('/categories/<int:id>', methods=['GET'])
def get_category(id):
    c = Category.query.get_or_404(id)
    return jsonify({'id': c.id, 'name': c.name, 'description': c.description})

@api_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json(force=True)
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    if Category.query.filter_by(name=name).first():
        return jsonify({'error': 'category already exists'}), 400
    category = Category(name=name, description=description)
    db.session.add(category)
    db.session.commit()
    return jsonify({'id': category.id, 'name': category.name, 'description': category.description}), 201

@api_bp.route('/categories/<int:id>', methods=['PUT'])
def replace_category(id):
    c = Category.query.get_or_404(id)
    data = request.get_json(force=True)
    name = data.get('name')
    description = data.get('description')
    if not name:
        return jsonify({'error': 'name is required'}), 400
    c.name = name
    c.description = description
    db.session.commit()
    return jsonify({'id': c.id, 'name': c.name, 'description': c.description})

@api_bp.route('/categories/<int:id>', methods=['PATCH'])
def update_category(id):
    c = Category.query.get_or_404(id)
    data = request.get_json(force=True)
    if 'name' in data:
        c.name = data['name']
    if 'description' in data:
        c.description = data['description']
    db.session.commit()
    return jsonify({'id': c.id, 'name': c.name, 'description': c.description})

@api_bp.route('/categories/<int:id>', methods=['DELETE'])
def delete_category(id):
    c = Category.query.get_or_404(id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({'status': 'deleted'}), 204