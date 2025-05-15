-- หาข้อความใน ซักประวัติ ตรวจร่างกาย
select
o.vn
,o.hn 
,o.vstdate
,o.vsttime
,o.screen_dep 
,o.bps ,o.bpd ,o.pulse ,o.rr ,o.temperature ,o.bw ,o.height ,o.bmi
,o.cc ,o.pe ,o.hpi ,o.pmh ,o.fh, o.symptom
,o.smoking_type_id ,o.drinking_type_id
,o.egfr ,o.hb ,o.cholesterol ,o.egfr ,o.creatinine_kidney_percent ,o.sodium ,o.potassium
from opdscreen o
where vstdate = CURDATE() -- AND  hpi LIKE '%tele%' -- AND screen_dep != '036'
order by vsttime DESC
;

-- หา PE DxText NULL
SELECT
o.vn AS 'VN'
,MAX(o.hn) AS 'HN' 
,MAX(o.an) AS 'AN' 
,MAX(o.vstdate) AS 'VstDate'
,MAX(o.vsttime) AS 'VstTime'
,MAX(ou.name) AS 'ผู้ซักประวัติ'
,MAX(o.doctor) AS 'รหัสแพทย์'
,MAX(d.name) AS 'ชื่อแพทย์'
,MAX(os.pe) AS 'PE'
,MAX(od.diag_text) AS 'Dx_Text'
,MAX(os.cc) AS 'CC' ,MAX(os.hpi) AS 'Hpi' ,MAX(v.pdx) AS 'PDx',MAX(v.dx1) AS 'Dx1',MAX(v.dx2) AS 'Dx2',MAX(v.dx3) AS 'Dx3'
FROM ovst o 
LEFT OUTER JOIN opdscreen os ON o.vn = os.vn
LEFT OUTER JOIN doctor d  ON o.doctor = d.code
LEFT OUTER JOIN screen_doctor sd on sd.vn = o.vn
LEFT OUTER JOIN opduser ou on ou.loginname = sd.staff
LEFT OUTER JOIN vn_stat v on v.vn = o.vn
LEFT OUTER JOIN ovst_doctor_diag od on od.vn = o.vn
WHERE o.vstdate BETWEEN '2025-05-06' AND CURDATE() -- o.doctor in ('247', '0086', '0087', '0088', '0089', '0090', '0052', '004', '123')
GROUP BY o.vn
ORDER BY MAX(o.vstdate) DESC, MAX(o.vsttime) DESC, MAX(o.doctor)
;

select * from ovst ORDER BY vstdate DESC, vsttime DESC ;

select * FROM opdscreen WHERE vstdate = CURDATE() AND hn = '0140611';

-- หาคนซักประวัติ
SELECT o.hn,o.vstdate , CONCAT(p.pname,p.fname," ",p.lname) as ชื่อ ,os.cc,d.name as ผู้ซักประวัติ
from ovst o
left outer join patient p on p.hn = o.hn
left outer join opdscreen os on os.vn = o.vn  
left outer join screen_doctor s on s.vn = o.vn 
left outer join opduser ou on ou.loginname = s.staff 
left outer join doctor d on d.code = ou.doctorcode 
where s.depcode = "033" and o.vstdate = "2025-04-28"
;

-- นัด ตั้งใจหา telemed
select *
from oapp 
-- where nextdate = CURDATE() - INTERVAL 0 DAY AND visit_vn is NULL
where nextdate = CURDATE() AND depcode = '033' AND clinic ='031'
order by vstdate DESC
;


-- นัดจาก นิด
select o.clinic,o.oapp_id
,concat(p.pname,p.fname,'  ',p.lname) as ptname
,o.doctor,  c.name as clinic_name,  d.name as doctor_name
,o.hn,o.vstdate,o.nextdate,o.nexttime,o.note,o.vn,o.depcode,o.spclty
,k.department
,count(v.hn) as visit_count  
from oapp o  
left outer join patient p on p.hn=o.hn  
left outer join clinic c on c.clinic=o.clinic  
left outer join doctor d on d.code=o.doctor  
left outer join kskdepartment k on k.depcode = o.depcode  
left outer join ovst v on v.vstdate=o.nextdate and v.hn=o.hn  
where o.nextdate between '2025-05-02' and '2025-05-02' and o.clinic='031'  
group by  o.clinic,o.oapp_id,p.pname,p.fname,p.lname,o.doctor
,c.name,d.name ,  o.hn,o.vstdate,o.nextdate,o.nexttime,o.note
,o.vn,o.depcode,o.spclty,k.department
;


