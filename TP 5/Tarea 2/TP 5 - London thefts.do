************************************************************************************
************************************************************************************
/*          		  HERRAMIENTAS COMPUTACIONALES DE INVESTIGACIÓN  		   	  */
/*								   TRABAJO PRÁCTICO 5  	 					   	  */
/*						  FELIPE GARCÍA VASSALLO & ROCÍO SENRA  			   	  */
************************************************************************************
************************************************************************************


/* INSTALACIÓN DE LOS PAQUETES NECESARIOS */

ssc install spmap
ssc install shp2dta
*net install sg162, from(http://www.stata.com/stb/stb60)
*net install st0292, from(http://www.stata-journal.com/software/sj13-2)
net install spwmatrix, from(http://fmwww.bc.edu/RePEc/bocode/s)
*net install splagvar, from(http://fmwww.bc.edu/RePEc/bocode/s)
*ssc install xsmle.pkg
*ssc install xtcsd
*net install st0446.pkg

cd "/Volumes/GoogleDrive/My Drive/UdeSA Maestria en Economia/Segundo Trimestre/Herramientas/TrabajosPracticos/TrabajosPracticos/TP 5/data"

use london_crime_shp.dta, clear

*Para las etiquetas
keep x_c y_c name
save "labels.dta", replace


*Cargamos la base
use london_crime_shp.dta, clear

*Armamos el mapa
spmap crimecount using coord_ls, id(id) line(data("coord_ls.dta") color(gs10) size(vthin)) ///
	clmethod(e) cln(4)  ///
	label(data("labels.dta") x(x_c) y(y_c) label(name) size(tiny))  ///
	legend(size(vsmall) position(5) xoffset(1)) legtitle("Amount of thefts by borough")  ///
	fcolor(Reds) plotregion(margin(large)) ndfcolor(gray)           


