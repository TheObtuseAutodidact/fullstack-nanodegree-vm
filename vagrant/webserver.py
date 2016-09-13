from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
#  from database_setup import *

# teacher's version
# CRUD
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#  Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

import pdb

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # if self.path.endswith("/hello"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #
            #     output = ""
            #     output += "<html><body>Hello!"
            #     output += "<form method='POST' enctype='multipart/form-data' action='/ \
            #                hello'><h2>What would you like me to say?</h2><input name='message' \
            #                type='text' ><input type='submit' value='Submit'></form>"
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output #  debug tool
            #     return
            #
            # elif self.path.endswith("/hola"):
            #     self.send_response(200)
            #     self.send_header('Content-type', 'text/html')
            #     self.end_headers()
            #
            #     output = ""
            #     output += "<html><body>&#161Hola! <a href='/hello' >Back to Hello</a>"
            #     output += "<form method='POST' enctype='multipart/form-data' action='/ \
            #                hello'><h2>What would you like me to say?</h2><input name='message' \
            #                type='text' ><input type='submit' value='Submit'></form>"
            #     output += "</body></html>"
            #     self.wfile.write(output)
            #     print output #  debug tool
            #     return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header("Content-type", 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>Add A New Restaurant!"
                output += "<form method='POST' enctype='multipart/form-data' action='/ \
                restaurants/new'><h2>Restaurant Name: </h2><input name='new_restaurant' \
                type='text' ><input type='submit' value='Submit'></form>"
                output += "</body></html>"

                print output
                self.wfile.write(output)
                return

            elif self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = session.query(Restaurant).all()

                output = ""
                output +="<html><body><h1>-- Index --<h1>"
                for restaurant in restaurants:
                    output +="<div><p>"
                    output += restaurant.name
                    output +="</p>"
                    output +="<p><a href="
                    output +="/restaurants/"
                    output += str(restaurant.id)
                    output += "/edit"
                    output += ">Edit</a></p>"
                    output +="<p><a href="
                    output += "/restaurants/"
                    output += str(restaurant.id)
                    output += "/delete"
                    output += ">Delete</a></p></br>"
                    output +="</div>"
                output += "</body></html>"
                print output
                self.wfile.write(output)

            elif self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                start = self.path.find('/restaurants') + len('/restaurants') + 1
                stop = self.path.find('/edit')
                restaurant_id = self.path[start:stop] #from 'restaurants/' up to '/edit'
                print restaurant_id
                restaurant = session.query(Restaurant).get(restaurant_id)
                print restaurant.name
                output = ""
                output += "<html><body>Edit Restaurant"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/"
                output += restaurant_id
                output += "/edit'><h2>Restaurant Name: </h2><input name='edit_restaurant' type='text' value='"
                output += restaurant.name
                output += "' ><input type='submit' value='Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)

            # elif self.path.endswith('/delete'):
            #     self.send_response(200) # delete response
            #     self.send_header("Content-type", "text/html")
            #     self.end_headers()
            #
            #     restaurant_id_path = self.path.split('/')[2]
            #     restaurant = session.query(Restaurant).get(restaurant_id_path)
            #
            #     output = ""
            #     output +="<html><body>Are you sure you want to DELETE "
            #     output += restaurant.name
            #     # output += "<form action=/restaurants/"
            #     # output += str(restaurant.id)
            #     # output += "/delete method='post'>"
            #     # output +="<button type='submit' value='submit'>Delete</button></form>"
            #     output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurant.id
            #     output += "<input type = 'submit' value = 'Delete'>"
            #     output += "</form>"
            elif self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"

                self.wfile.write(output)
                return


        except IOError:
            send.send_error(404, "File Not Found %s" % self.path)


    def do_POST(self):
        try:
            # if self.path.endswith('/delete'):
            #     pdb_set_trace()
            #     # ctype, pdict = cgi.parse_header(
            #     #     self.headers.getheader('content-type'))
            #     restaurant_id_path = self.path.split('/')[2]
            #     restaurant = session.query(Restaurant).get(restaurant_id_path)
            #     session.delete(restaurant)
            #     session.commit()
            #
            #     self.send_response(301) # delete response
            #     self.send_header("Content-type", "text/html")
            #     self.send_header('Location', '/restaurants')
            #     self.end_headers()

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(
                    id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()


            elif self.path.endswith('restaurants/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant = fields.get('new_restaurant')

                    res = Restaurant(name=new_restaurant[0])
                    session.add(res)
                    session.commit()

                    self.send_response(301) #  why 301 ?
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    # return

            elif self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                # pdb.set_trace()
                if ctype == 'multipart/form-data':
                    fields=cgi.parse_multipart(self.rfile, pdict)
                    edit_restaurant = fields.get('edit_restaurant')
                    # teacher solution to my start/stop
                    #restaurant_id_path = self.path.split('/')[2]
                    start = self.path.find('/restaurants') + len('/restaurants') + 1
                    stop = self.path.find('/edit')
                    restaurant_id = self.path[start:stop] #from 'restaurants/' up to '/edit'
                    print restaurant_id

                    restaurant = session.query(Restaurant).get(restaurant_id)
                    restaurant.name = edit_restaurant[0]
                    # pdb.set_trace()
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return



                # else:
                #     messagecontent = fields.get('message')
                #
                #     output = ""
                #     output += "<html><body>"
                #     output += "<h2> Okay, how about this: </h2>"
                #     output += "<h1> %s </h1>" % messagecontent[0]
                #
                #     output += "<form method='POST' enctype='multipart/form-data' action='/ \
                #                hello'><h2>What would you like me to say?</h2><input name='message' \
                #                type='text' ><input type='submit' value='Submit'></form>"
                #     output += "</body></html>"
                #     self.wfile.write(output)
                #     print output

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()


###########################################################################
####   complete solution from instructor's notes
# 
# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import cgi
#
# # import CRUD Operations from Lesson 1 ##
# from database_setup import Base, Restaurant, MenuItem
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
#
# # Create session and connect to DB ##
# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()
#
#
# class webServerHandler(BaseHTTPRequestHandler):
#
#     def do_GET(self):
#         try:
#             # Objective 3 Step 2 - Create /restaurants/new page
#             if self.path.endswith("/restaurants/new"):
#                 self.send_response(200)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 output = ""
#                 output += "<html><body>"
#                 output += "<h1>Make a New Restaurant</h1>"
#                 output += "<form method = 'POST' enctype='multipart/form-data' action = '/restaurants/new'>"
#                 output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name' > "
#                 output += "<input type='submit' value='Create'>"
#                 output += "</form></html></body>"
#                 self.wfile.write(output)
#                 return
#             if self.path.endswith("/edit"):
#                 restaurantIDPath = self.path.split("/")[2]
#                 myRestaurantQuery = session.query(Restaurant).filter_by(
#                     id=restaurantIDPath).one()
#                 if myRestaurantQuery:
#                     self.send_response(200)
#                     self.send_header('Content-type', 'text/html')
#                     self.end_headers()
#                     output = "<html><body>"
#                     output += "<h1>"
#                     output += myRestaurantQuery.name
#                     output += "</h1>"
#                     output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/%s/edit' >" % restaurantIDPath
#                     output += "<input name = 'newRestaurantName' type='text' placeholder = '%s' >" % myRestaurantQuery.name
#                     output += "<input type = 'submit' value = 'Rename'>"
#                     output += "</form>"
#                     output += "</body></html>"
#
#                     self.wfile.write(output)
#             if self.path.endswith("/delete"):
#                 restaurantIDPath = self.path.split("/")[2]
#
#                 myRestaurantQuery = session.query(Restaurant).filter_by(
#                     id=restaurantIDPath).one()
#                 if myRestaurantQuery:
#                     self.send_response(200)
#                     self.send_header('Content-type', 'text/html')
#                     self.end_headers()
#                     output = ""
#                     output += "<html><body>"
#                     output += "<h1>Are you sure you want to delete %s?" % myRestaurantQuery.name
#                     output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % restaurantIDPath
#                     output += "<input type = 'submit' value = 'Delete'>"
#                     output += "</form>"
#                     output += "</body></html>"
#                     self.wfile.write(output)
#
#             if self.path.endswith("/restaurants"):
#                 restaurants = session.query(Restaurant).all()
#                 output = ""
#                 # Objective 3 Step 1 - Create a Link to create a new menu item
#                 output += "<a href = '/restaurants/new' > Make a New Restaurant Here </a></br></br>"
#
#                 self.send_response(200)
#                 self.send_header('Content-type', 'text/html')
#                 self.end_headers()
#                 output += "<html><body>"
#                 for restaurant in restaurants:
#                     output += restaurant.name
#                     output += "</br>"
#                     # Objective 2 -- Add Edit and Delete Links
#                     # Objective 4 -- Replace Edit href
#
#                     output += "<a href ='/restaurants/%s/edit' >Edit </a> " % restaurant.id
#                     output += "</br>"
#                     # Objective 5 -- Replace Delete href
#                     output += "<a href ='/restaurants/%s/delete'> Delete </a>" % restaurant.id
#                     output += "</br></br></br>"
#
#                 output += "</body></html>"
#                 self.wfile.write(output)
#                 return
#         except IOError:
#             self.send_error(404, 'File Not Found: %s' % self.path)
#
#     # Objective 3 Step 3- Make POST method
#     def do_POST(self):
#         try:
#             if self.path.endswith("/delete"):
#                 restaurantIDPath = self.path.split("/")[2]
#                 myRestaurantQuery = session.query(Restaurant).filter_by(
#                     id=restaurantIDPath).one()
#                 if myRestaurantQuery:
#                     session.delete(myRestaurantQuery)
#                     session.commit()
#                     self.send_response(301)
#                     self.send_header('Content-type', 'text/html')
#                     self.send_header('Location', '/restaurants')
#                     self.end_headers()
#
#             if self.path.endswith("/edit"):
#                 ctype, pdict = cgi.parse_header(
#                     self.headers.getheader('content-type'))
#                 if ctype == 'multipart/form-data':
#                     fields = cgi.parse_multipart(self.rfile, pdict)
#                     messagecontent = fields.get('newRestaurantName')
#                     restaurantIDPath = self.path.split("/")[2]
#
#                     myRestaurantQuery = session.query(Restaurant).filter_by(
#                         id=restaurantIDPath).one()
#                     if myRestaurantQuery != []:
#                         myRestaurantQuery.name = messagecontent[0]
#                         session.add(myRestaurantQuery)
#                         session.commit()
#                         self.send_response(301)
#                         self.send_header('Content-type', 'text/html')
#                         self.send_header('Location', '/restaurants')
#                         self.end_headers()
#
#             if self.path.endswith("/restaurants/new"):
#                 ctype, pdict = cgi.parse_header(
#                     self.headers.getheader('content-type'))
#                 if ctype == 'multipart/form-data':
#                     fields = cgi.parse_multipart(self.rfile, pdict)
#                     messagecontent = fields.get('newRestaurantName')
#
#                     # Create new Restaurant Object
#                     newRestaurant = Restaurant(name=messagecontent[0])
#                     session.add(newRestaurant)
#                     session.commit()
#
#                     self.send_response(301)
#                     self.send_header('Content-type', 'text/html')
#                     self.send_header('Location', '/restaurants')
#                     self.end_headers()
#
#         except:
#             pass
#
#
# def main():
#     try:
#         server = HTTPServer(('', 8080), webServerHandler)
#         print 'Web server running...open localhost:8080/restaurants in your browser'
#         server.serve_forever()
#     except KeyboardInterrupt:
#         print '^C received, shutting down server'
#         server.socket.close()
#
#
# if __name__ == '__main__':
#     main()
