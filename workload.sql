select vn
,main_dep
,hn
,vstdate
,doctor 
,command_doctor
from ovst o
where vstdate = '2025-04-01' and main_dep = '033' 
-- -AND doctor = '004'
;

--- พยายามจะหา workload แพทย์
select *
from vn_stat vs  
where vstdate = '2025-04-01' 
;

--- Create View

CREATE VIEW v_opitemrece AS
select * from opitemrece
;

SELECT * from v_opitemrece;


--- อันนีใช้ได้ใกล้เคียงมาก
select doctor
,count(doctor)
FROM
(select vn
,doctor
from opitemrece
where vstdate = '2025-04-02'
group by vn) AS sub1
GROUP BY doctor
;



select COUNT(VN)
from ovst o
where vstdate = '2024-10-11' and main_dep = '033'
;

SELECT *
from vn_stat v
JOIN ovst o  ON v.vn = o.vn
where v.vstdate = '2025-04-01' AND v.dx_doctor = '004'
-- AND v.hn = '0102916'
;

SELECT
v.vn, o.vn AS o_vn, v.hn, v.cid, v.pdx, v.lastvisit  ,o.diag_text , v.main_pdx , v.dx0 , v.dx1 , v.dx2 , v.dx3 , v.dx4 , v.dx5 , v.op0 , v.op1 , v.op2 , v.op3 , v.op4 , v.op5 
,v.vstdate , o.vstdate AS o_vstdate, o.vsttime AS o_vsttime, v.lastvisit_vn ,v.lastvisit_hour 
,v.dx_doctor , o.doctor ,o.sign_doctor , o.command_doctor 
,o.oqueue ,o.ovstist , o.ovstost 
,o.main_dep , o.main_dep_queue , o.cur_dep , o.cur_dep_busy , o.cur_dep_time , o.last_dep
,o.rx_queue 
from vn_stat v
JOIN ovst o  ON v.vn = o.vn
where v.vstdate = '2025-04-01' AND v.dx_doctor = '004' 
-- AND cur_dep = '033'
;