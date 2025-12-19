<%@ page language="java" contentType="text/html; charset=UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <title>Order Confirmation</title>
    <style>
        body {
            font-family: Arial;
            background: #f5f5f5;
        }
        .container {
            width: 50%;
            margin: 60px auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 0 10px #ccc;
            text-align: center;
        }
        .success {
            font-size: 60px;
            color: #28a745;
        }
        .details {
            text-align: left;
            margin-top: 20px;
            background: #f1f1f1;
            padding: 15px;
            border-radius: 5px;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            text-decoration: none;
            background: #007bff;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
        }
        a:hover {
            background: #0056b3;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    </style>
</head>

<body>
<div class="container">
    <div class="success">✔</div>
    <h2>Order Placed Successfully!</h2>
    <p>Thank you for your purchase.</p>

    <!-- Order Details -->
    <div class="details">
        <h4>Order Details</h4>
        <pre><%= request.getAttribute("orderResponse") %></pre>
    </div>

    <a href="index.jsp">← Back to Catalog</a>
</div>
</body>
</html>
