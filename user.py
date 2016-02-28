class User(Entity):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    contact_number = db.Column(db.Integer)
    date_of_birth=db.Column(db.DateTime())
    address=db.Column(db.String(128))
    state=db.Column(db.String(128))
    city=db.Column(db.String(128))
    zipcode=db.Column(db.String(128))


    def __init__(self, **kwargs):
        if 'name' not in kwargs:
            raise AttributeRequired("mandatory attribute `name` is missing")
        self.set_name(kwargs['name'])

        if 'email' not in kwargs:
            raise AttributeRequired("mandatory attribute `email` is missing")
        self.set_email(kwargs['email'])

        if 'role' not in kwargs:
            raise AttributeRequired("mandatory attribute `role` is missing")
        self.set_role(kwargs['role'])

        if 'contact_number' in kwargs:
            self.set_last_active(kwargs['contact_number'])
        if 'date_of_birth' in kwargs:
            self.set_last_active(kwargs['date_of_birth'])
        if 'address' in kwargs:
            self.set_last_active(kwargs['address'])
        if 'state' in kwargs:
            self.set_last_active(kwargs['state'])
        if 'city' in kwargs:
            self.set_last_active(kwargs['city'])
        if 'zipcode' in kwargs:
            self.set_last_active(kwargs['zipcode'])


    def __str__(self):
        return "Name = %s, e-mail id = %s, role = %s, last_active = %s" % \
            (self.name, self.email, self.role.name, self.last_active)

    def __repr__(self):
        return "Name = %s, e-mail id = %s, role = %s, last_active = %s" % \
            (self.name, self.email, self.role.name, self.last_active)

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    def get_name(self):
        return self.name

    def get_email(self):
        return self.email

    def get_role(self):
        return self.role

    def get_created(self):
        return self.created

    def get_last_active(self):
        return self.last_active

    @typecheck(name=Name)
    def set_name(self, name):
        self.name = name.value

    @typecheck(email=Email)
    def set_email(self, email):
        self.email = email.value

    def set_last_active(self, last_active):
        self.last_active = last_active

    @typecheck(role=Role)
    def set_role(self, role):
        self.role = role

    def to_client(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'role': self.role.to_client(),
            'last_active': self.last_active,
            'created': self.created.isoformat()
        }
