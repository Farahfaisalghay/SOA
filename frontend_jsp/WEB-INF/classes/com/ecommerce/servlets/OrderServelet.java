package com.ecommerce.servlets;
import jakarta.servlet.*;
import jakarta.servlet.http.*;
import jakarta.servlet.annotation.WebServlet;
import java.io.IOException;
import java.net.URI;
import java.net.http.*;

@WebServlet("/submitOrder")
public class OrderServlet extends HttpServlet {

    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String customerId = request.getParameter("customer_id");
        String productId = request.getParameter("product_id");
        String quantity = request.getParameter("quantity");

        String jsonPayload = String.format(
            "{\"customer_id\":%s,\"products\":[{\"product_id\":%s,\"quantity\":%s}]}",
            customerId, productId, quantity
        );

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest flaskRequest = HttpRequest.newBuilder()
            .uri(URI.create("http://localhost:5001/api/orders/create"))
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
            .build();

        try {
            HttpResponse<String> flaskResponse =
                client.send(flaskRequest, HttpResponse.BodyHandlers.ofString());

            request.setAttribute("orderResponse", flaskResponse.body());
            request.getRequestDispatcher("/confirmations.jsp").forward(request, response);

        } catch (Exception e) {
            response.getWriter().println("Order Service not running");
        }
    }
}
