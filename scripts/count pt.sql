SELECT 
	o.main_dep
	,k.department AS aa
	,COUNT(vn) AS tt 
FROM ovst o 
LEFT OUTER JOIN kskdepartment k ON k.depcode = o.main_dep 
WHERE o.vstdate = '2025-05-08'
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
i.hn
,i.an
,i.vn
,i.pttype ,p.name  ,p.hipdata_code
,i.admdoctor 
,i.first_ward ,i.ward ,w.name 
,i.regdate ,i.regtime
,ia.bedno ,ia.bedtype ,b.name
,ia.roomno ,ia.move_in_bed_datetime
,ia.rate
,i.dch_doctor 
,i.dchdate 
,i.dchtime 
FROM ipt i
LEFT OUTER JOIN ward w ON w.ward = i.ward
LEFT OUTER JOIN pttype p  ON p.pttype = i.pttype
LEFT OUTER JOIN iptadm ia ON ia.an = i.an
LEFT OUTER JOIN bedtype b  ON ia.bedtype = b.bedtype
WHERE i.regdate BETWEEN '2025-04-01' AND '2025-04-30'
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
WHERE regdate BETWEEN '2025-05-01' AND '2025-05-31'
GROUP BY regdate 
;

SELECT
	COUNT(an) AS AdmitPt,
	COUNT(an) / (1+DATEDIFF('2025-04-30', '2025-04-01')) AS AVG_PT
	FROM ipt
	WHERE regdate BETWEEN '2025-04-01' AND '2025-04-30'
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