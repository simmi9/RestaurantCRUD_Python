from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
#importing CRUD Operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                firstResult = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += '''<!DOCTYPE html><html lang="en"><head>
                <title>Bootstrap Example</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
                </head>'''
                output += "<body>"
                output += ''' <nav class="navbar navbar-inverse"><div class="container-fluid">
                <div class="navbar-header"><a class="navbar-brand" href="http://localhost:8080/restaurants">
                Restaurants and Menus</a></div>
                <ul class="nav navbar-nav"><li class="active">
                <a href="http://localhost:8080/restaurants">Home</a></li>
                <li class="dropdown">
                <a class="dropdown-toggle" data-toggle="dropdown" href="#">Restaurants 
                <span class="caret"></span></a><ul class="dropdown-menu">
                <li><a href="http://localhost:8080/restaurants/new">Create New</a></li>
                </ul></li></ul></div></nav>'''
                output += '''<h1 align="center">Restaurant Details</h1>'''
                output += '''<div class="container text-center">'''
                output += '''<table class="table table-hover">'''
                output += '''<thead><tr> <th>Restaurant name</th><th>Modify Restaurant</th>
                <th>Delete Restaurant</th></tr></thead><tbody>'''
                for fr in firstResult:
                    output += '''<tr><td>'''
                    output += fr.name
                    output += '''</td>'''
                    output += '''<td>'''
                    output += '''<a href="http://localhost:8080/restaurants/%s/edit">Modify Restaurant</a>''' % fr.id
                    output += '''</td>'''
                    output += '''<td>'''
                    output += '''<a href="http://localhost:8080/restaurants/confirmdelete">Delete Restaurant</a>'''
                    output += '''</td>'''
                    output += '''</tr>'''
                    print fr.name
                    print "\n"
                output += '''</tbody></table></div>'''
                output += '''</div>''' 
                #output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()        
                output = ""
                output += '''<!DOCTYPE html><html lang="en"><head>
                <title>Bootstrap Example</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
                </head>'''
                output += "<body>"
                output += "<h1>Create New Restaurant</h1>"
                output += '''<form method ='POST'  enctype='multipart/form-data' action = '/restaurants/new'>
                <div class="form-group">
                <label for="New Restaurant Name">New Restaurant Name</label>
                <input type="text" class="form-control" id="rname" name = 'newRestaurantName' placeholder = 'New Restaurant Name'>
                </div>'''
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                    # Create new Restaurant Object
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()


            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(
                self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()