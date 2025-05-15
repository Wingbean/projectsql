SELECT *
FROM clinicmember
WHERE lastvisit = '2025-05-08' 
ORDER BY lastvisit  DESC, clinic
;

-- หา hn ใน ทะเบียน
SELECT *
FROM clinicmember
WHERE hn IN ('0121079') 
;

-- หา hn ใน ทะเบียน ที่ไม่มี regdate
SELECT
	cm.clinic
	,c.name
	,cms.clinic_member_status_name  AS 'status'
	,cm.doctor
	,cm.hn
	,cm.regdate 
	,cm.lastvisit
	,cm.begin_date 
	,cm.dchdate
	,cm.current_status
	,cm.lastupdate
	,cm.other_chronic_text
	,cm.modify_staff
	,cm.last_hba1c_date ,cm.last_hba1c_value
	,cm.last_bp_date ,cm.last_bp_bps_value, cm.last_bp_bpd_value
	,cm.last_fbs_date ,cm.last_fbs_value
FROM clinicmember cm
LEFT OUTER JOIN clinic c ON c.clinic = cm.clinic
LEFT OUTER JOIN clinic_member_status cms ON cms.clinic_member_status_id = cm.clinic_member_status_id
WHERE regdate IS NULL AND cm.clinic_member_status_id != '3'
;


-- หาคนที่ไม่ได้ขึ้นทะเบียนที่มารับบริการวันนั้น
SELECT
	o.hn
	,MAX(c.regdate)
FROM ovst o
LEFT OUTER JOIN clinicmember c ON o.hn = c.hn
WHERE o.vstdate = CURDATE() AND o.main_dep = '033' AND c.regdate IS NULL
GROUP BY o.hn
;

SELECT 
	o.main_dep
	,k.department AS aa
	,COUNT(vn) AS tt 
FROM ovst o 
LEFT OUTER JOIN kskdepartment k ON k.depcode = o.main_dep 
WHERE o.vstdate = '2025-05-08'
GROUP BY o.main_dep 
;

-- หา last visit ใน clinicmember
SELECT
	hn
	,clinic
	,regdate
FROM clinicmember
;