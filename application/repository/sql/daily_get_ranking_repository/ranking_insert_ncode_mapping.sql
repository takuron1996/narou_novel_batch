INSERT INTO ncode_mapping(
    id,
    ncode
)
VALUES(:id, :ncode)
ON  CONFLICT(ncode) DO NOTHING
;