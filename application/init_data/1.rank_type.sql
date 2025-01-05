INSERT INTO rank_type (type, period)
VALUES
    ('d', '日間'),
    ('w', '週間'),
    ('m', '月間'),
    ('q', '四半期')
ON  CONFLICT(type) DO NOTHING;