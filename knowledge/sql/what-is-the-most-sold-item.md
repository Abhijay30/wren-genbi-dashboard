---
nl: what is the most sold item
sql: SELECT product_categories.category_name, SUM(invoices.quantity) AS total_quantity_sold
  FROM invoices JOIN product_categories ON invoices.category_id = product_categories.category_id
  GROUP BY product_categories.category_name ORDER BY total_quantity_sold DESC LIMIT
  1
source: user
---
