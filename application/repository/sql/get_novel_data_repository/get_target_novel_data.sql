select
	nm.id,
	nm.ncode
from
	ncode_mapping nm
left join novel n
on
	nm.id = n.id
where
	n.id is null;