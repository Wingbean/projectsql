select p.cid,lh.lab_order_number,lh.hn,concat(p.pname,p.fname,"  ",p.lname)as ptname,lh.order_date,lh.vn,concat("หมู่",v.moopart," ",t.full_name)as address 
,CASE WHEN lo.lab_items_code = 76 THEN lo.lab_order_result ELSE "-" END as "FBS"
,CASE WHEN lo.lab_items_code = 78 THEN lo.lab_order_result ELSE "-" END as "CR"
,CASE WHEN lo.lab_items_code = 91 THEN lo.lab_order_result ELSE "-" END as "HDL"
,CASE WHEN lo.lab_items_code = 92 THEN lo.lab_order_result ELSE "-" END as "LDL"
,CASE WHEN lo.lab_items_code = 102 THEN lo.lab_order_result ELSE "-" END as "Chol"
,CASE WHEN lo.lab_items_code = 103 THEN lo.lab_order_result ELSE "-" END as "TG"
,CASE WHEN lo.lab_items_code = 930 THEN lo.lab_order_result ELSE "-" END as "Uma"
,CASE WHEN lo.lab_items_code = 948 THEN lo.lab_order_result ELSE "-" END as "Hba1c"
,CASE WHEN lo.lab_items_code = 81 THEN lo.lab_order_result ELSE "-" END as "K"
,CASE WHEN lo.lab_items_code = 99 THEN lo.lab_order_result ELSE "-" END as "SGOT"
,CASE WHEN lo.lab_items_code = 100 THEN lo.lab_order_result ELSE "-" END as "SGPT"
,CASE WHEN lo.lab_items_code = 199 THEN lo.lab_order_result ELSE "-" END as "HCT"
,CASE WHEN lo.lab_items_code = 79 THEN lo.lab_order_result ELSE "-" END as "Uric"
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
