gl main "C:\Users\felip\Documents\UdeSA\Maestría\Herramientas computacionales\TrabajosPracticos\TP final\Replication & Slave trade maps"
gl input "$main/input"
gl output "$main/output"

sort murdock_name

by murdock_name: egen prom_trust_relative=mean(trust_relatives)
by murdock_name: egen prom_trust_neigh=mean(trust_neighbors)
by murdock_name: egen prom_trust_intra=mean(intra_group_trust)
by murdock_name: egen prom_trust_inter=mean(inter_group_trust)
by murdock_name: egen prom_trust_gov=mean(trust_local_council)

by murdock_name: gen n=_n
keep if n==1
keep murdock_name isocode prom*

export delimited using "$output/Trust.csv", replace