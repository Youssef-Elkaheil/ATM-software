# ATM software

## An ATM software with GUI that do the following:

1. The system first asks the user to enter his account number then click Enter

2. If the account number is not identified by the system, the system would show an error message
then reset

3. After the user enter the correct account number, the system would ask the user to enter the 
password. The user would have three trials to enter his password. Each time the password in 
incorrect, the system would ask the user to reenter the password showing to him a message that 
the password is incorrect.

4. If the password is entered incorrect for 3 successive times, the system would lock the account 
forever. And the user would be able to enter his account. If the user tried to enter a locked account, 
the system would show a message that this account is locked, please go to the branch.
Note, the password shall be shown as stars (*)

5. If the user entered a valid password, the system will give him the following options:

• Cash Withdraw 

• Cash Deposit 

• Balance Inquiry

• Password Change

• Fawry Service

• Exit

## Cash Withdraw

1. When the user choose the cash withdraw system, the system would ask the user to enter the 
desired amount to withdraw, if the balance covers this amount of balance, the system would 
call the function **ATM_Actuator_Out** which will provide the money to the client from the ATM 
outlet. This function takes the amount of money to be provided.
**Note:** Implement this function as an empty function, we would come back to it in the course in the HW part.

2. After the withdraw operation, the system shall print a thank you message and return to the 
home page.

3. Maximum allowed value per transaction is 5000 L.E

4. The allowed values are multiple of 100L.E, otherwise the system shall print not allowed value 
and ask the user to reenter the value

5. If the balance can not cover the withdraw value, the system shall print a message to the user 
telling him no sufficient balance then the system shall go to the home window.

## Balance Inquiry

When the user chooses this option, the system shall print the user balance as well as the user full 
name. The system would show a button with the text Ok when pressed, the system shall go to the 
home page.

## Password Change

When the user chooses this option, the system shall ask the user to enter the new password twice. 

The system shall accept only a password with a length four. The two passwords shall be matched in 
order to save. Otherwise the system would ask the user to repeat the operation.

## Fawry Service

The system provides 4 Fawry services which are:

1. Orange Recharge
2. Etisalat Recharge
3. Vodafone Recharge
4. We Recharge.

After the user chooses an option, the system would ask the user to enter the phone number and 
the amount of recharge. If the user balance would cover this operation, it would be done (Consider 
nothing to do for now) and the balance would be updated. If not, the system would print no 
sufficient balance then go to the home page.

------
ID | Data 
-- | -- 
215321701332    | 
-|  Name Ahmed Abdelrazek Mohamed 
-|  Password 1783
-|  Balance 3500166
203659302214 |
-|  Name Salma Mohamed Foaad
-|  Password 1390
-|  Balance 520001
126355700193    | 
-|  Name Adel Khaled Abdelrahman
-|  Password 1214
-|  Balance 111000
201455998011    | 
-|  Name Saeed Amin Elsawy
-|  Password 2001
-|  Balance 1200
201122369851    | 
-|  Name Amir Salama Elgendy
-|  Password 8935
-|  Balance 178933
201356788002    | 
-|  Name Wael Mohamed khairy
-|  Password 3420
-|  Balance 55000
203366789564    | 
-|  Name Mina Sameh Bishoy
-|  Password 1179
-|  Balance 18000
201236787812    | 
-|  Name Omnia Ahmed Awad
-|  Password 1430
-|  Balance 180350 
