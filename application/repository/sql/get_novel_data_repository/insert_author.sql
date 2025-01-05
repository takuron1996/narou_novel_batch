INSERT INTO author(
    author_id,
    userid,
    writer
)
VALUES(:author_id, :userid, :writer)
ON  CONFLICT(userid) DO UPDATE SET writer = EXCLUDED.writer
;