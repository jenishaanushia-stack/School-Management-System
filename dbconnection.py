import pyodbc

def connection():
    return pyodbc.connect(
        r'Driver={SQL Server};'
        r'Server=LAPTOP-KVDFO2KA\SQL2019;'
        r'Database=STUDENT_QUERY;'
        r'Trusted_Connection=yes;'
    )
