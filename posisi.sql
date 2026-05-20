select e.pernr ,
	   e.name ,
	   p.plans ,
	   p.psabv ,
	   p.pstxt 
from hris.itptka_hrm_employee e
inner join hris.itptka_hrm_posisi p 
	ON e.plans = p.plans 
	where e.persg not in ('5', '2')
	AND NULLIF(REGEXP_REPLACE(p.grade, '[^0-9]', '', 'g'), '')::integer >= 12
	and p.endat = '9999-12-31'