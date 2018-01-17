from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CItem

engine = create_engine('sqlite:///catalog.db')
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


# Menu for UrbanBurger
catalog1 = Catalog(name="Urban Burger")

session.add(catalog1)
session.commit()

cItem2 = CItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     catalog=catalog1)

session.add(cItem2)
session.commit()


cItem1 = CItem(name="French Fries", description="with garlic and parmesan",
                     catalog=catalog1)

session.add(cItem1)
session.commit()

cItem2 = CItem(name="Chicken Burger", description="Juicy grilled chicken patty with tomato mayo and lettuce",
                     catalog=catalog1)

session.add(cItem2)
session.commit()

cItem3 = CItem(name="Chocolate Cake", description="fresh baked and served with ice cream",
                     catalog=catalog1)

session.add(cItem3)
session.commit()

cItem4 = CItem(name="Sirloin Burger", description="Made with grade A beef",
                     catalog=catalog1)

session.add(cItem4)
session.commit()

cItem5 = CItem(name="Root Beer", description="16oz of refreshing goodness",
                     catalog=catalog1)

session.add(cItem5)
session.commit()

cItem6 = CItem(name="Iced Tea", description="with Lemon",
                     catalog=catalog1)

session.add(cItem6)
session.commit()

cItem7 = CItem(name="Grilled Cheese Sandwich", description="On texas toast with American Cheese",
                     catalog=catalog1)

session.add(cItem7)
session.commit()

cItem8 = CItem(name="Veggie Burger", description="Made with freshest of ingredients and home grown spices",
                     catalog=catalog1)

session.add(cItem8)
session.commit()


# Menu for Super Stir Fry
catalog2 = Catalog(name="Super Stir Fry")

session.add(catalog2)
session.commit()


cItem1 = CItem(name="Chicken Stir Fry", description="With your choice of noodles vegetables and sauces",
                     catalog=catalog2)

session.add(cItem1)
session.commit()

cItem2 = CItem(
    name="Peking Duck", description=" A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", catalog=catalog2)

session.add(cItem2)
session.commit()

cItem3 = CItem(name="Spicy Tuna Roll", description="Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ",
                     catalog=catalog2)

session.add(cItem3)
session.commit()

cItem4 = CItem(name="Nepali Momo ", description="Steamed dumplings made with vegetables, spices and meat. ",
                     catalog=catalog2)

session.add(cItem4)
session.commit()

cItem5 = CItem(name="Beef Noodle Soup", description="A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.",
                     catalog=catalog2)

session.add(cItem5)
session.commit()

cItem6 = CItem(name="Ramen", description="a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.",
                     catalog=catalog2)

session.add(cItem6)
session.commit()


# Menu for Panda Garden
catalog1 = Catalog(name="Panda Garden")

session.add(catalog1)
session.commit()


cItem1 = CItem(name="Pho", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.",
                     catalog=catalog1)

session.add(cItem1)
session.commit()

cItem2 = CItem(name="Chinese Dumplings", description="a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.",
                     catalog=catalog1)

session.add(cItem2)
session.commit()

cItem3 = CItem(name="Gyoza", description="The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner",
                     catalog=catalog1)

session.add(cItem3)
session.commit()

cItem4 = CItem(name="Stinky Tofu", description="Taiwanese dish, deep fried fermented tofu served with pickled cabbage.",
                     catalog=catalog1)

session.add(cItem4)
session.commit()

cItem2 = CItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     catalog=catalog1)

session.add(cItem2)
session.commit()


# Menu for Thyme for that
catalog1 = Catalog(name="Thyme for That Vegetarian Cuisine ")

session.add(catalog1)
session.commit()


cItem1 = CItem(name="Tres Leches Cake", description="Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.",
                     catalog=catalog1)

session.add(cItem1)
session.commit()

cItem2 = CItem(name="Mushroom risotto", description="Portabello mushrooms in a creamy risotto",
                     catalog=catalog1)

session.add(cItem2)
session.commit()

cItem3 = CItem(name="Honey Boba Shaved Snow", description="Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi",
                     catalog=catalog1)

session.add(cItem3)
session.commit()

cItem4 = CItem(name="Cauliflower Manchurian", description="Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions",
                     catalog=catalog1)

session.add(cItem4)
session.commit()

cItem5 = CItem(name="Aloo Gobi Burrito", description="Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom",
                     catalog=catalog1)

session.add(cItem5)
session.commit()

cItem2 = CItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     catalog=catalog1)

session.add(cItem2)
session.commit()


# Menu for Tony's Bistro
catalog1 = Catalog(name="Tony\'s Bistro ")

session.add(catalog1)
session.commit()


cItem1 = CItem(name="Shellfish Tower", description="Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower",
                     catalog=catalog1)

session.add(cItem1)
session.commit()

cItem2 = CItem(name="Chicken and Rice", description="Chicken... and rice",
                     catalog=catalog1)

session.add(cItem2)
session.commit()

cItem3 = CItem(name="Mom's Spaghetti", description="Spaghetti with some incredible tomato sauce made by mom",
                     catalog=catalog1)

session.add(cItem3)
session.commit()

cItem4 = CItem(name="Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)",
                     description="Milk, cream, salt, ..., Liquid nitrogen magic", catalog=catalog1)

session.add(cItem4)
session.commit()

cItem5 = CItem(name="Tonkatsu Ramen", description="Noodles in a delicious pork-based broth with a soft-boiled egg",
                     catalog=catalog1)

session.add(cItem5)
session.commit()


# Menu for Andala's
catalog1 = Catalog(name="Andala\'s")

session.add(catalog1)
session.commit()


cItem1 = CItem(name="Lamb Curry", description="Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.",
                     catalog=catalog1)

session.add(cItem1)
session.commit()

cItem2 = CItem(name="Chicken Marsala", description="Chicken cooked in Marsala wine sauce with mushrooms",
                     catalog=catalog1)

session.add(cItem2)
session.commit()

cItem3 = CItem(name="Potstickers", description="Delicious chicken and veggies encapsulated in fried dough.",
                     catalog=catalog1)

session.add(cItem3)
session.commit()

cItem4 = CItem(name="Nigiri Sampler", description="Maguro, Sake, Hamachi, Unagi, Uni, TORO!",
                     catalog=catalog1)

session.add(cItem4)
session.commit()

cItem2 = CItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     catalog=catalog1)

session.add(cItem2)
session.commit()


# Menu for Auntie Ann's
catalog1 = Catalog(name="Auntie Ann\'s Diner ")

session.add(catalog1)
session.commit()

cItem9 = CItem(name="Chicken Fried Steak", description="Fresh battered sirloin steak fried and smothered with cream gravy",
                     catalog=catalog1)

session.add(cItem9)
session.commit()


cItem1 = CItem(name="Boysenberry Sorbet", description="An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness",
                     catalog=catalog1)

session.add(cItem1)
session.commit()

cItem2 = CItem(name="Broiled salmon", description="Salmon fillet marinated with fresh herbs and broiled hot & fast",
                     catalog=catalog1)

session.add(cItem2)
session.commit()

cItem3 = CItem(name="Morels on toast (seasonal)", description="Wild morel mushrooms fried in butter, served on herbed toast slices",
                     catalog=catalog1)

session.add(cItem3)
session.commit()

cItem4 = CItem(name="Tandoori Chicken", description="Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.",
                     catalog=catalog1)

session.add(cItem4)
session.commit()

cItem2 = CItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     catalog=catalog1)

session.add(cItem2)
session.commit()

cItem10 = CItem(name="Spinach Ice Cream", description="vanilla ice cream made with organic spinach leaves",
                      catalog=catalog1)

session.add(cItem10)
session.commit()


# Menu for Cocina Y Amor
catalog1 = Catalog(name="Cocina Y Amor ")

session.add(catalog1)
session.commit()


cItem1 = CItem(name="Super Burrito Al Pastor", description="Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla",
                     catalog=catalog1)

session.add(cItem1)
session.commit()

cItem2 = CItem(name="Cachapa", description="Golden brown, corn-based Venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ",
                     catalog=catalog1)

session.add(cItem2)
session.commit()


catalog1 = Catalog(name="State Bird Provisions")
session.add(catalog1)
session.commit()

cItem1 = CItem(name="Chantrelle Toast", description="Crispy Toast with Sesame Seeds slathered with buttery chantrelle mushrooms",
                     catalog=catalog1)

session.add(cItem1)
session.commit()

cItem1 = CItem(name="Guanciale Chawanmushi", description="Japanese egg custard served hot with spicey Italian Pork Jowl (guanciale)",
                     catalog=catalog1)

session.add(cItem1)
session.commit()


cItem1 = CItem(name="Lemon Curd Ice Cream Sandwich", description="Lemon Curd Ice Cream Sandwich on a chocolate macaron with cardamom meringue and cashews",
                     catalog=catalog1)

session.add(cItem1)
session.commit()

print "added menu items!"
