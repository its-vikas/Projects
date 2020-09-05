from weather import db,City

db.create_all()
city1=City('Roorkee')
db.session.add_all([city1])
db.session.commit()
print(City.query.all())

