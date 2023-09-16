import argparse
import psycopg2

def create_tables(conn):
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                tax_id INT PRIMARY KEY,
                parent_tax_id INT,
                rank VARCHAR(50),
                embl_code VARCHAR(10),
                division_id INT,
                inherited_div_flag BOOLEAN,
                genetic_code_id INT,
                inherited_GC_flag BOOLEAN,
                mitochondrial_genetic_code_id INT,
                inherited_MGC_flag BOOLEAN,
                GenBank_hidden_flag BOOLEAN,
                hidden_subtree_root_flag BOOLEAN,
                comments TEXT
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS names (
                tax_id INT,
                name_txt text,
                unique_name text,
                name_class VARCHAR(50),
                PRIMARY KEY (tax_id, name_txt, unique_name, name_class)
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS divisions (
                division_id INT PRIMARY KEY,
                division_cde VARCHAR(10),
                division_name VARCHAR(255),
                comments TEXT
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS gencodes (
                genetic_code_id INT PRIMARY KEY,
                abbreviation VARCHAR(50),
                name VARCHAR(255),
                cde VARCHAR(50),
                starts VARCHAR(50)
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS delnodes (
                tax_id INT PRIMARY KEY
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS merged_nodes (
                old_tax_id INT,
                new_tax_id INT,
                PRIMARY KEY (old_tax_id, new_tax_id)
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS citations (
                cit_id INT PRIMARY KEY,
                cit_key TEXT,
                pubmed_id INT,
                medline_id INT,
                url TEXT,
                text TEXT,
                taxid_list TEXT
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS images (
                image_id INT PRIMARY KEY,
                image_key VARCHAR(225),
                url TEXT,
                license TEXT,
                attribution TEXT,
                source VARCHAR(255),
                properties TEXT,
                taxid_list TEXT
            )
        ''')
        conn.commit()

def import_nodes(conn, filepath):
    with conn.cursor() as cur, open(filepath) as f:
        for line in f:
            fields = line.rstrip('|\n').split('\t|\t')
            cur.execute('''
                INSERT INTO nodes VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', fields)
            print(f"Inserted: {fields}")
        conn.commit()


def import_names(conn, filepath):
    with conn.cursor() as cur, open(filepath) as f:
        for line in f:
            fields = line.rstrip('\t|\n').split('\t|\t')
            cur.execute('''
                INSERT INTO names VALUES (%s, %s, %s, %s)
            ''', fields)
            print(f"Inserted: {fields}")
        conn.commit()


def import_divisions(conn, filepath):
    with conn.cursor() as cur, open(filepath) as f:
        for line in f:
            fields = line.rstrip('\t|\n').split('\t|\t')
            cur.execute('''
                INSERT INTO divisions VALUES (%s, %s, %s, %s)
            ''', fields)
            print(f"Inserted: {fields}")
        conn.commit()

def import_gencodes(conn, filepath):
    with conn.cursor() as cur, open(filepath) as f:
        for line in f:
            fields = line.rstrip('\t|\n').split('\t|\t')
            cur.execute('''
                INSERT INTO gencodes VALUES (%s, %s, %s, %s, %s)
            ''', fields)
            print(f"Inserted: {fields}")
        conn.commit()

def import_delnodes(conn, filepath):
    with conn.cursor() as cur, open(filepath) as f:
        for line in f:
            fields = [line.rstrip('\t|\n')]
            cur.execute('''
                INSERT INTO delnodes VALUES (%s)
            ''', fields)
            print(f"Inserted: {fields}")
        conn.commit()

def import_merged_nodes(conn, filepath):
    with conn.cursor() as cur, open(filepath) as f:
        for line in f:
            fields = line.rstrip('\t|\n').split('\t|\t')
            cur.execute('''
                INSERT INTO merged_nodes VALUES (%s, %s)
            ''', fields)
            print(f"Inserted: {fields}")
        conn.commit()

def import_citations(conn, filepath):
    with conn.cursor() as cur, open(filepath) as f:
        for line in f:
            fields = line.rstrip('|\n').split('\t|\t')
            print(f"Trying: {fields}")
            cur.execute('''
                INSERT INTO citations VALUES (%s, %s, %s, %s, %s, %s, %s)
            ''', fields)
            print(f"Inserted: {fields}")
        conn.commit()

def import_images(conn, filepath):
    with conn.cursor() as cur, open(filepath) as f:
        for line in f:
            fields = line.rstrip('\n').split('\t|\t')
            cur.execute('''
                INSERT INTO images VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', fields)
            print(f"Inserted: {fields}")
        conn.commit()

def import_dump(conn, path, file_choice=None):
    choices = {
        "1": "nodes",
        "2": "names",
        "3": "division",
        "4": "gencode",
        "5": "delnodes",
        "6": "merged",
        "7": "citations",
        "8": "images",
    }
    pretty_choices = {
        "1": "Nodes",
        "2": "Names",
        "3": "Divisions",
        "4": "Genetic codes",
        "5": "Deleted nodes",
        "6": "Merged nodes",
        "7": "Citations",
        "8": "Organism images",
    }

    if not file_choice:
        print("Select the dump file to import:")
        for key, value in choices.items():
            print(f"{key}. {pretty_choices[key]}")

        file_choice = input("Enter the number corresponding to your choice: ")

    if file_choice in choices:
        filepath = f"{path}/{choices[file_choice]}.dmp"

        if file_choice == "1":
            import_nodes(conn, filepath)
        elif file_choice == "2":
            import_names(conn, filepath)
        elif file_choice == "3":
            import_divisions(conn, filepath)
        elif file_choice == "4":
            import_gencodes(conn, filepath)
        elif file_choice == "5":
            import_delnodes(conn, filepath)
        elif file_choice == "6":
            import_merged_nodes(conn, filepath)
        elif file_choice == "7":
            import_citations(conn, filepath)
        elif file_choice == "8":
            import_images(conn, filepath)

        print(f"Selected file: {filepath}")
    else:
        print("Invalid choice. Exiting.")
        return

def main():
    parser = argparse.ArgumentParser(description='NCBI taxdump import tool')
    parser.add_argument('--create-tables', action='store_true', help='Create necessary database tables before importing.')
    parser.add_argument('--path', default='./taxdump', help='Path to the taxdump directory')
    parser.add_argument('--choice', default=None, help='File choice (1-8)')
    args = parser.parse_args()

    # Database connection
    conn = psycopg2.connect(database="jp", user="jp", password="your_password", host="localhost", port="5432")

    # If create tables flag is set, create the database tables
    if args.create_tables:
        create_tables(conn)
        print("Tables created successfully.")
        exit()

    print(f'Using taxdump files from: {args.path}')
    import_dump(conn, args.path, args.choice)
if __name__ == '__main__':
    main()
