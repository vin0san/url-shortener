-- 1. Core Redirection Engine Lookup
-- Fetches metadata so the backend application can safely handle 404 vs 410 logic.
SELECT 
    long_url, 
    expires_at
FROM urls
WHERE short_key = 'git-trend';


-- 2. Geographical Metrics Breakdown
-- Groups and counts clicks per country for a specific target URL ID.
SELECT 
    country_code, 
    COUNT(*) AS click_count
FROM clicks_analytics
WHERE url_id = 1
GROUP BY country_code
ORDER BY click_count DESC;


-- 3. Traffic Source Referer Metrics
-- Groups and counts incoming domain sources (Fixed column name to 'referer' to match schema).
SELECT 
    referer, 
    COUNT(*) AS click_count
FROM clicks_analytics
WHERE url_id = 1
GROUP BY referer
ORDER BY click_count DESC;


-- 4. Time Series Metric Timeline (Hourly Graphing)
-- Buckets click volumes into clean hourly increments over the trailing 24 hours.
SELECT 
    DATE_TRUNC('hour', clicked_at) AS click_hour, 
    COUNT(*) AS click_count
FROM clicks_analytics
WHERE url_id = 1 
  AND clicked_at >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
GROUP BY click_hour
ORDER BY click_hour ASC;


-- 5. Deep-Dive Historical Campaign Performance Report
-- Joins schema tables to compile overall status metrics for a dashboard.
SELECT 
    u.long_url,
    u.created_at,
    u.expires_at,
    CASE 
        WHEN u.expires_at < CURRENT_TIMESTAMP THEN 'Expired' 
        ELSE 'Active' 
    END AS status,
    COUNT(c.id) AS total_clicks,
    COUNT(DISTINCT c.country_code) AS unique_countries
FROM urls u
LEFT JOIN clicks_analytics c ON u.id = c.url_id
WHERE u.id = 1
GROUP BY u.id, u.long_url, u.created_at, u.expires_at;
