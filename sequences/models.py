from sequences import db, app


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    integration = db.Column(db.String(length=30), nullable=False, unique=True)
    sun_a = db.Column(db.String(length=30), nullable=False, unique=True)
    sun_b = db.Column(db.String(length=30), nullable=False, unique=True)
    sun_b_plus = db.Column(db.String(length=30), nullable=False, unique=True)
    standing_peak = db.Column(db.String(length=30), nullable=False, unique=True)
    surrender = db.Column(db.String(length=30), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'


with app.app_context():
    db.create_all()
