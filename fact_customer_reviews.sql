select * from dbo.customer_reviews


select ReviewID, ReviewDate, ProductID, CustomerID, Rating,
	REPLACE(ReviewText, '  ', ' ') as ReviewText
from dbo.customer_reviews