from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, asc, desc
from sqlalchemy.sql import select
engine = create_engine('mysql://root:brainbeam@localhost/hexahealth', echo=True)
meta = MetaData()

doctors = Table(
   'doctors', meta, 
   Column('id', Integer, primary_key = True), 
   Column('firstname', String(20)), 
   Column('lastname', String(20)),
   Column('email', String(20)),
   Column('mobile', String(10))
)

addresses = Table(
   'addresses', meta, 
   Column('id', Integer, primary_key = True), 
   Column('doctor_id', Integer, ForeignKey('doctors.id')), 
   Column('door', String(5)),
   Column('street', String(20)),
   Column('area', String(20)),
   Column('city', String(20)),
   Column('pin', String(6)))

# meta.create_all(engine)

conn = engine.connect()

def create_table():
    meta.create_all(engine)

def insert_doctors():
    result = conn.execute(doctors.insert().values([
        {'firstname':'Anandan', 'lastname':'Subbiah', 'email':"anandan@gmail.com", 'mobile':'9986600371'},
        {'firstname':'Rajiv', 'lastname' : 'Kumar', 'email':"reajiv@gmail.com", 'mobile':'9986600372'},
        {'firstname':'Saravanan','lastname' : 'Krishnasamy', 'email':"sara@gmail.com", 'mobile':'9986600373'},
        {'firstname':'Abdul','lastname' : 'Rahman', 'email':"abdul@gmail.com", 'mobile':'9986600374'},
        {'firstname':'Domnic','lastname' : 'Jhon', 'email':"dominc@gmail.com", 'mobile':'9986600375'},
    ]))
    return result

def insert_addresses():
    result = conn.execute(addresses.insert().values([
        {'doctor_id':1, 'door':'6011', 'street':'ORR', 'area':'DB Halli', 'city':'Bangalore', 'pin': '560103'},
        {'doctor_id':2, 'door':'6012', 'street':'Rajaji Road', 'area':'Bellandur', 'city':'Bangalore', 'pin': '560104'},
        {'doctor_id':3, 'door':'6013', 'street':'KK Road', 'area':'HSR Layout', 'city':'Bangalore', 'pin': '560104'},
        {'doctor_id':4, 'door':'6014', 'street':'JJ Road', 'area':'BTM Layout', 'city':'Bangalore', 'pin': '560105'},
        {'doctor_id':5, 'door':'6015', 'street':'KC Road', 'area':'JP Ngar', 'city':'Bangalore', 'pin': '560106'},
    ]))
    return result

def get_all_doctors():
    stmt = doctors.select()
    resultset = conn.execute(stmt)
    return resultset

def get_doctors_with_address():
    s = select([doctors, addresses]).where(doctors.c.id == addresses.c.doctor_id)
    result = conn.execute(s)    
    return result

def get_doctors_with_join():
    addrs = doctors.join(addresses, doctors.c.id == addresses.c.doctor_id)
    stmt = select([doctors, addresses]).select_from(addrs)
    result = conn.execute(stmt).fetchall()
    return result

def get_doctors_ordered():
    stmt = select([doctors]).order_by(asc(doctors.c.firstname))
    result = conn.execute(stmt)
    return result


# recs = insert_doctors()
# print(recs)

# for rec in recs:
#     print(rec)

# insert_doctors()
    
# insert_addresses()

recs = get_doctors_ordered()
for rec in recs:
    print(rec)

conn.close()