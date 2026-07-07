-- queries.sql
-- url redirection service database seed data

SELECT long_url
FROM urls
WHERE short_key = 'git-trend'
    AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP);

-- Country metrics for URL with short_key 'git-trend'

SELECT country_code, COUNT(*) AS click_count
FROM clicks_analytics
WHERE url_id = (SELECT id FROM urls WHERE short_key = 'git-trend')
GROUP BY country_code
ORDER BY click_count DESC;

-- Referrer metrics for URL with short_key 'git-trend'

SELECT referrer, COUNT(*) AS click_count
FROM clicks_analytics
WHERE url_id = (SELECT id FROM urls WHERE short_key = 'git-trend')
GROUP BY referrer
ORDER BY click_count DESC;

-- Time series metrics for URL with short_key 'git-trend'

SELECT DATE_TRUNC('hour', clicked_at) AS click_hour, COUNT(*) AS click_count
FROM clicks_analytics
WHERE url_id = (SELECT id FROM urls WHERE short_key = 'git-trend')
GROUP BY click_hour
ORDER BY click_hour ASC;

-- Background job to clean up expired URLs (to be scheduled as a cron job)

DELETE FROM urls
WHERE expires_at IS NOT NULL AND expires_at < CURRENT_TIMESTAMP;