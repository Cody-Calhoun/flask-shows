from flaskapp.config.mysqlconnection import connectToMySQL
from flask import flash
from flaskapp.models import user

class Show():
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.release_date = data['release_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.creator = None #User Object

    @classmethod
    def get_all_shows(cls):
        query = "SELECT * FROM shows"
        return connectToMySQL('ripened_tomatoes').query_db(query)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM shows WHERE id = %(id)s"
        results = connectToMySQL('ripened_tomatoes').query_db(query, data)
        return cls(results[0])

    @staticmethod
    def show_validator(data):
        is_valid = True
        if len(data['title']) < 3:
            flash('Title must be at least 3 characters')
            is_valid = False
        query = "SELECT * FROM shows WHERE title = %(title)s"
        results = connectToMySQL('ripened_tomatoes').query_db(query, data)
        if len(results) != 0:
            flash('TV Show already exists.')
            is_valid = False
        if len(data['description']) < 3:
            flash('Description must be at least 3 characters')
            is_valid = False
        if data['release_date'] == '':
            flash('Please select a date')
            is_valid = False
        return is_valid
    
    @classmethod
    def create_show(cls, form_data):
        query = "INSERT INTO shows (title, description, release_date, users_id) VALUES (%(title)s, %(description)s, %(release_date)s, %(users_id)s)"
        return connectToMySQL('ripened_tomatoes').query_db(query, form_data)

    @classmethod
    def get_all_shows_with_users(cls):
        query = "SELECT * FROM shows LEFT JOIN users ON shows.users_id = users.id;"
        shows = connectToMySQL('ripened_tomatoes').query_db(query)
        results = []
        for show in shows:
            data = {
                'id': show['users.id'],
                'first_name': show['first_name'],
                'last_name': show['last_name'],
                'email': show['email'],
                'password': show['password'],
                'created_at': show['users.created_at'],
                'updated_at': show['users.updated_at']
            }
            one_show = cls(show)
            one_show.creator = user.User(data)
            results.append(one_show)
        return results

    @classmethod
    def update_show(cls, form_data):
        query = "UPDATE shows SET title=%(title)s, description=%(description)s, release_date=%(release_date)s WHERE id=%(id)s"
        return connectToMySQL('ripened_tomatoes').query_db(query, form_data)

    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM shows WHERE id=%(id)s'
        return connectToMySQL('ripened_tomatoes').query_db(query, data)