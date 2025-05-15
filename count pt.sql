SELECT 
	o.main_dep
	,k.department AS aa
	,COUNT(vn) AS tt 
FROM ovst o 
LEFT OUTER JOIN kskdepartment k ON k.depcode = o.main_dep 
WHERE o.vstdate = CURDATE() 
GROUP BY o.main_dep 
;

# จำนวนผู้รับบริการผู้ป่วยใน
SELECT 
	a.ward AS iw
	, w.name AS ww
	, COUNT(a.hn) AS cc 
FROM ipt a
LEFT OUTER JOIN ovst o ON o.an = a.an
LEFT OUTER JOIN ward w ON w.ward = a.ward
WHERE a.dchstts IS NULL 
GROUP BY a.ward
;

# Count admit
SELECT
hn
,an
,vn
,admdoctor 
,ward
,regdate 
,regtime
,dch_doctor 
,dchdate 
,dchtime 
FROM ipt
WHERE regdate = CURDATE()
;

# Count admit
SELECT
regdate AS 'วันที่ admit'
,COUNT(an) AS 'จำนวนที่ Admit'
,CASE
		WHEN COUNT(an) >= 25 THEN 'YES'
        WHEN COUNT(an) < 25 THEN 'NO'
        ELSE 'NO'
        END AS 'ผ่านเกณฑ์25ราย'
FROM ipt
WHERE regdate BETWEEN '2025-04-01' AND '2025-04-30'
GROUP BY regdate 
;

SELECT
	COUNT(an) AS AdmitPt,
	COUNT(an) / (1+DATEDIFF('2025-03-31', '2025-03-01')) AS AVG_PT
	FROM ipt
	WHERE regdate BETWEEN '2025-03-01' AND '2025-03-31'
;

SELECT
    DATE_FORMAT(regdate, '%Y-%m') AS ReportMonth,
    COUNT(an) AS 'จำนวนผู้ป่วย admit',
    COUNT(an) / DAY(LAST_DAY(regdate)) AS 'จำนวนผู้ป่วย admit เฉลี่ยต่อวัน'
FROM ipt
WHERE
    regdate BETWEEN '2025-01-01' AND CURDATE()
GROUP BY
    ReportMonth
ORDER BY
    ReportMonth;