from seed import *

populate_db()


x = input('Commit? True/False')

if eval(x) is True:
    db.session.commit()
    print('\n\n***DATABASE READY***')
else:
    print('<<<<<<<<<<<<<Session Not Committed >>>>>>>>>>>>')
