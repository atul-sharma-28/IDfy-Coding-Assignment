# IDfy Coding Assignment
> Written in Python 3.6.1

This repository contains solutuons to both of the coding assignments.
* IP Address generator 
    * PROBLEM STATEMENT : Generate a list of all valid IP Addresses from a user input integer, without changing the order of the input digits.
* Flask Shopping Cart
    * PROBLEM STATEMENT : Create a shopping cart application, in which user can add items to the cart and the application then generates the final payable amount after applying necessary discounts.

## IP Address generator

For this problem, the code takes in an integer input from the user and stores it as a string for manipulation. It then checks the number of digits in the input integer continues forward only if they meet the constraint for valid number of digits for an IP address i.e 4 to 12. Upon verification the code generates all possible combinations of 3 indices within the string where '.' can be inserted to generate an IP Address. Corresponding IP addresses are then created, stored in a list and compared to a regex of a valid IP Address. This filters out only the valid IP Addresses from the interim list.

### Running the code

```
python3 ipaddress.py
```

## Flask Shopping Cart

For this problem, I created a database using sqlite3 which comprised of tables for products, cart, discounts and discount conditions. The program allows user to add products of user specified quantities to the cart. Upon adding items to the cart, the program then calculates the highest possible discount applicable, while avoiding item quantity overflow and redundant discounts, with the constraint of MAX_NO_OF_DISCOUNTS_APPLIED = 3. This value can be increased or decereased based on computing and time constraints.

### Database Tables

* Products table:

|product_id          |product_name|product_price|
|--------------------|------------|-------------|
|12120001            |Product A   |199.0        |
|12120002            |Product B   |399.0        |
|12120003            |Product C   |449.0        |
|12120004            |Product D   |499.0        |
|12120005            |Product E   |249.0        |
|12120006            |Product F   |249.0   	    |


* Discount Conditions tabe:

|condition_id        |condition_verb|itemA_qty |itemA_id  |boolean_condition|itemB_qty |itemB_id  	|
|--------------------|--------------|----------|----------|-----------------|----------|----------	|
|1                   |BUYS          |1         |12120001  |AND              |2         |12120005  	|
|2                   |BUYS          |2         |12120001  |AND              |2         |12120002  	|
|3                   |BUYS          |2         |12120002  |AND              |1         |12120004  	|
|4                   |BUYS          |1         |12120003  |AND              |1         |12120005	  |



* Discounts table:

|discount_id         |condition_id|discount_price|
|--------------------|------------|--------------|
|1                   |1           |199.0         |
|2                   |2           |249.0         |
|3                   |3           |149.0         |
|4                   |4           |99.0        	 |


### Running the code

```
python3 app.py
```

### Test Case

Steps 1-3 can be performed in any order

* Add “Product A - Qty = 3” . 
* Add “Product B - Qty = 2” . 
* Add “Product E - Qty = 2” . 
* Check Cart . 
* Remove “Product B” and/or “Product E” and view change in discount .
