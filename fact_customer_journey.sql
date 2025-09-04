with DuplicateRecords as (
	select JourneyID, CustomerID, ProductID, VisitDate, Stage, Action, Duration,
	ROW_NUMBER() over(Partition by CustomerID, ProductID, VisitDate, Stage, Action order by JourneyID) as row_num
	from dbo.customer_journey
	)

select * from DuplicateRecords
where row_num > 1
order by JourneyID
    
SELECT JourneyID, CustomerID, ProductID, VisitDate, Stage, Action, COALESCE(Duration, avg_duration) AS Duration
FROM 
    (
        SELECT JourneyID, CustomerID, ProductID, VisitDate,
			UPPER(Stage) AS Stage, Action, Duration, 
			AVG(Duration) OVER (PARTITION BY VisitDate) AS avg_duration,
			ROW_NUMBER() OVER (PARTITION BY CustomerID, ProductID, VisitDate, UPPER(Stage), Action ORDER BY JourneyID) AS row_num  
								FROM dbo.customer_journey) AS subquery WHERE row_num = 1;