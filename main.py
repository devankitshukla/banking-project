from oop import *
Dhruv = BankAccount(1000,"Dhruv","Punjab")
Jyotshna = BankAccount(1500,"Jyotshna","Delhi")

Dhruv.getBalance()
Jyotshna.getBalance()

Dhruv.deposit(500)
Jyotshna.withdraw(150)

Dhruv.transfer(2000,Jyotshna)
Jyotshna.transfer(50,Dhruv)

# Customer Created Reward Account
Shyam = InterestRewardAccount(2000,"Shyam","Mumbai")
Shyam.getBalance()
Shyam.deposit(500)
Shyam.getBalance()

#Customer Created Saving Account
Tirth = SavingAccount(3000,"Tirth", "Ahmedabad")
Tirth.getBalance()
Tirth.deposit(300)
Tirth.getBalance()

#Joint Account For Childrens
Shruti = JointAccount(1500,"Shruti","Devankit", "Ahmedabad")
Shruti.getOwners()
Shruti.deposit(50)
Shruti.getBalance()



#Final Testing Of Multiple Transaction At Once

Shyam.transfer(250,Jyotshna)
Shyam.transfer(500,Dhruv)
Jyotshna.transfer(500,Tirth)
Dhruv.transfer(70,Shyam)
Tirth.transfer(250,Jyotshna)

#Final Balance 

Dhruv.getBalance()

Jyotshna.getBalance()

Shyam.getBalance()

Tirth.getBalance()


Tirth.applyInterest()

# checking transation history
Tirth.getStatement()
Shyam.getStatement()
Dhruv.getStatement()
Jyotshna.getStatement()

#Opening A FD 
Tirth = FixedDepositAccount(5000,"Tirth","Ahmedabad")
Tirth.showDetails()

#   Getting Account info

Tirth.getInfo()
Jyotshna.getInfo()
Dhruv.getInfo()
Shyam.getInfo()
Shruti.getInfo()
