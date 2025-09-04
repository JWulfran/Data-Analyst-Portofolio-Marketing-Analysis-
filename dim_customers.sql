Select * from dbo.customers
select * from dbo.geography

Select c.CustomerID, c.CustomerName, c.Email, c.Gender, c.Age, g.Country, g.City
from dbo.customers as c
left join dbo.geography g on c.GeographyID = g.GeographyID