from playhouse.migrate import *  # @UnusedWildImport

# SQLite example:
my_db = SqliteDatabase('../spidermeta.db')
migrator = SqliteMigrator(my_db)

test_field = CharField(default='')

with my_db.transaction():
    migrate(
        #migrator.add_column('spidermeta', 'test', test_field),
        migrator.drop_column('spidermeta', 'test'),    
    )   