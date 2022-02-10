
var country_arr = new Array("Afghanistan (AF)", "Albania (AL)", "Algeria (DZ)", "American Samoa (AS)", "Angola (AD)", "Anguilla (AI)", "Antartica (AQ)", "Antigua and Barbuda (AG)", "Argentina (AR)", "Armenia (AM)", "Aruba (AW)", "Australia (AU)", "Austria (AT)", "Azerbaijan (AZ)", "Bahamas (BS)", "Bahrain (BH)", "Bangladesh (BD)", "Barbados (BB)", "Belarus (BY)", "Belgium (BE)", "Belize (BZ)", "Benin (BJ)", "Bermuda (BM)", "Bhutan (BT)", "Bolivia (BO)", "Bosnia and Herzegovina (BA)", "Botswana (BW)", "Brazil (BR)", "British Virgin Islands (VG)", "Brunei (BG)", "Bulgaria (BN)", "Burkina Faso (BF)", "Burma (Myanmar) (MM)", "Burundi (BI)", "Cambodia (KH)", "Cameroon (CM)", "Canada (CA)", "Cape Verde (CV)", "Cayman Islands (KY)", "Central African Republic (CF)", "Chad (TD)", "Chile (CL)", "China (CN)", "Christmas Island (CX)", "Cocos (Keeling) Islands (CC)", "Colombia (CO)", "Comoros (KM)", "Congo, Democratic Republic (CD)", "Congo, Republic (CG)", "Cook Islands (CK)", "Costa Rica (CR)", "Cote d'Ivoire (CI)", "Croatia (HR)", "Cuba (CU)","Curaçao (CW)", "Cyprus (CY)", "Czeck Republic (CZ)", "Denmark (DK)", "Djibouti (DJ)", "Dominica (DM)", "Dominican Republic (DO)","East Timor (TP)", "Ecuador (EC)", "Egypt (EG)", "El Salvador (SV)", "Equatorial Guinea (GQ)", "Eritrea (ER)", "Estonia (EE)", "Ethiopia (ET)", "Falkland Islands (Islas Malvinas) (FK)", "Faroe Islands (FO)", "Fiji (FJ)", "Finland (FI)", "France (FR)", "French Guiana (GF)", "French Polynesia (PF)", "Gabon (GA)", "Gambia, The (GM)", "Georgia (GE)", "Germany (DE)", "Ghana (GH)", "Gibraltar (GI)", "Greece (GR)", "Greenland (GL)", "Grenada (GD)", "Guadeloupe (GP)", "Guam (GU)", "Guatemala (GT)", "Guernsey (GG)", "Guinea (GN)", "Guinea-Bissau (GW)", "Guyana (GY)", "Haiti (HT)", "Holy See (Vatican City) (VA)", "Honduras (HN)", "Hong Kong (HK)", "Hungary (HU)", "Iceland (IS)", "India (IN)", "Indonesia (ID)", "Iran (IR)", "Iraq (IQ)", "Ireland (IE)", "Israel (IL)", "Italy (IT)", "Jamaica (JM)", "Japan (JP)", "Jordan (JO)", "Kazakhstan (KZ)", "Kenya (KE)", "Kiribati (KI)", "Korea, North (KP)", "Korea, South (KR)", "Kuwait (KW)", "Kyrgyzstan (KG)", "Lao People's Democratic Republic (LA)", "Latvia (LV)", "Lebanon (LB)", "Lesotho (LS)", "Liberia (LR)", "Libya (LY)", "Liechtenstein (LI)", "Lithuania (LT)", "Luxembourg (LU)", "Macau (MO)", "Macedonia, Former Yugoslav Republic of (MK)", "Madagascar (MG)", "Malawi (MW)", "Malaysia (MY)", "Maldives (MV)", "Mali (ML)", "Malta (MT)", "Man, Isle of (IM)", "Marshall Islands (MH)", "Martinique (MQ)", "Mauritania (MR)", "Mauritius (MU)", "Mayotte (YT)", "Mexico (MX)", "Micronesia, Federated States of (FM)","Moldova (MD)", "Monaco (MC)", "Mongolia (MN)","Montenegro (ME)", "Montserrat (MS)", "Morocco (MA)","Mozambique (MZ)", "Namibia (NA)", "Nauru (NR)", "Nepal (NP)", "Netherlands (NL)", "New Caledonia (NC)", "New Zealand (NZ)", "Nicaragua (NI)", "Niger (NE)", "Nigeria (NG)", "Niue (NU)", "Norfolk Island (NF)", "Northern Mariana Islands (MP)", "Norway (NO)", "Oman (OM)", "Pakistan (PK)", "Palau (PW)", "Panama (PA)", "Papua New Guinea (PG)", "Paraguay (PY)", "Peru (PE)", "Philippines (PH)", "Palestinian Territory, Occupied (PS)", "Poland (PL)", "Portugal (PT)", "Puerto Rico (PR)", "Qatar (QA)", "Reunion (RE)", "Romainia (RO)", "Russia (RU)", "Rwanda (RW)", "Saint Helena (SH)", "Saint Kitts and Nevis (KN)", "Saint Lucia (LC)", "Saint Pierre and Miquelon (PM)", "Saint Vincent and the Grenadines (VC)", "Samoa (WS)", "San Marino (SM)", "Sao Tome and Principe (ST)", "Saudi Arabia (SA)", "Senegal (SN)","Serbia (RS)", "Seychelles (SC)", "Sierra Leone (SL)", "Singapore (SG)","Sint Marteen (SX)", "Slovakia (SK)", "Slovenia (SI)", "Solomon Islands (SB)", "Somalia (SO)", "South Africa (SA)","South Sudan (SS)", "Spain (ES)", "Sri Lanka (LK)", "Sudan (SD)", "Suriname (SR)", "Svalbard And Jan Mayen (SJ)", "Swaziland (SZ)", "Sweden  (SE)", "Switzerland (CH)", "Syria (SY)", "Taiwan (TW)", "Tajikistan (TJ)", "Tanzania (TZ)", "Thailand (TH)", "Trinidad and Tobago (TT)", "Togo (TG)", "Tonga (TO)", "Tunisia (TN)", "Turkey (TR)", "Turkmenistan (TM)", "Tuvalu (TV)", "Uganda(UG)", "Ukraine (UA)", "United Arab Emirates (AE)", "United Kingdom (GB)", "Uruguay (UY)", "United States of America (US)", "Uzbekistan (UZ)", "Vanuatu (VU)", "Venezuela (VE)", "Vietnam (VN)", "Virgin Islands, United States (VI)", "Wallis and Futuna (WF)", "Yemen (YE)", "Zambia (ZM)", "Zimbabwe (ZW)");																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																									    
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																			    
			//remove antartica																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																				   
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																													// States
var s_a = new Array();
s_a[0]="";
s_a[1]="Badakhshan|Badghis|Baghlan|Balkh|Bamyan|Daykundi|Farah|Faryab|Ghazni|Ghor|Helmand|Herat|Jowzjan|Kabul|Kandahar|Kapisa|Khost|Kunar|Kunduz|Laghman|Logar|Nangarhar|Nimruz|Nuristan|Paktia|Paktika|Panjshir|Parwan|Samangan|Sar-e Pol|Takhar|Uruzgan|Wardak|Zabul";
s_a[2]="Berat County|Dibër County|Durrës County|Elbasan County|Fier County|Gjirokastër County|Korçë County|Kukës County|Lezhë County|Shkodër County|Tirana County|Vlorë County";
s_a[3]="Adrar|Aïn Defla|Aïn Témouchent|Algiers|Annaba|Batna|Béchar|Béjaïa|Béni Abbès|Biskra|Blida|Bordj Baji Mokhtar|Bordj Bou Arréridj|Bouïra|Boumerdès|Chlef|Constantine|Djanet|Djelfa|El Bayadh|El M'ghair|El Menia|El Oued|El Taref|Ghardaïa|Guelma|Illizi|In Guezzam|In Salah|Jijel|Khenchela|Laghouat|M'sila|Mascara|Médéa|Mila|Mostaganem|Naâma|Oran|Ouargla|Ouled Djellal|Oum el-Bouaghi|Relizane|Saïda|Sétif|Sidi Bel Abbès|Skikda|Souk Ahras|Tamanghasset|Tébessa|Tiaret|Timimoun|Tindouf|Tipaza|Tissemsilt|Tizi Ouzou|Tlemcen|Touggourt";
s_a[4]="American Samao";
s_a[5]="Bengo|Benguela|Bié|Cabinda|Cuando Cubango|Cuanza Norte|Cuanza Sul|Cunene|Huambo|Huíla|Luanda|Lunda Norte|Lunda Sul|Malanje|Moxico|Namibe|Uíge|Zaire";
s_a[6]="Blowing Point|East End|George Hill|Island Harbour|North Hill|North Side|Sandy Ground|Sandy Hill|South Hill|Stoney Ground|The Farrington|The Quarter|The Valley|West End";
s_a[7]="Antartica";
s_a[8]="Barbuda|Redonda|Saint George Parish|Saint John Parish|Saint Mary Parish|Saint Paul Parish|Saint Peter Parish|Saint Philip Parish";
s_a[9]="Buenos Aires|Catamarca|Chaco|Chubut|Ciudad de Buenos Aires|Córdoba|Corrientes|Entre Ríos|Formosa|Jujuy|La Pampa|La Rioja|Mendoza|Misiones|Neuquén|Río Negro|Salta|San Juan|San Luis|Santa Cruz|Santa Fe|Santiago del Estero|Tierra del Fuego|Tucumán";
s_a[10]="Aragatsotn|Ararat|Armavir|Gegharkunik|Kotayk|Lori|Shirak|Syunik|Tavush|Vayots Dzor|Yerevan";
s_a[11]="Aruba";
s_a[12]="Australian Capital Territory|New South Wales|Northern Territory|Queensland|South Australia|Tasmania|Victoria|Western Australia";
s_a[13]="Burgenland|Carinthia|Lower Austria|Upper Austria|Salzburg|Styria|Tyrol|Vorarlberg|Vienna";
s_a[14]="Absheron|Agjabadi|Agdam|Agdash|Agstafa|Agsu|Astara|Babek|Balakan|Barda|Beylagan|Bilasuvar|Dashkasan|Davachi|Fizuli|Gadabay|Goranboy|Goychay|Hajigabul|Imishli|Ismailli|Jabrayil|Jalilabad|Julfa|Kalbajar|Kangarli|Kurdamir|Lachin|Lankaran|Lerik|Masally|Neftchala|Oguz|Ordubad|Qabala|Qakh|Qazakh|Qobustan|Quba|Qubadli|Qusar|Saatly|Sabirabad|Sadarak|Shaki|Shahbuz|Sharur|Salyan|Shamakhi|Shamkir|Samukh|Siazan|Shusha|Tartar|Tovuz|Ujar|Khachmaz|Goygol|Khizi|Khojali|Khojavend|Yardymli|Yevlakh|Zangilan|Zaqatala|Zardab";
s_a[15]="Acklins|Berry Islands|Bimini|Black Point|Cat Island|Central Abaco|Central Andros|Central Eleuthera|Crooked Island|East Grand Bahama|Exuma|Grand Cay|Harbour Island|Hope Town|Inagua|Long Island|Mangrove Cay|Mayaguana|Moore's Island|New Providence|North Abaco|North Andros|North Eleuthera|Ragged Island|Rum Cay|San Salvador|South Abaco|South Andros|South Eleuthera|Spanish Wells|West Grand Bahama";
s_a[16]=" Capital Governorate| Muharraq Governorate|Northern Governate|Southern Governate";
s_a[17]="Barisal|Chittagong|Dhaka|Khulna|Mymensingh|Rajshahi|Sylhet|Rangpur";
s_a[18]="Christ Church|Saint Andrew|Saint George|Saint James|Saint John|Saint Joseph|Saint Lucy|Saint Michael|Saint Peter|Saint Philip|Saint Thomas";
s_a[19]=" Minsk|Minsk Region|Gomet Region|Brest Region|Grodno Region|Vitebsk Region|Mogilev Region"; 
s_a[20]="Brussels Region|Flemish Region|Walloon Region";
s_a[21]="Belize|Cayo|Corozal|Orange Walk|Stann Creek|Toledo";
s_a[22]="Alibori|Atakora|Atlantique|Borgou|Collines|Donga|Kuoffo|Littoral|Mono|Ouémé|Plateau|Zou";
s_a[23]="Devonshire|Hamilton|Paget|Pembroke|Saint George's|Sandys|Smith's|Southampton|Warwick";
s_a[24]="Bumthang|Daga|Kurmaed|Kurtoed|Paro|Punakha|Thimphu|Trongsa|Wangdue Phodrang";
s_a[25]="Beni|Chuquisaca|Cochabamba|La Paz|Oruro|Pando|Potosi|Santa Cruz|Tarija";
s_a[26]="Brčko District|Federation of Bosnia and Herzegovina|Republika Srpska";
s_a[27]="Central|Chobe|Ghanzi|Kgalagadi|Kgatleng|Kweneng|Ngamiland|North-East|South-East|Southern";
s_a[28]="Acre|Alagoas|Amapá|Amazonas|Bahia|Ceará|Distrito Federal|Espírito Santo|Goiás|Maranhão|Mato Grosso|Mato Grosso do Sul|Minas Gerais|Pará|Paraíba|Paraná|Pernambuco|Piauí|Rio de Janeiro|Rio Grande do Norte|Rio Grande do Sul|Rondônia|Roraima|Santa Catarina|São Paulo|Sergipe|Tocantins";
s_a[29]="Anegada|Jost Van Dyke|Tortola|Virgin Gorda";
s_a[30]="Belait|Brunei-Muara|Temburong|Tutong";
s_a[31]="Severozapaden Planning|Severen Tsentralen Planning|Severoiztochen Planning|Yugozapaden Planning|Yuzhen Tsentralen Planning|Yugoiztochen Planning";
s_a[32]="Boucle du Mouhoun|Cascades|Centre|Centre-Est|Centre-Nord|Centre-Ouest|Centre-Sud|Est|Hauts-Bassins|Nord|Plateau-Central|Sahel|Sud-Ouest";
s_a[33]="Ayeyarwady|Bago|Chin|Kachin|Kayah|Kayin|Magway|Mandalay|Mon State|Naypyidaw Union Territory|Rakhine|Sagaing|Shan|Tanintharyi|Yangon";
s_a[34]="Bubanza|Bujumbura Mairie|Bujumbura Rural|Bururi|Cankuzo|Cibitoke|Gitega|Karuzi|Kayanza|Kirundo|Makamba|Muramvya|Muyinga|Mwaro|Ngozi|Rumonge|Rutana|Ruyigi";
s_a[35]="Banteay Meancheay|Battambang|Kampong Cham|Kampong Chhnang|Kampong Speu|Kampong Thom|Kampot|Kandal|Kep|Koh Kong|Kratié|Mondulkiri|Oddar Meanchey|Pailin|Phnom Penh|Preah Sihanouk|Preah Vihear|Prey Veng|Pursat|Ratanak Kiri|Siem Reap|Stung Treng|Svay Rieng|Takéo";
s_a[36]="Adamawa|Central|East|Far North|Littoral|North|Northwest|South|Southwest|West";
s_a[37]="Alberta|British Columbia|Manitoba|New Brunswick|Newfoundland and Labrador|Northwest Territories|Nova Scotia|Nunavut|Ontario|Prince Edward Island|Quebec|Saskatchewan|Yukon Territory";
s_a[38]="Boa Vista|Brava|Maio|Mosteiros|Paul|Porto Novo|Praia|Ribeira Brava|Ribeira Grande|Ribeira Grande de Santiago|Sal|Santa Catarina|Santa Catarina do Fogo|Santa Cruz|São Domingos|São Filipe|São Lourenço dos Órgãos|São Miguel|São Salvador do Mundo|São Vicente|Tarrafal|Tarrafal de São Nicolau";
s_a[39]="Cayman Islands";
s_a[40]="Bangui|Bamingui-Bangoran|Basse-Kotto|Haute-Kotto|Haut-Mbomou|Kémo|Lobaye|Mambéré-Kadéï|Mbomou|Nana-Grébizi|Nana-Mambéré|Ombella-M'Poko|Ouaka|Ouham|Ouham-Pendé|Sangha-Mbaéré|Vakaga";
s_a[41]="Bahr el Gazel|Batha|Borkou|Chari-Baguirmi|Ennedi-Est|Ennedi-Ouest|Guéra|Hadjer-Lamis|Kanem|Lac|Logone Occidental|Logone Oriental|Mandoul|Mayo-Kebbi Est|Mayo-Kebbi Ouest|Moyen-Chari|N'Djamena|Ouaddaï|Salamat|Sila|Tandjilé|Tibesti|Wadi Fira";
s_a[42]="Arica y Parinacota|Antofagasta|Araucanía|Atacama|Aysén|Biobío|Coquimbo|Los Lagos|Los Ríos|Magellan and the Chilean Antarctic|Maule|Ñuble|O'Higgins|Santiago Metropolitan|Tarapacá|Valparaíso";
s_a[43]="Anhui|Beijing|Chongqing|Fujian|Gansu|Guangdong|Guangxi Zhuang Autonomous|Guizhou|Hainan|Hebei|Heilongjiang|Henan|Hubei|Hunan|Inner Mongolia Autonomous|Jiangsu|Jiangxi|Jilin|Liaoning|Nei Mongol|Ningxia Hui Autonomous|Qinghai|Shaanxi|Shandong|Shanghai|Shanxi|Sichuan|Tianjin|Tibet Autonomous|Xinjiang Uyghur Autonomous|Yunnan|Zhejiang";
s_a[44]="Christmas Island";
s_a[45]="Direction Island|Home Island|Horsburgh Island|North Keeling Island|South Island|West Island";
s_a[46]="Amazonas|Antioquia|Arauca|Atlántico|Bogotá|Bolívar|Boyacá|Caldas|Caquetá|Casanare|Cauca|Cesar|Chocó|Córdoba|Cundinamarca|Guainía|Guaviare|Huila|La Guajira|Magdalena|Meta|Nariño|Norte de Santander|Putumayo|Quindío|Risaralda|San Andrés y Providencia|Santander|Sucre|Tolima|Valle del Cauca|Vaupés|Vichada";
// <!-- -->
s_a[47]="Anjouan|Grande Comore|Mohéli";
s_a[48]="Bas-Uele|Équateur|Haut-Katanga|Haut-Lomami|Haut-Uele|Ituri|Kasaï|Kasaï-Central|Kasaï-Oriental|Kinshasa|Kongo Central|Kwango|Kwilu|Lomami|Lualaba|Mai-Ndombe|Maniema|Mongala|Nord-Ubangi|North Kivu|Sankuru|South Kivu|Sud-Ubangi|Tanganyika|Tshopo|Tshuapa";
s_a[49]="Bouenza|Brazzaville|Cuvette|Cuvette-Ouest|Kouilou|Lékoumou|Likouala|Niari|Plateaux|Pointe-Noire|Pool|Sangha";
s_a[50]="Cooks Island";
s_a[51]="Alajuela|Cartago|Guanacaste|Heredia|Limón|Puntarenas|San José";
s_a[52]="Abidjan|Bas-Sassandra|Comoé|Denguélé|Gôh-Djiboua|Lacs|Lagunes|Montagnes|Sassandra-Marahoué|Savanes|Vallée du Bandama|Woroba|Yamoussoukro|Zanzan";
s_a[53]="Bjelovar-Bilogora|Brod-Posavina|Dubrovnik-Neretva|Istria|Karlovac|Koprivnica-Križevci|Krapina-Zagorje|Lika-Senj|Međimurje|Osijek-Baranja|Požega-Slavonia|Primorje-Gorski Kotar|Šibenik-Knin|Sisak-Moslavina|Split-Dalmatia|Varaždin|Virovitica-Podravina|Vukovar-Syrmia|Zadar|Zagreb|City of Zagreb";
s_a[54]="Artemisa|Camagüey|Ciego de Ávila|Cienfuegos|Ciudad de La Habana|Granma|Guantánamo|Holguín|Isla de la Juventud|Las Tunas|Matanzas|Mayabeque|Pinar del Río|Sancti Spíritus|Santiago de Cuba|Villa Clara";
s_a[55]="Curaçao";

s_a[56]="Famagusta|Kyrenia|Larnaca|Limassol|Nicosia|Paphos";
s_a[57]="Central Bohemian|Hradec Králové|Karlovy Vary|Liberec|Moravian-Silesian|Olomouc|Pardubice|Plzeň|Prague|South Bohemian|South Moravian|Ústí nad Labem|Vysočina|Zlín";
s_a[58]="Capital Region of Denmark|Central Denmark Region|North Denmark Region|Southern Denmark|Region Zealand";
s_a[59]="'Ali Sabieh|Arta|Dikhil|Djibouti|Obock|Tadjourah";
s_a[60]="Saint Andrew Parish|Saint David Parish|Saint George Parish|Saint John Parish|Saint Joseph Parish|Saint Luke Parish|Saint Mark Parish|Saint Patrick Parish|Saint Paul Parish|Saint Peter Parish";
s_a[61]="Azua|Baoruco|Barahona|Dajabón|Distrito Nacional|Duarte|Elías Piña|El Seibo|Espaillat|Hato Mayor|Hermanas Mirabal|Independencia|La Altagracia|La Romana|La Vega|María Trinidad Sánchez|Monseñor Nouel|Monte Cristi|Monte Plata|Pedernales|Peravia|Puerto Plata|Samaná|San Cristóbal|San José de Ocoa|San Juan|San Pedro de Macorís|Sánchez Ramírez|Santiago|Santiago Rodríguez|Santo Domingo|Valverde";
s_a[62] ="Aileu Municipality|Ainaro Municipality|Baucau Municipality|Bobonaro Municipality|Cova Lima Municipality|Dili Municipality|Ermera Municipality|Lautém Municipality|Liquiçá Municipality|Manatuto Municipality|Manufahi Municipality|Oecusse Municipality|Viqueque Municipality";
// <!-- -->
s_a[63]="Azuay|Bolívar|Cañar|Carchi|Chimborazo|Cotopaxi|El Oro|Esmeraldas|Galápagos|Guayas|Imbabura|Loja|Los Ríos|Manabí|Morona-Santiago|Napo|Orellana|Pastaza|Pichincha|Santa Elena|Santo Domingo de los Tsáchilas|Sucumbíos|Tungurahua|Zamora-Chinchipe";
s_a[64]="Alexandria|Aswan|Asyut|Beheira|Beni Suef|Cairo|Dakahlia|Damietta|Faiyum|Gharbia|Giza|Ismailia|Kafr El Sheikh|Luxor|Matruh|Minya|Monufia|New Valley|North Sinai|Port Said|Qalyubia|Qena|Red Sea|Sharqia|Sohag|South Sinai|Suez";
s_a[65]="Ahuachapán|Cabañas|Chalatenango|Cuscatlán|La Libertad|La Paz|La Unión|Morazán|San Miguel|San Salvador|San Vicente|Santa Ana|Sonsonate|Usulután";

s_a[66]="Annobón|Bioko Norte|Bioko Sur|Centro Sur|Djibloho|Kié-Ntem|Litoral|Wele-Nzas";
s_a[67]="Anseba|Debub|Gash-Barka|Maekel|Northern Red Sea|Southern Red Sea";
s_a[68]="Harju|Hiiu|Ida-Viru|Järva|Jõgeva|Lääne|Lääne-Viru|Pärnu|Põlva|Rapla|Saare|Tartu|Valga|Viljandi|Võru";
s_a[69]="Addis Ababa|Afar|Amhara|Benishangul-Gumuz|Dire Dawa|Gambela|Harari|Oromia|Sidama|Somali|Southern Nations, Nationalities, and Peoples' Region|Tigray";
s_a[70]="Falkland Islands"
s_a[71]="Eysturoy|Norðoyar|Sandoy|Streymoy|Suduroy|Vágar";
s_a[72]="Central|Eastern|Northern|Rotuma|Western";
s_a[73]="Åland|Central Finland|Central Ostrobothnia|Kainuu|Kymenlaakso|Lapland|North Karelia|North Ostrobothnia|Northern Savonia|Ostrobothnia|Päijänne Tavastia|Pirkanmaa|Satakunta|South Karelia|South Ostrobothnia|Southern Savonia|Finland Proper|Tavastia Proper|Uusimaa";
s_a[74]="Auvergne-Rhône-Alpes|Bourgogne-Franche-Comté|Brittany|Centre-Val de Loire|Corsica|Grand Est|Hauts-de-France|Île-de-France|Normandy|Nouvelle-Aquitaine|Occitanie|Pays de la Loire|Provence-Alpes-Côte d'Azur";
s_a[75]="French Guiana";
s_a[76]="French Polynesia";
s_a[77]="Estuaire|Haut-Ogooué|Moyen-Ogooué|Ngounié|Nyanga|Ogooué-Ivindo|Ogooué-Lolo|Ogooué-Maritime|Woleu-Ntem";
s_a[78]="Banjul|Central River|Lower River|North Bank|Upper River|Western";
s_a[79]="Abkhazia|Adjara|Guria|Imereti|Kakheti|Kvemo Kartli|Mtskheta-Mtianeti|Racha-Lechkhumi and Kvemo Svaneti|Samegrelo-Zemo Svaneti|Samtskhe-Javakheti|Shida Kartli|South Ossetia|Tbilisi";
s_a[80]="Baden-Württemberg|Bavaria|Berlin|Brandenburg|Bremen|Hamburg|Hesse|Lower Saxony|Mecklenburg-Vorpommern|North Rhine-Westphalia|Rhineland-Palatinate|Saarland|Saxony|Saxony-Anhalt|Schleswig-Holstein|Thuringia";
s_a[81]="Ahafo|Ashanti|Bono|Bono East|Central|Eastern|Greater Accra|Northern|North East|Oti|Savanna|Upper East|Upper West|Volta|Western|Western North";
s_a[82]="Gibraltar";

s_a[83]="Aegean|Attica|Crete|Epirus|Centre Macedonia|Peloponnese|Thessaly";
s_a[84]="Avannaata|Kujalleq|Qeqertalik|Qeqqata|Sermersooq";
s_a[85]="Carriacou and Petite Martinique|Saint Andrew|Saint David|Saint George|Saint John|Saint Mark|Saint Patrick";
s_a[86]="Guadeloupe";
s_a[87]="Guam";
s_a[88]="Alta Verapaz|Baja Verapaz|Chimaltenango|Chiquimula|El Progreso|Escuintla|Guatemala|Huehuetenango|Izabal|Jalapa|Jutiapa|Petén|Quetzaltenango|Quiché|Retalhuleu|Sacatepéquez|San Marcos|Santa Rosa|Sololá|Suchitepéquez|Totonicapán|Zacapa";
s_a[89]="Guernsey";
s_a[90]="Boké|Conakry|Faranah|Kankan|Kindia|Labé|Mamou|Nzérékoré";
s_a[91]="Bafatá|Biombo|Bissau|Bolama|Cacheu|Gabú|Oio|Quinara|Tombali";
s_a[92]="Barima-Waini|Pomeroon-Supenaam|Essequibo Islands-West Demerara|Demerara-Mahaica|Mahaica-Berbice|East Berbice-Corentyne|Cuyuni-Mazaruni|Potaro-Siparuni|Upper Takutu-Upper Essequibo|Upper Demerara-Berbice";
s_a[93]="Artibonite|Centre|Grand'Anse|Nippes|Nord|Nord-Est|Nord-Ouest|Ouest|Sud|Sud-Est";
s_a[94]="Vatican City"
s_a[95]="Atlántida|Bay Islands|Choluteca|Colón|Comayagua|Copán|Cortés|El Paraíso|Francisco Morazán|Gracias a Dios|Intibucá|La Paz|Lempira|Ocotepeque|Olancho|Santa Bárbara|Valle|Yoro";
s_a[96]="Hong Kong Island|Kowloon|New Territories";

s_a[97]="Baranya|Bács-Kiskun|Békés|Borsod-Abaúj-Zemplén|Budapest|Csongrád-Csanád|Fejér|Győr-Moson-Sopron|Hajdú-Bihar|Heves|Jász-Nagykun-Szolnok|Komárom-Esztergom|Nógrád|Pest|Somogy|Szabolcs-Szatmár-Bereg|Tolna|Vas|Veszprém|Zala";
s_a[98]="Austurland|Höfuðborgarsvæðið|Norðurland eystra|Norðurland vestra|Suðurland|Suðurnes|Vestfirðir|Vesturland";
s_a[99]="Andaman and Nicobar Islands|Arunachal Pradesh|Andhra Pradesh|Assam|Bihar|Chandigarh|Chhattisgarh|Dadra and Nagar Haveli and Daman and Diu|Delhi|Goa|Gujarat|Haryana|Himachal Pradesh|Jammu and Kashmir|Jharkhand|Karnataka|Kerala|Ladakh|Lakshadweep|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Puducherry|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal";
s_a[100]="Aceh|Bali|Bangka Belitung Islands|Banten|Bengkulu|Central Java|Central Kalimantan|Central Sulawesi|East Java|East Kalimantan|East Nusa Tenggara|Gorontalo|Jakarta|Jambi|Irian Jaya|Jakarta Raya|Jambi|Lampung|Maluku|North Kalimantan|North Maluku|North Sulawesi|North Sumatra|Papau|Riau|Riau Islands|Southeast Sulawesi|South Kalimantan|South Sulawesi|South Sumatra|West Java|West Kalimantan|West Nusa Tenggara|West Papau|West Sulawesi|West Sumatra|Yogyakarta";
s_a[101]="Alborz|Ardabil|Bushehr|Chaharmahal and Bakhtiari|East Azerbaijan|Fars|Gilan|Golestan|Hamadan|Hormozgan|Ilam|Isfahan|Kerman|Kermanshah|Khuzestan|Kohgiluyeh and Boyer-Ahmad|Kurdistan|Lorestan|Markazi|Mazandaran|North Khorasan|Qazvin|Qom|Razavi Khorasan|Semnan|Sistan and Baluchestan|South Khorasan|Tehran|West Azerbaijan|Yazd|Zanjan";
s_a[102]="Anbar|Babil|Baghdad|Basra|Dhi Qar|Diyala|Dohuk|Erbil|Halabja|Karbala|Kirkuk|Maysan|Muthanna|Najaf|Nineveh|Qadisiyyah|Saladin|Sulaymaniyah|Wasit";
s_a[103]="Connacht|County Cavan|County Donegal|County Monaghan|Leinster|Munster";

s_a[104]="Central District|Haifa District|Jerusalem District|Northern District|Southern District|Tel Aviv District";
s_a[105]="Abruzzo|Aosta Valley|Apulia|Basilicata|Calabria|Campania|Emilia-Romagna|Friuli Venezia Giulia|Lazio|Liguria|Lombardy|Marche|Molise|Piedmont|Sardinia|Sicily|Trentino-South Tyrol|Tuscany|Umbria|Veneto";
s_a[106]="Clarendon|Hanover|Kingston|Manchester|Portland|Saint Andrew|Saint Ann|Saint Catherine|Saint Elizabeth|Saint James|Saint Mary|Saint Thomas|Trelawny|Westmoreland";
s_a[107]="Aichi|Akita|Aomori|Chiba|Ehime|Fukui|Fukuoka|Fukushima|Gifu|Gumma|Hiroshima|Hokkaido|Hyōgo|Ibaraki|Ishikawa|Iwate|Kagawa|Kagoshima|Kanagawa|Kōchi|Kumamoto|Kyoto|Mie|Miyagi|Miyazaki|Nagano|Nagasaki|Nara|Niigata|Ōita|Okayama|Okinawa|Osaka|Saga|Saitama|Shiga|Shimane|Shizuoka|Tochigi|Tokushima|Tokyo|Tottori|Toyama|Wakayama|Yamagata|Yamaguchi|Yamanashi";
s_a[108]="Ajloun|Amman|Aqaba|Balqa|Irbid|Jerash|Karak|Ma'an|Madaba|Mafraq|Tafilah|Zarqa";

s_a[109]="Akmola|Aktobe|Almaty|Atyrau|East Kazakhstan|Jambyl|Karaganda|Kostanay|Kyzylorda|Mangystau|North Kazakhstan|Nur-Sultan|Pavlodar|Shymkent|Turkistan|West Kazakhstan";
s_a[110]="Baringo|Bomet|Bungoma|Busia|Elgeyo-Marakwet|Embu|Garissa|Homa Bay|Isiolo|Kajiado|Kakamega|Kericho|Kiambu|Kilifi|Kirinyaga|Kisii|Kisumu|Kitui|Kwale|Laikipia|Lamu|Machakos|Makueni|Mandera|Marsabit|Meru|Migori|Mombasa|Murang'a|Nairobi|Nakuru|Nandi|Narok|Nyamira|Nyandarua|Nyeri|Samburu|Siaya|Taita-Taveta|Tana River|Tharaka-Nithi|Trans-Nzoia|Turkana|Uasin Gishu|Vihiga|Wajir|West Pokot";
s_a[111]="Abaiang|Abemama|Aranuka|Arorae|Banaba|Banaba|Beru|Butaritari|Central Gilberts|Gilbert Islands|Kanton|Kiritimati|Kuria|Line Islands|Line Islands|Maiana|Makin|Marakei|Nikunau|Nonouti|Northern Gilberts|Onotoa|Phoenix Islands|Southern Gilberts|Tabiteuea|Tabuaeran|Tamana|Tarawa|Tarawa|Teraina";
s_a[112]="Chagang|North Hamgyong|South Hamgyong|North Hwanghae|South Hwanghae|Kangwon|North Pyongan|South Pyongan|Ryanggang";
s_a[113]="Busan|Daegu|Daejeon|Gwangju|Incheon|North Chungcheong|South Chungcheong|Gangwon|Gyeonggi|Jeju|North Gyeongsang|Sejong|Seoul|South Gyeongsang|North Jeolla|South Jeolla|Ulsan";
s_a[114]="Ahmadi Governate|Al Farwaniya Governate|Al-Kabeer Governate|Capital Governate|Hawalli Governate|Jahra Governate|Mubarak Governate";
s_a[115]="Batken|Bishkek|Chuy|Issyk-Kul|Jalal-Abad|Naryn|Osh|Talas";
s_a[116]="Attapeu Province|Bokeo Province|Bolikhamsai Province|Champasak Province|Houaphanh Province|Khammouane Province|Luang Namtha Province|Luang Prabang Province|Oudomxay Province|Phongsaly Province|Sainyabuli Province|Salavan Province|Savannakhet Province|Sekong Province|Vientiane Province|Vientiane Prefecture|Xaisomboun Province|Xiangkhouang Province";
s_a[117]="Aglona Municipality|Aizkraukle Municipality|Aizpute Municipality|Aknīste Municipality|Aloja Municipality|Alsunga Municipality|Alūksne Municipality|Amata Municipality|Ape Municipality|Auce Municipality|Ādaži Municipality|Babīte Municipality|Baldone Municipality|Baltinava Municipality|Balvi Municipality|Bauska Municipality|Beverīna Municipality|Brocēni Municipality|Burtnieki Municipality|Carnikava Municipality|Cesvaine Municipality|Cēsis Municipality|Cibla Municipality|Dagda Municipality|Daugavpils Municipality|Daugavpils|Dobele Municipality|Dundaga Municipality|Durbe Municipality|Engure Municipality|Ērgļi Municipality|Garkalne Municipality|Grobiņa Municipality|Gulbene Municipality|Iecava Municipality|Ikšķile Municipality|Ilūkste Municipality|Inčukalns Municipality|Jaunjelgava Municipality|Jaunpiebalga Municipality|Jaunpils Municipality|Jelgava Municipality|Jelgava|Jēkabpils Municipality|Jēkabpils|Jūrmala|Kandava Municipality|Kārsava Municipality|Kocēni Municipality|Koknese Municipality|Krāslava Municipality|Krimulda Municipality|Krustpils Municipality|Kuldīga Municipality|Ķegums Municipality|Ķekava Municipality|Lielvārde Municipality|Liepāja|Limbaži Municipality|Līgatne Municipality|Līvāni Municipality|Lubāna Municipality|Ludza Municipality|Madona Municipality|Mazsalaca Municipality|Mālpils Municipality|Mārupe Municipality|Mērsrags Municipality|Naukšēni Municipality|Nereta Municipality|Nīca Municipality|Ogre Municipality|Olaine Municipality|Ozolnieki Municipality|Pārgauja Municipality|Pāvilosta Municipality|Pļaviņas Municipality|Preiļi Municipality|Priekule Municipality|Priekuļi Municipality|Rauna Municipality|Rēzekne Municipality|Rēzekne|Riebiņi Municipality|Riga|Roja Municipality|Ropaži Municipality|Rucava Municipality|Rugāji Municipality|Rundāle Municipality|Rūjiena Municipality|Salacgrīva Municipality|Sala Municipality|Salaspils Municipality|Saldus Municipality|Saulkrasti Municipality|Sēja Municipality|Sigulda Municipality|Skrīveri Municipality|Skrunda Municipality|Smiltene Municipality|Stopiņi Municipality|Strenči Municipality|Talsi Municipality|Tērvete Municipality|Tukums Municipality|Vaiņode Municipality|Valka Municipality|Valmiera|Varakļāni Municipality|Vārkava Municipality|Vecpiebalga Municipality|Vecumnieki Municipality|Ventspils Municipality|Ventspils|Viesīte Municipality|Viļaka Municipality|Viļāni Municipality|Zilupe Municipality";
s_a[118]="Akkar Governate|Baalbek-Hermel Governate|Beirut Governate|Beqaa Governate|Mount Lebanon Governate|Nabatieh Governate|North Governate|South Governate";
s_a[119]="Berea|Butha-Buthe|Leribe|Mafeteng|Maseru|Mohale's Hoek|Mokhotlong|Qacha's Nek|Quthing|Thaba-Tseka";
s_a[120]="Bomi|Bong|Gbarpolu|Grand Bassa|Grand Cape Mount|Grand Gedeh|Grand Kru|Lofa|Margibi|Maryland|Montserrado|Nimba|Rivercess|River Gee|Sinoe";
s_a[121]="Benghazi|Butnan|Derna|Ghat|Jebel el-Akhdar|Jabal al Gharbi|Jafara|Jufra|Kufra|Marj|Misrata|Murqub|Murzuq|Nalut|Nuqat al Khams|Sebha|Sirte|Tripoli|Wadi al Hayaa|Wadi al Shatii|Al Wahat|Zawiya";
s_a[122]="Balzers|Eschen|Gamprin|Mauren|Planken|Ruggell|Schaan|Schellenberg|Triesen|Triesenberg|Vaduz";
s_a[123]="Alytus|Kaunas|Klaipėda|Marijampolė|Panevėžys|Šiauliai|Tauragė|Telšiai|Utena|Vilnius";
s_a[124]="Canton of Capellen|Canton of Clervaux|Canton of Diekirch|Canton of Echternach|Canton of Esch-sur-Alzette|Canton of Grevenmacher|Canton of Luxembourg|Canton of Mersch|Canton of Redange|Canton of Remich|Canton of Vianden|Canton of Wiltz";
s_a[125]="Macau";
s_a[126]="Berovo|Češinovo-Obleševo|Delčevo|Karbinci|Kočani|Makedonska Kamenica|Pehčevo|Probištip|Štip|Vinica|Zrnovci|Kratovo|Kriva Palanka|Kumanovo|Lipkovo|Rankovce|Staro Nagoričane|Bitola|Demir Hisar|Dolneni|Krivogaštani|Kruševo|Mogila|Novaci|Prilep|Resen|Bogovinje|Brvenica|Gostivar|Jegunovce|Mavrovo and Rostuša|Tearce|Tetovo|Vrapčište|Želino|Aračinovo|Čučer-Sandevo|Ilinden|Petrovec|Sopište|Studeničani|Zelenikovo|Bogdanci|Bosilovo|Dojran|Gevgelija|Konče|Novo Selo|Radoviš|Strumica|Valandovo|Vasilevo|Centar Župa|Debar|Debarca|Kičevo|Makedonski Brod|Ohrid|Plasnica|Struga|Vevčani|Čaška|Demir Kapija|Gradsko|Kavadarci|Lozovo|Negotino|Rosoman|Sveti Nikole|Veles|Aerodrom|Butel|Čair|Centar|Gazi Baba|Gjorče Petrov|Karpoš|Kisela Voda|Saraj|Šuto Orizari";
s_a[127]="Antananarivo|Antsiranana|Fianarantsoa|Mahajanga|Toamasina|Toliara";
s_a[128]="Central Region|Northern Region|Southern Region";
s_a[129]="Johor|Kedah|Kelantan|Kuala Lumpur|Labuan|Malacca|Negeri Sembilan|Pahang|Penang|Perak|Perlis|Putrajaya|Sabah|Sarawak|Selangor|Terengganu";
s_a[130]="Addu|Alif Alif|Alif Dhaal|Baa|Dhaalu|Faafu|Gaafu Alif|Gaafu Dhaalu|Gnaviyani|Haa Alif|Haa Dhaalu|Kaafu|Laamu|Lhaviyani|Malé|Meemu|Noonu|Raa|Shaviyani|Thaa|Vaavu";
s_a[131]="Bamako|Gao|Kayes|Kidal|Koulikoro|Ménaka|Mopti|Ségou|Sikasso|Taoudénit|Tombouctou";
s_a[132]="Central Region|Gozo Region|Northern Region|South Eastern Region|Southern Region";
s_a[133]="Isle of Man";
s_a[134]="Ailinglaplap|Ailuk|Arno|Aur|Ebon|Enewetok|Erikub|Jabat|Jaluit|Jemo|Kili|Kwajalein|Lae|Lib|Likiep|Majuro|Maloelap|Mejit|Mili|Namorik|Namu|Rongelap|Ujae|Utirik|Wotho|Wotje";
s_a[135]="Martinique";
s_a[136]="Adrar|Assaba|Brakna|Dakhlet Nouadhibou|Gorgol|Guidimaka|Hodh Ech Chargui|Hodh El Gharbi|Inchiri|Nouakchott-Nord|Nouakchott-Ouest|Nouakchott-Sud|Tagant|Tiris Zemmour|Trarza";
s_a[137]="Flacq|Grand Port|Moka|Pamplemousses|Plaines Wilhems|Port Louis|Rivière du Rempart|Rivière Noire|Savanne";
s_a[138]="Mayotte";
s_a[139]="Aguascalientes|Baja California|Baja California Sur|Campeche|Chiapas|Chihuahua|Coahuila|Colima|Durango|Guanajuato|Guerrero|Hidalgo|Jalisco|Mexico|Mexico city|Michoacán|Morelos|Nayarit|Nuevo León|Oaxaca|Puebla|Querétaro|Quintana Roo|San Luis Potosí|Sinaloa|Sonora|Tabasco|Tamaulipas|Tlaxcala|Veracruz|Yucatán|Zacatecas";
s_a[140]="Chuuk|Kosrae|Pohnpei|Yap";
s_a[141]="Anenii Noi|Basarabeasca|Bender|Briceni|Cahul|Cantemir|Călărași|Camenca|Căușeni|Ceadîr-Lunga|Cimișlia|Comrat|Criuleni|Dondușeni|Drochia|Dubăsari|Edineț|Fălești|Florești|Glodeni|Grigoriopol|Hîncești|Ialoveni|Leova|Nisporeni|Ocnița|Orhei|Rezina|Rîșcani|Rîbnița|Sîngerei|Slobozia|Soroca|Strășeni|Șoldănești|Ștefan Vodă|Taraclia|Telenești|Tiraspol|Ungheni|Vulcăneșt";
s_a[142]="Monte Carlo|Saint Roman|Larvotto|La Condamine|Monaco-Ville|Fontvieille|La Colle|Les Révoires|Moneghetti|Saint Michel";
s_a[143]="Arkhangai|Bayankhongor|Bayan-Ölgii|Bulgan|Darkhan-Uul|Dornod|Dornogovi|Dundgovi|Govi-Altai|Govisümber|Khentii|Khovd|Khövsgöl|Ömnögovi|Orkhon|Övörkhangai|Selenge|Sükhbaatar|Töv|Ulaanbaatar|Uvs|Zavkhan";
s_a[144]  ="Andrijevica Municipality|Bar Municipality|Berane Municipality|Bijelo Polje Municipality|Budva Municipality|Cetinje Municipality|Danilovgrad Municipality|Gusinje Municipality|Herceg Novi Municipality|Kolašin Municipality|Kotor Municipality|Mojkovac Municipality|Nikšić Municipality|Petnjica Municipality|Plav Municipality|Pljevlja Municipality|Plužine Municipality|Podgorica|Rožaje Municipality|Šavnik Municipality|Tivat Municipality|Tuzi Municipality|Ulcinj Municipality|Žabljak Municipality";
s_a[145]="Montserrat";
s_a[146]="Béni Mellal-Khénifra|Casablanca-Settat|Dakhla-Oued Ed-Dahab|Drâa-Tafilalet|Fès-Meknès|Guelmim-Oued Noun|Laâyoune-Sakia El Hamra|Marrakech-Safi|Oriental|Rabat-Salé-Kénitra|Souss-Massa|Tanger-Tetouan-Al Hoceima";
s_a[147]="Cabo Delgado Province|Gaza Province|Inhambane Province|Manica Province|Maputo|Maputo Province|Nampula Province|Niassa Province|Sofala Province|Tete Province|Zambezia Province";
s_a[148]="Erongo Region|Hardap Region|Kavango East Region|Kavango West Region|Khomas Region|Kunene Region|Ohangwena Region|Omaheke Region|Omusati Region|Oshana Region|Oshikoto Region|Otjozondjupa Region|Zambezi Region|Karas Region";
s_a[149]="Aiwo|Anabar|Anetan|Anibare|Baiti|Boe|Buada|Denigomodu|Ewa|Ijuw|Meneng|Nibok|Uaboe|Yaren";
s_a[150]="Province No. 1|Province No. 2|Province No. 5|Bagmati|Gandaki|Karnali|Sudurpashchim";
s_a[151]="Drenthe|Flevoland|Friesland|Gelderland|Groningen|Limburg|North Brabant|North Holland|Overijssel|South Holland|Utrecht|Zeeland";
s_a[152]="New Caledonia";
s_a[153]="Auckland|Bay of Plenty|Canterbury|Gisborne|Hawke's Bay|Manawatū-Whanganui|Marlborough|Nelson|Northland|Otago|Southland|Taranaki|Tasman|Waikato|Wellington|West Coast";
s_a[154]="Boaco|Carazo|Chinandega|Chontales|Esteli|Granada|Jinotega|León|Madriz|Managua|Masaya|Matagalpa|North Caribbean Coast Autonomous Region|Nueva Segovia|Río San Juan|Rivas|South Caribbean Coast Autonomous Region";
s_a[155]="Agadez|Diffa|Dosso|Maradi|Niamey|Tahoua|Tillabéri|Zinder";
s_a[156]="Abia|Adamawa|Akwa Ibom|Anambra|Bauchi|Bayelsa|Benue|Borno|Cross River|Delta|Ebonyi|Edo|Ekiti|Enugu|Federal Capital Territory|Gombe|Imo|Jigawa|Kaduna|Kano|Katsina|Kebbi|Kogi|Kwara|Lagos|Nassarawa|Niger|Ogun|Ondo|Osun|Oyo|Plateau|Rivers|Sokoto|Taraba|Yobe|Zamfara";
s_a[157]="Niue";
s_a[158]="Norfolk Island";
s_a[159]="Northern Mariana Islands";
s_a[160]="Agder|Innlandet|Møre og Romsdal|Nordland|Oslo|Rogaland|Troms og Finnmark|Trøndelag|Vestfold og Telemark|Vestland|Viken";
s_a[161]="Ad Dakhiliyah|Ad Dhahirah|Al Batinah North|Al Batinah South|Al Buraymi|Al Wusta|Ash Sharqiyah North|Ash Sharqiyah South|Dhofar|Muscat|Musandam";
s_a[162]="Azad Kashmir|Balochistan|Gilgit-Baltistan|Islamabad Capital Territory|Khyber Pakhtunkhwa|Punjab|Sindh";
s_a[163]="Aimeliik|Airai|Angaur|Hatobohei|Kayangel|Koror|Melekeok|Ngaraard|Ngarchelong|Ngardmau|Ngatpang|Ngchesar|Ngeremlengui|Ngiwal|Peleliu|Sonsoral";
s_a[164]="Bocas del Toro|Chiriquí|Coclé|Colón|Darién|Emberá-Wounaan Comarca|Guna Yala|Herrera|Los Santos|Ngäbe-Buglé Comarca|Panamá|Panamá Oeste|Veraguas";
s_a[165]="Autonomous Region of Bougainville|Central|Chimbu|East New Britain|East Sepik|Eastern Highlands|Enga|Oro|Gulf|Hela|Jiwaka|Madang|Manus|Milne Bay|Morobe|National Capital|New Ireland|Sandaun|Southern Highlands|West New Britain|Western|Western Highlands";
s_a[166]="Alto Paraguay|Alto Paraná|Amambay|Capital District|Boquerón|Caaguazú|Caazapá|Canindeyú|Central|Concepción|Cordillera|Guairá|Itapúa|Misiones|Ñeembucú|Paraguarí|Presidente Hayes|San Pedro";
s_a[167]="Amazonas|Áncash|Apurímac|Arequipa|Ayacucho|Cajamarca|Callao|Cusco|Huancavelica|Huánuco|Ica|Junín|La Libertad|Lambayeque|Lima|Loreto|Madre de Dios|Moquegua|Pasco|Piura|Puno|San Martín|Tacna|Tumbes|Ucayali";
s_a[168]="Bangsamoro|Bicol|Cagayan Valley|Calabarzon|Caraga|Central Luzon|Central Visayas|Cordillera Administrative Region|Davao|Eastern Visayas|Ilocos|Manila|Mimaropa|Northern Mindanao|Soccsksargen|Western Visayas|Zamboanga Peninsula";
s_a[169]="Bethlehem Governate|Deir Al-Balah Governate|Gaza Governate|Hebron Governate|Jenin Governate|Jericho & Al Aghwar Governate|Jerusalem Governate|Khan Yunis Governate|Nablus Governate|North Gaza Governate|Qalqiliya Governate|Rafah Governate|Ramallah & Al-Bireh Governate|Salfit Governate|Tubas Governate|Tulkarm Governate";
s_a[170]="Greater Poland|Kuyavian-Pomeranian|Lesser Poland|Łódź|Lower Silesian|Lublin|Lubusz|Masovian|Opole|Podkarpackie|Podlaskie|Pomeranian|Silesian|Świętokrzyskie|Warmian-Masurian|West Pomeranian";
s_a[171]="Aveiro|Azores|Beja|Braga|Bragança|Castelo Branco|Coimbra|Évora|Faro|Guarda|Leiria|Lisbon|Madeira|Portalegre|Porto|Santarém|Setúbal|Viana do Castelo|Vila Real|Viseu";
s_a[172]="Puerto Rico";
s_a[173]="Al Khor|Al-Shahaniya|Ad Dawhah|Al Daayen|Al Rayyan|Al Wakrah|Madinat ash Shamal|Umm Salal";
s_a[174]="Réunion";
s_a[175]="Alba|Arad|Argeș|Bacău|Bihor|Bistrița-Năsăud|Botoșani|Brașov|Brăila|Bucharest|Buzău|Caraș-Severin|Călărași|Cluj|Constanța|Covasna|Dâmbovița|Dolj|Galați|Giurgiu|Gorj|Harghita|Hunedoara|Ialomița|Iași|Ilfov|Maramureș|Mehedinți|Mureș|Neamț|Olt|Prahova|Satu Mare|Sălaj|Sibiu|Suceava|Teleorman|Timiș|Tulcea|Vaslui|Vâlcea|Vrancea";
s_a[176]="Central Federal District|Far Eastern Federal District|North Caucasian Federal District|Northwestern Federal District|Siberian Federal District|Southern District|Ural Federal District|Volga Federal District";
s_a[177]="Eastern Province|Kigali Province|Northern Province|Southern Province|Western Province";
s_a[178]="Saint Helena";
s_a[179]="Saint Kitts|Nevis";
s_a[180]="Anse la Raye|Castries|Choiseul|Dauphin|Dennery|Gros Islet|Laborie|Micoud|Praslin|Soufrière|Vieux Fort";
s_a[181]="Miquelon|Saint Pierre";
s_a[182]="Charlotte|Grenadines|Saint Andrew|Saint David|Saint George|Saint Patrick";
s_a[183]="A'ana|Aiga-i-le-Tai|Atua|Fa'asaleleaga|Gaga'emauga|Gagaifomauga|Palauli|Satupa'itea|Tuamasaga|Va'a-o-Fonoti|Vaisigano";
s_a[184]="Acquaviva|Borgo Maggiore|Chiesanuova|Domagnano|Faetano|Fiorentino|Montegiardino|San Marino|Serravalle";
s_a[185]="Principe|Sao Tome";
s_a[186]="Al Bahah|Northern Borders|Al Jawf|Medina|Al Qasim|Riyadh|Eastern Province|'Asir|Ha'il|Jizan|Mecca|Najran|Tabuk";
s_a[187]="Dakar|Diourbel|Fatick|Kaffrine|Kaolack|Kédougou|Kolda|Louga|Matam|Saint-Louis|Sédhiou|Tambacounda|Thiès|Ziguinchor";
s_a[188]="Belgrade|Bor|Braničevo|Central Banat|Jablanica|Kolubara|Kosovo|Kosovo-Pomoravlje|Kosovska Mitrovica|Mačva|Moravica|Nišava|North Bačka|North Banat|Pčinja|Peć|Prizren|Pirot|Podunavlje|Pomoravlje|Raška|Rasina|South Bačka|South Banat|Šumadija|Srem|Toplica|West Bačka|Zaječar|Zlatibor";
s_a[189]="Mahe|Praslin|La Digue";
s_a[190]="Eastern Province|Northern Province|North West Province|Southern Province|Western Area";
s_a[191]="Central Singapore Community Development Council|North East Community Development Council|North West Community Development Council|South East Community Development Council|South West Community Development Council";
s_a[192]= "Sint Marteen";
s_a[193]="Banská Bystrica|Bratislava|Košice|Nitra|Prešov|Trenčín|Trnava|Žilina";
s_a[194]="Ajdovščina|Ankaran|Apače|Beltinci|Benedikt|Bistrica ob Sotli|Bled|Bloke|Bohinj|Borovnica|Bovec|Braslovče|Brda|Brežice|Brezovica|Cankova|Celje|Cerklje na Gorenjskem|Cerknica|Cerkno|Cerkvenjak|Cirkulane|Črenšovci|Črna na Koroškem|Črnomelj|Destrnik|Divača|Dobje|Dobrepolje|Dobrna|Dobrova–Polhov Gradec|Dobrovnik|Dol pri Ljubljani|Dolenjske Toplice|Domžale|Dornava|Dravograd|Duplek|Gorenja Vas–Poljane|Gorišnica|Gorje|Gornja Radgona|Gornji Grad|Gornji Petrovci|Grad|Grosuplje|Hajdina|Hoče–Slivnica|Hodoš|Horjul|Hrastnik|Hrpelje-Kozina|Idrija|Ig|Ilirska Bistrica|Ivančna Gorica|Izola|Jesenice|Jezersko|Juršinci|Kamnik|Kanal ob Soči|Kidričevo|Kobarid|Kobilje|Kočevje|Komen|Komenda|Koper|Kostanjevica na Krki|Kostel|Kozje|Kranj|Kranjska Gora|Križevci|Krško|Kungota|Kuzma|Laško|Lenart|Lendava|Litija|Ljubno|Ljutomer|Log-Dragomer|Logatec|Loška Dolina|Loški Potok|Lovrenc na Pohorju|Ljubljana|Luče|Lukovica|Majšperk|Makole|Maribor|Markovci|Medvode|Mengeš|Metlika|Mežica|Miklavž na Dravskem Polju|Miren-Kostanjevica|Mirna|Mirna Peč|Mislinja|Mokronog-Trebelno|Moravče|Moravske Toplice|Mozirje|Murska Sobota|Muta|Naklo|Nazarje|Novo Mesto|Nova Gorica|Odranci|Oplotnica|Ormož|Osilnica|Pesnica|Piran|Pivka|Podčetrtek|Podlehnik|Podvelka|Poljčane|Polzela|Postojna|Prebold|Preddvor|Prevalje|Ptuj|Puconci|Rače–Fram|Radeče|Radenci|Radlje ob Dravi|Radovljica|Ravne na Koroškem|Razkrižje|Rečica ob Savinji|Renče–Vogrsko|Ribnica|Ribnica na Pohorju|Rogaška Slatina|Rogašovci|Rogatec|Ruše|Šalovci|Selnica ob Dravi|Semič|Šempeter-Vrtojba|Šenčur|Šentilj|Šentjernej|Šentjur|Šentrupert|Sevnica|Sežana|Škocjan|Škofja Loka|Škofljica|Slovenj Gradec|Slovenska Bistrica|Slovenske Konjice|Šmarje pri Jelšah|Šmarješke Toplice|Šmartno pri Litiji|Šmartno ob Paki|Sodražica|Solčava|Šoštanj|Središče ob Dravi|Starše|Štore|Straža|Sveta Ana|Sveta Trojica v Slovenskih Goricah|Sveti Andraž v Slovenskih Goricah|Sveti Jurij ob Ščavnici|Sveti Jurij v Slovenskih Goricah|Sveti Tomaž|Tabor|Tišina|Tolmin|Trbovlje|Trebnje|Trnovska Vas|Tržič|Trzin|Turnišče|Velenje|Velika Polana|Velike Lašče|Veržej|Videm|Vipava|Vitanje|Vodice|Vojnik|Vransko|Vrhnika|Vuzenica|Zagorje ob Savi|Žalec|Zavrč|Železniki|Žetale|Žiri|Žirovnica|Zreče|Žužemberk";
s_a[195]="Central|Choiseul|Guadalcanal|Honiara|Isabel|Makira-Ulawa|Malaita|Rennell and Bellona|Temotu|Western";
s_a[196]="Awdal|Bakool|Banaadir|Bari|Bay|Galguduud|Gedo|Hiran|Middle Juba|Lower Juba|Mudug|Nugal|Sanaag|Middle Shebelle|Lower Shebelle|Sool|Togdheer|Woqooyi Galbeed";
s_a[197]="Eastern Cape|Free State|Gauteng|Kwa|Zulu-Natal|Limpopo|Mpumalanga|North West|Northern Cape|Western Cape";
s_a[198]  ="Abyei|Central Equatoria|Eastern Equatoria|Jonglei|Lakes|Northern Bahr el Ghazal|Pibor|Ruweng|Unity|Upper Nile|Warrap|Western Bahr el Ghazal|Western Equatoria";
s_a[199]="Andalusia|Aragon|Asturias|Balearic Islands|Basque Country|Canary Islands|Cantabria|Castilla–La Mancha|Castile and León|Catalonia|Ceuta|Extremadura|Galicia|La Rioja|Madrid|Melilla|Murcia|Navarre|Valencia";
s_a[200]="Central Province|Eastern Province|North Central Province|North Eastern Province|North Western Province|Northern Province|Sabaragamuwa Province|Southern Province|Uva Province|Western Province";
s_a[201]="Blue Nile|Central Darfur|East Darfur|Gezira|Kassala|Khartoum|North Darfur|North Kordofan|Northern|Al Qadarif|Red Sea|River Nile|Sennar|South Darfur|South Kordofan|West Darfur|West Kordofan|White Nile";
s_a[202]="Brokopondo District|Commewijne District|Coronie District|Marowijne District|Nickerie District|Para District|Paramaribo District|Saramacca District|Sipaliwini District|Wanica District";
s_a[203]="Barentsoya|Bjornoya|Edgeoya|Hopen|Kvitoya|Nordaustandet|Prins Karls Forland|Spitsbergen";
s_a[204]="Hhohho|Lubombo|Manzini|Shiselweni";
s_a[205]="Blekinge|Dalarna|Gävleborg|Gotland|Halland|Jämtland|Jönköping|Kalmar|Kronoberg|Norrbotten|Örebro|Östergötland|Scania|Södermanland|Stockholm|Uppsala|Värmland|Västerbotten|Västernorrland|Västmanland|Västra Götaland";
s_a[206]="Canton of Aargau|Appenzell Ausserrhoden|Appenzell Innerrhoden|Basel-Landschaft|Basel-Stadt|Bern|Fribourg|Geneva|Glarus|Graubünden|Jura|Luzern|Neuchâtel|Nidwalden|Obwalden|Schaffhausen|Schwyz|Solothurn|St. Gallen|Thurgau|Ticino|Uri|Valais|Vaud|Zug|Zürich";
s_a[207]="Aleppo|Damascus|Daraa|Deir ez-Zor|Hama|Al-Hasakah|Homs|Idlib|Latakia|Quneitra|Raqqa|Rif Dimashq|As-Suwayda|Tartus";
s_a[208]="Fujian|Kaohsiung|New Taipei|Taipei|Taoyuan|Taichung|Tainan|Taiwan";
s_a[209]="Districts of Republican Subordination|Dushanbe|Gorno-Badakhshan Autonomous Region|Khatlon Region|Sughd Region";
s_a[210]="Arusha Region|Dar es Salaam Region|Dodoma Region|Gieta Region|Iringa Region|Kagera Region|Katavi Region|Kigoma Region|Kilimanjaro Region|Lindi Region|Manyara Region|Mara Region|Mjina Magharibi Region|Mbeya Region|Morogoro Region|Mtwara Region|Mwanza Region|Njombe Region|Pemba North Region|Pemba South Region|Pwani Region|Rukwa Region|Ruvuma Region|Shinyanga Region|Simiyu Region|Singida Region|Songwe Region|Tabora Region|Tanga Region|Unguja North Region|Unguja South Region";
s_a[211]="Amnat Charoen|Ang Thong|Bangkok|Bueng Kan|Buriram|Chachoengsao|Chai Nat|Chaiyaphum|Chanthaburi|Chiang Mai|Chiang Rai|Chonburi|Chumphon|Kalasin|Kamphaeng Phet|Kanchanaburi|Khon Kaen|Krabi|Lampang|Lamphun|Loei|Lopburi|Mae Hong Son|Maha Sarakham|Mukdahan|Nakhon Nayok|Nakhon Pathom|Nakhon Phanom|Nakhon Ratchasima|Nakhon Sawan|Nakhon Si Thammarat|Nan|Narathiwat|Nong Bua Lamphu|Nong Khai|Nonthaburi|Pathum Thani|Pattani|Phang Nga|Phatthalung|Phayao|Phetchabun|Phetchaburi|Phichit|Phitsanulok|Phra Nakhon Si Ayutthaya|Phrae|Phuket|Prachinburi|Prachuap Khiri Khan|Ranong|Ratchaburi|Rayong|Roi Et|Sa Kaeo|Sakon Nakhon|Samut Prakan|Samut Sakhon|Samut Songkhram|Saraburi|Satun|Sing Buri|Sisaket|Songkhla|Sukhothai|Suphan Buri|Surat Thani|Surin|Tak|Trang|Trat|Ubon Ratchathani|Udon Thani|Uthai Thani|Uttaradit|Yala|Yasothon";
s_a[212]="Arima|Chaguanas|Couva–Tabaquite–Talparo|Diego Martin|Mayaro–Rio Claro|Penal–Debe|Point Fortin|Port of Spain|Princes Town|San Fernando|San Juan–Laventille|Sangre Grande|Siparia|Tunapuna–Piarco";
s_a[213]="Centrale Region|Kara Region|Maritime Region|Plateaux|Savanes";

s_a[214]="ʻEua|Haʻapai|Ongo Niua|Vavaʻu|Tongatapu";
s_a[215]="Ariana|Béja|Ben Arous|Bizerte|Gabès|Gafsa|Jendouba|Kairouan|Kasserine|Kebili|Kef|Mahdia|Manouba|Medenine|Monastir|Nabeul|Sfax|Sidi Bouzid|Siliana|Sousse|Tataouine|Tozeur|Tunis|Zaghouan";
s_a[216]="Adana|Adıyaman|Afyonkarahisar|Ağrı|Aksaray|Amasya|Ankara|Antalya|Ardahan|Artvin|Aydın|Balıkesir|Bartın|Batman|Bayburt|Bilecik|Bingöl|Bitlis|Bolu|Burdur|Bursa|Çanakkale|Çankırı|Çorum|Denizli|Diyarbakır|Düzce|Edirne|Elazığ|Erzincan|Erzurum|Eskişehir|Gaziantep|Giresun|Gümüşhane|Hakkâri|Hatay|Iğdır|Isparta|Istanbul|İzmir|Kahramanmaraş|Karabük|Karaman|Kars|Kastamonu|Kayseri|Kilis|Kırıkkale|Kırklareli|Kırşehir|Kocaeli|Konya|Kütahya|Malatya|Manisa|Mardin|Mersin|Muğla|Muş|Nevşehir|Niğde|Ordu|Osmaniye|Rize|Sakarya|Samsun|Siirt|Sinop|Sivas|Şanlıurfa|Şırnak|Tekirdağ|Tokat|Trabzon|Tunceli|Uşak|Van|Yalova|Yozgat|Zonguldak";
s_a[217]="Ashgabat|Ahal Region|Balkan Region|Daşoguz Region|Lebap Region|Mary Region";
s_a[218]="Tuvalu";
s_a[219]="Central Region|Eastern Region|Western Region|Northern Region";
s_a[220]="Autonomous Republic of Crimea|Cherkasy Oblast|Chernihiv Oblast|Chernivtsi Oblast|Dnipropetrovsk Oblast|Donetsk Oblast|Ivano-Frankivsk|Kiev|Kharkiv Oblast|Kherson Oblast|Khmelnytskyi Oblast|Kiev Oblast|Kirovohrad Oblast|Luhansk Oblast|Lviv Oblast|Mykolaiv Oblast|Odessa Oblast|Poltava Oblast|Rivne Oblast|Sevastopol|Sumy Oblast|Ternopil Oblast|Vinnytsia Oblast|Volyn Oblast|Zakarpattia Oblast|Zaporizhia Oblast|Zhytomyr Oblast";
s_a[221]="Abu Dhabi|Ajman|Dubai|Fujairah|Ras Al Khaimah|Sharjah|Umm al Quwain";
s_a[222]="England|Northern Ireland|Scotland|Wales"
s_a[223]="Artigas|Canelones|Cerro Largo|Colonia|Durazno|Flores|Florida|Lavalleja|Maldonado|Montevideo|Paysandu|Río Negro|Rivera|Rocha|Salto|San José|Soriano|Tacuarembó|Treinta y Tres";
s_a[224]="Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|District of Columbia|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming";
s_a[225]="Andijon Region|Bukhara Region|Fergana Region|Jizzakh Region|Xorazm Region|Namangan Region|Navoiy Region|Qashqadaryo Region|Samarqand Region|Sirdaryo Region|Surxondaryo Region|Karakalpakstan|Tashkent Region|Tashkent";
s_a[226]="Malampa|Penama|Sanma|Shefa|Tafea|Torba";
s_a[227]="Amazonas|Anzoátegui|Apure|Aragua|Barinas|Bolívar|Capital District|Carabobo|Cojedes|Delta Amacuro|Falcón|Federal Dependencies|Guárico|Lara|Mérida|Miranda|Monagas|Nueva Esparta|Portuguesa|Sucre|Táchira|Trujillo|Vargas|Yaracuy|Zulia";
s_a[228]="An Giang|Bắc Giang|Bắc Kạn|Bạc Liêu|Bắc Ninh|Bà Rịa-Vũng Tàu|Bến Tre|Bình Định|Bình Dương|Bình Phước|Bình Thuận|Cà Mau|Cao Bằng|Cần Thơ|Đà Nẵng|Đắk Lắk|Đắk Nông|Điện Biên|Đồng Nai|Đồng Tháp|Gia Lai|Hà Giang|Hà Nam|Hà Nội|Hà Tĩnh|Hải Dương|Hải Phòng|Hòa Bình|Hồ Chí Minh City|Hậu Giang|Hưng Yên|Khánh Hòa|Kiên Giang|Kon Tum|Lai Châu|Lâm Đồng|Lạng Sơn|Lào Cai|Long An|Nam Định|Nghệ An|Ninh Bình|Ninh Thuận|Phú Thọ|Phú Yên|Quảng Bình|Quảng Nam|Quảng Ngãi|Quảng Ninh|Quảng Trị|Sóc Trăng|Sơn La|Tây Ninh|Thái Bình|Thái Nguyên|Thanh Hóa|Thừa Thiên-Huế|Tiền|Giang|Trà Vinh|Tuyên Quang |Vĩnh Long|Vĩnh Phúc|Yên Bái";
s_a[229]="United States Virgin Islands";
s_a[230]="Futuna|Wallis";
s_a[231]="'Abyan|Aden|Al Mahrah|Hadramaut|Lahij|Shabwah|Dhale'Amran|Al Bayda|Al Hudaydah|Al Jawf|Al Mahwit|Amanat Al Asimah|Dhamar|Hajjah|Ibb|Ma'rib|Raymah|Saada|Sana'a|Taiz|Socotra";
s_a[232]="Central|Copperbelt|Eastern|Luapula|Muchinga|Lusaka|North-Western|Northern|Southern|Western";
s_a[233]="Bulawayo|Harare|Manicaland|Mashonaland Central|Mashonaland East|Mashonaland West|Masvingo|Matabeleland North|Matabeleland South|Midlands";

function populateStates( countryElementId, stateElementId ){
	
	var selectedCountryIndex = document.getElementById( countryElementId ).selectedIndex;

	var stateElement = document.getElementById( stateElementId );
	
	stateElement.length=0;	// Fixed by Julian Woods
	stateElement.options[0] = new Option('Select State','');
	stateElement.selectedIndex = 0;
	
	var state_arr = s_a[selectedCountryIndex].split("|");
	
	for (var i=0; i<state_arr.length; i++) {
		stateElement.options[stateElement.length] = new Option(state_arr[i],state_arr[i]);
	}
}

function populateCountries(countryElementId, stateElementId){
	// given the id of the <select> tag as function argument, it inserts <option> tags
	var countryElement = document.getElementById(countryElementId);
	countryElement.length=0;
	countryElement.options[0] = new Option('Select Country','-1');
	countryElement.selectedIndex = 0;
	for (var i=0; i<country_arr.length; i++) {
		countryElement.options[countryElement.length] = new Option(strip(country_arr[i]),country_arr[i]);
	}

	// Assigned all countries. Now assign event listener for the states.

	if( stateElementId ){
		countryElement.onchange = function(){
			populateStates( countryElementId, stateElementId );
		};
	}
}
function strip(string) { 
              return string.replace(/\(.{2}\)/,''); 
        } 