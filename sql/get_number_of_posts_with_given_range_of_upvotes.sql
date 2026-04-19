-- uniform buckets of 500
SELECT 
    FLOOR(upvote_count / 500) * 500 AS upvote_count_bucket_start,
    FLOOR(upvote_count / 500) * 500 + 499 AS upvote_count_bucket_end,
    COUNT(*) AS posts_count
FROM POSTS
GROUP BY upvote_count_bucket_start
ORDER BY upvote_count_bucket_start;

-- custome buckets
SELECT 
    CASE 
        WHEN upvote_count < 100 THEN '0-99'
        WHEN upvote_count BETWEEN 100 AND 499 THEN '100-499'
        WHEN upvote_count BETWEEN 500 AND 999 THEN '500-999'
        WHEN upvote_count BETWEEN 1000 AND 1999 THEN '1000-1999'
        WHEN upvote_count BETWEEN 2000 AND 2999 THEN '2000-2999'
        WHEN upvote_count BETWEEN 3000 AND 3999 THEN '3000-3999'
        ELSE '>=4000'
    END AS upvote_bucket,
    COUNT(*) AS count
FROM POSTS
GROUP BY upvote_bucket
order by count desc;