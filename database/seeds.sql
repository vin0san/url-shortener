-- ============================================================================
-- 1. SEED USERS (3 Records)
-- ============================================================================
INSERT INTO users (email, pass_hash, created_at, updated_at) VALUES
('alex.jones@example.com',   '$2b$12$K3vZ7X9yB8mQ2zR5vT6uOe1A2b3c4d5e6f7g8h9i0j1k2l3m4n5o6', CURRENT_TIMESTAMP - INTERVAL '90 days', CURRENT_TIMESTAMP - INTERVAL '45 days'), -- Profile modified 45 days ago
('priya.sharma@example.in',  '$2b$12$M9xY8w7v6u5t4s3r2q1p0oNmLkJiHgFeDcBa9876543210zyx', CURRENT_TIMESTAMP - INTERVAL '30 days', CURRENT_TIMESTAMP - INTERVAL '30 days'), -- Created & never modified
('sam.smith@example.co.uk',  '$2b$12$A1b2C3d4E5f6G7h8I9j0k1L2m3N4o5P6q7R8s9T0u1V2w3X4y5Z6a', CURRENT_TIMESTAMP,                  CURRENT_TIMESTAMP);                  -- Brand new signup today

-- ============================================================================
-- 2. SEED URLS (5 Records: 2 Active with Future Expiry, 1 Expired, 2 No Expiry)
-- ============================================================================
INSERT INTO urls (long_url, short_key, user_id, expires_at) VALUES
-- Active links (Expires 30 days in the future)
('https://github.com',            'git-trend',  1, CURRENT_TIMESTAMP + INTERVAL '30 days'),
('https://ycombinator.com',           'hn-top',     2, CURRENT_TIMESTAMP + INTERVAL '30 days'),

-- Expired link (Expired 5 days ago)
('https://blackfridaydeals.com',  'bf-deals',   1, CURRENT_TIMESTAMP - INTERVAL '5 days'),

-- Permanent links (No expiration date)
('https://stackoverflow.com',              'so-home',    2, NULL),
('https://wikipedia.org',                  'wiki-main',  3, NULL);

-- ============================================================================
-- 3. SEED CLICKS ANALYTICS (30 Records distributed across active URLs: 1, 2, 4, 5)
-- ============================================================================
INSERT INTO clicks_analytics (url_id, user_agent, country_code, referrer, clicked_at) VALUES
-- Clicks for URL 1 (git-trend)
(1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'US', 'https://t.co', CURRENT_TIMESTAMP - INTERVAL '1 hour'),
(1, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15', 'US', 'https://linkedin.com', CURRENT_TIMESTAMP - INTERVAL '2 hours'),
(1, 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 'IN', 'https://ycombinator.com', CURRENT_TIMESTAMP - INTERVAL '3 hours'),
(1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0', 'GB', NULL, CURRENT_TIMESTAMP - INTERVAL '4 hours'),
(1, 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/605.1.15', 'US', 'https://t.co', CURRENT_TIMESTAMP - INTERVAL '5 hours'),
(1, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'DE', 'https://reddit.com', CURRENT_TIMESTAMP - INTERVAL '6 hours'),
(1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'CA', 'https://t.co', CURRENT_TIMESTAMP - INTERVAL '7 hours'),
(1, 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/605.1.15', 'IN', NULL, CURRENT_TIMESTAMP - INTERVAL '8 hours'),

-- Clicks for URL 2 (hn-top)
(2, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'US', 'https://ycombinator.com', CURRENT_TIMESTAMP - INTERVAL '30 minutes'),
(2, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'GB', 'https://t.co', CURRENT_TIMESTAMP - INTERVAL '1 hour'),
(2, 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 'IN', 'https://linkedin.com', CURRENT_TIMESTAMP - INTERVAL '2 hours'),
(2, 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/605.1.15', 'US', 'https://reddit.com', CURRENT_TIMESTAMP - INTERVAL '4 hours'),
(2, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15', 'FR', NULL, CURRENT_TIMESTAMP - INTERVAL '6 hours'),
(2, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0', 'IN', 'https://t.co', CURRENT_TIMESTAMP - INTERVAL '12 hours'),
(2, 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 'AU', 'https://ycombinator.com', CURRENT_TIMESTAMP - INTERVAL '1 day'),

-- Clicks for URL 4 (so-home)
(4, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'IN', 'https://google.com', CURRENT_TIMESTAMP - INTERVAL '15 minutes'),
(4, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'IN', 'https://bing.com', CURRENT_TIMESTAMP - INTERVAL '45 minutes'),
(4, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'US', 'https://google.com', CURRENT_TIMESTAMP - INTERVAL '2 hours'),
(4, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'DE', 'https://github.com', CURRENT_TIMESTAMP - INTERVAL '5 hours'),
(4, 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/605.1.15', 'GB', 'https://t.co', CURRENT_TIMESTAMP - INTERVAL '8 hours'),
(4, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0', 'US', NULL, CURRENT_TIMESTAMP - INTERVAL '1 day'),
(4, 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 'BR', 'https://google.com', CURRENT_TIMESTAMP - INTERVAL '2 days'),
(4, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15', 'JP', 'https://github.com', CURRENT_TIMESTAMP - INTERVAL '3 days'),

-- Clicks for URL 5 (wiki-main)
(5, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'US', 'https://google.com', CURRENT_TIMESTAMP - INTERVAL '10 minutes'),
(5, 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/605.1.15', 'GB', 'https://wikipedia.org', CURRENT_TIMESTAMP - INTERVAL '1 hour'),
(5, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36', 'CA', 'https://google.com', CURRENT_TIMESTAMP - INTERVAL '3 hours'),
(5, 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 'IN', 'https://t.co', CURRENT_TIMESTAMP - INTERVAL '6 hours'),
(5, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0', 'US', NULL, CURRENT_TIMESTAMP - INTERVAL '12 hours'),
(5, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15', 'AU', 'https://facebook.com', CURRENT_TIMESTAMP - INTERVAL '1 day'),
(5, 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0', 'NL', 'https://google.com', CURRENT_TIMESTAMP - INTERVAL '4 days'); 
