import easygui
import pickle
import os

#This function will take data from the user and store it in a binary file.
def save_userdata():
    data_qty = easygui.integerbox("Enter number of data you want to save:", "Save Data", lowerbound=1)
    if not data_qty:
        return

    for _ in range(data_qty):
        link = easygui.enterbox("Enter website link or website name:", "Save Data")
        user_data = easygui.enterbox("Enter Username:", "Save Data")
        user_pass = easygui.passwordbox("Enter Password:", "Save Data")
        data_list = [user_data, user_pass]
        data_dict = {link: data_list}
        with open("newpass.dat", "ab") as f:
            pickle.dump(data_dict, f)
    easygui.msgbox("Data saved successfully!", "Success")

#This function will read the data from the binary file and output the username and password for the input platform name.
def read_userdata():
    search_data = easygui.enterbox("Enter website link or website name:", "Read Data")
    if not search_data:
        return

    value_fetched = False
    try:
        with open("newpass.dat", "rb") as f:
            while True:
                data = pickle.load(f)
                if search_data in data:
                    temp_data = data[search_data]
                    easygui.msgbox(f"Username: {temp_data[0]}\nPassword: {temp_data[1]}", "Data Found")
                    value_fetched = True
                    break
    except (EOFError, FileNotFoundError):
        pass
    if not value_fetched:
        easygui.msgbox("Data not present, please check the spelling", "Error")
        
#This function will delete the record from the binary file by taking the platform name as input and removing the data associated with it.
def delete_userdata():
    search_data = easygui.enterbox("Enter website link or website name to be deleted:", "Delete Data")
    if not search_data:
        return

    found = False
    try:
        with open("newpass.dat", "rb") as f, open("newpass_temp.dat", "wb") as temp_file:
            while True:
                data = pickle.load(f)
                if search_data not in data:
                    pickle.dump(data, temp_file)
                else:
                    found = True
    except (EOFError, FileNotFoundError):
        pass
    os.remove("newpass.dat")
    os.rename("newpass_temp.dat", "newpass.dat")
    if found:
        easygui.msgbox("Data deleted successfully!", "Success")
    else:
        easygui.msgbox("Data not found", "Error")

def main():
    #This statement will take input as a username and password in order to execute the program further.
    login_info = easygui.multpasswordbox("Enter login credentials", "Login", ["Username", "Password"])
    if not login_info or login_info[0] != "MayurPagote" or login_info[1] != "MagicPassword":
        easygui.msgbox("Wrong username or password", "Error")
        return
    
    #The above entered username and password will be checked, and if both are correct, the user will get options to execute the functions in order to save, access, and delete usernames and passwords.
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
