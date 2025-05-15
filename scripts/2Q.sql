SELECT 
	v.vn
	,p.cid
	,p.hn
	,concat(p.pname, p.fname, " ", p.lname ) AS ptname
	,v.age_y
	,v.vstdate
	,ps.pp_special_code
from vn_stat v
JOIN patient p ON p.hn = v.hn
JOIN pp_special pp  on  pp.vn = v.vn
JOIN pp_special_type ps  on  ps.pp_special_type_id = pp.pp_special_type_id
WHERE v.vstdate BETWEEN "2024-04-01" and "2024-04-12" and ps.pp_special_code NOT in ("1B130","1B131","1B0280","1B0281","1B141","1B141")
;