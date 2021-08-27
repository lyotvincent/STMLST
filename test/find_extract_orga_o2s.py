f = open("./md/seqsero_on_s_set_record.md", 'r')
lines = f.readlines()
f.close()

our_orgas = "	Abaetetuba	Aberdeen	Abony	Abortusequi	Abortusovis	Adelaide	Aderike	Agama	Agbeni	Ago	Agona	Ajiobo	Alachua	Albany	Altona	Amsterdam	Anatum	Anecho	Apapa	Arechavaleta	Ashford	Augustenborg	Baguida	Baildon	Bareilly	Berta	Binza	Blockley	Bonariensis	Bovismorbificans	Braenderup	Brandenburg	Brazzaville	Bredeney	Brunei	Caracas	Carmel	Carno	Carrau	Carshalton	Cerro	Charity	Chester	Choleraesuis	Coeln	Colchester	Coleypark	Colindale	Concord	CoppettsWood	Cork	Corvallis	Cotham	Cubana	Curacao	Derby	Dublin	Durham	Ealing	Eastbourne	Edinburg	Eimsbuettel	Emek	Enteritidis	Farsta	Florida	Fluntern	Frimley	Gafsa	Galiema	Gallinarum	Gaminara	Give	Glostrup	Goelzau	Gold coast	Goodmayes	Goverdhan	Hadar	Haifa	Harrow	Hartford	Havana	Heidelberg	Herston	Hull	Hvittingfoss	Idikan	Indiana	Inganda	Inverness	Ipswich	Irumu	Isangi	Java	Javiana	Jedburgh	Johannesburg	Kentucky	Kenya	Kiambu	Kibusi	Kingslynn	Kingston	Kintambo	Kisangani	Kisarawe	Kottbus	Kua	Labadi	Lagos	Lexington	Lika	Lille	Lingwala	Litchfield	Livingstone	Lomalinda	London	Maastricht	Manhattan	Maritzburg	Martonos	Matadi	Maybush	Mbandaka	Meleagridis	Mgulani	Miami	Mikawasima	Minnesota	Mississippi	Monschaui	Montevideo	Muenchen	Muenster	Naestved	Namur	Napoli	Nchanga	Newport	Newport I	Newport II	Newport III	Nima	Norwich	Nottingham	Oakland	Ohio	Oranienburg	Orientalis	Orion	Oslo	Panama	Paratyphi A	Paratyphi B	Paratyphi BI	Paratyphi BII	Paratyphi BIII	Paratyphi BIV	Paratyphi C	Pomona	Poole	Poona	Pullorum	Ramatgan	Reading	Richmond	Ridge	Rissen	Rubislaw	Saintpaul	Sandbanks	Sandiego	Schwarzengrund	Senftenberg	Singapore	Sloterdijk	Soerenga	Stafford	Stanley	Stanleyville	Sundsvall	Szentes	Tallahassee	Teko	Tennessee	Thompson	Tomegbe	Torbay	Treforest	Tucson	Typhi	Typhimurium	Typhisuis	Uganda	Umbilo	Urbana	Vejle	Virchow	Vitkin	Wandsworth	Wangata	Weltevreden	Welwyn	Weslaco	Westhampton	Worthington	Zanzibar	other	unknown	Infantis	Total"

all_false_sero = set()
for l in lines:
    if "1896 2048 0.92578125" in l or "1982 2048 0.9677734375" in l:
        continue
    lk = l.split("|")[2].strip()
    all_false_sero.add(lk)
print(all_false_sero)
print(len(all_false_sero))

orga_set = set()
for l in lines:
    if "1896 2048 0.92578125" in l:
        continue
    lk = l.split("|")[2].strip()
    if lk not in our_orgas:
        orga_set.add(lk)

print(orga_set)



