import streamlit as st
import random
class Bank:
    bank_name = "Apna Bank"
    def __init__(self, branch_name, branch_deposit=0):
        self.branch_name = branch_name
        self.branch_deposit = branch_deposit
        self.branch_accounts = []

    def open_account(self, cnic, account_title, initial_deposit=0):
        account = {
            'cnic': cnic,
            'title': account_title,
            'balance': initial_deposit,
            'account_number': random.randint(1000, 9999),
            'pin': random.randint(1000, 9999),
        }
        self.branch_deposit += initial_deposit
        self.branch_accounts.append(account)
        return account
    
    def show_balance(self, account_number, pin):
        for acc in self.branch_accounts:
            if acc['account_number'] == account_number:
                if acc['pin'] == pin:
                    return acc['balance'], None
                else:
                    return None, "Invalid Pin"
        return None, "Account Not Found"

    def deposit_amt(self, account_number, amount):
        for acc in self.branch_accounts:
            if acc['account_number'] == account_number:
                acc['balance'] += amount
                return acc['balance'], None
        return None, "Account Not Found"

    def withdraw_amt(self, account_number, pin, amount):
        for acc in self.branch_accounts:
            if acc['account_number'] == account_number:
                if acc['pin'] != pin:
                    return None, "Invalid Pin"
                if amount > acc['balance']:
                    return None, "Insufficient Balance"
                acc['balance'] -= amount
                return acc['balance'], None
        return None, "Account Not Found"

    def transfer_amt(self, account_number, pin, amount, beneficiary_acc):
        sender = None
        receiver = None

        for acc in self.branch_accounts:
            if acc['account_number'] == account_number:
                sender = acc
            if acc['account_number'] == beneficiary_acc:
                receiver = acc

        if not sender:
            return None, "Sender Account Not Found"
        if not receiver:
            return None, "Beneficiary Account Not Found"
        if sender['pin'] != pin:
            return None, "Invalid Pin"
        if sender['balance'] < amount:
            return None, "Insufficient Balance"

        sender['balance'] -= amount
        receiver['balance'] += amount
        return sender['balance'], None

    def show_all_accounts(self):
        return self.branch_accounts
# ----------------------------
# Initialize Bank Branch
# ----------------------------
if "branch1" not in st.session_state:
    st.session_state.branch1 = Bank("Mehran", 0)

branch1 = st.session_state.branch1

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="Banking System", page_icon="🏦")

st.title("🏦 Simple Banking System")
st.write("Manage Accounts — Open, Check Balance, Deposit, Withdraw, and Transfer")

menu = st.sidebar.selectbox(
    "Select Action",
    ["Open Account", "Check Balance", "Deposit", "Withdraw", "Transfer", "Show All Accounts"]
)

# -----------------------------------
# Open Account
# -----------------------------------
if menu == "Open Account":
    st.header("➕ Open New Bank Account")

    cnic = st.text_input("Enter CNIC")
    title = st.text_input("Account Title")
    deposit = st.number_input("Initial Deposit", min_value=0)

    if st.button("Create Account"):
        if cnic == "" or title == "":
            st.error("Please enter CNIC and Account Title")
        else:
            acc = branch1.open_account(cnic, title, deposit)
            st.success("Account Created Successfully!")
            st.write(f"**Account Number:** {acc['account_number']}")
            st.write(f"**PIN:** {acc['pin']} (Save this!)")

# -----------------------------------
# Check Balance
# -----------------------------------
elif menu == "Check Balance":
    st.header("💰 Check Balance")

    acc_no = st.number_input("Enter Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999)

    if st.button("Show Balance"):
        bal, err = branch1.show_balance(acc_no, pin)
        if err:
            st.error(err)
        else:
            st.success(f"Your Current Balance: **Rs {bal}**")

# -----------------------------------
# Deposit Amount
# -----------------------------------
elif menu == "Deposit":
    st.header("📥 Deposit Amount")

    acc_no = st.number_input("Enter Account Number", min_value=1000, max_value=9999)
    amt = st.number_input("Deposit Amount", min_value=1)

    if st.button("Deposit"):
        bal, err = branch1.deposit_amt(acc_no, amt)
        if err:
            st.error(err)
        else:
            st.success(f"Amount Deposited! New Balance: **Rs {bal}**")

# -----------------------------------
# Withdraw Amount
# -----------------------------------
elif menu == "Withdraw":
    st.header("📤 Withdraw Money")

    acc_no = st.number_input("Enter Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("Enter PIN", min_value=1000, max_value=9999)
    amt = st.number_input("Withdraw Amount", min_value=1)

    if st.button("Withdraw"):
        bal, err = branch1.withdraw_amt(acc_no, pin, amt)
        if err:
            st.error(err)
        else:
            st.success(f"Withdrawal Successful! Remaining Balance: **Rs {bal}**")

# -----------------------------------
# Transfer Money
# -----------------------------------
elif menu == "Transfer":
    st.header("💸 Transfer Money")

    acc_no = st.number_input("Sender Account Number", min_value=1000, max_value=9999)
    pin = st.number_input("Sender PIN", min_value=1000, max_value=9999)
    amt = st.number_input("Amount", min_value=1)
    ben = st.number_input("Beneficiary Account Number", min_value=1000, max_value=9999)

    if st.button("Transfer"):
        bal, err = branch1.transfer_amt(acc_no, pin, amt, ben)
        if err:
            st.error(err)
        else:
            st.success(f"Transfer Successful! Sender Remaining Balance: **Rs {bal}**")

# -----------------------------------
# Show All Accounts
# -----------------------------------
elif menu == "Show All Accounts":
    st.header("📋 All Accounts")

    if st.button("Load All Accounts"):
        data = branch1.show_all_accounts()
        if len(data) == 0:
            st.warning("No Accounts Found")
        else:
            st.table(data)
