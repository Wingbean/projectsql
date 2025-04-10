-- code from report
select p.cid,lh.lab_order_number,lh.hn,concat(p.pname,p.fname,"  ",p.lname)as ptname,lh.order_date,lh.vn,concat("หมู่",v.moopart," ",t.full_name)as address ,
MAX(CASE WHEN lo.lab_items_code = 76 THEN lo.lab_order_result ELSE "-" END) AS "FBS",MAX(CASE WHEN lo.lab_items_code = 78 THEN lo.lab_order_result ELSE "-" END) AS "CR",
MAX(CASE WHEN lo.lab_items_code = 91 THEN lo.lab_order_result ELSE "-" END) AS "HDL",MAX(CASE WHEN lo.lab_items_code = 92 THEN lo.lab_order_result ELSE "-" END) AS "LDL",
MAX(CASE WHEN lo.lab_items_code = 102 THEN lo.lab_order_result ELSE "-" END) AS "Chol",MAX(CASE WHEN lo.lab_items_code = 103 THEN lo.lab_order_result ELSE "-" END) AS "TG",
MAX(CASE WHEN lo.lab_items_code = 930 THEN lo.lab_order_result ELSE "-" END) AS "Uma",MAX(CASE WHEN lo.lab_items_code = 948 THEN lo.lab_order_result ELSE "-" END) AS "Hba1c",
MAX(CASE WHEN lo.lab_items_code = 81 THEN lo.lab_order_result ELSE "-" END) AS "K",MAX(CASE WHEN lo.lab_items_code = 99 THEN lo.lab_order_result ELSE "-" END) AS "SGOT",
MAX(CASE WHEN lo.lab_items_code = 100 THEN lo.lab_order_result ELSE "-" END) AS "SGPT",MAX(CASE WHEN lo.lab_items_code = 199 THEN lo.lab_order_result ELSE "-" END) AS "HCT",
MAX(CASE WHEN lo.lab_items_code = 79 THEN lo.lab_order_result ELSE "-" END) AS "Uric",
CASE WHEN EXISTS (SELECT 0 FROM opitemrece oi WHERE oi.vn = lh.vn AND oi.icode IN ('1481453', '1000122', '1460151'))THEN 'Y' ELSE 'N'END AS "Enalapril/Losartan", 
CASE WHEN EXISTS (SELECT 0 FROM clinicmember cm WHERE cm.hn = p.hn AND cm.clinic IN ('001', '002')) THEN 'DM/HT' WHEN EXISTS (SELECT 1 FROM clinicmember cm WHERE cm.hn = p.hn AND cm.clinic = '001') THEN 'DM' WHEN EXISTS (SELECT 2 FROM clinicmember cm WHERE cm.hn = p.hn AND cm.clinic = '002') THEN 'HT'ELSE '-'END AS "ขึ้นทะเบียน"
from lab_head lh 
left outer join patient p on p.hn=lh.hn 
LEFT OUTER JOIN lab_order lo ON lo.lab_order_number = lh.lab_order_number
left outer join vn_stat v on v.vn=lh.vn 
left outer join ovst o on o.vn=v.vn 
left outer join kskdepartment k on k.depcode=o.main_dep  
left outer join thaiaddress t on t.addressid=v.aid 
where lh.form_name="Check up DM/HT" and lh.confirm_report="Y" 
and lh.order_date between "2024-03-01" and "2024-03-01" 
and o.main_dep = "033" 
GROUP BY v.vn
;

-- เริ่มต้นจาก code นี้
select lh.lab_order_number
,lh.vn 
,lh.hn
,concat(p.pname,p.fname,"  ",p.lname)as ptname
,lh.order_date
,lh.order_time
,lo.lab_items_code
,lo.lab_order_result AS "Cr"
from  lab_head lh
LEFT outer join lab_order lo ON lo.lab_order_number = lh.lab_order_number
LEFT outer join patient p ON p.hn = lh.hn
where lh.order_date = "2025-04-03" AND lo.lab_items_code = 78
;

-- จากนิด
SELECT p.cid, v.hn,CONCAT(p.pname, p.fname, ' ', p.lname) AS "NAME",MAX(lh.order_date) AS "วันที่เจาะ",
    MAX(CASE WHEN lh.order_date = cc1.aa1 THEN lo.lab_order_result END) AS "ผล",
    MAX(CASE WHEN lh.order_date = dd2.bb2 THEN lh.order_date END) AS "วันที่เจาะ2",
    MAX(CASE WHEN lh.order_date = dd2.bb2 THEN lo.lab_order_result END) AS "ผล2"
FROM vn_stat v
LEFT OUTER JOIN lab_head lh ON lh.vn = v.vn
LEFT OUTER JOIN lab_order lo ON lo.lab_order_number = lh.lab_order_number
LEFT OUTER JOIN lab_items li ON li.lab_items_code = lo.lab_items_code
LEFT OUTER JOIN patient p ON p.hn = v.hn
LEFT OUTER JOIN sex s ON s.code = v.sex
LEFT OUTER JOIN (SELECT vv2.hn
										  ,COUNT(*) AS visit_count 
								FROM vn_stat vv2 
								LEFT OUTER JOIN lab_head lh ON lh.vn = vv2.vn
    							LEFT OUTER JOIN lab_order lo ON lo.lab_order_number = lh.lab_order_number 
    							WHERE vv2.vstdate BETWEEN '2024-10-01' AND '2025-01-01' AND lo.lab_items_code IN ('78')  
    							GROUP BY hn) v2 
    					ON v2.hn = v.hn
LEFT OUTER JOIN (SELECT hn
										  ,MAX(order_date) AS aa1 
								FROM lab_head lh 
								JOIN lab_order lo ON lo.lab_order_number = lh.lab_order_number
    							WHERE lo.lab_items_code = '78' GROUP BY hn) cc1 
    					ON cc1.hn = v.hn
LEFT OUTER JOIN (SELECT hn
										  ,MAX(order_date) AS bb2 
								FROM lab_head lh 
								JOIN lab_order lo ON lo.lab_order_number = lh.lab_order_number
    							WHERE lo.lab_items_code = '78' AND order_date < (SELECT MAX(order_date) 
    																										FROM lab_head lh2 
    																										JOIN lab_order lo2 ON lo2.lab_order_number = lh2.lab_order_number
    																										WHERE lo2.lab_items_code = '78' AND lh2.hn = lh.hn) 
    							GROUP BY hn ) dd2 
    					ON dd2.hn = v.hn
WHERE v.vstdate BETWEEN '2024-10-01' AND '2025-01-01' AND lo.lab_items_code IN ('78') AND v2.visit_count <= 2 
GROUP BY v.hn ORDER BY v.hn
;

-- นิด optimized
SELECT
    p.cid,
    v.hn,
    p_name.full_name AS "NAME",
    MAX(CASE WHEN lo.lab_items_code = '78' THEN lh.order_date END) AS "วันที่เจาะ",
    MAX(CASE WHEN lo.lab_items_code = '78' AND lh.order_date = latest_cr.latest_date THEN lo.lab_order_result END) AS "ผล",
    MAX(CASE WHEN lo.lab_items_code = '78' AND lh.order_date = second_latest_cr.second_latest_date THEN lh.order_date END) AS "วันที่เจาะ2",
    MAX(CASE WHEN lo.lab_items_code = '78' AND lh.order_date = second_latest_cr.second_latest_date THEN lo.lab_order_result END) AS "ผล2"
FROM vn_stat v
LEFT JOIN patient p ON p.hn = v.hn
LEFT JOIN (SELECT hn, pname, fname, lname, CONCAT(pname, fname, ' ', lname) AS full_name FROM patient) AS p_name ON p_name.hn = v.hn
LEFT JOIN lab_head lh ON lh.vn = v.vn
LEFT JOIN lab_order lo ON lo.lab_order_number = lh.lab_order_number AND lo.lab_items_code = '78'
LEFT JOIN (
    SELECT lh_inner.hn, MAX(lh_inner.order_date) AS latest_date
    FROM lab_head lh_inner
    WHERE EXISTS (SELECT 1 FROM lab_order lo_inner WHERE lo_inner.lab_order_number = lh_inner.lab_order_number AND lo_inner.lab_items_code = '78')
    GROUP BY lh_inner.hn
) AS latest_cr ON latest_cr.hn = v.hn
LEFT JOIN (
    SELECT lh_inner.hn, MAX(lh_inner.order_date) AS second_latest_date
    FROM lab_head lh_inner
    WHERE EXISTS (SELECT 1 FROM lab_order lo_inner WHERE lo_inner.lab_order_number = lh_inner.lab_order_number AND lo_inner.lab_items_code = '78')
      AND lh_inner.order_date < (
          SELECT MAX(lh_inner2.order_date)
          FROM lab_head lh_inner2
          WHERE EXISTS (SELECT 1 FROM lab_order lo_inner2 WHERE lo_inner2.lab_order_number = lh_inner2.lab_order_number AND lo_inner2.lab_items_code = '78')
            AND lh_inner2.hn = lh_inner.hn
      )
    GROUP BY lh_inner.hn
) AS second_latest_cr ON second_latest_cr.hn = v.hn
LEFT JOIN (
    SELECT vv2.hn, COUNT(*) AS visit_count
    FROM vn_stat vv2
    LEFT JOIN lab_head lh_v2 ON lh_v2.vn = vv2.vn
    LEFT JOIN lab_order lo_v2 ON lo_v2.lab_order_number = lh_v2.lab_order_number AND lo_v2.lab_items_code = '78'
    WHERE vv2.vstdate BETWEEN '2024-10-01' AND '2025-01-01'
    GROUP BY vv2.hn
) AS v2 ON v2.hn = v.hn
WHERE v.vstdate BETWEEN '2024-10-01' AND '2025-01-01'
  AND EXISTS (SELECT 1 FROM lab_head lhh JOIN lab_order loo ON loo.lab_order_number = lhh.lab_order_number WHERE lhh.vn = v.vn AND loo.lab_items_code = '78')
  AND v2.visit_count <= 2
GROUP BY v.hn
ORDER BY v.hn
;

-- ใช้งาน
SELECT
    lh.lab_order_number,
    lh.vn,
    lh.hn,
    concat(p.pname, p.fname, " ", p.lname) AS ptname,
    lh.order_date,
    lh.order_time,
    lo.lab_items_code,
    lo.lab_order_result AS "Cr"
FROM
    lab_head lh
LEFT OUTER JOIN
    lab_order lo ON lh.lab_order_number = lo.lab_order_number
LEFT OUTER JOIN
    patient p ON p.hn = lh.hn
WHERE
    lh.order_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 90 DAY) AND CURDATE()
    AND lo.lab_items_code = 883
ORDER BY lh.hn , lh.order_date DESC, lh.order_time DESC
;

-- select specific date ไม่นับจำนวนการเจาะรายเดือน จะเห็นว่ามีการเจาะlab อื่นด้วย แต่ไม่มีผลขึ้น เพราะเรา เลือก JOIN แค่ item 78
SELECT
    lh.lab_order_number,
    lh.vn,
    lh.hn,
    concat(p.pname, p.fname, " ", p.lname) AS ptname,
    lh.order_date,
    lh.order_time,
    lo.lab_items_code,
    CASE
        WHEN lo.lab_items_code = 78 THEN lo.lab_order_result
        ELSE NULL
    END AS "Cr"
FROM
    lab_head lh
LEFT OUTER JOIN
    lab_order lo ON lh.lab_order_number = lo.lab_order_number AND lo.lab_items_code = 78
LEFT OUTER JOIN
    patient p ON p.hn = lh.hn
WHERE
    lh.order_date = "2025-04-03"
;

-- รับ YM ดูแค่ Cr ล่าสุด
SELECT
    p.hn,
    concat(p.pname, p.fname, " ", p.lname) AS ptname,
    '2025-03' AS YM,
    (
        SELECT
            sub_lo.lab_order_result
        FROM
            lab_head sub_lh
        LEFT OUTER JOIN
            lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
        WHERE
            sub_lh.hn = p.hn
            AND sub_lh.order_date BETWEEN '2025-03-01' AND '2025-03-31'
            AND sub_lo.lab_items_code = 78
        ORDER BY
            sub_lh.order_date DESC, sub_lh.order_time DESC
        LIMIT 1
    ) AS latest_cr_result
FROM
    patient p
WHERE
    EXISTS (
        SELECT 1
        FROM lab_head lh
        LEFT OUTER JOIN lab_order lo ON lh.lab_order_number = lo.lab_order_number
        WHERE lh.hn = p.hn
          AND lh.order_date BETWEEN '2025-03-01' AND '2025-03-31'
          AND lo.lab_items_code = 78
    )
ORDER BY
    p.hn;

-- 1mo
SELECT
    p.hn,
    concat(p.pname, p.fname, " ", p.lname) AS ptname,
    '2025-03' AS YM,
    (
        SELECT
            sub_lo.lab_order_result
        FROM
            lab_head sub_lh
        LEFT OUTER JOIN
            lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
        WHERE
            sub_lh.hn = p.hn
            AND sub_lh.order_date BETWEEN '2025-03-01' AND '2025-03-31'
            AND sub_lo.lab_items_code = 78
        ORDER BY
            sub_lh.order_date DESC, sub_lh.order_time DESC
        LIMIT 1
    ) AS latest_cr_result,
    (
        SELECT
            COUNT(*)
        FROM
            lab_head sub_lh
        LEFT OUTER JOIN
            lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
        WHERE
            sub_lh.hn = p.hn
            AND sub_lh.order_date BETWEEN '2025-03-01' AND '2025-03-31'
            AND sub_lo.lab_items_code = 78
    ) AS cr_count
FROM
    patient p
WHERE
    EXISTS (
        SELECT 1
        FROM lab_head lh
        LEFT OUTER JOIN lab_order lo ON lh.lab_order_number = lo.lab_order_number
        WHERE lh.hn = p.hn
          AND lh.order_date BETWEEN '2025-03-01' AND '2025-03-31'
          AND lo.lab_items_code = 78
    )
ORDER BY
    p.hn;

-- 2mo
SELECT
    p.hn,
    concat(p.pname, p.fname, " ", p.lname) AS ptname,
    -- ข้อมูลสำหรับเดือนกุมภาพันธ์ 2025
    (
        SELECT
            COUNT(*)
        FROM
            lab_head sub_lh
        LEFT OUTER JOIN
            lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
        WHERE
            sub_lh.hn = p.hn
            AND sub_lh.order_date BETWEEN '2025-02-01' AND '2025-02-28'
            AND sub_lo.lab_items_code = 78
    ) AS '2025_02_cr_count',
    (
        SELECT
            sub_lo.lab_order_result
        FROM
            lab_head sub_lh
        LEFT OUTER JOIN
            lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
        WHERE
            sub_lh.hn = p.hn
            AND sub_lh.order_date BETWEEN '2025-02-01' AND '2025-02-28'
            AND sub_lo.lab_items_code = 78
        ORDER BY
            sub_lh.order_date DESC, sub_lh.order_time DESC
        LIMIT 1
    ) AS '2025_02_latest_cr_result',
    -- ข้อมูลสำหรับเดือนมีนาคม 2025
    (
        SELECT
            COUNT(*)
        FROM
            lab_head sub_lh
        LEFT OUTER JOIN
            lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
        WHERE
            sub_lh.hn = p.hn
            AND sub_lh.order_date BETWEEN '2025-03-01' AND '2025-03-31'
            AND sub_lo.lab_items_code = 78
    ) AS '2025_03_cr_count',
    (
        SELECT
            sub_lo.lab_order_result
        FROM
            lab_head sub_lh
        LEFT OUTER JOIN
            lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
        WHERE
            sub_lh.hn = p.hn
            AND sub_lh.order_date BETWEEN '2025-03-01' AND '2025-03-31'
            AND sub_lo.lab_items_code = 78
        ORDER BY
            sub_lh.order_date DESC, sub_lh.order_time DESC
        LIMIT 1
    ) AS '2025_03_latest_cr_result'
FROM
    patient p
WHERE
    EXISTS (
        SELECT 1
        FROM lab_head lh
        LEFT OUTER JOIN lab_order lo ON lh.lab_order_number = lo.lab_order_number
        WHERE lh.hn = p.hn
          AND lh.order_date BETWEEN '2025-02-01' AND '2025-03-31'
          AND lo.lab_items_code = 78
    )
ORDER BY
    p.hn
;

-- 12mo
SELECT
    p.hn,
    concat(p.pname, p.fname, " ", p.lname) AS ptname,
    DATE_FORMAT(lh.order_date, '%Y-%m') AS YM,
    COUNT(CASE WHEN lo.lab_items_code = 78 THEN 1 ELSE NULL END) AS cr_count,
    (
        SELECT
            sub_lo.lab_order_result
        FROM
            lab_head sub_lh
        LEFT OUTER JOIN
            lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
        WHERE
            sub_lh.hn = p.hn
            AND DATE_FORMAT(sub_lh.order_date, '%Y-%m') = DATE_FORMAT(lh.order_date, '%Y-%m')
            AND sub_lo.lab_items_code = 78
        ORDER BY
            sub_lh.order_date DESC, sub_lh.order_time DESC
        LIMIT 1
    ) AS latest_cr_result
FROM
    patient p
JOIN
    lab_head lh ON p.hn = lh.hn
LEFT OUTER JOIN
    lab_order lo ON lh.lab_order_number = lo.lab_order_number AND lo.lab_items_code = 78
WHERE
    lh.order_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 12 MONTH) AND CURDATE()
GROUP BY
    p.hn,
    ptname,
    YM
ORDER BY
    p.hn,
    YM
;

-- 2ครั้งล่าสุด ห่างกัน > 90 วัน ไม่ work ควรอัป maria DB 12.2
SELECT
    p1.hn,
    p1.ptname,
    p1.order_date AS latest_cr_date,
    p1.order_time AS latest_cr_time,
    p1.cr_result AS latest_cr_result,
    p2.order_date AS previous_cr_date,
    p2.order_time AS previous_cr_time,
    p2.cr_result AS previous_cr_result
FROM
    (
        SELECT
            p.hn,
            concat(p.pname, p.fname, " ", p.lname) AS ptname,
            lh.order_date,
            lh.order_time,
            lo.lab_order_result AS cr_result,
            (
                SELECT COUNT(*)
                FROM lab_head sub_lh
                JOIN lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
                WHERE sub_lo.lab_items_code = 78
                  AND sub_lh.hn = p.hn
                  AND (sub_lh.order_date > lh.order_date OR (sub_lh.order_date = lh.order_date AND sub_lh.order_time >= lh.order_time))
            ) + 1 AS rn
        FROM
            patient p
        JOIN
            lab_head lh ON p.hn = lh.hn
        JOIN
            lab_order lo ON lh.lab_order_number = lo.lab_order_number
        WHERE
            lo.lab_items_code = 78
            AND lh.order_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE()
    ) AS p1
LEFT JOIN
    (
        SELECT
            p.hn,
            lh.order_date,
            lh.order_time,
            lo.lab_order_result AS cr_result,
            (
                SELECT COUNT(*)
                FROM lab_head sub_lh
                JOIN lab_order sub_lo ON sub_lh.lab_order_number = sub_lo.lab_order_number
                WHERE sub_lo.lab_items_code = 78
                  AND sub_lh.hn = p.hn
                  AND (sub_lh.order_date > lh.order_date OR (sub_lh.order_date = lh.order_date AND sub_lh.order_time >= lh.order_time))
            ) + 1 AS rn
        FROM
            patient p
        JOIN
            lab_head lh ON p.hn = lh.hn
        JOIN
            lab_order lo ON lh.lab_order_number = lo.lab_order_number
        WHERE
            lo.lab_items_code = 78
            AND lh.order_date BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 YEAR) AND CURDATE()
    ) AS p2 ON p1.hn = p2.hn AND p1.rn = 1 AND p2.rn = 2
WHERE
    p1.rn = 1
    AND p2.order_date <= DATE_SUB(p1.order_date, INTERVAL 90 DAY)
ORDER BY
    p1.hn;