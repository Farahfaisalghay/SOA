<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>

<%
    // Get data from product page
    String productId = request.getParameter("product_id");
    String productName = request.getParameter("product_name");

    int price = Integer.parseInt(request.getParameter("price"));
    int quantity = Integer.parseInt(request.getParameter("quantity"));
    int total = price * quantity;
%>

<!DOCTYPE html>
<html>
<head>
    <title>Checkout</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f5f5f5;
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

        /* CONTAINER */
        .container {
            width: 50%;
            margin: 40px auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }

        h2 {
            text-align: center;
        }

        .summary {
            background: #f1f1f1;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 25px;
        }

        .summary p {
            margin: 8px 0;
        }

        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
        }

        input {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }

        button {
            width: 100%;
            margin-top: 25px;
            padding: 12px;
            background: #28a745;
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
            border-radius: 4px;
        }

        button:hover {
            background: #218838;
        }

        footer {
            background: #343a40;
            color: white;
            text-align: center;
            padding: 15px;
            margin-top: 40px;
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

<!-- CHECKOUT CONTAINER -->
<div class="container">
    <h2>🧾 Checkout</h2>

    <!-- ORDER SUMMARY -->
    <div class="summary">
        <p><strong>Product:</strong> <%= productName %></p>
        <p><strong>Price:</strong> $<%= price %></p>
        <p><strong>Quantity:</strong> <%= quantity %></p>
        <hr>
        <p><strong>Total:</strong> $<%= total %></p>
    </div>

    <!-- CHECKOUT FORM -->
    <form action="submitOrder" method="post">

        <!-- Hidden Fields -->
        <input type="hidden" name="product_id" value="<%= productId %>">
        <input type="hidden" name="product_name" value="<%= productName %>">
        <input type="hidden" name="price" value="<%= price %>">
        <input type="hidden" name="quantity" value="<%= quantity %>">
        <input type="hidden" name="total" value="<%= total %>">

        <!-- Customer Info -->
        <label>Customer ID</label>
        <input type="number" name="customer_id" placeholder="Enter your customer ID" required>

        <button type="submit">Place Order</button>
    </form>
</div>

<!-- FOOTER -->
<footer>
    © 2025 E-Commerce Order Management System
</footer>

</body>
</html>
