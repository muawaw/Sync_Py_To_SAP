select pernr, 
	   plans, 
	   posisi, 
	   orgeh, 
	   plans_pelakhar, 
	   pelakhar,
	   pymt,
	   tgl_mulai,
	   tgl_berakhir
from hris.itptka_pelakhar
	   where jenis = '1'
	   and tag = 1
	   AND tgl_mulai >= CURRENT_DATE - INTERVAL '1 month'
	   order by tgl_mulai desc