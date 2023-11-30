import yaml
import pymysql

# This file accesses the data

"""Place commands in this file to access the data electronically. Don't remove any missing values, or deal with outliers. Make sure you have legalities correct, both intellectual property and personal data privacy rights. Beyond the legal side also think about the ethical issues around this data. """


def get_credentials(cred):
    # retrieves contents within file `cred`
    with open(cred) as file:
        credentials = yaml.safe_load(file)
    return credentials


def create_connection(user, password, host, database, port=3306):
    """ Create a database connection to the MariaDB database
        specified by the host url and database name.
    :param user: username
    :param password: password
    :param host: host url
    :param database: database
    :param port: port number
    :return: Connection object or None
    """
    conn = None
    try:
        conn = pymysql.connect(user=user,
                               passwd=password,
                               host=host,
                               port=port,
                               local_infile=1,
                               db=database
                               )
    except Exception as e:
        print(f"Error connecting to the MariaDB Server: {e}")
    return conn


def use(conn, database):
    # executes sql command "USE DATABASE_NAME"
    cur = conn.cursor()
    command = f"USE `{database}`;"
    cur.execute(command)
    conn.commit()


def load_data(conn, table,  files):
    """
    load all files in `files` into `table`
    """
    cur = conn.cursor()
    for file in files:
        sql_query = f'''
        LOAD DATA LOCAL INFILE '{file}' INTO TABLE {table}
        FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED by '"'
        LINES STARTING BY '' TERMINATED BY '\\n';
        '''
        cur.execute(sql_query)
    conn.commit()


def create_index(conn, table, column, idx):
    # create index `idx` on column `column` in table `table`
    cur = conn.cursor()
    command = f"CREATE INDEX {idx} ON `{table}` ({column});"
    cur.execute(command)
    conn.commit()


def add_primary_key(conn, table, column):
    # adds `column` as primary key in `table`
    cur = conn.cursor()
    query = f'''
    ALTER TABLE `{table}`
    ADD PRIMARY KEY (`{column}`);
    '''
    cur.execute(query)
    conn.commit()


def modify(conn, table, column, property):
    # modifies the property of `column` to `property` in `table`
    cur = conn.cursor()
    query = f'''
    ALTER TABLE `{table}`
    MODIFY {column} {property};
    '''
    cur.execute(query)
    conn.commit()
