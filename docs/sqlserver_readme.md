# [Linux and Windows] - Install SQL Server 17 Driver

* Linux
```
https://docs.microsoft.com/pt-br/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15
```

* Windows 
```
https://docs.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
```

# [Linux] - Check that it has been configured

* Linux

```
cat /etc/odbcinst.ini
```
Output:
```
[ODBC Driver 17 for SQL Server]
Description=Microsoft ODBC Driver 17 for SQL Server
Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.7.so.2.1
UsageCount=1
```

# [Linux] - Install linux dependencies

```
sudo apt-get update
sudo apt-get install unixodbc unixodbc-dev libgssapi-krb5-2 -y 
```

# [Linux and Windows] - Install python dependencies

* Linux and Windows

```
pip install pip --upgrade
pip install pyodbc
```

# Test connection
1. Create file python.
```
nano db.py
```

2. Add the code to the file.

```python
import pyodbc

server = "tcp:<hostname>"
user = "<username>" 
password = "<password>"
database = "<database>"
driver="{ODBC Driver 17 for SQL Server}" # default value
authentication="ActiveDirectoryPassword" # default value

uri = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"PORT=1433;DATABASE={database};"
    f"UID={user};"
    f"PWD={password};"
    f"Authentication={authentication}" 
) # this creates a string, don't change it.

try:
    conn = pyodbc.connect(conn_str)
    print("Connect")
except Exception as error:
    print("Error:", error)
```

3. Save file and exit.

```
ctrl + X
```

4. Run the python file.
```
python db.py
```