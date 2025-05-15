SELECT 
	v.vn
	,p.cid
	,p.hn
	,concat(p.pname, p.fname, " ", p.lname ) AS ptname
	,v.age_y
	,v.vstdate
from vn_stat v
JOIN patient p ON p.hn = v.hn
JOIN pp_special pp  on  pp.vn = v.vn
JOIN pp_special_type ps  on  ps.pp_special_type_id = pp.pp_special_type_id
WHERE v.vstdate BETWEEN "2024-06-13" and "2024-06-13"
GROUP BY v.vn;

SELECT
	v.vn
	,v.age_y
	,v.vstdate
	,p.cid
	,p.hn
	,concat(p.pname, p.fname, " ", p.lname ) AS ptname
FROM vn_stat v
JOIN patient p ON p.hn = v.hn
WHERE v.vstdate BETWEEN "2024-06-13" and "2024-06-13";