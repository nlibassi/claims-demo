class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    insured_id = db.Column(db.Integer, db.ForeignKey('insured.id'))
    first_name = db.Column(db.String(64))
    middle_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    #rel to emp and similar others can be string for now
    # but should be int with lookup tables in production
    relationship_to_insured = db.Column(db.Integer)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.Integer)

    def __repr__(self):
        return '<First name: {}, Last name: {}>'.format(self.first_name, self.last_name)