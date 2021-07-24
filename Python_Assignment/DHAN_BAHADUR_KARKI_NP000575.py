# DHAN BAHADUR KARKI
# NP000575

import sys
import re
import datetime
import calendar
import sys
from uuid import uuid4
import tabulate

#****************************************************

def reading_file_data(filename,mode): # take filename and mode as paramenter
    with open(filename,mode) as fo:
        file_content = fo.read()
        file_content = file_content.split('\n') # splitting file data by '\n'
        data_list = []
        
        for data in file_content:
            data = data.split(',') # splitting data again by ','
            data_list.append(data)
        data_list.pop(-1) # removing empty list
    return data_list


#**************** Admin functions*************
# Admin Login
def admin_login():
    while True:
        admin_name = input("Username: ")
        admin_psd = input("Password: ")
        admin_list = reading_file_data('admins.txt','r')
        flag = 0
        for c_data in admin_list:
            
            if admin_name in c_data and admin_psd in c_data:
                print(c_data[0],c_data[1])
                flag = 1
                
        if flag:
            print("\nYou have logged in successfully.\n")
            all_admin_functions()
        else: 
            print("\nAccess Denied !!!\n")
                     

# Admin menu
def all_admin_functions():
    print("""\n
  ----------Admin Menu ------------\n
    1. Verify Customer Requests
    2. Verify Loan Requests
    3. View Transactions
    4. Go to Main Menu
    \n""")
    try:
        ch = int(input("Select what you want to do: "))
    except:
        print("\nNumber input are only acceptable !!!\n")
        all_admin_functions()
    else:
        if ch == 1:
            def verify_customer_request(): # verify customer requests
                
                view_unverified_req()
                verify_req = input("\nDo you want to verify user request (y/n) ?  ")
                while verify_req == 'y':
                    
                    username = input("Enter username: ")
                    if verify_customers(username):
                        
                        print(f"\n{username} has been verified...\n")
                        verify_customer_request()
                all_admin_functions()
            verify_customer_request()


        elif ch == 2:
            def verify_loan_request():  # providing unique loan id and verifying loan requests
                placing_loan_id_in_file()      # calling generated loan id to write in file
                view_unverified_loan()
                verify_loan = input("\nDo you want to verify user loans (y/n) ?")
                while verify_loan == 'y':
                    loan_id = input("Enter Loan ID: ")

                    if verify_user_loan_id(loan_id): # calling function that verify requested user id and write in a file
                        if placing_installment_date(loan_id): # calling function that place installment data in a file
                            if calculates_loan_emi(loan_id): # calling function that writes loan calculation details in a file
                                    print(f"\n Loan ID '{loan_id}' has been verified...\n")
                            verify_loan_request()
                all_admin_functions()
            verify_loan_request()

        elif ch == 3:
            view_transactions_menu()
        else:
            main_menu()

def view_transactions_menu():    # view transactions menu
    print("""
------ Transactions View Menu -------\n    
    1. View by Specific Customers
    2. View by Specific Loan Type
    3. View of all customer
    4. View transaction of all types Loan
    5. Go to Admin Menu
    """)
    ch = int(input("\nSelect what you want to do (1-4):"))
    if ch == 1:
        view_of_specific_customers()
    elif ch == 2:
        view_of_specific_loan_type()
    elif ch == 3:
        view_of_all_customers()
    elif ch == 4:
        view_transactions_of_all_types_loan()
    else:
        all_admin_functions()

def goto_view_transactions_menu():  # go back to admin menu
    inp_user = input("\nDo you want to go back to previous menu (y/n)?")
    if inp_user == 'y':
        view_transactions_menu()
    else: 
        sys.exit()


def view_of_specific_customers():
    user_name = input("Enter username: ")  
    loan_details = reading_file_data('applied_loan.txt','r')
    table_data = []
    for loan_data in loan_details:
        if loan_data[2] == user_name: 

            titled_data = loan_data[1],loan_data[2],loan_data[4],loan_data[5],loan_data[6]+' years',loan_data[7] +' %',loan_data[8],loan_data[9]
            table_data.append(titled_data)
    title = ['Loan Id','Username','Loan Types','Applied Loan Amt','Loan Tenure','Loan Rate','Installment Amt','Due Amt']
    print(tabulate.tabulate(table_data, headers=title,tablefmt="github"))
    goto_view_transactions_menu()
                     

def view_of_specific_loan_type(): # view transactions of specific loan type
    loan_type = input("\nEnter types of loan: ")
    loan_details = reading_file_data('applied_loan.txt','r') # calling reading_file_data
    table_data = []
    for loan_data in loan_details:
        if loan_type in loan_data:   # checking userid and if it finds, functions other task on the vary line
            titled_data = loan_data[1],loan_data[2],loan_data[4],loan_data[5],loan_data[6]+' years',loan_data[7] +' %',loan_data[8],loan_data[9]
            table_data.append(titled_data)
    title = ['Loan Id','Username','Loan Types','Applied Loan Amt','Loan Tenure','Loan Rate','Installment Amt','Due Amt']
    print(tabulate.tabulate([titled_data], headers=title,tablefmt="github")) 
    goto_view_transactions_menu()                       
    

def view_of_all_customers():    # view transactions data of all customers
    loan_details = reading_file_data('applied_loan.txt','r') # calling reading_file_data
    table_data = []
    for loan_data in loan_details:
        if loan_data[-1] == 'Verified':
            titled_data = loan_data[1],loan_data[2],loan_data[4],loan_data[5],loan_data[6]+' years',loan_data[7] +' %',loan_data[8],loan_data[9]
            table_data.append(titled_data)
    title = ['Loan Id','Username','Loan Types','Applied Loan Amt','Loan Tenure','Loan Rate','Installment Amt','Due Amt']
    print(tabulate.tabulate([titled_data], headers=title,tablefmt="github"))    # using tabulate module to make table
    goto_view_transactions_menu()



def view_transactions_of_all_types_loan():
    view_of_all_customers()
    goto_view_transactions_menu()


def verify_customers(username): # verify requested userid
    with open('details.txt','r+') as file:

        customer_details = file.readlines()
        
        for elem in range(len(customer_details)):
            if username in customer_details[elem]: # checking if username 
                user_data = customer_details[elem].split(',')
                user_data[-1] = user_data[-1].replace(user_data[-1][:5],'Verified') # changing unverified to verified of the searched user

                str_ud = ','.join([str(e) for e in user_data]) # converting user data into string
                customer_details[elem] = customer_details[elem].replace(str(customer_details[elem]),str_ud)
        file.seek(0)
        file.writelines(customer_details)
    return True


def view_unverified_req():
    c_list = reading_file_data('details.txt','r')
    pending_users = []
    for ele in c_list:
        if ele[-1] == "False":
            pending_users.append(ele)
    title= ["Name", "Address", "E-mail", "Contact No.", "Gender", "DOB", "Username","Password","Is Admin", "User Status"]
    print(tabulate.tabulate(pending_users,title,tablefmt="github"))
    
#------------------------------------------------------

def generate_loan_id(): # function that generates unique loan id
    unique_loan_id = str(uuid4())
    splt_loan_id = unique_loan_id.split('-')
    loan_id = 'LiD-'+''.join(splt_loan_id[4]) 
    return loan_id

#------------------------------------------------------
def placing_loan_id_in_file(): # placing user loan id in the file
    with open('applied_loan.txt','r+') as file:
        loan_details = file.readlines()
        for elem in range(len(loan_details)):
            loan_data = loan_details[elem].split(',')
            if len(loan_data) <7:   # total element with loanid in one line of loan_details.txt is 7  so if more it does not give unique id
                loan_data.insert(1,generate_loan_id()) # inserting called unique loan id
            str_loan_data = ','.join([str(e) for e in loan_data]) # converting user data into comma separated string
            loan_details[elem] = loan_details[elem].replace(str(loan_details[elem]),str_loan_data) # replacing the whole data
        file.seek(0)
        file.writelines(loan_details)


def placing_installment_date(loan_id): # verify user loan id
    with open('applied_loan.txt','r+') as file:

        loan_details = file.readlines()
        
        for elem in range(len(loan_details)):
            if loan_id in loan_details[elem]:   # checking userid and if it finds, functions other task on the vary line
                
                #  finding installment date
                loan_data = loan_details[elem].split(',')
                loan_data[0] = loan_data[0].split('-')
                loan_data[0] = ','.join(loan_data[0])
                loan_data[0].replace(',','-')
                joined_date = datetime.datetime.strptime(loan_data[0],"%Y,%m,%d")
                days_in_month = calendar.monthrange(joined_date.year, joined_date.month)[1]
                installment_date = str(joined_date + datetime.timedelta(days=days_in_month)).split(' ')[0]
                loan_data[0] = loan_data[0].replace(str(loan_data[0]),str(joined_date).split(' ')[0])
                loan_data.insert(3,installment_date) # inserting installment date in file
                str_loan_data = ','.join([str(e) for e in loan_data]) # converting user data into string
                loan_details[elem] = loan_details[elem].replace(str(loan_details[elem]),str_loan_data)
        file.seek(0)
        file.writelines(loan_details)  
    return True


def calculates_loan_emi(loan_id): # verify user loan id
    with open('applied_loan.txt','r+') as file:

        loan_details = file.readlines()
        
        for elem in range(len(loan_details)):
            if loan_id in loan_details[elem]:
                loan_data = loan_details[elem].split(',')
                proposed_loan_amt = float(loan_data[5])    # loan amt from file
                loan_tenure = int(loan_data[6]) # laon tenure from file
                loan_types = loan_data[4] # loan_types from file

                if loan_types == 'Car Loan':
                    if loan_tenure <=5:
                        loan_rate = 11.02
                    elif loan_tenure <=10:
                        loan_rate = 12.52
                    else:
                        print("Loan period is out of range !!!") 

                elif loan_types == 'Education Loan':
                    if loan_tenure <=5:
                        loan_rate = 11.32
                    elif loan_tenure <=10:
                        loan_rate = 12.32
                    else:
                        print("Loan period is out of range !!!")
                
                elif loan_types == 'Home Loan':
                    if loan_tenure <=5:
                        loan_rate = 11.32
                    elif loan_tenure <=10:
                        loan_rate = 12.32
                    elif loan_tenure > 10:
                        loan_rate = 12.50
                
                elif loan_types == 'Personal Loan':
                    if loan_tenure <=5:
                        loan_rate = 10.50
                    elif loan_tenure <=10:
                        loan_rate = 11.50
                    else:
                        print("Loan period is out of range !!!")
                    
                no_mnths = loan_tenure *12
                r = loan_rate/(12*100)  # calculates interest rate per month    
                emi = proposed_loan_amt * r * ((1+r)**no_mnths)/((1+r)**no_mnths - 1) # calculates Equated Monthly Installment (EMI)
                total_loan_amt = emi * no_mnths

                loan_data.insert(7,loan_rate)
                loan_data.insert(8,round(emi,3))
                loan_data.insert(9,round(total_loan_amt,3))
                                
                str_loan_data = ','.join([str(e) for e in loan_data]) # converting user data into string
                loan_details[elem] = loan_details[elem].replace(str(loan_details[elem]),str_loan_data)
        file.seek(0)
        file.writelines(loan_details)  
    return True

#------------------------------------------------------
def get_installment_date():  # Finding next month installment date
    c_list = reading_file_data('applied_loan.txt','r')

    for loaned_date in c_list:
        loaned_date[0] = str(loaned_date[0]).split('-')
        loaned_date[0] = ','.join(loaned_date[0])
    
    loaned_date[0]=loaned_date[0].replace(',','-')
    loan_borrowed_date = datetime.datetime.strptime(loaned_date[0],"%Y,%m,%d")
    days_in_month = calendar.monthrange(loan_borrowed_date.year, loan_borrowed_date.month)[1]
    installment_date = str(loan_borrowed_date + datetime.timedelta(days=days_in_month)).split(' ')[0]
    return installment_date

#------------------------------------------------------
def view_unverified_loan(): # verify unverified loans
    placing_loan_id_in_file()      # calling generated loan id to write in file
    loan_list = reading_file_data('applied_loan.txt','r')
    pending_loans  = []
    for ele in loan_list:
        if ele[-1] == "False":
            pending_loans.append(ele)
    title = ["Applied Date","Loan ID","Username","Loan Type","Loan Amount","Loan Tenure","Loan Status"]
    print(tabulate.tabulate(pending_loans,title,tablefmt="github"))

def verify_user_loan_id(loan_id): # verify user loan id
    with open('applied_loan.txt','r+') as file:

        loan_details = file.readlines()
        
        for elem in range(len(loan_details)):
            if loan_id in loan_details[elem]: # checking userid and if it finds, functions other task on the vary line
                loan_data = loan_details[elem].split(',')
                loan_data[-1] = loan_data[-1].replace(loan_data[-1][:5],'Verified') # changing unverified to verified of the searched user
                str_loan_data = ','.join([str(e) for e in loan_data]) # converting user data into string
                loan_details[elem] = loan_details[elem].replace(str(loan_details[elem]),str_loan_data)
        file.seek(0)
        file.writelines(loan_details)  
          
    return True



#***********New customer Functions**********************
def new_customer_functions():
    while True:
        try:
            print("""
            -------New Customer's Menu------\n
                1. Check Loan Details
                2. Loan Calculator
                3. Register new Account
                4. Go to Main Menu
            """)
            new_customer_func = int(input("\nSelect what you want to do (1-4):"))
        except ValueError:
            print("Number Input are only acceptable !!!")
        else:
            if new_customer_func == 1: # Check loan Details
                show_loan_details()
            elif new_customer_func == 2: # Loan Calculator
                emi_calculation()
            elif new_customer_func == 3: # Register new Account
                register_new_account()

            elif new_customer_func == 4: # main menu
                main_menu()

def new_customer_menu():
    inp_user = input("\nDo you want to go back to previous menu (y/n)?")
    if inp_user == 'y':
        new_customer_functions()
    else: 
        sys.exit()

# age eligibitlity
def calculate_age():
    while True:
        try:
            dob = datetime.datetime.strptime(input("Date of birth (yyyy mm dd): "), "%Y %m %d")
        except ValueError:
            print("\nDate is not in correct format !!!\n")
        else:
            today = datetime.datetime.today()
            age = today.year - dob.year
            
            if age > 18:
                dob = str(dob).split(' ')[0] # splitting date and time
                return dob
                break
                
            else:
                print("Minimum age limit for loan is 18 years !!!\n")
                

def check_username():
    while True:
        usr_name = input("Username: ")

        with open('details.txt','r') as fo:

            customer_list = fo.read()
            customer_list = list(filter(None,customer_list.split('\n'))) # splitting by new line and removing empty strings from list 
            flag = 0
            try:
                for ele in customer_list:
                    ele = ele.split(',')
                    if usr_name == ele[6]: #checking if username is in the index 9 of file
                        flag = 1
            except:
                return usr_name
                break
            else:
                if not flag:
                    return usr_name # return new user name
                    break
                else:
                    print("\nUsername is already available.. Tryout next username !!!\n")
                # return True
               

def check_user_password():
    
    pswd_pattern = '(?=.*[A-Z]+)(?=.*\d+)(?=.*[!@#$%^.&*]+)(?!.*\s)' # password only includes upper case letters, digits, specific symbols and ignore whitespace
    while 1:
        usr_pswd = input("Enter password: ")
        if len(usr_pswd)<8:
            print("\nYour password must be 8-16 characters long !!!\n")
        elif not re.search(pswd_pattern, usr_pswd): # check password and password pattern are satified or not
            print("\nPassword must contain uppercase, number and special symbols !!!\n")
        else:
            usr_confirm_pswd = input("Enter Confirm Password: ")

            if usr_pswd == usr_confirm_pswd:
                return usr_confirm_pswd
                break

            else:
                print("\nPassword and confirm password is not same.\n")
                     
    
def register_new_account():
    # reading file and also checking existence. If not, file is created.
        try:
            fp = open('details.txt','r')
        except FileNotFoundError:
            fp = open('details.txt','w')
        else:
            if fp:
                fp.close()
                fp = open("details.txt", "a")
            
        print("Please fill out the following requirements to be a new customer: \n ")
        full_name = input("Name: ")
        address = input("Address: ")
        email_ad = input ("E-mail: ")
        contact_no = int (input("Contact no.: "))
        gender = input("Gender: ") 
        date_of_birth = calculate_age() # calling age_eligibility functions
        user_name = check_username() # calls a unique username
        user_password = check_user_password()
        is_admin = False
        active_user = False
        user_info = f"{full_name.title()},{address.title()},{email_ad},{contact_no},{gender.title()},{date_of_birth},{user_name},{user_password},{is_admin},{active_user}\n"
        print(f"\n{full_name.title()}, Thank you for creating an account ...\n")
        fp.write(user_info)
        fp.close()
        new_customer_menu()


def emi_calculation(): # emi calculator functions
    loan_amt = float(input("Enter Loan amount: "))
    loan_rate = float(input("Enter annual interest rate (%): "))
    no_mnths = int(input("Enter number of months: " ))
    r = loan_rate/(12*100)  # calculates interest rate per month    
    emi = loan_amt * r * ((1+r)**no_mnths)/((1+r)**no_mnths - 1) # calculates Equated Monthly Installment (EMI)

    print("Monthly Payment(EMI) = %.2f" %emi)
    new_customer_menu()


#*******************Registered Customer Functions*************************
def reg_customer_login(): # Registered customer login page
    while True:
        usr_name = input("Username: ")
        usr_psd = input("Password: ")
        customer_list = reading_file_data('details.txt','r')
        for c_data in customer_list:
            if usr_name in c_data and usr_psd in c_data:
                if (c_data[9]!='Verified'): # checking if username is verified
                    print(f"\nUsername {usr_name} has not been verified yet !!!\n")
                    
                else:
                    print("\nYou have logged in successfully.\n")
                    registered_customer_menu(usr_name)
                    break
                    
        else:
            print("\nUsername and password is not available !!!\n")
            reg_customer_login()
            break

def registered_customer_menu(usr_name): # registered customer menu
    while 1:
        print("""
    -------Registered Customer Menu-----\n
        1. View Loan Details and Apply 
        2. Pay Loan Installment
        3. View Transaction
        4. Status of Loan
        5. Back to Main menu\n\n""")
        try:
            registered_customer_func = int(input("Select what you want to do (1-4):"))
        except ValueError:
            print("\nNumber inputs are only acceptable !!!\n")
        else:
            if registered_customer_func == 1:
                if show_loan_details():
                    apply_for_loan(usr_name)
                    registered_customer_menu(usr_name)
                    break
            elif registered_customer_func == 2:
                pay_loan_installment(usr_name)
                break

            elif registered_customer_func == 3:
                view_transactions(usr_name)
                    
            elif registered_customer_func == 4:
                    status_of_loan(usr_name)
                    break
            elif registered_customer_func == 5:
                sys.exit()
            

def view_transactions(usr_name):
    with open('applied_loan.txt','r+') as file:
        loan_details = file.readlines()
        # loan_transactions = []
        for elem in range(len(loan_details)):
            if usr_name in loan_details[elem]:   # checking userid and if it finds, functions other task on the vary line
                loan_data = loan_details[elem].split(',')
                print(tabulate.tabulate([['Loan Id', 'User', 'Paid Amount', 'Due Amount'],[loan_data[1],loan_data[2],loan_data[8],loan_data[9]]], headers="firstrow",tablefmt="github"))
                goto_customer_menu(usr_name)



def show_loan_details():# Offered loan details by the bank
    print()
    title = "Loan Details"
    print(title.center(78,"-")) # center "Loan Details" inside - appearance on both sides
    print()
    loans = [['Education Loan (HL)','11.32%', '12.32%','-'],
            ['Car Loan (CL)','11.02%', '12.52%','-'],
            ['Home Loan (HL)', '11.32%', '12.32%', '12.50%'],
            ['Personal Loan (PL)','10.50%','11.50%','-']]
    title= ['Loan Types','Upto 5 years','Upto 10 years','Above 10 years']
    print(tabulate.tabulate(loans, headers=title,tablefmt="github")) 

    with open('loan_details.txt','w') as fw:
            for elem in loans:
                elem = ','.join(elem) + '\n'
                fw.write(elem)  # writing loans_data
    return True

def apply_for_loan(usr_name):   # function that asks user details for loans
    try:
        fr = open('applied_loan.txt','r')
    except FileNotFoundError:
        fr = open("applied_loan.txt","w")
    else:
        if fr:
            fr.close()
            fr = open("applied_loan.txt", "a") 

    print("\nFill the required fields to apply for loan !\n")

    is_verified = False

    pick_loan_types = available_loan_types()

    proposed_loan = float(input("Proposed Loan: "))

    loan_tenure = int(input ("Tenure of Loans (in years): "))

    loan_applied_date = str(datetime.datetime.today()).split(' ')[0]

    apply_loan = f"{loan_applied_date},{usr_name},{pick_loan_types},{proposed_loan},{loan_tenure},{is_verified}\n"
    
    print("Your loan request has been sent successfully...\n")
    fr.write(apply_loan)
    fr.close()
    goto_customer_menu(usr_name)    # return to previous menu



def available_loan_types(): # shows avalilable loans and asks users to choose loans
    print("\nChoose types of Loan:\n")
    loan_lst = ["1. Education Loan (EL)","2. Car Loan ","3. Home Loan","4. Personal Loan"]
    for types in loan_lst:
        print(f'  {types}')
    while True:
        try:
            ch = int(input("\n>>> "))
        except ValueError:
            print("Number input are only acceptable !!!")
            available_loan_types()
            break
        else:
            if ch == 1:
                return 'Education Loan'
                break
            elif ch == 2:
                return 'Car Loan'
                break
            elif ch == 3:
                return 'Home Loan'
                break
            elif ch == 4:
                return 'Personal Loan'
                break


def pay_loan_installment(usr_name): # loan installment payment
    with open('applied_loan.txt','r+') as file:
        loan_details = file.readlines()
        for elem in range(len(loan_details)):
            if usr_name in loan_details[elem]:   # checking userid and if it finds, functions other task on the vary line
                loan_data = loan_details[elem].split(',')

                print(f"\n{loan_data[2].title()} your monthly installment amount is {loan_data[8]}\n")

                while True:
                    try:
                        pay_installment = float(input("\nEnter amount to pay loan installment: "))
                    except ValueError:
                        print("\nNumber inputs are only acceptable !!!")
                    else:
                        total_loan_amt_topay = float(loan_data[9])
                        total_loan_amt_topay = total_loan_amt_topay - pay_installment

                        loan_data[9] = loan_data[9].replace(str(loan_data[9]),str(total_loan_amt_topay).split(' ')[0])
      
                        str_loan_data = ','.join([str(e) for e in loan_data]) # converting user data into string and joining by ,
                        loan_details[elem] = loan_details[elem].replace(str(loan_details[elem]),str_loan_data)
                        file.seek(0)
                        file.writelines(loan_details) 

                        print(f"{usr_name}, Rs.{pay_installment} installment amount has been paid successfully...")
                        goto_customer_menu(usr_name)

def status_of_loan(usr_name):
    loan_details = reading_file_data('applied_loan.txt','r') # calling reading_file_data
    for loan_data in loan_details:
        if usr_name in loan_data:   # checking userid and if it finds, functions other task on the vary line
            print(f"\n-----------Loan Details-------------\n")
            print(f"Username : {loan_data[2]}")
            print(f"Loan ID : {loan_data[1]}")
            print(f"Types of Loan: {loan_data[4]}")
            print(f"Applied Loan Amount : Rs.{loan_data[5]}")
            print(f"Rate for Loan Amount : {loan_data[7]}%")
            print(f"Loan Tenure: {loan_data[6]} years")
            print(f"Date of Loan Applied : {loan_data[0]}")
            print(f"Installment Date : {loan_data[3]}")
            print(f"Total loan amount to pay: Rs.{loan_data[9]}")
            print(f"Monthly Installment Amount : Rs.{loan_data[8]}\n")
            goto_customer_menu(usr_name)

def goto_customer_menu(usr_name):
    inp_user = input("\nDo you want to go back to previous menu (y/n)?")
    if inp_user == 'y':
        registered_customer_menu(usr_name)
    else: 
        sys.exit()

def main_menu():
    print("\n\nMalaysia Bank Online Loan Management System (MBOLMS)\n\n")
    while True:
        try:
            print("""
      -------- Main Menu ----------    
            1. Admin
            2. New Customer 
            3. Registered Customer 
            4. Exit
            """)
            system_users = int(input("Select your login method from the following (1-3): "))
            print()

            if system_users == 1: # Admin
                admin_login()

            elif system_users == 2: # New customer
                new_customer_functions()
                
            elif system_users == 3: # registered customer
                reg_customer_login()

            elif system_users == 4: 
                print("Progarm has been closed successfully.\n")
                sys.exit()
                
            else:
                print("You made the wrong choice. Please select the choice between 1-3 !!!\n\n")

        except ValueError:
            print("\nNumber input are only acceptable !!!\n")
main_menu()