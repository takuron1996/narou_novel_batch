INSERT INTO novel (
    id,
    author_id,
    title,
    biggenre_code,
    genre_code,
    novel_type_id,
    isr15,
    isbl,
    isgl,
    iszankoku,
    istensei,
    istenni
)
VALUES(
	:id,
	(SELECT author_id FROM author WHERE userid = :userid),
	:title,
	:biggenre_code,
	:genre_code,
	:novel_type_id,
	:isr15,
	:isbl,
	:isgl,
	:iszankoku,
	:istensei,
	:istenni
)
ON CONFLICT(id) DO UPDATE SET
	author_id = EXCLUDED.author_id,
	title = EXCLUDED.title,
	biggenre_code = EXCLUDED.biggenre_code,
    genre_code = EXCLUDED.genre_code,
    novel_type_id = EXCLUDED.novel_type_id,
    isr15 = EXCLUDED.isr15,
    isbl = EXCLUDED.isbl,
    isgl = EXCLUDED.isgl,
    iszankoku = EXCLUDED.iszankoku,
    istensei = EXCLUDED.istensei,
    istenni = EXCLUDED.istenni
;