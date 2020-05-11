def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def execute_query(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
            
create_connection("./rodents_data.db")

rodent_df = pd.read_csv("../data/rodent_inspection_clean.csv")
rodent_df.replace(0, float('NaN'), inplace=True)
rodent_df.dropna(subset = ["LATITUDE","LONGITUDE"], inplace=True)
rodent_df = rodent_df.round({"LATITUDE":2, "LONGITUDE":2})
tuples = [tuple(x) for x in rodent_df.to_numpy()]

def insertIntoDB():
    conn = sqlite3.connect('rodents_data.db')
    create_table_sql = """ CREATE TABLE IF NOT EXISTS rodent_incidents (
                                        inspection_type text,
                                        latitude real,
                                        longitude real,
                                        borough text,
                                        inspection_date TEXT,
                                        result text
                                    ); """
    execute_query(conn, create_table_sql)
    truncate_table = """ DELETE FROM rodent_incidents;"""
    execute_query(conn, truncate_table)
    cur = conn.cursor()
    cur.executemany('INSERT INTO rodent_incidents VALUES(?,?,?,?,?,?);',tuples);
    print('We have inserted', cur.rowcount, 'records to the table.')\
        
    #commit the changes to db			
    conn.commit()
    #close the connection
    conn.close()
insertIntoDB()
