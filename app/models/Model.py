from system.core.model import *
import re     
class Model(Model):
    def __init__(self):
        super(Model, self).__init__()
    def register(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        PASSWORD_REGEX = re.compile(r'^([^0-9]*|[^A-Z]*)$')
        errors = []
        if len(info['name']) < 2 or not info['name'].isalpha():
            errors.append("Invalid  Name. (Letters only, at least 2 characters.)")
        if len(info['alias']) < 2 or not info['alias'].isalpha():
            errors.append("Invalid Alias. (Letters only, at least 2 characters.)")   
        if len(info['email']) < 1 or not EMAIL_REGEX.match(info['email']):
            errors.append ("Invalid Email Address!")    
        if len(info['password']) < 8 :
            errors.append("Password should be more than 8 characters")
        if info['password'] != info['confirm_password']:
            errors.append('Password and confirm password must match!')
        if PASSWORD_REGEX.match(info['confirm_password']):
            errors.append("Password requires to have at least 1 uppercase letter and 1 numeric value ")   
        if errors:
            return {"status":False, "errors":errors}            
        else:  
            query = "INSERT into users (name, alias, email, password, created_at, updated_at) VALUES(:name,:alias,:email,:password, NOW(),NOW())"
            data = {'name': info['name'], 'alias': info['alias'], 'email' :info['email'], 'password' :info['password']}
            self.db.query_db(query, data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return {"status": True, "user": users[0]}
    def login(self,info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if len(info['email']) < 1 or not EMAIL_REGEX.match(info['email']):
            errors.append ("Invalid Email Address!")    
        if len(info['password']) < 8 :
            errors.append("Password should be more than 8 characters")
        if errors:
            return {"status":False, "errors":errors}            
        else:  
            query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            data = {'email' : info['email']}
            users = self.db.query_db(query,data) 
            return {"status": True, "user": users[0]}
    def book_has_review(self):
        query="select users.id as users_id, books.title as titles, books.id as books_id, rating, review, users.name as name, reviews.created_at as created_on from reviews left join books on books.id = reviews.book_id left join users on users.id = reviews.user_id order by reviews.created_at DESC limit 3"
        return self.db.query_db(query)
    def other_book(self):
        query="select books.title as titles, rating, review, users.name as name,books.id as books_id, reviews.created_at as created_on from reviews left join books on books.id = reviews.book_id left join users on users.id = reviews.user_id order by reviews.created_at ASC"  
        return self.db.query_db(query) 
    def users_page(self, user_id):
        query= "select users.name as name, alias, email, count(reviews.user_id) as count, books.title as titles, books.id as books_id from users left join reviews on reviews.user_id = users.id left join books on books.id = reviews.book_id where users.id = :id"   
        data =  {"id" : user_id}
        return self.db.query_db(query, data)
    def books_info(self, book_id):
        query = "select users.id as users_id, books.title as titles,books.id as books_id, rating, review, author, users.name as name, reviews.created_at as created_on from reviews left join books on books.id = reviews.book_id left join users on users.id = reviews.user_id where books.id = :book_id"
        data =  {"book_id" : book_id}
        return self.db.query_db(query, data)
    def add_review(self, info):
        query = "insert into reviews (review, rating, created_at, updated_at, user_id, book_id) values (:review, :rating ,now(),now(), :user_id, :book_id)"
        data = {'review': info['review'], 'rating': info['rating'], 'user_id' :info['user_id'], 'book_id' :info['book_id']}
        return self.db.query_db(query, data)
    def create_book(self,info):
        query = "insert into books (title, author, created_at, updated_at) values (:title, :author ,now(),now())"
        data = {'title': info['title'], 'author': info['author']}
        return self.db.query_db(query, data)
    def remove_review(self, user_id):
        query="delete from reviews where user_id = :user_id"
        data =  {"user_id" : user_id}
        return self.db.query_db(query, data)


