import os
import re
import duckdb

def parse_and_load(sql_filepath, db_filepath):
    print(f"Reading SQL file: {sql_filepath}")
    if os.path.exists(db_filepath):
        os.remove(db_filepath)
        print(f"Removed existing database file: {db_filepath}")
        
    con = duckdb.connect(db_filepath)
    
    with open(sql_filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    print(f"Processing {len(lines)} lines...")
    
    current_stmt = []
    in_copy = False
    copy_table = ""
    copy_cols = []
    copy_rows = []
    
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if in_copy:
            if stripped == '\\.':
                in_copy = False
                # Insert rows
                if copy_rows:
                    cols_str = ", ".join(copy_cols)
                    placeholders = ", ".join(["?" for _ in copy_cols])
                    insert_query = f"INSERT INTO {copy_table} ({cols_str}) VALUES ({placeholders})"
                    con.executemany(insert_query, copy_rows)
                    print(f"Loaded {len(copy_rows)} rows into table: {copy_table}")
                    copy_rows = []
            else:
                # split by tab
                row = line.split('\t')
                row = [None if x == '\\N' else x for x in row]
                copy_rows.append(row)
            continue
            
        # Check for COPY
        copy_match = re.match(r'^COPY\s+(\w+)\s*\(([^)]+)\)\s*FROM\s+STDIN;', stripped, re.IGNORECASE)
        if copy_match:
            # First, execute any buffered statement
            if current_stmt:
                stmt = "".join(current_stmt).strip()
                if stmt:
                    stmt = re.sub(r'\bCASCADE\b', '', stmt, flags=re.IGNORECASE)
                    stmt = re.sub(r'\bSERIAL\b', 'INTEGER', stmt, flags=re.IGNORECASE)
                    con.execute(stmt)
                current_stmt = []
                
            copy_table = copy_match.group(1)
            copy_cols = [c.strip() for c in copy_match.group(2).split(',')]
            in_copy = True
            copy_rows = []
            continue
            
        # Skip transaction controls
        if stripped in ('BEGIN;', 'COMMIT;', 'ROLLBACK;'):
            continue
            
        if line.strip() == "" or line.strip().startswith('--'):
            continue
            
        current_stmt.append(line + "\n")
        if stripped.endswith(';'):
            stmt = "".join(current_stmt).strip()
            # Clean up
            stmt = re.sub(r'\bCASCADE\b', '', stmt, flags=re.IGNORECASE)
            stmt = re.sub(r'\bSERIAL\b', 'INTEGER', stmt, flags=re.IGNORECASE)
            con.execute(stmt)
            current_stmt = []
            
    con.close()
    print(f"Database initialization completed successfully. DuckDB file saved to: {db_filepath}")

if __name__ == '__main__':
    sql_path = r"C:\Users\abhij\Downloads\shopping_data.sql"
    db_path = r"C:\Users\abhij\.gemini\antigravity\scratch\wren_integration\shopping_data.duckdb"
    
    # Ensure parent dir exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    parse_and_load(sql_path, db_path)
