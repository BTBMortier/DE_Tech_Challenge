SELECT 
c.first_name,
c.last_name,
COUNT(r.customer_id) n_rentals,
a.address,
a.city,
a.postal_code,
a.latitude,
a.longitude

FROM rental r

JOIN customer c ON c.customer_id = r.customer_id
JOIN address a ON a.address_id = c.address_id 

GROUP BY r.customer_id 
ORDER BY n_rentals DESC

LIMIT 1
