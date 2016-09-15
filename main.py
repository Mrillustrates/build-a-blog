import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
            autoescape = True)


#template code required
class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self,template, **kw):
        self.write(self.render_str(template, **kw))





#create class to represent submission from the user
class Blog(db.Model):
    #define types of entities that will represent one column in table
    subject = db.StringProperty(required = True)
    blog = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    #id = db.IntegerProperty(indexed=True)



class MainPage(Handler):

    def render_front(self):
        #create a way to run query
        blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5 ")

        #search= Blog.get_by_id(int(id))
        #blog = blog.key().id()
        #render the html file with variables used for substitution
        self.render("base.html", blogs = blogs)

    def get(self):
        self.render_front()

class BlogSubmit(Handler):
    def render_submit(self, subject = "", blog = "", error= ""):
        #create a way to run query
        #blogs = db.GqlQuery("SELECT * FROM Blog ORDER BY created DESC LIMIT 5 ")

        self.render("bases.html", subject = subject , blog = blog, error = error)

    def get(self):
        self.render_submit()

    def post(self):
        #first have to retrieve values from HTML
        subject = self.request.get('subject')
        blog = self.request.get('blog')

        if subject and blog:
            a = Blog(subject = subject , blog = blog)
            #.put() GAE method stores into database
            a.put()
            #post.key().id()

            self.redirect("/blog/" + str(a.key().id()))
            #self.response.write(d)

        else:
            #error message to user
            error = "Invalid! Subject and blog entry required"
            self.render_submit(subject, blog, error)

class ViewPostHandler(Handler):
    def get(self, id):
        #id = int(self.request.get('id'))
        #Post.get_by_id(id)

        #entity = MyModel.get_by_id(id)
        search = Blog.get_by_id(int(id))
        #Key (cls, id).get() is same as get_by_id()

        self.render("viewpost.html", search = search)
        #self.response.write(search)

        #id = db.GqlQuery("SELECT * FROM Blog ORDER BY created LIMIT 1 ")
        #pass #replace this with some code to handle the request

app = webapp2.WSGIApplication([('/blog', MainPage),
                                webapp2.Route('/blog/<id:\d+>', ViewPostHandler),
                                ('/blog/newpost', BlogSubmit),
                                ], debug = True)
