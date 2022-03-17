from app import db, login
from flask_login import UserMixin 
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

class Cart(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), primary_key=True)
    

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default = dt.utcnow)
    admin = db.Column(db.Boolean, default=False)
    user_item = db.relationship(
        'Item',
        secondary = 'cart',
        backref= 'users',        
        lazy='dynamic'
    )

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])

    def total_items(self):
        pass

    def total_price(self):
        pass
       
    def save(self):
        db.session.add(self)
        db.session.commit() 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Integer)
    desc = db.Column(db.Text)
    img = db.Column(db.String)
    category = db.Column(db.String)
    created_on = db.Column(db.DateTime, index=True, default=dt.utcnow)
    

    def __repr__ (self):
        return f'<Item: {self.id} | {self.name}>'

    def to_dict(self):
        data={
            'id':self.id ,
            'name':self.name ,
            'desc':self.desc ,
            'price':self.price ,
            'img':self.img ,
            'category':self.category ,
            'created_on':self.created_on ,       
        }
        return data

    def from_dict(self, data):
        for field in ["name", "desc", "price", "img", "category"]:
            if field in data:
                setattr(self,field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()