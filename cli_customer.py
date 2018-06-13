def welcome_client():
    print("Welcome to Mike Will Made Inc.")
    time.sleep(2)
    print("If you are a new customer to Mike Will Made Inc. please refer to the help opperator...")
    time.sleep(2)
    print("If you are already an account holder you may proceed. ")

    print("1. Account holder")
    print('2. Exit')

    reply = input("> ") 

    if reply == '1' or reply == 'Account holder':
        print('Thank you for choosing Mike Will Made Inc. Please proceed..')
        time.sleep(3)
        client_info()
        

# This function is for customers who are checking in on their personal information
def client_info():
    print("Welcome back! Please enter your name and access code to view your personal account...")

    name = input('Name: ')
    code = input('4-digit pin: ')