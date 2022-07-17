cd "C:\Users\felip\Documents\UdeSA\Maestría\Herramientas computacionales\TrabajosPracticos\TP 3"

use "MD_final.dta", clear

replace ID=11 if ID==.

egen objid_mes = concat(ID month), punct(-)

export delimited using "C:\Users\felip\Documents\UdeSA\Maestría\Herramientas computacionales\TrabajosPracticos\TP 3\crime_final.csv", replace
