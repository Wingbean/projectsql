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

'''
ช่อง 1 คือ check ว่าเป็น หรือไม่เป็นเบาหวาน ถ้าจำไม่ผิด จากการหาว่า มี ICD E110-E119 ไหม ไม่แน่ใจนะ

ช่อง 2 มีเหมือนกันถูกต้อง

ช่อง 3 ขึ้นทะเบียน ใน end user จะระบุ ว่า ขึ้นทะเบียน DM ในแฟ้ม chronic ไหม ถ้าใช่แสดงคำว่า DM //  ถ้าไม่มี DM ถึงจะดูว่าขึ้น HT ในแฟ้ม chronic ไหม ถ้ามี ขึ้นแสดงว่า HT // ถ้าไม่มีทั้งคู่ ค่อยแสดง -

ช่อง 4 check ว่า วันที่ ตรวจ LAB ผู้ป่วยมีการสั่งยาอะไรกลับบ้านไหม ถ้ามีแม้แต่ 1 รายการ ให้ขึ้นว่ามียา / ถ้าไม่มีการสั่งยาให้ขึ้นว่า ไม่มียา
'''
