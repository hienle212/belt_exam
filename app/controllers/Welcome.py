from system.core.controller import *
class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)
        self.load_model('Model')
    def index(self):
        return self.load_view('login.html')
    def register(self):
        user_info = self.models['Model'].register(request.form)
        if user_info['status'] == True:
            session['id'] = user_info['user']['id'] 
            session['name'] = user_info['user']['name']            
            return redirect ('/books')
        else:
            for message in user_info['errors']:
                flash(message)
            return redirect('/')
    def login(self):
        login_info = self.models['Model'].login(request.form)
        print login_info
        if login_info['status'] == True:
            session['id'] = login_info['user']['id'] 
            session['name'] = login_info['user']['name']
            return redirect('/books')
        else:
            for message in login_info['errors']:
                flash(message)
            return redirect('/')
    def showbook(self):
        book_review = self.models['Model'].book_has_review()
        other_book = self.models['Model'].other_book()
        return self.load_view('book_page.html', book_review = book_review, other_book= other_book)
    def show_users(self, user_id):
        user_info = self.models['Model'].users_page(user_id)
        return self.load_view('userpage.html', user_info = user_info)
    def show_bookinfo(self, book_id):
        books = self.models['Model'].books_info(book_id)
        print books
        return self.load_view('book_info.html', books = books)
    def add_review(self):
        newreview = {'review': request.form['review'], 'rating' : request.form['rating'], 'user_id': session['id'], 'book_id' : request.form['book_id']}
        self.models['Model'].add_review(newreview)
        return redirect ('/books')
    def add_reviewpage(self):
        return self.load_view('add_book.html')
    def add_book(self):
        book_id = self.models['Model'].create_book(request.form)
        newreview = {'review': request.form['review'], 'rating' : request.form['rating'], 'user_id': session['id'], 'book_id' : book_id}
        self.models['Model'].add_review(newreview)
        return redirect ('/books')
    def remove_review(self,user_id):
        self.models['Model'].remove_review(user_id)
        return redirect ('/books')






