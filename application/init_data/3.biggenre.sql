INSERT INTO biggenre (code, name)
VALUES
    (0, '未選択'),
    (1, '恋愛'),
    (2, 'ファンタジー'),
    (3, '文芸'),
    (4, 'SF'),
    (99, 'その他'),
    (98, 'ノンジャンル')
ON  CONFLICT(code) DO NOTHING;