INSERT INTO keyword(
    keyword_id,
    name
)
VALUES(:keyword_id, :name)
ON  CONFLICT(name) DO NOTHING
;