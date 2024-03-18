from sequences import db, app, login_manager
from sequences import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    sanskrit = db.Column(db.String(length=30), nullable=False, unique=True)
    level = db.Column(db.String(length=12), nullable=False)
    focus = db.Column(db.String(length=1024), nullable=False)
    alignment = db.Column(db.String(length=30), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'

    def add(self, user=None):
        if user:
            self.owner = user.id
        else:
            self.owner = None

        db.session.add(self)
        db.session.commit()

    def remove(self, user):
        self.owner = None
        db.session.commit()


with app.app_context():
    db.drop_all()
    db.create_all()

    # items data
    items = [
        {'id': 1, 'name': 'Childs Pose', 'sanskrit': 'Balasana', 'level': 'Beginner',
         'focus': 'Forward Bend, Hip-Opening, and Restorative', 'alignment': '../static/images/childs-pose.jpeg',
         'description': 'Child’s Pose isn’t entirely inactive if you take the version with your arms outstretched in front of you, which engages and stretches your back muscles as well as your shoulders and arms. Because Balasana involves compressing the body on the mat or floor, it can be challenging—physically and emotionally. There are multiple variations that can help different bodies relax into the pose.'},
        {'id': 2, 'name': 'Cobra Pose', 'sanskrit': 'Bhujangasana', 'level': 'Beginner',
         'focus': 'Chest-Opening and Backbend', 'alignment': '../static/images/cobra-pose.jpeg',
         'description': 'Bhujangasana (Cobra Pose) is a heart-opening backbend that allows you to stretch your entire upper body. You cau adjust the intensity of the backbend by straightening or bending your elbows to suit your needs.'},
        {'id': 3, 'name': 'Extended Side Angle', 'sanskrit': 'Utthita Parsvakonasana', 'level': 'Beginner',
         'focus': 'Standing and Strengthening', 'alignment': '../static/images/extended-side-angle.jpeg',
         'description': 'Utthita Parsvakonasana (Extended Side Angle Pose) is all about the extension: in your arms, your legs, and your stance. In this challenging and invigorating posture, you’ll feel a stretch from the outer heel of your foot to your fingertips. Your oblique muscles are worked while the rib cage opens, encouraging you to breathe ever deeper.'},
        {'id': 4, 'name': 'Forward Fold', 'sanskrit': 'Uttanasana', 'level': 'Beginner',
         'focus': 'Forward Bend and Standing', 'alignment': '../static/images/forward-fold.jpeg',
         'description': 'The Sanskrit word uttanasana comprises ut, which means “intense,” “powerful,” or “deliberate,” and the verb tan, meaning to “stretch,” “extend,” or “lengthen.” Uttanasana is a stretch of the entire back body, a yogic term that covers the territory from the soles of the feet and up the backs of the legs; spans the lower, middle, and upper back; rises up the neck; and circles over the scalp and back down the forehead, finally ending at the point between the eyebrows.'},
        {'id': 5, 'name': 'Halfway Lift', 'sanskrit': 'Ardha Uttanasana', 'level': 'Beginner',
         'focus': 'Forward Bend and Standing', 'alignment': '../static/images/halfway-lift.jpeg',
         'description': 'In Standing Half Forward Bend, the aim is to keep your back flat to create length throughout your upper body—something that is important to learn for many other yoga postures. If you can’t do this while keeping your knees completely straight, microbend your knees, or place your hands on top of blocks or on your shins.'},
        {'id': 6, 'name': 'Mountain Pose', 'sanskrit': 'Tadasana', 'level': 'Beginner',
         'focus': 'Standing', 'alignment': '../static/images/mountain-pose.jpeg',
         'description': 'Tadasana (Mountain Pose) seems pretty straightforward. The foundational posture asks you to stand upright with your feet facing forward parallel to each other and your arms at your sides, palms facing forward. But there’s actually a lot to pay attention to in the basic pose.'},
        {'id': 7, 'name': 'Cat Pose', 'sanskrit': 'Marjaryasana', 'level': 'Beginner',
         'focus': 'Core', 'alignment': '../static/images/cat-pose.jpeg',
         'description': 'It’s such a common pose that it can be easy to fall into autopilot and practice it mindlessly or to rush through it on your way to what follows. Slow down. Let yourself experience it. While in this pose, focus on tucking your tailbone, rounding your spine, and releasing your neck.'},
        {'id': 8, 'name': 'Triangle', 'sanskrit': 'Utthita Trikonasana', 'level': 'Beginner',
         'focus': 'Standing and Strengthening', 'alignment': '../static/images/triangle.jpeg',
         'description': 'Utthita Trikonasana brings about grounded stability and a heart-opening expansion of the chest. It stretches the hamstrings and back muscles while activating the abdominal muscles. It’s a pose that requires concentration, body awareness, balance, and a steady breath, which can help focus a wandering mind and bring you back to what’s happening on your mat.'},
        {'id': 9, 'name': 'Warrior I', 'sanskrit': 'Virabhadrasana I', 'level': 'Beginner',
         'focus': 'Standing and Strengthening', 'alignment': '../static/images/warrior-I.jpeg',
         'description': 'Warrior 1 Pose is filled with opposing alignments, but when all of the opposing movements work together, the pose offers a full-body experience. You will stretch the ankles and calves, strengthen the quadriceps and back, lengthen the psoas, and stretch your upper body and arms. There’s almost no body part that doesn’t reap the rewards of holding Virabhadrasana 1.'},
        {'id': 10, 'name': 'Warrior II', 'sanskrit': 'Virabhadrasana II', 'level': 'Beginner',
         'focus': 'Strengthening, Balancing, and Standing', 'alignment': '../static/images/warrior-II.jpeg',
         'description': 'In the pose, your front knee bends to create a stretch in your hips, your arms engage and extend straight out from your shoulders, and your gaze, or dristhi, remains calm and steady toward your front hand. It is the second of three poses dedicated to Virabhadra.'}
    ]

    # Loop through the items data and add them to the database
    for item in items:
        new_item = Item(
            id=item['id'],
            name=item['name'],
            sanskrit=item['sanskrit'],
            level=item['level'],
            focus=item['focus'],
            alignment=item['alignment'],
            description=item['description']
        )
        db.session.add(new_item)

    # Commit the changes to the database
    db.session.commit()
