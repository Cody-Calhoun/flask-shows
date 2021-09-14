from flaskapp.config.mysqlconnection import connectToMySQL

class Review():
    def __init__(self, data):
        self.id = data['id']
        self.review = data['review']
        self.created_at = ['created_at']
        self.updated_at = ['updated_at']
        self.user = None
        self.show = None