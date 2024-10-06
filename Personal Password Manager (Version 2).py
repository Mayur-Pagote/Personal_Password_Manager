import easygui
import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='password_manager',
            user='root', 
            password='mayur123' 
        )
        return connection
    except Error as e:
        easygui.msgbox(f"Error: {e}", "Database Connection Error")
        return None

def save_userdata():
    connection = create_connection()
    if connection is None:
        return

    data_qty = easygui.integerbox("Enter number of data you want to save:", "Save Data", lowerbound=1)
    if not data_qty:
        return

    cursor = connection.cursor()
    for _ in range(data_qty):
        link = easygui.enterbox("Enter website link or website name:", "Save Data")
        user_data = easygui.enterbox("Enter Username:", "Save Data")
        user_pass = easygui.passwordbox("Enter Password:", "Save Data")

        insert_query = "INSERT INTO credentials (website, username, password) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (link, user_data, user_pass))

    connection.commit()
    cursor.close()
    connection.close()
    easygui.msgbox("Data saved successfully!", "Success")

def read_userdata():
    connection = create_connection()
    if connection is None:
        return

    search_data = easygui.enterbox("Enter website link or website name:", "Read Data")
    if not search_data:
        return

    cursor = connection.cursor()
    cursor.execute("SELECT username, password FROM credentials WHERE website = %s", (search_data,))
    result = cursor.fetchone()

    if result:
        easygui.msgbox(f"Username: {result[0]}\nPassword: {result[1]}", "Data Found")
    else:
        easygui.msgbox("Data not present, please check the spelling", "Error")

    cursor.close()
    connection.close()

def delete_userdata():
    connection = create_connection()
    if connection is None:
        return

    search_data = easygui.enterbox("Enter website link or website name to be deleted:", "Delete Data")
    if not search_data:
        return

    cursor = connection.cursor()
    cursor.execute("DELETE FROM credentials WHERE website = %s", (search_data,))
    connection.commit()

    if cursor.rowcount > 0:
        easygui.msgbox("Data deleted successfully!", "Success")
    else:
        easygui.msgbox("Data not found", "Error")

    cursor.close()
    connection.close()

def main():
    login_info = easygui.multpasswordbox("Enter login credentials", "Login", ["Username", "Password"])
    if not login_info or login_info[0] != "MayurPagote" or login_info[1] != "Mayx123":
        easygui.msgbox("Wrong username or password", "Error")
        return

    while True:
        choice = easygui.buttonbox("Select an option:", "Password Manager", 
                                   choices=["Save new Username and Password", 
                                            "Access Username and Password", 
                                            "Delete Username and Password", 
                                            "Exit"])
        if choice == "Save new Username and Password":
            save_userdata()
        elif choice == "Access Username and Password":
            read_userdata()
        elif choice == "Delete Username and Password":
            delete_userdata()
        elif choice == "Exit":
            break

if __name__ == "__main__":
    main()
