with t as 
	(select row_number() over (order by upvote_count desc) as rank_of_upvotes, post_id, author_id, created_utc, post_title, upvote_count, downvote_count, comments_count, crossposts_count, post_url, media_url
	from POSTS)
select * from t
where rank_of_upvotes <= 20;