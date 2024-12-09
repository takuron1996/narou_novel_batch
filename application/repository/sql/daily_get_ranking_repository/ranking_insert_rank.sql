WITH mapping_id(id) AS(
    SELECT
        COALESCE(
            (SELECT id FROM ncode_mapping WHERE ncode = :ncode),
            :id
        ) AS id
)
INSERT INTO rank(
    id,
    rank,
    rank_date
)
SELECT
    id,
    :rank,
    :rank_date
FROM
    mapping_id
;