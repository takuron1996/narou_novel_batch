INSERT INTO novel_type (code, name)
VALUES
    (1, '連載'),
    (2, '短編')
ON  CONFLICT(code) DO NOTHING;