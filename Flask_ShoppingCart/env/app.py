from flask import *
import sqlite3 as sql
import hashlib, os, itertools, copy

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'nuttertools'
cart_items = list()

@app.route('/')
def show_products():
	with sql.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute('SELECT product_id, product_name, product_price FROM products')
		itemData = cur.fetchall()
	itemData = parse(itemData)
	return render_template('index.html', items = itemData)
	
@app.route('/cart')
def cart():
	with sql.connect('database.db') as conn:
		cur = conn.cursor()
		cur.execute("SELECT products.product_id, products.product_name, products.product_price, cart.product_qty FROM products, cart WHERE products.product_id = cart.product_id")
		products = cur.fetchall()
	products = parse_cart(products)
	print(products)
	totalPrice = 0
	discount = getDiscounts(products)
	for product in products:
		totalPrice += product["product_price"] * product["product_qty"]
	return render_template('cart.html', items = products, total_price = totalPrice, discount = discount)

@app.route("/addToCart", methods=['POST'])
def addToCart():
	productId = int(request.args.get('productId'))
	qty = int(request.form['qty'])
	if qty > 0:
		with sql.connect('database.db') as conn:
			cur = conn.cursor()
			cur.execute('SELECT product_id, product_qty FROM cart WHERE product_id = ?',(productId,))
			product = cur.fetchall()
			if len(product) == 0:
				try:
					cur.execute("INSERT INTO cart(product_id, product_qty) VALUES(?,?)", (productId,qty))
					conn.commit()
					msg = "Added successfully"
				except Exception as ex:
					conn.rollback()
					msg = ex
				print(msg)
			else:
				qty_in_cart = product[0][1]
				try:
					cur.execute("UPDATE cart SET product_qty = ? WHERE product_id = ?;",(qty_in_cart+qty, productId))
					conn.commit()
					msg = "Updated successfully"
				except Exception as ex:
					conn.rollback()
					msg = ex
				print(msg)
		conn.close()
	return redirect(url_for('show_products'))

@app.route("/removeFromCart", methods=['POST'])
def removeFromCart():
	productId = int(request.args.get('productId'))
	with sql.connect('database.db') as conn:
		cur = conn.cursor()
		try:
			cur.execute("DELETE FROM cart WHERE product_id = ?", (productId,))
			conn.commit()
			msg = "Removed successfully"
		except Exception as ex:
			conn.rollback()
			msg = ex
		print(msg)
	conn.close()
	return redirect(url_for('cart'))

def parse(data):
    list_of_dicts = []
    for tuple in data:
    	temp_dict = dict()
    	temp_dict["product_id"] = tuple[0]
    	temp_dict["product_name"] = tuple[1]
    	temp_dict["product_price"] = tuple[2]
    	list_of_dicts.append(temp_dict)
    return list_of_dicts
    
def parse_cart(data):
    list_of_dicts = []
    for tuple in data:
    	temp_dict = dict()
    	temp_dict["product_id"] = tuple[0]
    	temp_dict["product_name"] = tuple[1]
    	temp_dict["product_price"] = tuple[2]
    	temp_dict["product_qty"] = tuple[3]
    	list_of_dicts.append(temp_dict)
    return list_of_dicts

def getDiscounts(cartProducts):
	discount = 0
	conditionsMet = []
	discountsArr = []
	with sql.connect('database.db') as conn:
		cur = conn.cursor()
		discountArr = []
		for item in cartProducts:
			cur.execute('SELECT condition_id, itemB_id, itemB_qty FROM conditions WHERE itemA_id = ? AND itemA_qty <= ?',(item["product_id"],item["product_qty"]))
			itemData = cur.fetchall()
			for item in itemData:
				if any(product['product_id'] == item[1] and product['product_qty'] >= item[2] for product in cartProducts):
					conditionsMet.append(item[0])
		for conditionId in conditionsMet:
			 cur.execute('SELECT condition_id, discount_price FROM discounts WHERE condition_id = ?',(conditionId,))
			 discountsArr += cur.fetchall()
		print(discountsArr)
		discount = getIdealDiscount(discountsArr, copy.deepcopy(cartProducts))
		'''for discountPrice in idealDiscount:
			discount += discountPrice[1]'''
	return discount

def getIdealDiscount(discountsArr, cartProducts):
	discount = 0
	possibleDiscounts = []
	discountCount = 1
	if len(discountsArr) >= 3:
		discountCount = 3
	else:
		discountCount = len(discountsArr)
	print(discountCount)
	with sql.connect('database.db') as conn:
		cur = conn.cursor()
		while discountCount > 0:
			indexArray = range(0,len(discountsArr))
			print(indexArray)
			indexCombinationsArray = list(itertools.combinations(indexArray,discountCount))
			print(indexCombinationsArray)
			for indexList in indexCombinationsArray:
				discountDetails = []
				cart = copy.deepcopy(cartProducts)
				for index in indexList:
					discount = discountsArr[index]
					cur.execute('SELECT itemA_id, itemA_qty, itemB_id, itemB_qty FROM conditions WHERE condition_id = ?',(discount[0],))
					discountDetails += cur.fetchall()
				for discount in discountDetails:
					cartIndex_itemA = next(index for (index, d) in enumerate(cart) if d["product_id"] == discount[0])
					cartIndex_itemB = next(index for (index, d) in enumerate(cart) if d["product_id"] == discount[2])
					cart[cartIndex_itemA]["product_qty"] -= discount[1]
					cart[cartIndex_itemB]["product_qty"] -= discount[3]
				if not any(product['product_qty'] < 0 for product in cart):
					temp_discount = 0
					for index in indexList:
						temp_discount += discountsArr[index][1]
					possibleDiscounts.append(temp_discount)
			discountCount -= 1
		print(discount)
		if possibleDiscounts:
			discount = max(possibleDiscounts) 
	return discount
	
if __name__ == "__main__":
	app.run()