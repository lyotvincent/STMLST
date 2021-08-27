import xlrd, subprocess, time, os

def extract_3_from_s_set():
    sheet = xlrd.open_workbook("/home/sjl/Workspace/aem.01746-19-sd002.xlsx").sheet_by_name('Table S1 (NARMS)')

    our_orgas = "	Abaetetuba	Aberdeen	Abony	Abortusequi	Abortusovis	Adelaide	Aderike	Agama	Agbeni	Ago	Agona	Ajiobo	Alachua	Albany	Altona	Amsterdam	Anatum	Anecho	Apapa	Arechavaleta	Ashford	Augustenborg	Baguida	Baildon	Bareilly	Berta	Binza	Blockley	Bonariensis	Bovismorbificans	Braenderup	Brandenburg	Brazzaville	Bredeney	Brunei	Caracas	Carmel	Carno	Carrau	Carshalton	Cerro	Charity	Chester	Choleraesuis	Coeln	Colchester	Coleypark	Colindale	Concord	CoppettsWood	Cork	Corvallis	Cotham	Cubana	Curacao	Derby	Dublin	Durham	Ealing	Eastbourne	Edinburg	Eimsbuettel	Emek	Enteritidis	Farsta	Florida	Fluntern	Frimley	Gafsa	Galiema	Gallinarum	Gaminara	Give	Glostrup	Goelzau	Gold coast	Goodmayes	Goverdhan	Hadar	Haifa	Harrow	Hartford	Havana	Heidelberg	Herston	Hull	Hvittingfoss	Idikan	Indiana	Inganda	Inverness	Ipswich	Irumu	Isangi	Java	Javiana	Jedburgh	Johannesburg	Kentucky	Kenya	Kiambu	Kibusi	Kingslynn	Kingston	Kintambo	Kisangani	Kisarawe	Kottbus	Kua	Labadi	Lagos	Lexington	Lika	Lille	Lingwala	Litchfield	Livingstone	Lomalinda	London	Maastricht	Manhattan	Maritzburg	Martonos	Matadi	Maybush	Mbandaka	Meleagridis	Mgulani	Miami	Mikawasima	Minnesota	Mississippi	Monschaui	Montevideo	Muenchen	Muenster	Naestved	Namur	Napoli	Nchanga	Newport	Newport I	Newport II	Newport III	Nima	Norwich	Nottingham	Oakland	Ohio	Oranienburg	Orientalis	Orion	Oslo	Panama	Paratyphi A	Paratyphi B	Paratyphi BI	Paratyphi BII	Paratyphi BIII	Paratyphi BIV	Paratyphi C	Pomona	Poole	Poona	Pullorum	Ramatgan	Reading	Richmond	Ridge	Rissen	Rubislaw	Saintpaul	Sandbanks	Sandiego	Schwarzengrund	Senftenberg	Singapore	Sloterdijk	Soerenga	Stafford	Stanley	Stanleyville	Sundsvall	Szentes	Tallahassee	Teko	Tennessee	Thompson	Tomegbe	Torbay	Treforest	Tucson	Typhi	Typhimurium	Typhisuis	Uganda	Umbilo	Urbana	Vejle	Virchow	Vitkin	Wandsworth	Wangata	Weltevreden	Welwyn	Weslaco	Westhampton	Worthington	Zanzibar	other	unknown	Infantis	Total"

    sero_dict = dict()
    for i in range(2, 2282):
        acc = sheet.cell_value(i, 1)
        serotype = sheet.cell_value(i, 3)
        if "Paratyphi" in serotype:
            serotype = "Paratyphi"
        serotype = serotype.lower()
        if ":" in serotype or serotype not in our_orgas.lower():
            continue
        # if ":" in serotype:
        #     continue
        if acc != "" and acc != None:
            if serotype not in sero_dict.keys():
                sero_dict[serotype] = list()
            sero_dict[serotype].append(acc)
    # print(sero_dict)
    # print(len(sero_dict.keys()))
    # j = 0
    # for i in sero_dict:
    #     j += len(sero_dict[i])
        # print(i, len(sero_dict[i]))
        # print(i, sero_dict[i][:3])
    # print(j)
    return sero_dict

if __name__ == "__main__":
    extract_3_from_s_set()