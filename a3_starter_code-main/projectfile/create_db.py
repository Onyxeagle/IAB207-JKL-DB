from website import db, create_app

# this needs to be run anytime you make a change to models so the database can be altered to refelect it 
# the database is in /projectfile/instance
app = create_app()
ctx = app.app_context()
ctx.push()
db.create_all()
quit()