import time
import pandas as pd

# author Arvind kumar

import pyodbc
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ARVIND-PC;'
                      'Database=bigdata;'
                      'Trusted_Connection=yes;')
cur = conn.cursor()

class jweller:
    def __init__(self):
        jweller.display_option(self)


    def display_option(self):
        print("=" * 5, " WEL-COME TO JWELLERY STORE ", "=" * 5)
        print("1. ADD CUSTOMER DETAIL")
        print("2. SEARCH CUSTOMER DETAIL")
        print("3. UPDATE CUSTOMER DETAIL")
        print("4. DELETE CUSTOMER DETAIL")
        print("5. EXIT")
        while True:
            try:
                option = int(input("Enter Any One Option >>"))

            except(ValueError):
                print("OOP ! sorry u entered something wrong try right option...")
                continue

            else:
                if (option == 1):
                    jweller.add_detail(self)
                elif (option == 2):
                    jweller.search_detail(self)
                elif (option == 3):
                    jweller.update_detail(self)
                elif (option == 4):
                    jweller.delete_detail(self)
                elif (option == 5):
                    exit()
                else:
                    print("OOP ! sorry u entered wrong input try again..")
                    continue
#===========================================================================================================================
    def add_detail(self):
        while True:
            print("\n\n")
            print('/' * 5, ' welcome to add detail ', '/' * 5,'\n')
            print('1. Add New Customer Details')
            print('2. Add Customer Item Details')
            print("3. Exit\n")
            while True:
                try:
                    option = int(input("Enter Any One Option >>"))
                except ValueError:
                    print("oop ! you entered something wrong pls try again...")
                    continue
                else:
                    if (option == 1):
                        jweller.add_new_cust(self)
                    elif (option == 2):
                        jweller.validate_cust_for_item(self)
                    elif (option == 3):
                        jweller.display_option(self)
                    else:
                        print("OOP ! sorry u entered wrong input try again..1")

    def add_new_cust(self):
        c_mob=int()
        print('====== welcome add new customer ========')
        c_name=input("Enter Customer Fullname : ").upper()
        while True:
            c_mob=input('Enter Customer Mob :')
            if(c_mob.isnumeric() and len(c_mob)<=11):
                break
            else:
                continue
        c_add=str(input("Enter Customer Address :")).upper()

        import datetime
        dt=datetime.datetime.now()
        cur=conn.cursor()

        query="insert into customer_detail(cust_name,cust_mob,cust_add,date_of_entry) values(?,?,?,?)"
        cur.execute(query,(c_name,c_mob,c_add,dt))
        print('added')
        conn.commit()
        jweller.add_detail(self)


    def validate_cust_for_item(self):
        cur = conn.cursor()

        while True:
            option = input('Enter Customer Anyone (Mobile/id \n:')
            opt = (option,)
            if (option.isnumeric() and len(option) == 10):

                cur.execute('select * from customer_detail where cust_mob=?', opt)
                row = cur.fetchone()
                if  row:
                    print('\nID :', row[0])
                    print('Name :', row[1])
                    print('Mob :', row[2])
                    print('Address :', row[3])
                    print('Date of Entry :', row[5])
                    while True:
                        id=row[0]

                        option2=input("\nif information is correct (y/n) :").upper()
                        if(option2=='Y'):
                            jweller.add_cust_item(self,id)
                        elif(option2=='N'):
                            print("\n Sorry You Entered Some  wrong Pls Check and try again")
                            break
                        else:
                            continue
                else:
                    print("id didn't found")
            elif (option.isnumeric() and len(option) <= 8):
                cur.execute('select * from customer_detail where cust_id=?', opt)
                row = cur.fetchone()
                if  row:
                    print('ID :', row[0])
                    print('Name :', row[1])
                    print('Mob :', row[2])
                    print('Address :', row[3])
                    print('Due Amount :', row[4])
                    print('Date of Entry :', row[5])
                else:
                    print("id didn't found")
                    continue
                while True:
                    id=row[0]
                    print(id)
                    option1 = str(input("\n if information is Correct (y/n) :")).upper()
                    if (option1 == 'Y'):
                        jweller.add_cust_item(self,id)
                    elif(option1=='N'):
                        print("\n Sorry You Entered Some  wrong Pls Check and try again")
                        break

                    else:
                        continue

            else:
                print("entered wrong...")
                continue

    def add_cust_item(self,id):
        print('\n ====== welcome add customer item =======\n')
        item_name=str(input("Enter Item Name :")).upper()
        item_type=str(input("Enter Item Type Like(Gold/silver/other) :")).upper()
        item_weight=str(input("Enter Item Weight :")).upper()
        while True:
            try:
                item_amt=int(input("Enter Item Amount :"))
                item_dep_amt=int(input("Enter Item Dep Amount :"))

            except ValueError:
                print("oop! entered wrong try again")
                continue
            else:
                due=item_amt-item_dep_amt
                import datetime
                dt = datetime.datetime.now()
                cur.execute("""insert into cust_item_detail(item_name,item_type,item_weight,item_amt,item_dep_amt,item_due_amt,item_date,c_id)
                    values(?,?,?,?,?,?,?,?)""",(item_name,item_type,item_weight,item_amt,item_dep_amt,due,dt,id))
                cur.execute('select item_due_amt from cust_item_detail where c_id=?',(id))
                row=cur.fetchall()
                ls=[]

                for x in row:
                    for y in x:
                        ls.append(y)
                s = sum(ls)
                cur.execute('update customer_detail set cust_due_pay=? where cust_id=?',(s,id))
                conn.commit()
            print("added item")
            jweller.add_detail(self)
# ==================================================================================================

    def search_detail(self):
        print('/' * 5, ' welcome to search detail ', '/' * 5)
        key=input("Enter Customer (ID/Mob) :")
        if (key.isnumeric() and len(key) == 10):
            cur.execute('select * from customer_detail where cust_mob=?',(key,))
            row = cur.fetchone()
            if row:
                print('\nID :', row[0])
                print('Name :', row[1])
                print('Mob :', row[2])
                print('Address :', row[3])
                print('Date of Entry :', row[5])
                print("\n")
                df=pd.read_sql('select * from customer_detail',conn)
                dt=df.loc[df['cust_mob']==key,'cust_id']
                k=dt[0]
                df1 = pd.read_sql('select * from cust_item_detail',conn)
                dt1=df1.loc[df1['c_id']==k,'item_id':'item_date']
                print(dt1)
                jweller.display_option(self)
        elif(key.isnumeric() and len(key)<=10):

            cur.execute('select * from customer_detail where cust_id=?', (key,))
            row = cur.fetchone()
            if row:
                print('\nID :', row[0])
                print('Name :', row[1])
                print('Mob :', row[2])
                print('Address :', row[3])
                print('Due Amount :',row[4])
                print('Date of Entry :', row[5])
                print("\n")

                df = pd.read_sql('select * from customer_detail', conn)
                rt=df.loc[df['cust_id']==key,'cust_due_pay']
                if(rt.empty):
                    print('this cust No Any Items')
                    jweller.display_option(self)
                else:
                    dt = df.loc[df['cust_id'] == key, 'cust_id']
                    k = dt[0]
                    df1 = pd.read_sql('select * from cust_item_detail', conn)
                    dt1 = df1.loc[df1['c_id'] == k, 'item_id':'item_date']
                    print(dt1)



                jweller.display_option(self)

            else:
                print("id didn't found")
            conn.commit()
#====================================================================================================

    def update_detail(self):
        print('/' * 5, ' welcome to update detail ', '/' * 5)
        print("1. update customer detail\n2.update item detail")
        while True:
            try:
                option=int(input('Enter anyone option :'))
            except ValueError:
                print('entered wrong try again')
                continue
            else:
                if(option == 1):
                    jweller.update_customer(self)
                elif(option == 2):
                    jweller.update_item_detail(self)
                else:
                    continue



    def update_customer(self):
        print('update customer')
        while True:
            try:
                id = int(input('Enter Customer Id :'))
            except ValueError:
                print("OOP ! you entered wrong pls enter right option")
                continue
            else:
                cur.execute('select cust_id from customer_detail where cust_id=?',(id,))
                row=cur.fetchone()
                while True:
                    if row:
                        print("=========== what do you want update ===========")
                        print("1.Customer Name")
                        print("2.Customer Mob Number ")
                        print("3.Customer Address")
                        key = int(input("Enter Anyone option :"))
                        if (key == 1):
                            name = str(input("Enter New Name :")).upper()
                            cur.execute('update customer_detail set cust_name=? where cust_id=?', (name, id))
                            print("Information updated")
                            conn.commit()
                            jweller.display_option(self)
                        elif (key == 2):
                            while True:
                                mob = input("Enter New Mob Number :")
                                if (mob.isnumeric() and len(mob) == 10):
                                    cur.execute('update customer_detail set cust_mob=? where cust_id=?', (mob, id))
                                    print("Information updated")
                                    conn.commit()
                                    jweller.display_option(self)
                                else:
                                    print("sorry u entered wrong try again")
                                    continue
                        elif (key == 3):
                            add = str(input("Enter New address :")).upper()
                            cur.execute('update customer_detail set cust_add=? where cust_id=?', (add, id))
                            print("Information updated")
                            conn.commit()
                            jweller.display_option(self)

                        else:
                            print('sorry u entered wrong try again')
                            continue

    def update_item_detail(self):
        print("update item detail")
        while True:
            try:
                id = int(input('Enter Customer Id :'))
            except ValueError:
                print("OOP ! you entered wrong pls enter right option")
                continue
            else:
                cur.execute('select * from customer_detail where cust_id=?',(id,))
                row=cur.fetchone()
                if row:
                    print("Customer ID :",row[0])
                    print("Customer Name :", row[1])
                    print("Customer Mob :", row[2])
                    print("Customer Address :", row[3])
                    print("Customer Due Amount :", row[4])
                    df=pd.read_sql('select * from cust_item_detail',conn)

                    items=df.loc[df['c_id']==id,'item_id':'item_date']
                    if not items.empty:
                        print(items)
                        info = str(input("\nIf You want this Customer items information update (y/n) :")).upper()
                        if (info == 'Y'):
                            it_id=int(input("Enter Item ID :"))

                            cur.execute('select item_id from cust_item_detail where item_id=?',(it_id,))
                            row=cur.fetchone()
                            if row:
                                print("======= WHAT YOU WANT UPDATE ITEM DETAIL =======")
                                print("1.Item Name")
                                print("2.Item Type")
                                print("3.Item Weight")
                                print("4.Item Amt")
                                print("5.Item Dep Amt")
                                key = int(input("Enter Anyone option :"))
                                if (key == 1):
                                    name = str(input("Enter New Item Name :")).upper()
                                    cur.execute('update cust_item_detail set item_name=? where item_id=?', (name,it_id))
                                    print("Information updated")
                                    conn.commit()
                                    jweller.display_option(self)
                                elif (key == 2):
                                    type = str(input("Enter New Item Type :")).upper()
                                    cur.execute('update cust_item_detail set item_type=? where item_id=?', (type, it_id))
                                    print("Information updated")
                                    conn.commit()
                                    jweller.display_option(self)
                                elif (key == 3):
                                    weight = str(input("Enter New Item Weight :")).upper()
                                    cur.execute('update cust_item_detail set item_weight=? where item_id=?', (weight,it_id))
                                    print("Information updated")
                                    conn.commit()
                                    jweller.display_option(self)
                                elif (key == 4):
                                    it_amt = int(input("Enter New Item Amount :"))
                                    cur.execute('update cust_item_detail set item_amt=? where item_id=?', (it_amt,it_id))
                                    conn.commit()
                                    cur.execute('select item_dep_amt from cust_item_detail where item_id=?',(it_id))
                                    row=cur.fetchall()
                                    s=float()
                                    if row:
                                        for x in row:
                                            for y in x:
                                                s=it_amt-y
                                    conn.commit()
                                    cur.execute('update cust_item_detail set item_due_amt=? where item_id=?',(s,it_id))
                                    conn.commit()
                                    cur.execute('select item_due_amt from cust_item_detail where c_id=?',(id))
                                    rows=cur.fetchall()
                                    total=0
                                    for row in rows:
                                        total+=row[0]
                                    conn.commit()
                                    cur.execute('update customer_detail set cust_due_pay=? where cust_id=?',(total,id))
                                    conn.commit()
                                    print("Information updated")
                                    jweller.display_option(self)
                                elif (key == 5):
                                    dp_amt = int(input("Enter New deposit Amount :"))
                                    cur.execute('update cust_item_detail set item_dep_amt=? where item_id=?',(dp_amt,it_id))
                                    conn.commit()
                                    cur.execute('select item_amt from cust_item_detail where item_id=?',(it_id))
                                    row=cur.fetchone()
                                    due=0
                                    for x in row:
                                        due=x-dp_amt
                                    conn.commit()
                                    cur.execute('update cust_item_detail set item_due_amt=? where item_id=?',(due,it_id))
                                    conn.commit()
                                    total=0
                                    cur.execute('select item_due_amt from cust_item_detail where c_id=?',(id))
                                    rows=cur.fetchall()
                                    for row in rows:
                                        total+=row[0]
                                    conn.commit()
                                    cur.execute('update customer_detail set cust_due_pay=? where cust_id=?',(total,id))
                                    conn.commit()
                                    print('information updated')
                                    jweller.display_option(self)
                                else:
                                    print("you entered wrong try again")
                                    continue
                    else:
                        print("this customer didn't found any item info..try other")
                        continue
                else:
                    print("sorry id didn't found")
                    continue
#====================================================================================================

    def delete_detail(self):
        print('/' * 5, ' welcome to delete detail ', '/' * 5)
        while True:
            try:
                id=int(input("Enter Customer id you want to delete :"))
            except ValueError:
                print("Sorry! you entered something wrong")

            else:
                cur.execute('select cust_due_pay from customer_detail where cust_id=?',(id))
                row=cur.fetchone()
                conn.commit()
                for x in row:
                    if(x==0.0000):
                        cur.execute('select * from customer_detail where cust_id=?', (id,))
                        row = cur.fetchone()
                        conn.commit()
                        if row:
                            print("Customer ID :", row[0])
                            print("Customer Name :", row[1])
                            print("Customer Mob :", row[2])
                            print("Customer Address :", row[3])
                            print("Customer Due Amount :", row[4])
                            while True:
                                opt = str(input("if you really want delete permanently this record(y/n) :")).upper()
                                if (opt == 'Y'):
                                    cur.execute('delete from cust_item_detail where c_id=?', (id))
                                    conn.commit()
                                    cur.execute('delete from customer_detail where cust_id=?', (id))
                                    print("record has been deleted.")
                                    conn.commit()
                                    break
                                elif (opt == 'N'):
                                    break
                                else:
                                    continue
                    elif(x==None):
                        cur.execute('delete from customer_detail where cust_id=?', (id))
                        print("record has been deleted.")

                        conn.commit()
                        jweller.display_option()
                    else:
                        print('OOP! STILL MIGHT THIS CUSTOMER DUE AMOUNT OR  U CAN\'T DELETE THIS RECORD ')
                        continue


j = jweller()

