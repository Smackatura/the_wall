from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.poster = None
    @classmethod
    def get_post(cls, data):
        query= "SELECT * FROM posts WHERE id = %(id)s"
        results = connectToMySQL("the_wall").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE id = %(id)s"
        return connectToMySQL("the_wall").query_db(query, data)
    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET content=%(content)s WHERE id = %(id)s"
        return connectToMySQL("the_wall").query_db(query, data)
    @classmethod
    def add_post(cls, data):
        query = "INSERT INTO posts(content, user_id) VALUES(%(content)s, %(user_id)s)"
        return connectToMySQL("the_wall").query_db(query, data)
    
    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM posts JOIN users ON user_id = users.id"
        posts = connectToMySQL("the_wall").query_db(query)
        results = []
        for post in posts:
            print(post)
            a_post = cls(post)
            poster_data = {
                "id" : post["users.id"],
                "first_name": post["first_name"],
                "last_name": post["last_name"],
                "email": post["email"],
                "password": post["password"],
                "created_at": post["users.created_at"],
                "updated_at": post["users.updated_at"]
            }
            a_post.poster = User(poster_data)
            results.append(a_post)
        return results

    @classmethod
    def get_user_posts(cls, data):
        query = "SELECT * FROM posts WHERE user_id =%(user_id)s"
        posts = connectToMySQL("the_wall").query_db(query, data)
        results = []
        for post in posts:
            results.append(cls(post))
        return results



# results = connectToMySQL('burgers').query_db( query , data )
#         # groups will be a list of music group objects from our raw data
#     	burger = cls( results[0] )
#         for row_from_db in results:
#             # Now we parse the topping data to make instances of toppings and add them into our list.
#             topping_data = {
#                 "id" : row_from_db["toppings.id"],
#                 "topping_name" : row_from_db["topping_name"],
#                 "created_at" : row_from_db["toppings.created_at"],
#                 "updated_at" : row_from_db["toppings.updated_at"]
#             }
#             burger.toppings.append( topping.Topping( topping_data ) )
#     	return burger