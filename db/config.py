import mysql.connector# type: ignore
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

def openConn():
    connection = mysql.connector.connect(
        host="localhost",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database="labnew_gestao_comercial"
    )
    cursor = connection.cursor()
    return connection, cursor

def closeConn(conn, cursor):
    cursor.close()
    conn.close()

def create_table():
    print("Creating or checking the 'labnew' table...")
    connection, cursor = openConn()

    try:
        # Altera para o banco de dados 'employeespy'
        cursor.execute("USE labnew_gestao_comercial")

        # Defina a estrutura da tabela
        table_query = """
        CREATE TABLE IF NOT EXISTS vendedores (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,           
            realizado FLOAT NOT NULL
        )
        """

        cursor.execute(table_query)
        connection.commit()

        print("Table 'vendedores' created or checked.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        closeConn(connection, cursor)

# Chama a função create_table quando este script é executado diretamente
if __name__ == "__main__":
    create_table()