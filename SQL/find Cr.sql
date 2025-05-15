SELECT
    p.cid,
    v.hn,
    CONCAT(p.pname, p.fname, ' ', p.lname) AS "NAME",
    MAX(CASE WHEN rn = 1 THEN lo.lab_order_result ELSE NULL END) AS "ผล creatinine 1",
    MAX(CASE WHEN rn = 2 THEN lo.lab_order_result ELSE NULL END) AS "ผล creatinine 2"
FROM vn_stat v
LEFT OUTER JOIN lab_head lh1 ON lh1.vn = v.vn
LEFT OUTER JOIN lab_order lo ON lo.lab_order_number = lh1.lab_order_number AND lo.lab_items_code = '78'
LEFT OUTER JOIN patient p ON p.hn = v.hn
LEFT OUTER JOIN (
    SELECT
        lh.vn,
        lo.lab_order_result,
        @rn := IF(@prev_vn = lh.vn, @rn + 1, 1) AS rn,
        @prev_vn := lh.vn
    FROM lab_head lh
    LEFT OUTER JOIN lab_order lo ON lo.lab_order_number = lh.lab_order_number
    JOIN (SELECT @rn := 0, @prev_vn := '') AS vars
    WHERE lo.lab_items_code = '78'
    ORDER BY lh.vn, lh.order_date DESC
) ranked_results ON ranked_results.vn = v.vn AND ranked_results.lab_order_result = lo.lab_order_result
WHERE v.vstdate BETWEEN '2024-01-01' AND '2025-02-28'
AND EXISTS (SELECT 1 FROM lab_head WHERE vn = v.vn AND lab_order_number IN (SELECT lab_order_number FROM lab_order WHERE lab_items_code = '78'))
AND ranked_results.rn <= 2
GROUP BY p.cid, v.hn, p.pname, p.fname, p.lname
ORDER BY (CASE WHEN MAX(lo.lab_order_result) IS NULL THEN 1 ELSE 0 END), v.hn;