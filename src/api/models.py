from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import relationship, backref
# to check the password
from werkzeug.security import safe_str_cmp
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

#------------------------------------------------------------------------------------------------------------------------------
#  USER
#------------------------------------------------------------------------------------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    birthday = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=True)
    gender = db.Column(db.String(120), nullable=True)
    occupation = db.Column(db.String(120), nullable=True)
    description = db.Column(db.String(220), nullable=True)
    avatar_url = db.Column(db.String(220), unique=False, nullable=True)
    current_room = db.Column(db.Integer) 
    temporal_current_room = db.Column(db.Integer) 
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city =  db.relationship("City", back_populates="users")
    
    tenancies = db.relationship("Tenancy", back_populates="user")
    rooms = db.relationship("Room", back_populates="user")
    reviews = db.relationship("Review", back_populates="renter")
    language = db.relationship("Language", secondary="spoken_languages")
    characteristic = db.relationship("Characteristic", secondary="characteristic_user", lazy='subquery')
    favorites = db.relationship("Favorites", back_populates="user")
    
    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "password":self.password,
            "birthday": self.birthday,
            "phone": self.phone,
            "gender": self.gender,
            "occupation": self.occupation,
            "description": self.description,
            "avatar_url": self.avatar_url,
            "city_id": self.city_id,
            "current_room": self.current_room,
            "temporal_current_room": self.temporal_current_room,
            "tenancies": list(map(lambda tenancy: tenancy.serialize(), self.tenancies)),
            "rooms": list(map(lambda room: room.serialize(), self.rooms)),
            "language": list(map(lambda language: language.serialize(), self.language)),
            "characteristic": list(map(lambda characterist: characterist.serialize(), self.characteristic)),
            "favorites": list(map(lambda favorite: favorite.serialize(), self.favorites))
        }
        
    # method to check the password and that verify that it is the user password
    def check_password(self, password_param):
       return safe_str_cmp(self.password.encode('utf-8'), password_param.encode('utf-8'))

#------------------------------------------------------------------------------------------------------------------------------
#  CITY
#------------------------------------------------------------------------------------------------------------------------------
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    lat = db.Column(db.Float(15))
    lng = db.Column(db.Float(15))
    
    country_id =  db.Column(db.Integer, db.ForeignKey('country.id'))
    country =  db.relationship("Country", back_populates="cities")
    
    users =  db.relationship("User", back_populates="city")
    
    rooms =  db.relationship("Room", back_populates="city")
    
    def __repr__(self):
        return '<City %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lng": self.lng,
            "country_id": self.country_id,
            "rooms": list(map(lambda room: room.serialize(), self.rooms))
        }

#------------------------------------------------------------------------------------------------------------------------------
#  Country
#------------------------------------------------------------------------------------------------------------------------------
class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=True)
    
    cities = db.relationship("City", back_populates="country")
    
    def __repr__(self):
        return '<Country %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "cities": list(map(lambda city: city.serialize(), self.cities))
        }

#------------------------------------------------------------------------------------------------------------------------------
#  Characteristics User: Tabla intermedia entre Usuario y caracteristicas (muchos a muchos)
#------------------------------------------------------------------------------------------------------------------------------       
class CharacteristicUser(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    characteristic_id = db.Column(db.Integer, db.ForeignKey('characteristic.id'))
    
    user = db.relationship("User", backref=backref("characteristicUser", cascade="all, delete-orphan"))
    characteristic = db.relationship("Characteristic", backref=backref("characteristicUser", cascade="all, delete-orphan"))

    
    def __repr__(self):
        return '<CharacteristicUser %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "characteristic_id": self.characteristic_id,
            "user_id": self.user_id
        }  

class Characteristic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(220))
    kind = db.Column(db.String(20)) # -->> Occupation e Interests
   
    user = db.relationship("User", secondary="characteristic_user")

    def __repr__(self):
        return '<Characteristic %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind
        } 

#------------------------------------------------------------------------------------------------------------------------------
# Languages
#------------------------------------------------------------------------------------------------------------------------------
class SpokenLanguages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))
    
    user = db.relationship("User", backref=backref("spoken_languages", cascade="all, delete-orphan"))
    language = db.relationship("Language", backref=backref("spoken_languages", cascade="all, delete-orphan"))
    
    def __repr__(self):
        return '<SpokenLanguages %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "language_id": self.language_id
        }  
 
class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    locale = db.Column(db.String(50))

    user = db.relationship("User", secondary="spoken_languages")
    
    def __repr__(self):
        return '<Language %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "locale": self.locale
        }   

#------------------------------------------------------------------------------------------------------------------------------
#  Tenancy (relation between tenant and room)
#------------------------------------------------------------------------------------------------------------------------------
class Tenancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="tenancies")

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship("Room", back_populates="tenancies")
    
    reviews = db.relationship("Review", back_populates="tenancy")
    
    def __repr__(self):
        return '<Tenancy %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            #"user_id": self.user_id,
            "room_id": self.room_id,
            "reviews": list(map(lambda review: review.serialize(), self.reviews))
        } 
        
#------------------------------------------------------------------------------------------------------------------------------
#  Review
#------------------------------------------------------------------------------------------------------------------------------
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(220))
    rating = db.Column(db.Integer)
    date = db.Column(db.Date)
    room_id=db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship("Room", back_populates="reviews")
    renter_id=db.Column(db.Integer, db.ForeignKey('user.id'))

    tenancy_id = db.Column(db.Integer, db.ForeignKey('tenancy.id'))
    tenancy = db.relationship("Tenancy", back_populates="reviews")
    renter = db.relationship("User", back_populates="reviews")

    def __repr__(self):
        return '<Review %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "rating": self.rating,
            "date": self.date,
            "tenancy_id": self.tenancy_id,
            "renter_id": self.renter_id
        }  
        
#------------------------------------------------------------------------------------------------------------------------------
#  ROOM
#------------------------------------------------------------------------------------------------------------------------------
class Room (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(8000))
    address = db.Column(db.String(220))
    country = db.Column(db.String(120))
    price = db.Column(db.Float())
    deposit = db.Column(db.Float())
    title =db.Column(db.String(120))
    type_bed = db.Column(db.String(50))
    lat = db.Column(db.Float(15))
    lng = db.Column(db.Float(15))
    room_url = db.Column(db.String(450))
    active_room = db.Column(db.Boolean, default=True)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    city =  db.relationship("City", back_populates="rooms")
    reviews = db.relationship("Review", back_populates="room")
    tenancies = db.relationship("Tenancy", back_populates="room")
    delete_room = db.Column(db.Boolean, default=False)
    temporal_renter = db.Column(db.Integer)
    current_renter = db.Column(db.Integer) 
    is_favorite = db.Column(db.Boolean, default=False)
     

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="rooms")
    room_archive = db.relationship("RoomArchive", back_populates="room")
    
    expense = db.relationship("Expense", secondary="expenses_room")
    feature = db.relationship("Feature", secondary="features_room")
    
    # Relación de 1 Room muchos Favorites
    favorites = db.relationship("Favorites", back_populates="room")
   
    
    def __repr__(self):
        return '<Room %r>' % self.title

    def serialize(self):
        current_renter_details=""
        if self.current_renter:
            current_renter_details=User.query.get(self.current_renter).serialize()
        
        return {
            "id": self.id,
            "description": self.description,
            "address": self.address,
            "country": self.country,
            "price": self.price,
            "deposit": self.deposit,
            "title": self.title, 
            "type_bed": self.type_bed,
            "lat": self.lat,
            "lng": self.lng,
            "city_id": self.city_id,
            "room_url":self.room_url,
            "owner_id": self.user_id,
            #"tenancies": list(map(lambda tenancy: tenancy.serialize(), self.tenancies)),
            "room_archive": list(map(lambda imagen: imagen.serialize(), self.room_archive)),
            "expense": list(map(lambda expen: expen.serialize(), self.expense)),
            "feature": list(map(lambda feat: feat.serialize(), self.feature)),
            "favorites": list(map(lambda favorite: favorite.serialize(), self.favorites)),
            "reviews": list(map(lambda review: review.serialize(), self.reviews)),
            "active_room":self.active_room,
            "delete_room":self.delete_room,
            "temporal_renter": self.temporal_renter,
            "current_renter": self.current_renter,
            "current_renter_details": current_renter_details,
            "is_favorite":self.is_favorite
        }
        
#------------------------------------------------------------------------------------------------------------------------------
#  Expenses ROOM
#------------------------------------------------------------------------------------------------------------------------------  
class ExpensesRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'))
    
    room = db.relationship("Room", backref=backref("expensesRoom", cascade="all, delete-orphan"))
    expense = db.relationship("Expense", backref=backref("expensesRoom", cascade="all, delete-orphan"))
    
    def __repr__(self):
        return '<ExpensesRoom %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "expense_id": self.expense_id,
            "room_id": self.room_id
        }
        
#------------------------------------------------------------------------------------------------------------------------------
#  Expense
#------------------------------------------------------------------------------------------------------------------------------  
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    
    room = db.relationship("Room", secondary="expenses_room")
    
    def __repr__(self):
        return '<Expense %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
        
#------------------------------------------------------------------------------------------------------------------------------
#  RoomArchive
#------------------------------------------------------------------------------------------------------------------------------
class RoomArchive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(250))
    
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship("Room", back_populates="room_archive")

    def __repr__(self):
        return '<RoomArchive %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "room_id": self.room_id
        }   
 
 
#------------------------------------------------------------------------------------------------------------------------------
#  Features Room
#------------------------------------------------------------------------------------------------------------------------------        
class FeaturesRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    feature_id = db.Column(db.Integer, db.ForeignKey('feature.id'))
    
    room = db.relationship("Room", backref=backref("featuresRoom", cascade="all, delete-orphan"))
    feature = db.relationship("Feature", backref=backref("featuresRoom", cascade="all, delete-orphan"))

    def __repr__(self):
        return '<FeaturesRoom %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "room_id": self.room_id,
            "feature_id": self.feature_id,
        }
  
#------------------------------------------------------------------------------------------------------------------------------
#  Feature
#------------------------------------------------------------------------------------------------------------------------------        
class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    
    room = db.relationship("Room", secondary="features_room")

    def __repr__(self):
        return '<Feature %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }  

  
#------------------------------------------------------------------------------------------------------------------------------
#  Favorites
#------------------------------------------------------------------------------------------------------------------------------        
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="favorites")
    
    # Relación de 1 Room muchos Favorites
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship("Room", back_populates="favorites")
    
    

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "room_id": self.room_id,
        }  



#------------------------------------------------------------------------------------------------------------------------------
#  SEED
#------------------------------------------------------------------------------------------------------------------------------

class SeedData:
    def __init__(self):
        self.first_user = None
        self.second_user = None
        self.third_user = None
        self.fourth_user = None
        self.fifth_user = None
        self.sixth_user = None
        self.first_city = None
        self.second_city = None
        self.third_city = None
        self.first_country = None
        self.first_room = None
        self.second_room = None
        self.third_room = None
        self.fourth_room = None
        self.fifth_room = None
        self.sixth_room = None
        self.seventh_room = None
        self.first_favorites = None # --->>> una habitación muchos favoritos
        self.second_favorites = None
        self.third_favorites = None
        self.first_tenancy = None
        self.second_tenancy = None
        self.third_tenancy = None
        self.fourth_tenancy = None
        self.first_review = None
        self.second_review = None
        self.third_review = None
        # self.first_characteristic = None
        # self.second_characteristic = None
        self.third_characteristic = None
        self.fourth_characteristic = None
        self.fifth_characteristic = None
        self.sixth_characteristic = None
        self.seventh_characteristic = None
        self.eigth_characteristic = None
        self.nineth_characteristic = None
        self.tenth_characteristic = None
        self.eleventh_characteristic = None
        self.twelfth_characteristic = None
        self.thirteenth_characteristic = None
        self.fourteenth_characteristic = None
        self.first_characteristicUser = None 
        self.second_characteristicUser = None
        self.third_characteristicUser = None 
        self.fourth_characteristicUser = None 
        self.fifth_characteristicUser = None
        self.first_language = None
        self.second_language = None
        self.third_language = None
        self.fouth_language = None
        self.fifth_language = None
        self.first_spokenLanguages = None
        self.second_spokenLanguages = None
        self.third_spokenLanguages = None
        self.fourth_spokenLanguages = None
        self.first_expense = None
        self.second_expense = None
        self.third_expense = None
        self.fourth_expense = None
        self.first_expensesRoom = None
        self.second_expensesRoom = None
        self.third_expensesRoom = None
        self.fourth_expensesRoom = None
        self.first_roomArchive = None
        self.second_roomArchive = None
        self.third_roomArchive = None
        self.fourth_roomArchive = None
        self.fifth_roomArchive = None
        self.sixth_roomArchive = None
        self.seventh_roomArchive = None
        self.eighth_roomArchive = None
        self.ninth_roomArchive = None
        self.tenth_roomArchive = None
        self.eleventh_roomArchive = None
        self.first_feature = None
        self.second_feature = None
        self.third_feature = None
        self.fourth_feature = None
        self.fifth_featuresRoom = None
        self.sixth_featuresRoom = None
        self.first_featuresRoom = None
        self.second_featuresRoom = None
        self.third_featuresRoom = None
        self.fourth_featuresRoom = None 
        
    
#------------------------
#  Country
#------------------------
    def create_seed_country(self):
        self.first_country = Country(
            name = "Spain"
        )
        
        db.session.add(self.first_country)
        db.session.commit()  
          
#------------------------
#  City
#------------------------    
    def create_seed_city(self):
        self.first_city = City(
            name = "Madrid",
            lat = 40.42297365084645, 
            lng = -3.707010830149073,
            country_id = self.first_country.id
        )
        
        self.second_city = City(
            name = "Barcelona",
            lat = 41.406295930261635, 
            lng = 2.1748621412984614,
            country_id = self.first_country.id
        )
        
        self.third_city = City(
            name = "Málaga",
            lat = 36.726732295907595, 
            lng = -4.422490437718872,
            country_id = self.first_country.id
        )
        
        db.session.add(self.first_city)
        db.session.add(self.second_city)
        db.session.add(self.third_city)
        db.session.commit()
        
#------------------------
#  User
#------------------------
    def create_seed_user(self):
        self.first_user = User( 
            name = "Adan",
            last_name = "Sánchez Romero",
            email = "adan_user@gmail.com",
            password = "1111",
            birthday = "01/01/1980",
            phone = "666362969",
            gender = "male",
            description = "Sportsman, adventurer and super sociable boy.I love meeting people and visiting new places",
            avatar_url = "https://d1bvpoagx8hqbg.cloudfront.net/259/b59e40d45c7460cb65467d2000705086.jpg",
            city_id = self.first_city.id,
            current_room = None,
            temporal_current_room= None
            
        ) 

        self.second_user = User( 
            email = "eva_user@gmail.com",
            name = "Eva",
            last_name = "Genesis",
            password = "1111",
            birthday = "01/01/1982",
            phone = "666362970",
            gender = "female",
            description = "I am a sociable girl, I love to dance and read",
            avatar_url = "https://img.europapress.es/fotoweb/fotonoticia_20200907131946_420.jpg",
            city_id = self.first_city.id,
            current_room = None,
            temporal_current_room= None
            
        )

        self.third_user = User( 
            email = "sara_user@gmail.com",
            name = "Sara",
            last_name = "Santiago Rojas",
            password = "1111",
            birthday = "01/01/1985",
            phone = "666362978",
            gender = "female",
            description = "I am super chefs, I love animals and swimming",
            avatar_url = "https://img.europapress.es/fotoweb/fotonoticia_20180118120033_420.jpg",
            city_id = self.first_city.id,
            current_room = None,
            temporal_current_room= None
        )

        self.fourth_user = User( 
            email = "abraham_user@gmail.com",
            name = "Abraham",
            last_name = "Browm",
            password = "1111",
            birthday = "01/01/1990",
            phone = "666362980",
            gender = "male",
            description =  "I love food, nice people and good music",
            avatar_url = "https://media.istockphoto.com/photos/portrait-of-young-man-in-yellow-tshirt-at-backyard-picture-id1180616281?k=20&m=1180616281&s=612x612&w=0&h=ZChvYgG8WCJ1M73lGE8oSyp0TMzWJxS3xRNw7uFwO6w=",
            city_id = self.second_city.id,
            current_room = None,
            temporal_current_room= None
        )

        self.fifth_user = User( 
            email = "noe_user@gmail.com",
            name = "Noé",
            last_name = "Herrera Muñoz",
            password = "1111",
            birthday = "01/01/1992",
            phone = "666362986",
            gender = "male",
            description = "I am a quiet guy. I like to stay at home reading or watching a good good movie.",
            avatar_url = "https://media.istockphoto.com/photos/portrait-of-a-smiling-student-at-the-city-street-picture-id1147289240?k=20&m=1147289240&s=612x612&w=0&h=sEx-9oXUdDRMqZF0o1viaumUjAud3Lsr9QxWAqrW3ks=",
            city_id = self.third_city.id,
            current_room = None,
            temporal_current_room= None
        )
        
        self.sixth_user = User( 
            email = "joe_user@gmail.com",
            name = "Joe",
            last_name = "Becker",
            password = "1111",
            birthday = "01/09/1993",
            phone = "666362986",
            gender = "male",
            description = "I am a quiet guy. I like to stay at home reading or watching a good good movie.",
            avatar_url = "https://los40es00.epimg.net/los40/imagenes/2017/08/31/tecnologia/1504205368_960402_1504205490_noticia_normal.jpg",
            city_id = self.third_city.id,
            current_room = None,
            temporal_current_room= None
        )
    
        db.session.add(self.first_user)
        db.session.add(self.second_user)
        db.session.add(self.third_user)
        db.session.add(self.fourth_user)
        db.session.add(self.fifth_user)
        db.session.add(self.sixth_user)
        db.session.commit()
   
#------------------------
#  Room
#------------------------
    def create_seed_room(self):
        self.first_room = Room( 
            description = "A premium large double room has become available in our very sought Boutique House share. 5 min walk from Forest Gate Station and 5-10min train journey to Westfield Shopping Centre + the Olympic Park! This premium space large double room is filled with luxury including a large wardrobe, chest of drawers, bedside table, a large desk and many more. This room also includes private garden access directly from the room and lets in a lot of natural light. The house includes a beautifully renovated open space kitchen lounge and many facilities. All tenants are warm and friendly professionals Local amenities: - Cafe's, shops, pubs - Huge range of parks - Westfield Shopping Centre: 3 min train journey (Including all types of shops from supermarkets to renowned luxury fashion brands and amazing restaurants). + Easy connections to Central London areas. * VERY generously sized premium double room * Professional House share * Washing machine * Large fridge with plenty of space * Large jacuzzi bath * 2 Bathrooms Rent will include: * Council Tax * Fortnightly cleaner * Electricity bill * Gas bill * Water rates * Super-fast broadband The professionals in the house will be looking for a tidy, sociable person to join their new home, and we are looking for someone who will pay their rent on time and treat the house as their home :) This is a friendly, respectful and tidy home for professionals to relax and enjoy. We take pride in serving our tenants and strive to be responsive to any needs that arise in our properties. Contact us for testimonials.",
            address = "Bastero 6",
            country = "Spain",
            price = 450,
            deposit = 450,
            title = "Exquisite Large Double Room in Prime Location",
            type_bed = "single",
            lat = 33.4329,
            lng = -4.642371,
            city_id = self.first_city.id,
            user_id = self.first_user.id,
            room_url = "https://media.revistaad.es/photos/60c2294bb4a53607d5b4669f/4:3/w_1568,h_1176,c_limit/231620.jpg",
            active_room = True,
            temporal_renter = self.sixth_user.id,
            current_renter = None
        )

        self.second_room = Room( 
            description = "I have very nice and clean double room for rent in 3 bed room sharing house at bilton road Perivale .This house is only 5 minutes away from Perivale tube station and Alperton is well.Supermarket Sainsbury and Tesco are 5 to 7 minute walking distance.A big shop londis and 297 bus stop are about 2 minutes walking distance from home. All bills are including with free WiFi No deposit required For single lady",
            address = "Bastero 26",
            country = "Spain",
            price = 400,
            deposit = 400,
            title = "Moder and Unique Room",
            type_bed = "single",
            lat = 36.4329,
            lng = -4.642371,
            city_id = self.first_city.id,
            user_id = self.second_user.id,
            room_url = "https://i.pinimg.com/originals/a2/04/d3/a204d395e71329a6769d097575490b7a.jpg",
            active_room = True,
            temporal_renter = None,
            current_renter = None
        )

        self.third_room = Room( 
            description = "This house has 5 bedrooms, 1 toilet and 1 washroom,1 Kitchen 1 quite and clean male tenant is currently living JUST 2 WEEKS OF DEPOSITS ROOM RENT : 550PCM Walthamstow Amazing Double room at Zone 3, E17 9QG Amenities: ✔ 💡Electric Bill ✔ 💧Water Bill ✔ 🌐High Speed Internet/Wifi ✔ 🛠️Repairs ✔ Council Tax Included ✔ *All bills included Advantages of these Rooms: ✔ 🚅Tubes (24/7) ✔ 🚌Bus Stations (24/7) ✔ 🍽️Restaurants/🥂Pub ✔ 📒Universities ✔ ⚕️Hospital/Pharmacy ✔ 💱Banks ✔ 🛍️Shops/Markets ✔ 🏞️Parks ✔ 🏞️Main Road/Street ** REFERENCES ARE REQUIRED** To arrange a viewing, please send me a message specifying your best date of move in and phone number",
            address = "Castellán 8",
            country = "Spain",
            price = 500,
            deposit = 500,
            title = "Amazing Double Room",
            type_bed ="doubleBed",
            lat = 23.4329,
            lng = -4.642371,
            city_id = self.first_city.id,
            user_id = self.third_user.id,
            room_url = "https://casaydiseno.com/wp-content/uploads/2016/08/dormitorios-con-encanto-decoracion-pequeno-comodo.jpg",
            active_room = True,
            temporal_renter = None,
            current_renter = None
        )

        self.fourth_room = Room( 
            description = "Big bright room to rent, must be paid on time all bills included no smokers and drinking must be done outdoors i expect the noise levels down after 10 and i do not accept guests coming over every day lastly i expect you to clean after yourself since i live here too i will get curtains and a wardrobe before you move in.The cloud above the bed can be removed if you would like i can provide bedsheets pillows and blankets which are new but if you would like to bring your own thats fine too the shower water pressure isnt the greatest but thats about it if you need anything or have any questions let me know the walls and ceiling are freshly painted and everything is bleached down",
            address= "Bastero 6",
            country = "Spain",
            price = 500,
            deposit = 500,
            title = "Lovely Clean Room",
            type_bed = "doubleBed",
            lat = 33.4329,
            lng = -4.642371,
            city_id = self.first_city.id,
            user_id = self.first_user.id,
            room_url = "https://i.pinimg.com/originals/5e/52/d4/5e52d4a5b28b76cbc6a73b5b0f43f42d.jpg",
            active_room = True,
            temporal_renter = None,
            current_renter = None
        )
        
        self.fifth_room = Room( 
            description = "Charming Double Bedroom available in this well kept house from the second week of August. The house consists of two full bathrooms, 5 flatmates and a spacious open plan kitchen with a private garden. The house is located on a residential, quiet road with super easy access to Gipsy Hill station (3 mins walk). We consider single professionals or students with UK based guarantors. Get in touch in order to get some more details.",
            address= "Avenida del Aeropuerto 10",
            country = "Spain",
            price = 300,
            deposit = 100,
            title = "Beautiful Room",
            type_bed = "doubleBed",
            lat = 33.4329,
            lng = -4.642371,
            city_id = self.second_city.id,
            user_id = self.fourth_user.id,
            room_url = "https://www.hola.com/imagenes/decoracion/20200220161121/iluminacion-habitaciones-juveniles/0-786-452/luz-teens-6a-a.jpg",
            active_room = True,
            temporal_renter = None,
            current_renter = None
        )
        
        self.sixth_room = Room( 
            description = "Friendly atmosphere. Is not just a house is a home! Come and ser for yourself, you’ll love it. Very closely to trains stations and big Tesco, Sainsbury’s and Lidl!!",
            address= "Avenida del Aeropuerto 10",
            country = "Spain",
            price = 500,
            deposit = 500,
            title = "Charming room",
            type_bed = "doubleBed",
            lat = 33.4329,
            lng = -4.642371,
            city_id = self.second_city.id,
            user_id = self.fourth_user.id,
            room_url = "https://www.elmueble.com/medio/2019/12/18/00501615_ec7cc8db_1000x750.jpg",
            active_room = True,
            temporal_renter = None,
            current_renter = None 
        )
        
        self.seventh_room = Room( 
            description = "Super spacious double room to rent in Avenida del Aeropuerto 10. We are looking for a quiet, tidy and friendly people to share the flat. Flat with separate toilet and bathroom and cozy kitchen. Couples 500€",
            address= "Avenida del Aeropuerto 10",
            country = "Spain",
            price = 500,
            deposit = 500,
            title = "Spacious and Beautiful Room in Málaga",
            type_bed = "doubleBed",
            lat = 33.4329,
            lng = -4.642371,
            city_id = self.third_city.id,
            user_id = self.fifth_user.id,
            room_url = "https://i.pinimg.com/736x/72/1a/8c/721a8c00c5e682403d13aa15d2168c79.jpg",
            active_room = True,
            temporal_renter = None,
            current_renter = None
        )

        db.session.add(self.first_room)
        db.session.add(self.second_room)
        db.session.add(self.third_room)
        db.session.add(self.fourth_room)
        db.session.add(self.fifth_room)
        db.session.add(self.sixth_room)
        db.session.add(self.seventh_room)
        db.session.commit()
        
#------------------------
#  Favorites
#------------------------
    # def create_seed_favorites(self):
    #     self.first_favorites = Favorites(
    #         room_id = self.first_room.id,
    #         user_id = self.second_user.id
    #     )
        
    #     self.second_favorites = Favorites(
    #         room_id = self.second_room.id,
    #         user_id = self.second_user.id
    #     )
        
    #     self.third_favorites = Favorites(
    #         room_id = self.third_room.id,
    #         user_id = self.second_user.id
    #     )
        
    #     db.session.add(self.first_favorites)
    #     db.session.add(self.second_favorites)
    #     db.session.add(self.third_favorites)
    #     db.session.commit() 

#------------------------
#  Tenancy (La relación entre inquilino y habitación)
#------------------------
    def create_seed_tenancy(self):
        self.first_tenancy = Tenancy(
           # user_id = self.second_user.id,
            room_id = self.first_room.id
        )
        
        self.second_tenancy = Tenancy(
            #user_id = self.third_user.id,
            room_id = self.first_room.id
        )
        
        self.third_tenancy = Tenancy(
            #user_id = self.fourth_user.id,
            room_id = self.first_room.id
        )
        
        self.fourth_tenancy = Tenancy(
           # user_id = self.fourth_user.id,
            room_id = self.second_room.id
        )
        
        db.session.add(self.first_tenancy)
        db.session.add(self.second_tenancy)
        db.session.add(self.third_tenancy)
        db.session.add(self.fourth_tenancy)
        db.session.commit()

#------------------------
#  Review
#------------------------
    def create_seed_review(self):
        self.first_review = Review( 
            comment = "The neighborhood is great, it is well connected by public transport, the metro is 5 minutes away and there are many nice areas to hang out.",
            rating = 4,
            date = "01/01/2021",
            tenancy_id = self.first_tenancy.id,
            room_id = self.first_room.id,
            renter_id = self.second_user.id
        )

        self.second_review = Review( 
            comment = "The area of the flat has a lot of night life. It is amazing!",
            rating = 5,
            date = "02/05/2021",
            tenancy_id = self.second_tenancy.id,
            room_id = self.first_room.id,
            renter_id = self.third_user.id
        )

        self.third_review = Review( 
            comment = "The area has many vegan and garden produce stores. I loved that !!",
            rating = 3,
            date = "01/06/2021",
            tenancy_id = self.third_tenancy.id,
            room_id = self.first_room.id,
            renter_id = self.fourth_user.id,
        )

        db.session.add(self.first_review)
        db.session.add(self.second_review)
        db.session.add(self.third_review)
        db.session.commit()
        
#------------------------
#  Characteristic
#------------------------
    def create_seed_characteristic(self):
            # self.first_characteristic = Characteristic(
            #     name = "worker",
            #     kind = "occupation"
            # )
            # self.second_characteristic = Characteristic(
            #     name = "student",
            #     kind = "occupation"
            # )
            self.third_characteristic = Characteristic(
                name = "Sporty",
                kind = "interest"
            )
            self.fourth_characteristic = Characteristic(
                name = "Dancer",
                kind = "interest"
            )
            self.fifth_characteristic = Characteristic(
                name = "Vegan",
                kind = "interest"
            )
            self.sixth_characteristic = Characteristic(
                name = "Sociable",
                kind = "interest"
            )
            self.seventh_characteristic = Characteristic(
                name = "Musician",
                kind = "interest"
            )
            self.eigth_characteristic = Characteristic(
                name = "Reader",
                kind = "interest"
            )
            self.nineth_characteristic = Characteristic(
                name = "Vegetarian",
                kind = "interest"
            )
            self.tenth_characteristic = Characteristic(
                name = "Animal Lover",
                kind = "interest"
            )
            self.eleventh_characteristic = Characteristic(
                name = "Movies",
                kind = "interest"
            )
            self.twelfth_characteristic = Characteristic(
                name = "Traveler",
                kind = "interest"
            )
            self.thirteenth_characteristic = Characteristic(
                name = "Partying",
                kind = "interest"
            )
            self.fourteenth_characteristic = Characteristic(
                name = "Gay Friendly",
                kind = "interest"
            )
            
            # db.session.add(self.first_characteristic)
            # db.session.add(self.second_characteristic)
            db.session.add(self.third_characteristic)
            db.session.add(self.fourth_characteristic)
            db.session.add(self.fifth_characteristic)
            db.session.add(self.sixth_characteristic)
            db.session.add(self.seventh_characteristic)
            db.session.add(self.eigth_characteristic)
            db.session.add(self.nineth_characteristic)
            db.session.add(self.tenth_characteristic)
            db.session.add(self.eleventh_characteristic)
            db.session.add(self.twelfth_characteristic)
            db.session.add(self.thirteenth_characteristic)
            db.session.add(self.fourteenth_characteristic)
            db.session.commit()  

#------------------------
#  characteristicUser
#------------------------
    def create_seed_characteristicUser(self):
        self.first_characteristicUser = CharacteristicUser(
            user_id = self.first_user.id,
            characteristic_id = self.sixth_characteristic.id
        )
        self.second_characteristicUser = CharacteristicUser(
            user_id = self.second_user.id,
            characteristic_id = self.seventh_characteristic.id
        )
        self.third_characteristicUser = CharacteristicUser(
            user_id = self.first_user.id,
            characteristic_id = self.third_characteristic.id
        )
        self.fourth_characteristicUser = CharacteristicUser(
            user_id = self.first_user.id,
            characteristic_id = self.fourth_characteristic.id
        )
        self.fifth_characteristicUser = CharacteristicUser(
            user_id = self.second_user.id,
            characteristic_id = self.fifth_characteristic.id
        )
        
        db.session.add(self.first_characteristicUser)
        db.session.add(self.second_characteristicUser)
        db.session.add(self.third_characteristicUser)
        db.session.add(self.fourth_characteristicUser)
        db.session.add(self.fifth_characteristicUser)
        db.session.commit() 

#------------------------
#  Language
#------------------------
    def create_seed_language(self):
        self.first_language = Language(
            name = "Spanish",
            locale = "es"
        )
        self.second_language = Language(
            name = "English",
            locale = "en"
        )
        self.third_language = Language(
            name = "French",
            locale = "fr"
        )
        self.fouth_language = Language(
            name = "Portuguese",
            locale = "pt"
        )
        self.fifth_language = Language(
            name = "German",
            locale = "ge"
        )
        
        db.session.add(self.first_language)
        db.session.add(self.second_language)
        db.session.add(self.third_language)
        db.session.add(self.fouth_language)
        db.session.add(self.fifth_language)
        db.session.commit() 

#------------------------
#  SpokenLanguages 
#------------------------
    def create_seed_spokenLanguages(self):
        self.first_spokenLanguages = SpokenLanguages(
            user_id = self.first_user.id,
            language_id = self.first_language.id
        )
        self.second_spokenLanguages = SpokenLanguages(
            user_id = self.first_user.id,
            language_id = self.second_language.id
        )
        self.third_spokenLanguages = SpokenLanguages(
            user_id = self.second_user.id,
            language_id = self.second_language.id
        )
        self.fourth_spokenLanguages = SpokenLanguages(
            user_id = self.third_user.id,
            language_id = self.third_language.id
        )
        
        db.session.add(self.first_spokenLanguages)
        db.session.add(self.second_spokenLanguages)
        db.session.add(self.third_spokenLanguages)
        db.session.add(self.fourth_spokenLanguages)
        db.session.commit()  

#------------------------
#  Expense
#------------------------
    def create_seed_expense(self):
        self.first_expense = Expense(
            name = "wifi"
        )
        self.second_expense = Expense(
            name = "light"
        )
        self.third_expense = Expense(
            name = "Water"
        )
        self.fourth_expense = Expense(
            name = "gas"
        )
        
        db.session.add(self.first_expense)
        db.session.add(self.second_expense)
        db.session.add(self.third_expense)
        db.session.add(self.fourth_expense)
        db.session.commit()

#------------------------
#  Expenses ROOM
#------------------------
    def create_seed_expensesRoom(self):
        self.first_expensesRoom = ExpensesRoom(
            room_id = self.first_room.id,
            expense_id = self.first_expense.id
        )
        self.second_expensesRoom = ExpensesRoom(
            room_id = self.first_room.id,
            expense_id = self.second_expense.id
        )
        self.third_expensesRoom = ExpensesRoom(
            room_id = self.first_room.id,
            expense_id = self.third_expense.id
        )
        self.fourth_expensesRoom = ExpensesRoom(
            room_id = self.first_room.id,
            expense_id = self.fourth_expense.id
        )
        
        db.session.add(self.first_expensesRoom)
        db.session.add(self.second_expensesRoom)
        db.session.add(self.third_expensesRoom)
        db.session.add(self.fourth_expensesRoom)
        db.session.commit()  
        
#------------------------
#  RoomArchive
#------------------------
    def create_seed_roomArchive(self):
        self.first_roomArchive = RoomArchive(
            url = "https://www.elmueble.com/medio/2021/02/17/00528735_045f0680_1500x2000.jpg",
            room_id = self.first_room.id
        )
        self.second_roomArchive = RoomArchive(
            url = "https://www.milideas.net/wp-content/uploads/ba%C3%B1o-peque%C3%B1o-moderno-bonito-22.jpg",
            room_id = self.first_room.id
        )
        self.third_roomArchive = RoomArchive(
            url = "https://www.elmueble.com/medio/2020/10/14/00449673_eaa6ff1e_600x600.jpg",
            room_id = self.first_room.id
        )
        self.fourth_roomArchive = RoomArchive(
            url = "https://tucasabonita.es/wp-content/uploads/2018/04/ideas-decorar-dormitorios-juveniles-modernos-chicas-29.jpg",
            room_id = self.second_room.id
        )
        self.fifth_roomArchive = RoomArchive(
            url = "https://casaydiseno.com/wp-content/uploads/2016/08/dormitorios-con-encanto-decoracion-pequeno-comodo.jpg",
            room_id = self.third_room.id
        )
        self.sixth_roomArchive = RoomArchive(
            url = "https://decoraideas.com/wp-content/uploads/2018/12/10_guetzli-2-768x768.jpg",
            room_id = self.fourth_room.id
        )
        self.seventh_roomArchive = RoomArchive(
            url = "https://2.bp.blogspot.com/-4OV19xVw0pw/WMa0mk2B3hI/AAAAAAAAevw/gCnN8PtgwLYj-zQh07bz94pOlAdFn0xYgCEw/s1600/ban%25CC%2583o%2Bestrecho.jpg",
            room_id = self.third_room.id
        )
        self.eighth_roomArchive = RoomArchive(
            url = "https://i.pinimg.com/originals/28/b2/a7/28b2a7bcda63e8fc1eb65631057c699a.jpg",
            room_id = self.second_room.id
        )
        
        self.ninth_roomArchive = RoomArchive(
            url = "https://www.hola.com/imagenes/decoracion/20200220161121/iluminacion-habitaciones-juveniles/0-786-452/luz-teens-6a-a.jpg",
            room_id = self.fifth_room.id
        )
        self.tenth_roomArchive = RoomArchive(
            url = "https://cafeversatil.com/nuestroshijos/wp-content/uploads/2019/11/01-2-768x576.jpg",
            room_id = self.sixth_room.id
        )
        self.eleventh_roomArchive = RoomArchive(
            url = "https://www.elmueble.com/medio/2017/12/11/00438564_o_c70b69b2_1335x2000.jpg",
            room_id = self.seventh_room.id
        )
        
        db.session.add(self.first_roomArchive)
        db.session.add(self.second_roomArchive)
        db.session.add(self.third_roomArchive)
        db.session.add(self.fourth_roomArchive)
        db.session.add(self.fifth_roomArchive)
        db.session.add(self.sixth_roomArchive)
        db.session.add(self.seventh_roomArchive)
        db.session.add(self.eighth_roomArchive)
        db.session.add(self.ninth_roomArchive)
        db.session.add(self.tenth_roomArchive)
        db.session.add(self.eleventh_roomArchive)
        db.session.commit() 
        
#------------------------
#  Feature
#------------------------
    def create_seed_feature(self):
        self.first_feature = Feature(
            name = "facing the street"
        )
        self.second_feature = Feature(
            name = "furnished room"
        )
        self.third_feature = Feature(
            name = "suite room"
        )
        self.fourth_feature = Feature(
            name = "shared room"
        )

        db.session.add(self.first_feature)
        db.session.add(self.second_feature)
        db.session.add(self.third_feature)
        db.session.add(self.fourth_feature)
        db.session.commit()  

#------------------------
#  FeaturesRoom
#------------------------
    def create_seed_featuresRoom(self):
        self.first_featuresRoom = FeaturesRoom(
            room_id = self.first_room.id,
            feature_id = self.first_feature.id
        )
        self.second_featuresRoom = FeaturesRoom(
            room_id = self.second_room.id,
            feature_id = self.second_feature.id
        )
        self.third_featuresRoom = FeaturesRoom(
            room_id = self.third_room.id,
            feature_id = self.third_feature.id
        )
        self.fourth_featuresRoom = FeaturesRoom(
            room_id = self.fourth_room.id,
            feature_id = self.fourth_feature.id
        )
        
        self.fifth_featuresRoom = FeaturesRoom(
            room_id = self.first_room.id,
            feature_id = self.third_feature.id
        )
        
        self.sixth_featuresRoom = FeaturesRoom(
            room_id = self.sixth_room.id,
            feature_id = self.third_feature.id
        )

        db.session.add(self.first_featuresRoom)
        db.session.add(self.second_featuresRoom)
        db.session.add(self.third_featuresRoom)
        db.session.add(self.fourth_featuresRoom)
        db.session.add(self.fifth_featuresRoom)
        db.session.add(self.sixth_featuresRoom)
        db.session.commit()          
                                          
       
    def create_seed_data(self):
        self.create_seed_country()
        self.create_seed_city()
        self.create_seed_user()
        self.create_seed_room()
        # self.create_seed_favorites() # ---->>> 1 habitación muchos favoritos
        self.create_seed_tenancy()
        self.create_seed_review()
        self.create_seed_characteristic()
        self.create_seed_characteristicUser()
        self.create_seed_language()
        self.create_seed_spokenLanguages()
        self.create_seed_expense()
        self.create_seed_expensesRoom()
        self.create_seed_roomArchive()
        self.create_seed_feature()
        self.create_seed_featuresRoom()
