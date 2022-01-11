from App import db

class Item(db.Model):
    No = db.Column(db.Integer(), nullable=False, unique=True, primary_key=True)
    ID = db.Column(db.String(), nullable=False, unique=True)
    Description = db.Column(db.String(), nullable=False)
    Date = db.Column(db.String(), nullable=False)
    Category = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'Item {self.ID}'