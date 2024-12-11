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
    rank_date,
    rank_type
)
SELECT
    id,
    :rank,
    :rank_date,
    :rank_type
FROM
    mapping_id
ON CONFLICT(id, rank, rank_date, rank_type) DO NOTHING
;