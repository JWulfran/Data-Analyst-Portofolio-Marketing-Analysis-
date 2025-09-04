select * from dbo.engagement_data

select EngagementID, ContentID, CampaignID, ProductID, 
	UPPER(Replace(ContentType, 'Socialmedia', 'Social Media')) as ContentType,
	LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined)-1) as Views,
	RIGHT(ViewsClicksCombined, len(ViewsClicksCombined)- charindex('-', ViewsClicksCombined)) as Clicks,
	Likes,
	FORMAT(convert(DATE, EngagementDate), 'dd.MM.yyyy') as EngagementDate
from dbo.engagement_data
where ContentType != 'Newsletter';