SELECT
o.icode as "รหัสยา"
,d.tmt_tp_code as "TTMT_code"
,d.name as "Drug"
,d.strength 
,d.units
,count(o.icode)as "list"
,sum(o.qty)as "quantity_จำนวนสั่ง"
,d.unitcost as "ราคาต่อหน่วย"
,(sum(o.qty)*d.unitcost)as "amount_มูลค่า"
from opitemrece o
join drugitems d on d.icode=o.icode 
where o.rxdate between "2025-03-27" and "2025-03-27" and d.tmt_tp_code IN(798783,717021,532586,940556,264414,9092983,666847,9374895,486941,715038)
group by o.icode order by d.name,d.strength 
;

SHOW VARIABLES LIKE 'character_set_database';
SHOW VARIABLES LIKE 'character_set_connection';
