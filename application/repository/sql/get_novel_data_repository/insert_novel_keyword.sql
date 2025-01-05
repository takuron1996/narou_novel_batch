INSERT INTO novel_keywords(
	id,
	keyword_id 
)
VALUES(
	:id,
	(SELECT keyword_id FROM keyword WHERE name = :keyword)
)
ON CONFLICT(id, keyword_id) DO NOTHING
;