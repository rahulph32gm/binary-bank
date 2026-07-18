import json
from pathlib import Path
import random
from datetime import datetime
import string

class Bank:
    """
    Binary Bank (BB) - A secure, modular banking system.
    Developed by: Rahulee (Hubballi's Rising Developer)
    """
    database = "data.json"
    __data = [] # Private class variable for data security (Encapsulation)
    
    # Rules dictionary for easy management of T&C
    tc_rules = {
        "eligibility": "1. Eligibility: Minimum age must be 18 years.",
        "min_balance": "2. Minimum Balance: Zero balance account.",
        "dep_limit": "3. Deposit Limit: Max 50,000 per transaction.",
        "security": "4. PIN Security: Do NOT share your 4-digit PIN.",
        "data_privacy": "5. Data: Your data is stored locally.",
        "withdraw_limit": "6. Withdrawal: Max 25,000 per transaction.",
        "update_policy": "7. Update Policy: Only Phone, Email, and PIN can be updated after account creation."
    }
    
    # Initializing the database: Loads data from JSON if it exists
    try:
        if Path(database).exists():
            with open(database) as file:
                __data = json.loads(file.read())
        else:
            __data = []
    except Exception as err:
        pass
    
    @classmethod
    def __accountNum(cls):
        acc = random.choices(string.digits, k=14)
        return int("".join(acc))
    
    @classmethod
    def __update(cls):
        with open(Bank.database, "w") as fs:
            fs.write(json.dumps(Bank.__data))
            
    def terms_and_conditions(self):
        t_and_c = """
        ====================================================
                    WELCOME TO BINARY BANK (BB) 🏦
        ====================================================
        1. Eligibility: Minimum age must be 18 years.
        2. Minimum Balance: Zero balance account (Special for BB).
        3. Deposit Limit: Max 50,000 per transaction.
        4. PIN Security: Do NOT share your 4-digit PIN with anyone.
        5. Data: Your data is stored locally in 'data.json'.
        6. Withdrawal: Maximum 25,000 per transaction.
        7. Update Policy: Only Phone, Email, and PIN can be updated after account creation.
        ====================================================
        """
        print(t_and_c)
    
    def valid_mail(self, email):
        return email.endswith("@gmail.com")
    
    def valid_contect(self, num):
        return len(str(num)) == 10
    
    def valid_pin(self, pin):
        return len(str(pin)) == 4
        
    def creatAccount_logic(self, info):
        dob_obj = datetime.strptime(info["DOB"], "%d-%m-%Y")
        today = datetime.today()
        age = today.year - dob_obj.year - ((today.month, today.day) < (dob_obj.month, dob_obj.day))
        info["Age"] = age
        info["Account_num"] = Bank.__accountNum()
        info["Balance"] = 0
        
        Bank.__data.append(info)
        Bank.__update()
        return info["Account_num"]
    
    def varification_logic(self, acc, pin):
        for i in Bank.__data:
            if i["Account_num"] == acc and i["PIN"] == pin:
                return i
        return None
    
    def create_account(self):
        print("Carefully read T&C")
        self.terms_and_conditions()
        exct = int(input("1 for accept: "))
        if exct == 1:
            print("Thanks for your convenience")
            print("Fill the details to Create an Account in BB")
            info = {
                "First_Name": input("First Name(as it is in Identity Card): "),
                "Last_Name": input("Last Name: "),
                "DOB": input("Date of Birth(DD-MM-YYYY): "),
                "PIN": int(input("PIN(4-Digits): ")),
                "Email": input("E-Mail: "),
                "gender": input("Gender(M/ F/ O): ").upper(),
                "Phone_num": int(input("Contact Number: ")),
                "Account_num": Bank.__accountNum(),
                "Balance": 0
            }
            
            dob_obj = datetime.strptime(info["DOB"], "%d-%m-%Y")
            today = datetime.today()
            age = today.year - dob_obj.year - ((today.month, today.day) < (dob_obj.month, dob_obj.day))
            info["Age"] = age
            
            if (info["gender"] in ["M", "F", "O"]) and (len(info["gender"]) == 1):
                if info["Age"] >= 18:
                    if self.valid_pin(info["PIN"]):
                        if self.valid_mail(info["Email"]):
                            if self.valid_contect(info["Phone_num"]):
                                Bank.__data.append(info)
                                Bank.__update()
                                print("Thanks for being a member of BB society")
                            else:
                                print("Invalid Contact details :(")
                        else:
                            print("Invalid Email :(")
                    else:
                        print("Read T&C carefully once again\n", Bank.tc_rules["security"])
                else:
                    print("Please read T&C carefully once again\n", Bank.tc_rules["eligibility"])
            else:
                print("Invalid Gender")
        else:
            print("Sorry for inconvenience but Account holder should agree with BB conditions")
    
    def varification(self):
        print("Before moving forward please verify: ")
        acc = int(input("AC number: "))
        pin = int(input("PIN: "))
        for i in Bank.__data:
            if i["Account_num"] == acc and i["PIN"] == pin:
                # 🔥 FIXED F-STRING STRUCTURAL QUOTES OVERRIDE
                print(f"Varification complite\nNamaste {i['First_Name']} {i['Last_Name']}")
                return i
        return None
    
    def deposit(self, user):
        amount = float(input("Enter Amount: "))
        if amount < 50000 and amount > 0:
            user["Balance"] += amount
            Bank.__update()
            return f"Rs {amount} deposited successfully\ncurrent Balance is: {user['Balance']}"
        else:
            return f"read T&C carefully\n, {Bank.tc_rules['dep_limit']}"

    def withdrawal(self, user):
        amount = float(input("Enter Amount: "))
        if user["Balance"] >= amount and amount <= 25000:
            user["Balance"] -= amount
            Bank.__update()
            return f"Rs {amount} drew successfully current\n balance: {user['Balance']}"
        if user["Balance"] <= amount:
            return f"insufficient funds\nBalance available: {user['Balance']}"
        if amount > 25000:
            return f"read T&C carefully\n {Bank.tc_rules['withdraw_limit']}"
            
    def transaction(self):
        user = self.varification()
        if user:
            inp = int(input("Press 1 to Deposit\nPress 2 to Withdraw: "))
            if inp == 1:
                dep_amount = self.deposit(user)
                print(dep_amount)
            if inp == 2:
                wit_amount = self.withdrawal(user)
                print(wit_amount)
        else:
            print("user not found")
    
    def details(self):
        user = self.varification()
        if user:
            print("Account details: ")
            for key, values in user.items():
                print(f"{key}:  {values}")
        else:
            print("user not found")
    
    def updateAC(self):
        user = self.varification()
        if not user:
            print("user not found")
            return
        print(Bank.tc_rules["update_policy"])
        new_pin = input("Update PIN else press enter: ") or user["PIN"]
        if new_pin != user["PIN"]:
            if self.valid_pin(new_pin):
                user["PIN"] = int(new_pin)
            else:
                print(Bank.tc_rules["security"])
        new_mail = input("Update mail address else press enter: ") or user["Email"]
        if new_mail != user["Email"]:
            if self.valid_mail(new_mail):
                user["Email"] = new_mail
            else:
                print("Not valid Email")
        new_num = input("Update contact details else press enter: ") or user["Phone_num"]
        if new_num != user["Phone_num"]:
            if self.valid_contect(new_num):
                user["Phone_num"] = int(new_num)
            else:
                print("Not valid Contact details")
        print("Account Details updated successfully")
        for i, j in user.items():
            print(i, j)
        Bank.__update()

    def delete(self):
        user = self.varification()
        if user:
            confirmation = input("press 'y' to give confirmation to delete account from BB: ").lower()
            if confirmation == "y":
                Bank.__data.remove(user)
                Bank.__update()
    
    def main_menu(self):
        border = "=" * 50
        header = "WELCOME TO BINARY BANK (BB) 🙏🏻"
        
        print(f"\n{border}")
        print(header.center(50))
        print(border)
        
        print("\nHow can we help you today? 🤝")
        print("-" * 50)
        
        services = [
            "📜 1. Terms and Conditions",
            "🆕 2. Create Account in BB",
            "💸 3. Transactions (Deposit/Withdraw)",
            "🔍 4. View Account Details",
            "📝 5. Update Account Details",
            "⚠️ 6. Delete Account (Danger Zone)",
            "🚪 0. Exit Bank"
        ]
        
        for service in services:
            print(f"    {service}")
            
        print("-" * 50)
        choice = input("\nSelect an option (0-6) ➔ ")
        if choice == "1":
            self.terms_and_conditions()
        elif choice == "2":
            self.create_account()
        elif choice == "3":
            self.transaction()
        elif choice == "4":
            self.details()
        elif choice == "5":
            self.updateAC()
        elif choice == "6":
            self.delete()
        elif choice == "0":
            print("Thanks for visiting :)\nHave a nice day")
            return 0
        
        return "continue"

if __name__ == "__main__":
    user = Bank()
    while True:
        status = user.main_menu()
        if status == 0:
            break
