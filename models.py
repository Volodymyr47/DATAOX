from sqlalchemy import Integer, String, Text, Column
from dbsettings import Base, db


class PostHead(Base):
    __tablename__ = 'posthead'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)
    creation_date = Column(String(20), nullable=True)
    price = Column(String(255), nullable=True)
    currency = Column(String(2), nullable=True)
    location = Column(String(100), nullable=True)
    text = Column(Text, nullable=True)
    beds_count = Column(String(20), nullable=True)

    def add_data(self, title, image, post_date, price, currency, location, descr, beds_count):
        '''
        Insert data into the DB, checking for duplicate rows first
        '''
        try:
            prev = db.query(PostHead).filter_by(image=image).first()
            if prev is None:
                new_data = PostHead(title=title,
                                    image=image,
                                    creation_date=post_date,
                                    price=price,
                                    currency=currency,
                                    location=location,
                                    text=descr,
                                    beds_count=beds_count)
                if new_data.title != '' and \
                    new_data.image != '' and \
                    new_data.creation_date != '' and \
                    new_data.price != '' and \
                    new_data.currency != '' and \
                    new_data.location != '' and \
                    new_data.beds_count != '':
                        db.add(new_data)
                        db.commit()
                return True
        except BaseException as err:
            db.rollback()
            print(err)
            return False





