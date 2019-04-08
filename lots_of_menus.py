#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import User, Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu_with_users.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
user = User(
    name='Robo Barista',
    email='robo@barista.com',
    picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png'
)

session.add(user)
session.commit()

user = User(
    name='Bob Ham',
    email='bob@ham.com',
    picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png'
)

session.add(user)
session.commit()

# Menu for UrbanBurger
restaurant = Restaurant(user_id=1, name="Urban Burger")

session.add(restaurant)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Veggie Burger",
    description="Juicy grilled veggie patty with tomato mayo & lettuce",
    price="$7.50",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()


menuItem = MenuItem(
    user_id=1,
    name="French Fries",
    description="With garlic & parmesan",
    price="$2.99",
    course="Appetizer",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Chicken Burger",
    description="Juicy grilled chicken patty with tomato mayo & lettuce",
    price="$5.50",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Chocolate Cake",
    description="Fresh baked & served with ice cream",
    price="$3.99",
    course="Dessert",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Sirloin Burger",
    description="Made with grade A beef",
    price="$7.99",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Root Beer",
    description="16oz of refreshing goodness",
    price="$1.99",
    course="Beverage",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Iced Tea",
    description="with Lemon",
    price="$0.99",
    course="Beverage",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Grilled Cheese Sandwich",
    description="On texas toast with American Cheese",
    price="$3.49",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Veggie Burger",
    description="Made with freshest of ingredients & home grown spices",
    price="$5.99",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()


# Menu for Super Stir Fry
restaurant = Restaurant(user_id=1, name="Super Stir Fry")

session.add(restaurant)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Chicken Stir Fry",
    description="With your choice of noodles vegetables & sauces",
    price="$7.99",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Peking Duck",
    description="A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin & little meat, sliced in front of the diners by the cook.",
    price="$25.00",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Spicy Tuna Roll",
    description="Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce.",
    price="$15.00",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Nepali Momo",
    description="Steamed dumplings made with vegetables, spices & meat. ",
    price="$12.00",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Beef Noodle Soup",
    description="A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables & Chinese noodles.",
    price="$14.00",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Ramen",
    description="A Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, & uses toppings such as sliced pork, dried seaweed, kamaboko, & green onions.",
    price="$12.00",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()


# Menu for Panda Garden
restaurant = Restaurant(user_id=1, name="Panda Garden")

session.add(restaurant)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Pho",
    description="A Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, & meat.",
    price="$8.99",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Chinese Dumplings",
    description="A common Chinese dumpling which generally consists of minced meat & finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin & elastic or thicker.",
    price="$6.99",
    course="Appetizer",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Gyoza",
    description="The most prominent differences between Japanese-style gyoza & Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt & soy sauce, & the fact that gyoza wrappers are much thinner.",
    price="$9.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Stinky Tofu",
    description="Taiwanese dish, deep fried fermented tofu served with pickled cabbage.",
    price="$6.99",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Veggie Burger",
    description="Juicy grilled veggie patty with tomato mayo & lettuce",
    price="$9.50",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()


# Menu for Thyme for That Vegetarian Cuisine
restaurant = Restaurant(user_id=1, name="Thyme for That Vegetarian Cuisine")

session.add(restaurant)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Tres Leches Cake",
    description="Rich, luscious sponge cake soaked in sweet milk & topped with vanilla bean whipped cream & strawberries.",
    price="$2.99",
    course="Dessert",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Mushroom risotto",
    description="Portabello mushrooms in a creamy risotto",
    price="$5.99",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Honey Boba Shaved Snow",
    description="Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, & freshly made mochi.",
    price="$4.50",
    course="Dessert",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Cauliflower Manchurian",
    description="Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions",
    price="$6.95",
    course="Appetizer",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Aloo Gobi Burrito",
    description="Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) & chutney. Nom Nom",
    price="$7.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Veggie Burger",
    description="Juicy grilled veggie patty with tomato mayo & lettuce",
    price="$6.80",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()


# Menu for Tony's Bistro
restaurant = Restaurant(user_id=1, name="Tony's Bistro ")

session.add(restaurant)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Shellfish Tower",
    description="Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower",
    price="$13.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Chicken & Rice",
    description="Chicken... & rice",
    price="$4.95",
    course="Entree",
    restaurant=restaurant)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Mom's Spaghetti",
    description="Spaghetti with some incredible tomato sauce made by mom",
    price="$6.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)",
    description="Milk, cream, salt, ..., Liquid nitrogen magic",
    price="$3.95",
    course="Dessert",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=1,
    name="Tonkatsu Ramen",
    description="Noodles in a delicious pork-based broth with a soft-boiled egg.",
    price="$7.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()


# Menu for Andala's
restaurant = Restaurant(user_id=2, name="Andala's")

session.add(restaurant)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Lamb Curry",
    description="Slow cook that thang in a pool of tomatoes, onions & alllll those tasty Indian spices. Mmmm.",
    price="$9.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Chicken Marsala",
    description="Chicken cooked in Marsala wine sauce with mushrooms",
    price="$7.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Potstickers",
    description="Delicious chicken & veggies encapsulated in fried dough.",
    price="$6.50",
    course="Appetizer",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Nigiri Sampler",
    description="Maguro, Sake, Hamachi, Unagi, Uni, TORO!",
    price="$6.75",
    course="Appetizer",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Veggie Burger",
    description="Juicy grilled veggie patty with tomato mayo & lettuce",
    price="$7.00",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()


# Menu for Auntie Ann's
restaurant = Restaurant(user_id=2, name="Auntie Ann\'s Diner' ")

session.add(restaurant)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Chicken Fried Steak",
    description="Fresh battered sirloin steak fried & smothered with cream gravy.",
    price="$8.99",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Boysenberry Sorbet",
    description="An unsettlingly huge amount of ripe berries turned into frozen (& seedless) awesomeness",
    price="$2.99",
    course="Dessert",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Broiled salmon",
    description="Salmon fillet marinated with fresh herbs & broiled hot & fast.",
    price="$10.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Morels on toast (seasonal)",
    description="Wild morel mushrooms fried in butter, served on herbed toast slices",
    price="$7.50",
    course="Appetizer",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Tandoori Chicken",
    description="Chicken marinated in yoghurt & seasoned with a spicy mix(chilli, tamarind among others) & slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.",
    price="$8.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Veggie Burger",
    description="Juicy grilled veggie patty with tomato mayo & lettuce",
    price="$9.50",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Spinach Ice Cream",
    description="Vanilla ice cream made with organic spinach leaves",
    price="$1.99",
    course="Dessert",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()


# Menu for Cocina Y Amor
restaurant = Restaurant(user_id=2, name="Cocina Y Amor ")

session.add(restaurant)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Super Burrito Al Pastor",
    description="Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla",
    price="$5.95",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Cachapa",
    description="Golden brown, corn-based Venezuelan pancake; usually stuffed with queso telita or queso de mano, & possibly lechon.",
    price="$7.99",
    course="Entree",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()


# Menu for State Bird Provisions
restaurant = Restaurant(user_id=2, name="State Bird Provisions")

session.add(restaurant)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Chantrelle Toast",
    description="Crispy Toast with Sesame Seeds slathered with buttery chantrelle mushrooms.",
    price="$5.95",
    course="Appetizer",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Guanciale Chawanmushi",
    description="Japanese egg custard served hot with spicey Italian Pork Jowl (guanciale).",
    price="$6.95",
    course="Dessert",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

menuItem = MenuItem(
    user_id=2,
    name="Lemon Curd Ice Cream Sandwich",
    description="Lemon Curd Ice Cream Sandwich on a chocolate macaron with cardamom meringue & cashews.",
    price="$4.25",
    course="Dessert",
    restaurant=restaurant
)

session.add(menuItem)
session.commit()

print("Added menu items!")
