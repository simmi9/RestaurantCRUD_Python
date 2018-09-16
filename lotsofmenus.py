from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
#	Creating rows
#myFirstRestaurant = Restaurant(name = "Pizza Palace")
#session.add(myFirstRestaurant)
#session.commit()

#cheesepizza = MenuItem(name="Cheese Pizza",
#	description = "Made with all natural ingredients and fresh mozzarella",
#	course="Entree", price="$8.99", restaurant=myFirstRestaurant)
#session.add(cheesepizza)
#session.commit()

#Reading results 
firstResult = session.query(Restaurant).first()
firstResult.name
print firstResult.name

#items = session.query(MenuItem).all()
#for item in items:
#    print item.name


#read and update

veggieBurgers = session.query(MenuItem).filter_by(name= 'Veggie Burger')
for veggieBurger in veggieBurgers:
    print veggieBurger.id
    print veggieBurger.price
    print veggieBurger.restaurant.name
    print "\n"

UrbanVeggieBurger = session.query(MenuItem).filter_by(id=3).one()
UrbanVeggieBurger.price = '$2.99'
session.add(UrbanVeggieBurger)
session.commit()     