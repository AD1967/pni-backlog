from sqlalchemy import create_engine, MetaData, event
from sqlalchemy.sql import sqltypes



# копирование базы данных с сервера в sqlite (файл sqlite_file)


# данные для подключения
host = "10.1.6.74"
port = ":"+"3306"
db_name = "tci"
user = "dbuser"
password = "j0v461k"

# файл для копии
sqlite_file = "copy_server.db"


src_engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}{port}/{db_name}")
src_metadata = MetaData(bind=src_engine)
exclude_tables = ('sqlite_master', 'sqlite_sequence', 'sqlite_temp_master')

tgt_engine = create_engine(f"sqlite:///{sqlite_file}")
tgt_metadata = MetaData(bind=tgt_engine)

@event.listens_for(src_metadata, "column_reflect")
def genericize_datatypes(inspector, tablename, column_dict):
   column_dict["type"] = column_dict["type"].as_generic(allow_nulltype=True)     

tgt_conn = tgt_engine.connect()
tgt_metadata.reflect()

# 
for table in reversed(tgt_metadata.sorted_tables):
   if table.name not in exclude_tables:
    print('dropping table =', table.name)
    table.drop()

# 
for table in reversed(tgt_metadata.sorted_tables):
   table.delete()

tgt_metadata.clear()
tgt_metadata.reflect()
src_metadata.reflect()

# 
for table in src_metadata.sorted_tables:
   if table.name not in exclude_tables:
    table.create(bind=tgt_engine)

# 
tgt_metadata.clear()
tgt_metadata.reflect()

# 
for table in tgt_metadata.sorted_tables:
   if table.name not in exclude_tables:
    src_table = src_metadata.tables[table.name]
    stmt = table.insert()
    for index, row in enumerate(src_table.select().execute()):
        print("table =", table.name, "Inserting row", index)
        stmt.execute(row._asdict())