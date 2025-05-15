SELECT DISTINCT pp.cid, pp.hn, concat( pp.pname, pp.fname, " ", pp.lname ) AS ptname, v.age_y , v.vstdate ,v.pdx
from vn_stat v
LEFT OUTER JOIN patient pp ON pp.hn = v.hn
WHERE  	v.vstdate  BETWEEN "2023-10-01" and "2024-06-11"
and v.pdx BETWEEN "F32" and "F39"
ORDER BY v.vstdate;

SELECT COUNT(pp.cid)
from vn_stat v
LEFT OUTER JOIN patient pp ON pp.hn = v.hn
WHERE  	v.vstdate  BETWEEN "2023-10-01" and "2024-06-11"
and v.pdx BETWEEN "F32" and "F39"
ORDER BY v.vstdate;