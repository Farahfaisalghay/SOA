<%@ page language="java" contentType="text/html; charset=UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>E-Commerce Store</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* NAVBAR */
        .navbar {
            background: #343a40;
            color: white;
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .navbar a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
        }

        /* MAIN CONTENT */
        .container {
            flex: 1;
            padding: 40px;
            display: flex;
            justify-content: center;
        }

        .products {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 30px;
            max-width: 900px;
            width: 100%;
        }

        .product {
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            align-self: start; /* fixes stretched cards */
        }

        .product h3 {
            margin-top: 0;
        }

        .product p {
            margin: 8px 0;
        }

        .product input {
            width: 60px;
            padding: 5px;
        }

        .product button {
            margin-top: 15px;
            padding: 8px 15px;
            background: #007bff;
            border: none;
            color: white;
            cursor: pointer;
            border-radius: 4px;
        }

        .product button:hover {
            background: #0056b3;
        }

        footer {
            background: #343a40;
            color: white;
            text-align: center;
            padding: 15px;
        }
    </style>
</head>

<body>

<!-- NAVBAR -->
<div class="navbar">
    <h2>🛒 E-Commerce</h2>
    <div>
        <a href="index.jsp">Home</a>
        <a href="index.jsp">Products</a>
    </div>
</div>

<!-- PRODUCT CATALOG -->
<div class="container">
    <div class="products">

        <!-- PRODUCT 1 -->
        <div class="product">
            <h3>Laptop</h3>
            <p>Price: $999</p>

            <form action="checkout.jsp" method="get">
                <input type="hidden" name="product_id" value="1">
                <input type="hidden" name="product_name" value="Laptop">
                <input type="hidden" name="price" value="999">

                Qty:
                <input type="number" name="quantity" value="1" min="1">

                <br>
                <button type="submit">Buy Now</button>
            </form>
        </div>

        <!-- PRODUCT 2 -->
        <div class="product">
            <h3>Mouse</h3>
            <p>Price: $29</p>

            <form action="checkout.jsp" method="get">
                <input type="hidden" name="product_id" value="2">
                <input type="hidden" name="product_name" value="Mouse">
                <input type="hidden" name="price" value="29">

                Qty:
                <input type="number" name="quantity" value="1" min="1">

                <br>
                <button type="submit">Buy Now</button>
            </form>
        </div>

        <!-- PRODUCT 3 -->
        <div class="product">
            <h3>Keyboard</h3>
            <p>Price: $79</p>

            <form action="checkout.jsp" method="get">
                <input type="hidden" name="product_id" value="3">
                <input type="hidden" name="product_name" value="Keyboard">
                <input type="hidden" name="price" value="79">

                Qty:
                <input type="number" name="quantity" value="1" min="1">

                <br>
                <button type="submit">Buy Now</button>
            </form>
        </div>

    </div>
</div>

<!-- FOOTER -->
<footer>
    © 2025 E-Commerce Order Management System
</footer>

</body>
</html>
