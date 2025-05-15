SELECT o.icode ,d.name , count( o.vn ) AS vn , sum(o.qty) AS total,d.unitprice
from opitemrece o
left outer join drugitems d on d.icode = o.icode
where o.rxdate BETWEEN "2024-08-01" and "2024-08-01"
and o.icode like "1%"
GROUP BY  o.icode
ORDER BY total  DESC
#limit 10