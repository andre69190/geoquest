import json, os, re

# ── CITIES ──────────────────────────────────────────────────────────────────
cities_raw = json.load(open('/tmp/geoquest_data/cities_clean.json'))
cities_slim = [{'id':c['id'],'n':c.get('name') or c.get('asciiName') or '',
                'c':c.get('country',''),'cc':(c.get('countryCode','') or '').lower(),
                'cont':c.get('continent',''),'sub':c.get('subregion') or c.get('continent',''),
                'pop':c.get('population',0)}
               for c in cities_raw]
CJ = json.dumps(cities_slim, separators=(',',':'), ensure_ascii=False)

# ── STATIC DATA ──────────────────────────────────────────────────────────────
CAPITALS = [
  {"country":"France","capital":"Paris","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"country":"Germany","capital":"Berlin","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"country":"Italy","capital":"Rome","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Spain","capital":"Madrid","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"country":"United Kingdom","capital":"London","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Portugal","capital":"Lisbon","cc":"pt","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Netherlands","capital":"Amsterdam","cc":"nl","continent":"Europe","subregion":"Western Europe"},
  {"country":"Belgium","capital":"Brussels","cc":"be","continent":"Europe","subregion":"Western Europe"},
  {"country":"Switzerland","capital":"Bern","cc":"ch","continent":"Europe","subregion":"Western Europe"},
  {"country":"Austria","capital":"Vienna","cc":"at","continent":"Europe","subregion":"Western Europe"},
  {"country":"Sweden","capital":"Stockholm","cc":"se","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Norway","capital":"Oslo","cc":"no","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Denmark","capital":"Copenhagen","cc":"dk","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Finland","capital":"Helsinki","cc":"fi","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Poland","capital":"Warsaw","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Czech Republic","capital":"Prague","cc":"cz","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Hungary","capital":"Budapest","cc":"hu","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Romania","capital":"Bucharest","cc":"ro","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Greece","capital":"Athens","cc":"gr","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Ukraine","capital":"Kyiv","cc":"ua","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Russia","capital":"Moscow","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Turkey","capital":"Ankara","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"country":"Serbia","capital":"Belgrade","cc":"rs","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Croatia","capital":"Zagreb","cc":"hr","continent":"Europe","subregion":"Southern Europe"},
  {"country":"Ireland","capital":"Dublin","cc":"ie","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Bulgaria","capital":"Sofia","cc":"bg","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Slovakia","capital":"Bratislava","cc":"sk","continent":"Europe","subregion":"Eastern Europe"},
  {"country":"Iceland","capital":"Reykjavik","cc":"is","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Estonia","capital":"Tallinn","cc":"ee","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Latvia","capital":"Riga","cc":"lv","continent":"Europe","subregion":"Northern Europe"},
  {"country":"Lithuania","capital":"Vilnius","cc":"lt","continent":"Europe","subregion":"Northern Europe"},
  {"country":"China","capital":"Beijing","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"Japan","capital":"Tokyo","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"South Korea","capital":"Seoul","cc":"kr","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"India","capital":"New Delhi","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Pakistan","capital":"Islamabad","cc":"pk","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Bangladesh","capital":"Dhaka","cc":"bd","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Thailand","capital":"Bangkok","cc":"th","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Vietnam","capital":"Hanoi","cc":"vn","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Indonesia","capital":"Jakarta","cc":"id","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Malaysia","capital":"Kuala Lumpur","cc":"my","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Philippines","capital":"Manila","cc":"ph","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Singapore","capital":"Singapore City","cc":"sg","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Saudi Arabia","capital":"Riyadh","cc":"sa","continent":"Asia","subregion":"Western Asia"},
  {"country":"Iran","capital":"Tehran","cc":"ir","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Iraq","capital":"Baghdad","cc":"iq","continent":"Asia","subregion":"Western Asia"},
  {"country":"Israel","capital":"Jerusalem","cc":"il","continent":"Asia","subregion":"Western Asia"},
  {"country":"Jordan","capital":"Amman","cc":"jo","continent":"Asia","subregion":"Western Asia"},
  {"country":"UAE","capital":"Abu Dhabi","cc":"ae","continent":"Asia","subregion":"Western Asia"},
  {"country":"Kazakhstan","capital":"Astana","cc":"kz","continent":"Asia","subregion":"Central Asia"},
  {"country":"Afghanistan","capital":"Kabul","cc":"af","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Myanmar","capital":"Naypyidaw","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Cambodia","capital":"Phnom Penh","cc":"kh","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Taiwan","capital":"Taipei","cc":"tw","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"Mongolia","capital":"Ulaanbaatar","cc":"mn","continent":"Asia","subregion":"Eastern Asia"},
  {"country":"Sri Lanka","capital":"Colombo","cc":"lk","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Nepal","capital":"Kathmandu","cc":"np","continent":"Asia","subregion":"Southern Asia"},
  {"country":"Laos","capital":"Vientiane","cc":"la","continent":"Asia","subregion":"Southeast Asia"},
  {"country":"Nigeria","capital":"Abuja","cc":"ng","continent":"Africa","subregion":"Western Africa"},
  {"country":"Ethiopia","capital":"Addis Ababa","cc":"et","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Egypt","capital":"Cairo","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"country":"DR Congo","capital":"Kinshasa","cc":"cd","continent":"Africa","subregion":"Middle Africa"},
  {"country":"South Africa","capital":"Pretoria","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"country":"Kenya","capital":"Nairobi","cc":"ke","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Tanzania","capital":"Dodoma","cc":"tz","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Ghana","capital":"Accra","cc":"gh","continent":"Africa","subregion":"Western Africa"},
  {"country":"Morocco","capital":"Rabat","cc":"ma","continent":"Africa","subregion":"Northern Africa"},
  {"country":"Algeria","capital":"Algiers","cc":"dz","continent":"Africa","subregion":"Northern Africa"},
  {"country":"Sudan","capital":"Khartoum","cc":"sd","continent":"Africa","subregion":"Northern Africa"},
  {"country":"Angola","capital":"Luanda","cc":"ao","continent":"Africa","subregion":"Middle Africa"},
  {"country":"Ivory Coast","capital":"Yamoussoukro","cc":"ci","continent":"Africa","subregion":"Western Africa"},
  {"country":"Senegal","capital":"Dakar","cc":"sn","continent":"Africa","subregion":"Western Africa"},
  {"country":"Uganda","capital":"Kampala","cc":"ug","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Zimbabwe","capital":"Harare","cc":"zw","continent":"Africa","subregion":"Eastern Africa"},
  {"country":"Tunisia","capital":"Tunis","cc":"tn","continent":"Africa","subregion":"Northern Africa"},
  {"country":"United States","capital":"Washington D.C.","cc":"us","continent":"North America","subregion":"Northern America"},
  {"country":"Canada","capital":"Ottawa","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"country":"Mexico","capital":"Mexico City","cc":"mx","continent":"North America","subregion":"Central America"},
  {"country":"Cuba","capital":"Havana","cc":"cu","continent":"North America","subregion":"Caribbean"},
  {"country":"Guatemala","capital":"Guatemala City","cc":"gt","continent":"North America","subregion":"Central America"},
  {"country":"Costa Rica","capital":"San Jose","cc":"cr","continent":"North America","subregion":"Central America"},
  {"country":"Brazil","capital":"Brasilia","cc":"br","continent":"South America","subregion":"South America"},
  {"country":"Argentina","capital":"Buenos Aires","cc":"ar","continent":"South America","subregion":"South America"},
  {"country":"Colombia","capital":"Bogota","cc":"co","continent":"South America","subregion":"South America"},
  {"country":"Peru","capital":"Lima","cc":"pe","continent":"South America","subregion":"South America"},
  {"country":"Chile","capital":"Santiago","cc":"cl","continent":"South America","subregion":"South America"},
  {"country":"Venezuela","capital":"Caracas","cc":"ve","continent":"South America","subregion":"South America"},
  {"country":"Ecuador","capital":"Quito","cc":"ec","continent":"South America","subregion":"South America"},
  {"country":"Uruguay","capital":"Montevideo","cc":"uy","continent":"South America","subregion":"South America"},
  {"country":"Bolivia","capital":"Sucre","cc":"bo","continent":"South America","subregion":"South America"},
  {"country":"Paraguay","capital":"Asuncion","cc":"py","continent":"South America","subregion":"South America"},
  {"country":"Australia","capital":"Canberra","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"country":"New Zealand","capital":"Wellington","cc":"nz","continent":"Oceania","subregion":"Australia and New Zealand"},
]
CAPJ = json.dumps(CAPITALS, separators=(',',':'), ensure_ascii=False)

RIVERS = [
  {"name":"Nil","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Amazonas","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Jangtsekiang","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Mississippi","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Kongo","country":"DR Congo","cc":"cd","continent":"Africa","subregion":"Middle Africa"},
  {"name":"Niger","country":"Nigeria","cc":"ng","continent":"Africa","subregion":"Western Africa"},
  {"name":"Wolga","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Mekong","country":"Vietnam","cc":"vn","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Ganges","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Indus","country":"Pakistan","cc":"pk","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Orinoko","country":"Venezuela","cc":"ve","continent":"South America","subregion":"South America"},
  {"name":"Sambesi","country":"Zambia","cc":"zm","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Rhein","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Donau","country":"Romania","cc":"ro","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Themse","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Seine","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Ebro","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Po","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Dnjepr","country":"Ukraine","cc":"ua","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Weichsel","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Elbe","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Murray","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Colorado","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Parana","country":"Argentina","cc":"ar","continent":"South America","subregion":"South America"},
  {"name":"Brahmaputra","country":"Bangladesh","cc":"bd","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Tigris","country":"Iraq","cc":"iq","continent":"Asia","subregion":"Western Asia"},
  {"name":"Euphrat","country":"Iraq","cc":"iq","continent":"Asia","subregion":"Western Asia"},
  {"name":"Irrawaddy","country":"Myanmar","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Huanghe","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Lena","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Ob","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Jenissei","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Amur","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Oranje","country":"South Africa","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Senegalfluss","country":"Senegal","cc":"sn","continent":"Africa","subregion":"Western Africa"},
  {"name":"Volta","country":"Ghana","cc":"gh","continent":"Africa","subregion":"Western Africa"},
  {"name":"Blauer Nil","country":"Ethiopia","cc":"et","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Loire","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Tejo","country":"Portugal","cc":"pt","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Guadalquivir","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Chao Phraya","country":"Thailand","cc":"th","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Missouri","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Sao Francisco","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Magdalena","country":"Colombia","cc":"co","continent":"South America","subregion":"South America"},
  {"name":"Irtysch","country":"Kazakhstan","cc":"kz","continent":"Asia","subregion":"Central Asia"},
  {"name":"Okawango","country":"Botswana","cc":"bw","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Limpopo","country":"South Africa","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Salween","country":"Myanmar","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Ural","country":"Russia","cc":"ru","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Illinois","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Yukon","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
]
RJ = json.dumps(RIVERS, separators=(',',':'), ensure_ascii=False)

LANDMARKS = [
  {"name":"Eiffelturm","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Kolosseum","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Big Ben","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Sagrada Familia","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Akropolis","country":"Greece","cc":"gr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Stonehenge","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Schiefer Turm von Pisa","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Brandenburger Tor","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Trevi-Brunnen","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Tower Bridge","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Alhambra","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Schloss Neuschwanstein","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Atomium","country":"Belgium","cc":"be","continent":"Europe","subregion":"Western Europe"},
  {"name":"Louvre","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Vatikan","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Hagia Sophia","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Blaue Moschee","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Kappadokien","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Freiheitsstatue","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Grand Canyon","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Golden Gate Bridge","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Mount Rushmore","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"CN Tower","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"name":"Chichen Itza","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Teotihuacan","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Christus der Erloser","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Machu Picchu","country":"Peru","cc":"pe","continent":"South America","subregion":"South America"},
  {"name":"Galapagos-Inseln","country":"Ecuador","cc":"ec","continent":"South America","subregion":"South America"},
  {"name":"Iguazu-Wasserfaelle","country":"Argentina","cc":"ar","continent":"South America","subregion":"South America"},
  {"name":"Osterinsel","country":"Chile","cc":"cl","continent":"South America","subregion":"South America"},
  {"name":"Grosse Mauer","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Verbotene Stadt","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Terrakotta-Armee","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Mount Fuji","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Fushimi Inari","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Angkor Wat","country":"Cambodia","cc":"kh","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Taj Mahal","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Rotes Fort","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Borobudur","country":"Indonesia","cc":"id","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Petronas Towers","country":"Malaysia","cc":"my","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Burj Khalifa","country":"UAE","cc":"ae","continent":"Asia","subregion":"Western Asia"},
  {"name":"Burj Al Arab","country":"UAE","cc":"ae","continent":"Asia","subregion":"Western Asia"},
  {"name":"Petra","country":"Jordan","cc":"jo","continent":"Asia","subregion":"Western Asia"},
  {"name":"Pyramiden von Gizeh","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Abu Simbel","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Kilimandscharo","country":"Tanzania","cc":"tz","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Victoriafaelle","country":"Zimbabwe","cc":"zw","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Tafelberg","country":"South Africa","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Grosse Barriereriff","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Oper von Sydney","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Uluru","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Milford Sound","country":"New Zealand","cc":"nz","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Niagara-Faelle","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"name":"Bagan-Tempel","country":"Myanmar","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
]
LMJ = json.dumps(LANDMARKS, separators=(',',':'), ensure_ascii=False)

NATIONAL_PARKS = [
  {"name":"Yellowstone","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Yosemite","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Everglades","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
  {"name":"Banff","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"name":"Jasper","country":"Canada","cc":"ca","continent":"North America","subregion":"Northern America"},
  {"name":"Kruger","country":"South Africa","cc":"za","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Serengeti-Nationalpark","country":"Tanzania","cc":"tz","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Masai Mara","country":"Kenya","cc":"ke","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Virunga","country":"DR Congo","cc":"cd","continent":"Africa","subregion":"Middle Africa"},
  {"name":"Bwindi Impenetrable Forest","country":"Uganda","cc":"ug","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Pantanal","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Torres del Paine","country":"Chile","cc":"cl","continent":"South America","subregion":"South America"},
  {"name":"Los Glaciares","country":"Argentina","cc":"ar","continent":"South America","subregion":"South America"},
  {"name":"Galapagos-Nationalpark","country":"Ecuador","cc":"ec","continent":"South America","subregion":"South America"},
  {"name":"Manu","country":"Peru","cc":"pe","continent":"South America","subregion":"South America"},
  {"name":"Kakadu","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Blue Mountains","country":"Australia","cc":"au","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Fiordland","country":"New Zealand","cc":"nz","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Tongariro","country":"New Zealand","cc":"nz","continent":"Oceania","subregion":"Australia and New Zealand"},
  {"name":"Jim Corbett","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Kaziranga","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Komodo","country":"Indonesia","cc":"id","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Zhangjiajie","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Jiuzhaigou","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Sagarmatha","country":"Nepal","cc":"np","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Sundarbans","country":"Bangladesh","cc":"bd","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Pyrenaaen-Nationalpark","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Bayerischer Wald","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Lake District","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Bialowieza-Wald","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Plitvicer Seen","country":"Croatia","cc":"hr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Teide","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Donana","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Gran Paradiso","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Sarek","country":"Sweden","cc":"se","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Thingvellir","country":"Iceland","cc":"is","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Rwenzori-Berge","country":"Uganda","cc":"ug","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Etosha","country":"Namibia","cc":"na","continent":"Africa","subregion":"Southern Africa"},
  {"name":"Goreme","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Khao Yai","country":"Thailand","cc":"th","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Chitwan","country":"Nepal","cc":"np","continent":"Asia","subregion":"Southern Asia"},
]
NPJ = json.dumps(NATIONAL_PARKS, separators=(',',':'), ensure_ascii=False)

UNESCO_SITES = [
  {"name":"Altstadt von Dubrovnik","country":"Croatia","cc":"hr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Meteora","country":"Greece","cc":"gr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Delphi","country":"Greece","cc":"gr","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Venedig und Lagune","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Pompeji","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Cinque Terre","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Amalfikueste","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Dolomiten","country":"Italy","cc":"it","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Altstadt von Toledo","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Altamira-Hoehle","country":"Spain","cc":"es","continent":"Europe","subregion":"Southern Europe"},
  {"name":"Historisches Zentrum von Prag","country":"Czech Republic","cc":"cz","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Krakauer Altstadt","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Wieliczka-Salzbergwerk","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Auschwitz-Birkenau","country":"Poland","cc":"pl","continent":"Europe","subregion":"Eastern Europe"},
  {"name":"Historisches Tallinn","country":"Estonia","cc":"ee","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Historisches Riga","country":"Latvia","cc":"lv","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Altstadt von Bruegge","country":"Belgium","cc":"be","continent":"Europe","subregion":"Western Europe"},
  {"name":"Koelner Dom","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Bamberger Altstadt","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Schloss Sanssouci","country":"Germany","cc":"de","continent":"Europe","subregion":"Western Europe"},
  {"name":"Wachau","country":"Austria","cc":"at","continent":"Europe","subregion":"Western Europe"},
  {"name":"Hallstatt","country":"Austria","cc":"at","continent":"Europe","subregion":"Western Europe"},
  {"name":"Palast von Versailles","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Mont-Saint-Michel","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Pont du Gard","country":"France","cc":"fr","continent":"Europe","subregion":"Western Europe"},
  {"name":"Timbuktu","country":"Mali","cc":"ml","continent":"Africa","subregion":"Western Africa"},
  {"name":"Felsenkirchen von Lalibela","country":"Ethiopia","cc":"et","continent":"Africa","subregion":"Eastern Africa"},
  {"name":"Historisches Kairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Tal der Koenige","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Medina von Fes","country":"Morocco","cc":"ma","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Medina von Marrakesch","country":"Morocco","cc":"ma","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Potala-Palast","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Lijiang-Altstadt","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Altstadt von Kyoto","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Horyu-ji-Tempel","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Historisches Hoi An","country":"Vietnam","cc":"vn","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Ajanta-Hoehlen","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Hampi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Bagan","country":"Myanmar","cc":"mm","continent":"Asia","subregion":"Southeast Asia"},
  {"name":"Chan Chan","country":"Peru","cc":"pe","continent":"South America","subregion":"South America"},
  {"name":"Historisches Cartagena","country":"Colombia","cc":"co","continent":"South America","subregion":"South America"},
  {"name":"Chaco Culture","country":"United States","cc":"us","continent":"North America","subregion":"Northern America"},
]
UNJ = json.dumps(UNESCO_SITES, separators=(',',':'), ensure_ascii=False)

CITY_LANDMARKS = [
  {"name":"Tokyo Tower","city":"Tokyo","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Senso-ji-Tempel","city":"Tokyo","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Tokyo Skytree","city":"Tokyo","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Shibuya-Kreuzung","city":"Tokyo","country":"Japan","cc":"jp","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"India Gate","city":"Delhi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Qutub Minar","city":"Delhi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Humayuns Grab","city":"Delhi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Lotus-Tempel","city":"Delhi","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Oriental Pearl Tower","city":"Shanghai","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Der Bund","city":"Shanghai","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Yu-Garten","city":"Shanghai","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Shanghai Tower","city":"Shanghai","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"MASP Museum","city":"Sao Paulo","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Ibirapuera-Park","city":"Sao Paulo","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Pinacoteca do Estado","city":"Sao Paulo","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Mercadao","city":"Sao Paulo","country":"Brazil","cc":"br","continent":"South America","subregion":"South America"},
  {"name":"Aegyptisches Museum Kairo","city":"Cairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Khan el-Khalili","city":"Cairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Zitadelle von Kairo","city":"Cairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Al-Azhar-Moschee","city":"Cairo","country":"Egypt","cc":"eg","continent":"Africa","subregion":"Northern Africa"},
  {"name":"Chapultepec-Schloss","city":"Mexico City","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Zocalo","city":"Mexico City","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Palacio de Bellas Artes","city":"Mexico City","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Templo Mayor","city":"Mexico City","country":"Mexico","cc":"mx","continent":"North America","subregion":"Central America"},
  {"name":"Himmelstempel","city":"Beijing","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Sommerpalast","city":"Beijing","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Beihai-Park","city":"Beijing","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"798 Kunstbezirk","city":"Beijing","country":"China","cc":"cn","continent":"Asia","subregion":"Eastern Asia"},
  {"name":"Gateway of India","city":"Mumbai","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Marine Drive","city":"Mumbai","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Chhatrapati Shivaji Terminus","city":"Mumbai","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Elephanta-Hoehlen","city":"Mumbai","country":"India","cc":"in","continent":"Asia","subregion":"Southern Asia"},
  {"name":"Topkapi-Palast","city":"Istanbul","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Galata-Turm","city":"Istanbul","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Grosser Basar","city":"Istanbul","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Dolmabahce-Palast","city":"Istanbul","country":"Turkey","cc":"tr","continent":"Europe","subregion":"Western Asia"},
  {"name":"Buckingham Palace","city":"London","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Hyde Park","city":"London","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Westminster Abbey","city":"London","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
  {"name":"Tate Modern","city":"London","country":"United Kingdom","cc":"gb","continent":"Europe","subregion":"Northern Europe"},
]
CLJ = json.dumps(CITY_LANDMARKS, separators=(',',':'), ensure_ascii=False)

# Phase 10: Top 50 subway systems (km, lines)
SUBWAYS = [
  {"city":"Shanghai","country":"China","cc":"cn","km":831,"lines":20},
  {"city":"Beijing","country":"China","cc":"cn","km":783,"lines":27},
  {"city":"Guangzhou","country":"China","cc":"cn","km":621,"lines":16},
  {"city":"Shenzhen","country":"China","cc":"cn","km":559,"lines":16},
  {"city":"Chengdu","country":"China","cc":"cn","km":518,"lines":13},
  {"city":"Delhi","country":"India","cc":"in","km":391,"lines":12},
  {"city":"Wuhan","country":"China","cc":"cn","km":439,"lines":14},
  {"city":"London","country":"United Kingdom","cc":"gb","km":402,"lines":11},
  {"city":"New York","country":"United States","cc":"us","km":380,"lines":36},
  {"city":"Nanjing","country":"China","cc":"cn","km":378,"lines":11},
  {"city":"Moscow","country":"Russia","cc":"ru","km":372,"lines":15},
  {"city":"Chongqing","country":"China","cc":"cn","km":350,"lines":10},
  {"city":"Hangzhou","country":"China","cc":"cn","km":361,"lines":10},
  {"city":"Seoul","country":"South Korea","cc":"kr","km":340,"lines":23},
  {"city":"Tokyo","country":"Japan","cc":"jp","km":337,"lines":13},
  {"city":"Qingdao","country":"China","cc":"cn","km":319,"lines":9},
  {"city":"Madrid","country":"Spain","cc":"es","km":293,"lines":13},
  {"city":"Kuala Lumpur","country":"Malaysia","cc":"my","km":213,"lines":9},
  {"city":"Hong Kong","country":"China","cc":"cn","km":264,"lines":10},
  {"city":"Singapore","country":"Singapore","cc":"sg","km":199,"lines":6},
  {"city":"Washington D.C.","country":"United States","cc":"us","km":188,"lines":6},
  {"city":"Istanbul","country":"Turkey","cc":"tr","km":190,"lines":7},
  {"city":"Los Angeles","country":"United States","cc":"us","km":169,"lines":7},
  {"city":"San Francisco","country":"United States","cc":"us","km":167,"lines":7},
  {"city":"Chicago","country":"United States","cc":"us","km":171,"lines":8},
  {"city":"Paris","country":"France","cc":"fr","km":226,"lines":16},
  {"city":"Mexico City","country":"Mexico","cc":"mx","km":226,"lines":12},
  {"city":"Taipei","country":"Taiwan","cc":"tw","km":131,"lines":6},
  {"city":"Santiago","country":"Chile","cc":"cl","km":136,"lines":7},
  {"city":"Jakarta","country":"Indonesia","cc":"id","km":168,"lines":2},
  {"city":"Bangkok","country":"Thailand","cc":"th","km":127,"lines":4},
  {"city":"Stockholm","country":"Sweden","cc":"se","km":110,"lines":3},
  {"city":"Barcelona","country":"Spain","cc":"es","km":122,"lines":12},
  {"city":"Osaka","country":"Japan","cc":"jp","km":137,"lines":9},
  {"city":"Berlin","country":"Germany","cc":"de","km":155,"lines":9},
  {"city":"Cairo","country":"Egypt","cc":"eg","km":90,"lines":3},
  {"city":"Dubai","country":"UAE","cc":"ae","km":90,"lines":2},
  {"city":"Mumbai","country":"India","cc":"in","km":87,"lines":3},
  {"city":"Athens","country":"Greece","cc":"gr","km":85,"lines":3},
  {"city":"Vienna","country":"Austria","cc":"at","km":83,"lines":5},
  {"city":"Budapest","country":"Hungary","cc":"hu","km":40,"lines":4},
  {"city":"Toronto","country":"Canada","cc":"ca","km":77,"lines":4},
  {"city":"Boston","country":"United States","cc":"us","km":73,"lines":4},
  {"city":"Prague","country":"Czech Republic","cc":"cz","km":65,"lines":3},
  {"city":"Buenos Aires","country":"Argentina","cc":"ar","km":55,"lines":6},
  {"city":"Amsterdam","country":"Netherlands","cc":"nl","km":53,"lines":4},
  {"city":"Lisbon","country":"Portugal","cc":"pt","km":44,"lines":4},
  {"city":"Brussels","country":"Belgium","cc":"be","km":39,"lines":4},
  {"city":"Warsaw","country":"Poland","cc":"pl","km":36,"lines":2},
  {"city":"Sao Paulo","country":"Brazil","cc":"br","km":101,"lines":6},
]
SWJ = json.dumps(SUBWAYS, separators=(',',':'), ensure_ascii=False)

print('Data prepared. Cities:', len(cities_slim), '| Subways:', len(SUBWAYS))


# ── LIFESTYLE DATA (Phases 22) ───────────────────────────────────────────────
FOOD = [{'dish': 'Sushi', 'country': 'Japan', 'cc': 'jp', 'emoji': '🍣'}, {'dish': 'Pizza', 'country': 'Italy', 'cc': 'it', 'emoji': '🍕'}, {'dish': 'Tacos', 'country': 'Mexico', 'cc': 'mx', 'emoji': '🌮'}, {'dish': 'Croissant', 'country': 'France', 'cc': 'fr', 'emoji': '🥐'}, {'dish': 'Paella', 'country': 'Spain', 'cc': 'es', 'emoji': '🥘'}, {'dish': 'Kimchi', 'country': 'South Korea', 'cc': 'kr', 'emoji': '🥬'}, {'dish': 'Pho', 'country': 'Vietnam', 'cc': 'vn', 'emoji': '🍜'}, {'dish': 'Pad Thai', 'country': 'Thailand', 'cc': 'th', 'emoji': '🍜'}, {'dish': 'Peking Duck', 'country': 'China', 'cc': 'cn', 'emoji': '🦆'}, {'dish': 'Biryani', 'country': 'India', 'cc': 'in', 'emoji': '🍛'}, {'dish': 'Samosa', 'country': 'India', 'cc': 'in', 'emoji': '🧆'}, {'dish': 'Rendang', 'country': 'Indonesia', 'cc': 'id', 'emoji': '🍖'}, {'dish': 'Nasi Goreng', 'country': 'Indonesia', 'cc': 'id', 'emoji': '🍚'}, {'dish': 'Jollof Rice', 'country': 'Nigeria', 'cc': 'ng', 'emoji': '🍚'}, {'dish': 'Injera', 'country': 'Ethiopia', 'cc': 'et', 'emoji': '🧇'}, {'dish': 'Tagine', 'country': 'Morocco', 'cc': 'ma', 'emoji': '🍲'}, {'dish': 'Borscht', 'country': 'Ukraine', 'cc': 'ua', 'emoji': '🍱'}, {'dish': 'Pierogi', 'country': 'Poland', 'cc': 'pl', 'emoji': '🥟'}, {'dish': 'Goulash', 'country': 'Hungary', 'cc': 'hu', 'emoji': '🍲'}, {'dish': 'Moussaka', 'country': 'Greece', 'cc': 'gr', 'emoji': '🍕'}, {'dish': 'Fish and Chips', 'country': 'United Kingdom', 'cc': 'gb', 'emoji': '🐟'}, {'dish': 'Poutine', 'country': 'Canada', 'cc': 'ca', 'emoji': '🍟'}, {'dish': 'Ceviche', 'country': 'Peru', 'cc': 'pe', 'emoji': '🐟'}, {'dish': 'Empanada', 'country': 'Argentina', 'cc': 'ar', 'emoji': '🥪'}, {'dish': 'Feijoada', 'country': 'Brazil', 'cc': 'br', 'emoji': '🍲'}, {'dish': 'Fondue', 'country': 'Switzerland', 'cc': 'ch', 'emoji': '🧀'}, {'dish': 'Wiener Schnitzel', 'country': 'Austria', 'cc': 'at', 'emoji': '🍖'}, {'dish': 'Bacalhau', 'country': 'Portugal', 'cc': 'pt', 'emoji': '🐟'}, {'dish': 'Shakshuka', 'country': 'Israel', 'cc': 'il', 'emoji': '🍳'}, {'dish': 'Bibimbap', 'country': 'South Korea', 'cc': 'kr', 'emoji': '🍱'}, {'dish': 'Stroganoff', 'country': 'Russia', 'cc': 'ru', 'emoji': '🥩'}, {'dish': 'Bobotie', 'country': 'South Africa', 'cc': 'za', 'emoji': '🍖'}, {'dish': 'Tom Yum', 'country': 'Thailand', 'cc': 'th', 'emoji': '🧅'}, {'dish': 'Churros', 'country': 'Spain', 'cc': 'es', 'emoji': '🍩'}, {'dish': 'Smorgasbord', 'country': 'Sweden', 'cc': 'se', 'emoji': '🥪'}]
FJ  = json.dumps(FOOD,   separators=(',',':'), ensure_ascii=False)

BRANDS = [{'brand': 'Samsung', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'LG', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Hyundai', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Kia', 'country': 'South Korea', 'cc': 'kr', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Nintendo', 'country': 'Japan', 'cc': 'jp', 'industry': 'Gaming', 'sub': 'Eastern Asia'}, {'brand': 'Sony', 'country': 'Japan', 'cc': 'jp', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Toyota', 'country': 'Japan', 'cc': 'jp', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Honda', 'country': 'Japan', 'cc': 'jp', 'industry': 'Autos', 'sub': 'Eastern Asia'}, {'brand': 'Yamaha', 'country': 'Japan', 'cc': 'jp', 'industry': 'Musik/Autos', 'sub': 'Eastern Asia'}, {'brand': 'Lenovo', 'country': 'China', 'cc': 'cn', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Alibaba', 'country': 'China', 'cc': 'cn', 'industry': 'E-Commerce', 'sub': 'Eastern Asia'}, {'brand': 'Xiaomi', 'country': 'China', 'cc': 'cn', 'industry': 'Elektronik', 'sub': 'Eastern Asia'}, {'brand': 'Huawei', 'country': 'China', 'cc': 'cn', 'industry': 'Telekommunikation', 'sub': 'Eastern Asia'}, {'brand': 'IKEA', 'country': 'Sweden', 'cc': 'se', 'industry': 'Moebel', 'sub': 'Northern Europe'}, {'brand': 'H&M', 'country': 'Sweden', 'cc': 'se', 'industry': 'Mode', 'sub': 'Northern Europe'}, {'brand': 'Volvo', 'country': 'Sweden', 'cc': 'se', 'industry': 'Autos', 'sub': 'Northern Europe'}, {'brand': 'Spotify', 'country': 'Sweden', 'cc': 'se', 'industry': 'Streaming', 'sub': 'Northern Europe'}, {'brand': 'LEGO', 'country': 'Denmark', 'cc': 'dk', 'industry': 'Spielzeug', 'sub': 'Northern Europe'}, {'brand': 'Bang & Olufsen', 'country': 'Denmark', 'cc': 'dk', 'industry': 'Elektronik', 'sub': 'Northern Europe'}, {'brand': 'Nokia', 'country': 'Finland', 'cc': 'fi', 'industry': 'Telekommunikation', 'sub': 'Northern Europe'}, {'brand': 'Volkswagen', 'country': 'Germany', 'cc': 'de', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'BMW', 'country': 'Germany', 'cc': 'de', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'Porsche', 'country': 'Germany', 'cc': 'de', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'ALDI', 'country': 'Germany', 'cc': 'de', 'industry': 'Einzelhandel', 'sub': 'Western Europe'}, {'brand': 'Airbus', 'country': 'France', 'cc': 'fr', 'industry': 'Luftfahrt', 'sub': 'Western Europe'}, {'brand': 'Renault', 'country': 'France', 'cc': 'fr', 'industry': 'Autos', 'sub': 'Western Europe'}, {'brand': 'Louis Vuitton', 'country': 'France', 'cc': 'fr', 'industry': 'Luxus', 'sub': 'Western Europe'}, {'brand': 'Ferrari', 'country': 'Italy', 'cc': 'it', 'industry': 'Autos', 'sub': 'Southern Europe'}, {'brand': 'Maserati', 'country': 'Italy', 'cc': 'it', 'industry': 'Autos', 'sub': 'Southern Europe'}, {'brand': 'Zara', 'country': 'Spain', 'cc': 'es', 'industry': 'Mode', 'sub': 'Southern Europe'}, {'brand': 'Shell', 'country': 'Netherlands', 'cc': 'nl', 'industry': 'Energie', 'sub': 'Western Europe'}, {'brand': 'Philips', 'country': 'Netherlands', 'cc': 'nl', 'industry': 'Elektronik', 'sub': 'Western Europe'}, {'brand': 'Heineken', 'country': 'Netherlands', 'cc': 'nl', 'industry': 'Bier', 'sub': 'Western Europe'}, {'brand': 'Nestle', 'country': 'Switzerland', 'cc': 'ch', 'industry': 'Lebensmittel', 'sub': 'Western Europe'}, {'brand': 'Rolex', 'country': 'Switzerland', 'cc': 'ch', 'industry': 'Uhren', 'sub': 'Western Europe'}, {'brand': 'Skoda', 'country': 'Czech Republic', 'cc': 'cz', 'industry': 'Autos', 'sub': 'Eastern Europe'}, {'brand': 'Emirates', 'country': 'UAE', 'cc': 'ae', 'industry': 'Luftfahrt', 'sub': 'Western Asia'}, {'brand': 'Petronas', 'country': 'Malaysia', 'cc': 'my', 'industry': 'Energie', 'sub': 'Southeast Asia'}, {'brand': 'Tata', 'country': 'India', 'cc': 'in', 'industry': 'Konglomerat', 'sub': 'Southern Asia'}, {'brand': 'Corona', 'country': 'Mexico', 'cc': 'mx', 'industry': 'Bier', 'sub': 'Central America'}, {'brand': 'Embraer', 'country': 'Brazil', 'cc': 'br', 'industry': 'Luftfahrt', 'sub': 'South America'}, {'brand': 'MTN', 'country': 'South Africa', 'cc': 'za', 'industry': 'Telekommunikation', 'sub': 'Southern Africa'}]
BJ  = json.dumps(BRANDS, separators=(',',':'), ensure_ascii=False)

CURRENCIES = [{'currency': 'Yen', 'symbol': '¥', 'country': 'Japan', 'cc': 'jp', 'sub': 'Eastern Asia'}, {'currency': 'Won', 'symbol': '₩', 'country': 'South Korea', 'cc': 'kr', 'sub': 'Eastern Asia'}, {'currency': 'Renminbi', 'symbol': '¥', 'country': 'China', 'cc': 'cn', 'sub': 'Eastern Asia'}, {'currency': 'Rupee', 'symbol': '₹', 'country': 'India', 'cc': 'in', 'sub': 'Southern Asia'}, {'currency': 'Taka', 'symbol': '৳', 'country': 'Bangladesh', 'cc': 'bd', 'sub': 'Southern Asia'}, {'currency': 'Baht', 'symbol': '฿', 'country': 'Thailand', 'cc': 'th', 'sub': 'Southeast Asia'}, {'currency': 'Dong', 'symbol': '₫', 'country': 'Vietnam', 'cc': 'vn', 'sub': 'Southeast Asia'}, {'currency': 'Ringgit', 'symbol': 'RM', 'country': 'Malaysia', 'cc': 'my', 'sub': 'Southeast Asia'}, {'currency': 'Peso', 'symbol': '₱', 'country': 'Philippines', 'cc': 'ph', 'sub': 'Southeast Asia'}, {'currency': 'Pound', 'symbol': '£', 'country': 'United Kingdom', 'cc': 'gb', 'sub': 'Northern Europe'}, {'currency': 'Krone', 'symbol': 'kr', 'country': 'Denmark', 'cc': 'dk', 'sub': 'Northern Europe'}, {'currency': 'Krone', 'symbol': 'kr', 'country': 'Norway', 'cc': 'no', 'sub': 'Northern Europe'}, {'currency': 'Krona', 'symbol': 'kr', 'country': 'Sweden', 'cc': 'se', 'sub': 'Northern Europe'}, {'currency': 'Forint', 'symbol': 'Ft', 'country': 'Hungary', 'cc': 'hu', 'sub': 'Eastern Europe'}, {'currency': 'Zloty', 'symbol': 'zł', 'country': 'Poland', 'cc': 'pl', 'sub': 'Eastern Europe'}, {'currency': 'Koruna', 'symbol': 'Kč', 'country': 'Czech Republic', 'cc': 'cz', 'sub': 'Eastern Europe'}, {'currency': 'Hryvnia', 'symbol': '₴', 'country': 'Ukraine', 'cc': 'ua', 'sub': 'Eastern Europe'}, {'currency': 'Leu', 'symbol': 'lei', 'country': 'Romania', 'cc': 'ro', 'sub': 'Eastern Europe'}, {'currency': 'Ruble', 'symbol': '₽', 'country': 'Russia', 'cc': 'ru', 'sub': 'Eastern Europe'}, {'currency': 'Lira', 'symbol': '₺', 'country': 'Turkey', 'cc': 'tr', 'sub': 'Western Asia'}, {'currency': 'Shekel', 'symbol': '₪', 'country': 'Israel', 'cc': 'il', 'sub': 'Western Asia'}, {'currency': 'Riyal', 'symbol': 'SAR', 'country': 'Saudi Arabia', 'cc': 'sa', 'sub': 'Western Asia'}, {'currency': 'Dirham', 'symbol': 'AED', 'country': 'UAE', 'cc': 'ae', 'sub': 'Western Asia'}, {'currency': 'Dinar', 'symbol': 'RSD', 'country': 'Serbia', 'cc': 'rs', 'sub': 'Southern Europe'}, {'currency': 'Tenge', 'symbol': '₸', 'country': 'Kazakhstan', 'cc': 'kz', 'sub': 'Central Asia'}, {'currency': 'Real', 'symbol': 'R$', 'country': 'Brazil', 'cc': 'br', 'sub': 'South America'}, {'currency': 'Peso', 'symbol': '$', 'country': 'Mexico', 'cc': 'mx', 'sub': 'Central America'}, {'currency': 'Peso', 'symbol': '$', 'country': 'Argentina', 'cc': 'ar', 'sub': 'South America'}, {'currency': 'Sol', 'symbol': 'S/', 'country': 'Peru', 'cc': 'pe', 'sub': 'South America'}, {'currency': 'Rand', 'symbol': 'R', 'country': 'South Africa', 'cc': 'za', 'sub': 'Southern Africa'}, {'currency': 'Naira', 'symbol': '₦', 'country': 'Nigeria', 'cc': 'ng', 'sub': 'Western Africa'}, {'currency': 'Birr', 'symbol': 'Br', 'country': 'Ethiopia', 'cc': 'et', 'sub': 'Eastern Africa'}, {'currency': 'Shilling', 'symbol': 'Sh', 'country': 'Kenya', 'cc': 'ke', 'sub': 'Eastern Africa'}, {'currency': 'Pound', 'symbol': 'E£', 'country': 'Egypt', 'cc': 'eg', 'sub': 'Northern Africa'}, {'currency': 'Dirham', 'symbol': 'MAD', 'country': 'Morocco', 'cc': 'ma', 'sub': 'Northern Africa'}]
CUJ = json.dumps(CURRENCIES, separators=(',',':'), ensure_ascii=False)
print('Lifestyle data: Food', len(FOOD), '| Brands', len(BRANDS), '| Currencies', len(CURRENCIES))


# ── LICENSE PLATES (Phase 23B) ── loaded at runtime via fetch()
import os as _os

# CSS
_css_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'geoquest_css.txt')
CSS = open(_css_path,'r',encoding='utf-8').read()

# Phase 28 data payloads — loaded at runtime via fetch()
print('CSS ready:', len(CSS), 'chars')
# JS TEMPLATE
JS = r'''

const SUPABASE_URL  = "https://lpwcqvxajahiftvwxovq.supabase.co";
const SUPABASE_ANON = "sb_publishable_HL6cIlPOtVAdkjycaiceGQ_CBNFF-dG";
/* ADMIN_EMAIL removed — use Supabase trigger instead */

/* PAYMENT CONFIG */
const STRIPE_PK = "";
function esc(s){return String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#x27;");}

const PAY_PRODUCTS = [
  {id:"coins_500",  name:"500 GeoCoins",         price:"1,99 \u20ac", coins:500,  premium:false, desc:"Einmalkauf \u2022 sofort gutgeschrieben"},
  {id:"coins_2000", name:"2.000 GeoCoins",        price:"4,99 \u20ac", coins:2000, premium:false, desc:"Beliebt \u2022 Sparpreis", featured:true},
  {id:"premium_m",  name:"Premium Monatlich",     price:"3,99 \u20ac", coins:200,  premium:true,  months:1,  desc:"Alle Modi \u2022 Keine Werbung"},
  {id:"premium_y",  name:"Premium J\u00e4hrlich", price:"29,99 \u20ac",coins:1000, premium:true,  months:12, desc:"40% g\u00fcnstiger \u2022 +1.000 Coins", featured:true},
  {id:"pu_5050",   name:"3\u00d7 50/50-Joker",   price:"0,99 \u20ac", coins:0,   premium:false, pu:"five0", pu_qty:3, desc:"2 falsche Antworten entfernen"},
  {id:"pu_freeze", name:"3\u00d7 Zeit-Stopp",     price:"0,99 \u20ac", coins:0,   premium:false, pu:"freeze", pu_qty:3, desc:"Timer 10 Sekunden einfrieren"},
];

/* LANGUAGE */
/* ── Phase 47/48: i18n — DE / EN / PL ───────────────────────────────────── */
const LANG={
de:{
  play:"SPIELEN",again:"NOCHMAL",menu:"Hauptmenü",board:"Bestenliste",pass:"Reisepass",
  profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Runden",
  btn_collect:"Sammeln",btn_back:"Zurück zum Hauptmenü",btn_next:"Weiter →",
  btn_again:"Nochmal",btn_menu:"Hauptmenü",btn_adapt:"Anpassen",
  spotter_title:"\u{1F697} Roadtrip-Spotter",
  spotter_hint:"Kennzeichen gesehen? Sofort eintragen!",
  spotter_all:"Alle Länder",spotter_unknown:"Unbekanntes Kennzeichen",
  spotter_not_in:"nicht in",spotter_but_in:"aber in",
  album_title:"\u{1F4D4} Kennzeichen-Album",album_list:"\u{1F4DD} Liste",album_map:"\u{1F5FA} Karte",
  album_empty_country:"Noch nichts aus {country} gesammelt — nutze den Spotter!",
  album_empty:"Noch nichts gesammelt!\nSpiele EU-Kennzeichen oder benutze den Spotter.",
  album_codes:"Kürzel",
  hl_higher:"⬆️ Mehr / Länger / Größer",hl_lower:"⬇️ Weniger / Kürzer / Kleiner",
  hl_more:"⬆️ Mehr Einwohner",hl_less:"⬇️ Weniger Einwohner",
  loc_detected:"Du bist in {country}",loc_adapt:"Anpassen",
  q_city:"In welchem Land liegt diese Stadt?",q_flag:"Welches Land zeigt diese Flagge?",
  q_capital:"Zu welchem Land gehört diese Hauptstadt?",q_river:"In welchem Land liegt dieser Fluss?",
  q_landmark:"In welchem Land liegt dieses Wahrzeichen?",q_park:"In welchem Land liegt dieser Nationalpark?",
  q_unesco:"In welchem Land liegt dieses UNESCO-Welterbe?",q_citymark:"Zu welcher Stadt gehört dieses Wahrzeichen?",
  q_subway:"In welcher Stadt ist diese U-Bahn?",q_flagsel:"Welche Flagge gehört zu …",
  q_rcapital:"Was ist die Hauptstadt von …?",q_rcity:"Welche Stadt liegt in …?",
  q_rriver:"Welcher Fluss fließt durch …?",q_outline:"Welches Land hat diese Form?",
  q_food:"Aus welchem Land kommt dieses Gericht?",q_brand:"Aus welchem Land kommt diese Marke?",
  q_currency:"Zu welchem Land gehört diese Währung?",q_curr_real:"Welche Währung hat …",
  q_pop_compare:"Mehr oder weniger Einwohner?",
  q_hl_pop:"Mehr Einwohner als {a}?",q_hl_river:"Länger als {a}?",q_hl_area:"Größer als {a}?",
  q_neighbor:"Welches Land grenzt an…?",q_neighbor_not:"Grenzt NICHT an…?",
  q_plates_casual:"Woher kommt dieses Kennzeichen?",q_plates_hard:"Region erkennen — kein Tipp!",
  q_river_real:"Durch welches Land fließt dieser Fluss?",q_map_guess:"Finde das Land auf der Karte",
  fb_correct:"✓ Richtig! +{pts}",fb_wrong:"✗ Falsch → {ans}",fb_time:"⏱ Zeit! → {ans}",
  plates_more:"+{n} weitere",pct_complete:"{pct}% vollständig",
  spotter_dup:"📋 {code} ({country}) bereits gesammelt!",
  map_unavail:"Karte nicht verfügbar",map_loading:"Kartendaten werden geladen…",
  q_subway_km:"Wie lang ist das U-Bahn-Netz … (km)?",q_subway_lines:"Wie viele U-Bahn-Linien hat …?"
},
en:{
  play:"PLAY",again:"PLAY AGAIN",menu:"Main Menu",board:"Leaderboard",pass:"Passport",
  profile:"Profile",stats:"Stats",casual:"Casual",hardcore:"Hardcore",rounds:"Rounds",
  btn_collect:"Collect",btn_back:"Back to Main Menu",btn_next:"Next →",
  btn_again:"Play Again",btn_menu:"Main Menu",btn_adapt:"Adapt",
  spotter_title:"\u{1F697} Road Trip Spotter",
  spotter_hint:"Spotted a plate? Log it now!",
  spotter_all:"All Countries",spotter_unknown:"Unknown plate",
  spotter_not_in:"not in",spotter_but_in:"but found in",
  album_title:"\u{1F4D4} Plate Collection",album_list:"\u{1F4DD} List",album_map:"\u{1F5FA} Map",
  album_empty_country:"Nothing from {country} yet — use the Spotter!",
  album_empty:"Nothing collected yet!\nPlay EU plates or use the Spotter above.",
  album_codes:"codes",
  hl_higher:"⬆️ More / Longer / Larger",hl_lower:"⬇️ Less / Shorter / Smaller",
  hl_more:"⬆️ More Population",hl_less:"⬇️ Less Population",
  loc_detected:"You are in {country}",loc_adapt:"Adapt",
  q_city:"In which country is this city?",q_flag:"Which country does this flag belong to?",
  q_capital:"Which country has this capital?",q_river:"In which country is this river?",
  q_landmark:"In which country is this landmark?",q_park:"In which country is this national park?",
  q_unesco:"In which country is this UNESCO site?",q_citymark:"Which city has this landmark?",
  q_subway:"Which city has this metro?",q_flagsel:"Which flag belongs to…",
  q_rcapital:"What is the capital of…?",q_rcity:"Which city is in…?",
  q_rriver:"Which river flows through…?",q_outline:"Which country has this shape?",
  q_food:"Which country does this dish come from?",q_brand:"Which country does this brand come from?",
  q_currency:"Which country uses this currency?",q_curr_real:"What currency does…",
  q_pop_compare:"More or fewer inhabitants?",
  q_hl_pop:"More inhabitants than {a}?",q_hl_river:"Longer than {a}?",q_hl_area:"Larger than {a}?",
  q_neighbor:"Which country borders…?",q_neighbor_not:"Does NOT border…?",
  q_plates_casual:"Which country has this plate?",q_plates_hard:"Identify the region — no hint!",
  q_river_real:"Which country does this river flow through?",q_map_guess:"Find the country on the map",
  fb_correct:"✓ Correct! +{pts}",fb_wrong:"✗ Wrong → {ans}",fb_time:"⏱ Time! → {ans}",
  plates_more:"+{n} more",pct_complete:"{pct}% complete",
  spotter_dup:"📋 {code} ({country}) already collected!",
  map_unavail:"Map not available",map_loading:"Loading map data…",
  q_subway_km:"How long is the metro network … (km)?",q_subway_lines:"How many metro lines does … have?"
},
pl:{
  play:"GRAJ",again:"ZAGRAJ PONOWNIE",menu:"Menu",board:"Ranking",pass:"Paszport",
  profile:"Profil",stats:"Statystyki",casual:"Zwykły",hardcore:"Trudny",rounds:"Rundy",
  btn_collect:"Zbierz",btn_back:"Powrót do menu",btn_next:"Dalej →",
  btn_again:"Zagraj ponownie",btn_menu:"Menu",btn_adapt:"Dostosuj",
  spotter_title:"\u{1F697} Spotter Podróżnika",
  spotter_hint:"Widzisz tablicę? Zapisz ją od razu!",
  spotter_all:"Wszystkie kraje",spotter_unknown:"Nieznana tablica",
  spotter_not_in:"nie ma w",spotter_but_in:"ale jest w",
  album_title:"\u{1F4D4} Album Tablic",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Nic z {country} jeszcze — użyj Spottera!",
  album_empty:"Nic jeszcze nie zebrano!\nGraj w tablice EU lub użyj Spottera.",
  album_codes:"kodów",
  hl_higher:"⬆️ Więcej / Dłużej / Większy",hl_lower:"⬇️ Mniej / Krócej / Mniejszy",
  hl_more:"⬆️ Więcej mieszkańców",hl_less:"⬇️ Mniej mieszkańców",
  loc_detected:"Jesteś w {country}",loc_adapt:"Dostosuj",
  q_city:"W jakim kraju leży to miasto?",q_flag:"Jakie państwo ma tę flagę?",
  q_capital:"Do jakiego kraju należy ta stolica?",q_river:"W jakim kraju płynie ta rzeka?",
  q_landmark:"W jakim kraju jest ta atrakcja?",q_park:"W jakim kraju jest ten park narodowy?",
  q_unesco:"W jakim kraju jest to dziedzictwo UNESCO?",q_citymark:"Do jakiego miasta należy ta atrakcja?",
  q_subway:"W jakim mieście jest to metro?",q_flagsel:"Która flaga należy do…",
  q_rcapital:"Jaka jest stolica …?",q_rcity:"Które miasto leży w …?",
  q_rriver:"Która rzeka płynie przez …?",q_outline:"Które państwo ma ten kształt?",
  q_food:"Z jakiego kraju pochodzi to danie?",q_brand:"Z jakiego kraju pochodzi ta marka?",
  q_currency:"Do jakiego kraju należy ta waluta?",q_curr_real:"Jaką walutę ma…",
  q_pop_compare:"Więcej czy mniej mieszkańców?",
  q_hl_pop:"Więcej mieszkańców niż {a}?",q_hl_river:"Dłuższa niż {a}?",q_hl_area:"Większy niż {a}?",
  q_neighbor:"Który kraj graniczy z…?",q_neighbor_not:"NIE graniczy z…?",
  q_plates_casual:"Do jakiego kraju należy ta tablica?",q_plates_hard:"Jaki region ma tę tablicę?",
  q_river_real:"Przez jaki kraj płynie ta rzeka?",q_map_guess:"Znajdź kraj na mapie",
  fb_correct:"✓ Dobrze! +{pts}",fb_wrong:"✗ Błąd → {ans}",fb_time:"⏱ Czas! → {ans}",
  plates_more:"+{n} więcej",pct_complete:"{pct}% ukończono",
  spotter_dup:"📋 {code} ({country}) już zebrane!",
  map_unavail:"Mapa niedostępna",map_loading:"Ładowanie mapy…",
  q_subway_km:"Jak długa jest sieć metra … (km)?",q_subway_lines:"Ile linii metra ma …?"
},
fr:{
  play:"JOUER",again:"REJOUER",menu:"Menu principal",board:"Classement",pass:"Passeport",
  profile:"Profil",stats:"Statistiques",casual:"Casual",hardcore:"Hardcore",rounds:"Manches",
  btn_collect:"Collecter",btn_back:"Retour au menu",btn_next:"Suivant →",
  btn_again:"Rejouer",btn_menu:"Menu principal",btn_adapt:"Adapter",
  spotter_title:"\u{1F697} Spotter de voyage",
  spotter_hint:"Vu une plaque ? Notez-la !",
  spotter_all:"Tous les pays",spotter_unknown:"Plaque inconnue",
  spotter_not_in:"pas dans",spotter_but_in:"mais dans",
  album_title:"\u{1F4D4} Collection de plaques",album_list:"\u{1F4DD} Liste",album_map:"\u{1F5FA} Carte",
  album_empty_country:"Rien de {country} encore — utilisez le Spotter !",
  album_empty:"Rien collecté encore !\nJouez aux plaques UE ou utilisez le Spotter.",
  album_codes:"codes",
  hl_higher:"⬆️ Plus / Plus long / Plus grand",hl_lower:"⬇️ Moins / Plus court / Plus petit",
  hl_more:"⬆️ Plus d'habitants",hl_less:"⬇️ Moins d'habitants",
  loc_detected:"Vous êtes en {country}",loc_adapt:"Adapter",
  q_city:"Dans quel pays se trouve cette ville ?",q_flag:"Quel pays a ce drapeau ?",
  q_capital:"À quel pays appartient cette capitale ?",q_river:"Dans quel pays coule ce fleuve ?",
  q_landmark:"Dans quel pays se trouve ce monument ?",q_park:"Dans quel pays se trouve ce parc national ?",
  q_unesco:"Dans quel pays se trouve ce site UNESCO ?",q_citymark:"À quelle ville appartient ce monument ?",
  q_subway:"Dans quelle ville se trouve ce métro ?",q_flagsel:"Quel drapeau appartient à…",
  q_rcapital:"Quelle est la capitale de… ?",q_rcity:"Quelle ville est dans… ?",
  q_rriver:"Quel fleuve traverse… ?",q_outline:"Quel pays a cette forme ?",
  q_food:"De quel pays vient ce plat ?",q_brand:"De quel pays vient cette marque ?",
  q_currency:"À quel pays appartient cette monnaie ?",q_curr_real:"Quelle monnaie a…",
  q_pop_compare:"Plus ou moins d'habitants ?",
  q_hl_pop:"Plus d'habitants que {a} ?",q_hl_river:"Plus long que {a} ?",q_hl_area:"Plus grand que {a} ?",
  q_neighbor:"Quel pays borde… ?",q_neighbor_not:"Ne borde PAS… ?",
  q_plates_casual:"De quel pays est cette plaque ?",q_plates_hard:"Identifier la région — aucun indice !",
  q_river_real:"Dans quel pays coule ce fleuve ?",q_map_guess:"Trouver le pays sur la carte",
  fb_correct:"✓ Correct ! +{pts}",fb_wrong:"✗ Faux → {ans}",fb_time:"⏱ Temps ! → {ans}",
  plates_more:"+{n} de plus",pct_complete:"{pct}% terminé",
  spotter_dup:"📋 {code} ({country}) déjà collecté !",
  map_unavail:"Carte non disponible",map_loading:"Chargement de la carte…",
  q_subway_km:"Quelle longueur a le réseau métro … (km)?",q_subway_lines:"Combien de lignes de métro a … ?"
},
es:{
  play:"JUGAR",again:"JUGAR DE NUEVO",menu:"Menú principal",board:"Clasificación",pass:"Pasaporte",
  profile:"Perfil",stats:"Estadísticas",casual:"Casual",hardcore:"Hardcore",rounds:"Rondas",
  btn_collect:"Coleccionar",btn_back:"Volver al menú",btn_next:"Siguiente →",
  btn_again:"Jugar de nuevo",btn_menu:"Menú principal",btn_adapt:"Adaptar",
  spotter_title:"\u{1F697} Spotter de viaje",
  spotter_hint:"¿Has visto una matrícula? ¡Anótala!",
  spotter_all:"Todos los países",spotter_unknown:"Matrícula desconocida",
  spotter_not_in:"no en",spotter_but_in:"pero en",
  album_title:"\u{1F4D4} Colección de matrículas",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Nada de {country} aún — ¡usa el Spotter!",
  album_empty:"¡Nada recopilado aún!\nJuega a matrículas UE o usa el Spotter.",
  album_codes:"códigos",
  hl_higher:"⬆️ Más / Más largo / Más grande",hl_lower:"⬇️ Menos / Más corto / Más pequeño",
  hl_more:"⬆️ Más habitantes",hl_less:"⬇️ Menos habitantes",
  loc_detected:"Estás en {country}",loc_adapt:"Adaptar",
  q_city:"¿En qué país está esta ciudad?",q_flag:"¿Qué país tiene esta bandera?",
  q_capital:"¿A qué país pertenece esta capital?",q_river:"¿En qué país está este río?",
  q_landmark:"¿En qué país está este monumento?",q_park:"¿En qué país está este parque nacional?",
  q_unesco:"¿En qué país está este sitio UNESCO?",q_citymark:"¿A qué ciudad pertenece este monumento?",
  q_subway:"¿En qué ciudad está este metro?",q_flagsel:"¿Qué bandera pertenece a…",
  q_rcapital:"¿Cuál es la capital de…?",q_rcity:"¿Qué ciudad está en…?",
  q_rriver:"¿Qué río atraviesa…?",q_outline:"¿Qué país tiene esta forma?",
  q_food:"¿De qué país viene este plato?",q_brand:"¿De qué país viene esta marca?",
  q_currency:"¿A qué país pertenece esta moneda?",q_curr_real:"¿Qué moneda tiene…",
  q_pop_compare:"¿Más o menos habitantes?",
  q_hl_pop:"¿Más habitantes que {a}?",q_hl_river:"¿Más largo que {a}?",q_hl_area:"¿Más grande que {a}?",
  q_neighbor:"¿Qué país limita con…?",q_neighbor_not:"¿NO limita con…?",
  q_plates_casual:"¿De qué país es esta matrícula?",q_plates_hard:"Identificar la región — ¡sin pista!",
  q_river_real:"¿Por qué país pasa este río?",q_map_guess:"Encuentra el país en el mapa",
  fb_correct:"✓ ¡Correcto! +{pts}",fb_wrong:"✗ Incorrecto → {ans}",fb_time:"⏱ ¡Tiempo! → {ans}",
  plates_more:"+{n} más",pct_complete:"{pct}% completado",
  spotter_dup:"📋 {code} ({country}) ya coleccionado!",
  map_unavail:"Mapa no disponible",map_loading:"Cargando mapa…",
  q_subway_km:"¿Cuánto mide la red de metro … (km)?",q_subway_lines:"¿Cuántas líneas de metro tiene …?"
},
it:{
  play:"GIOCA",again:"GIOCA ANCORA",menu:"Menu principale",board:"Classifica",pass:"Passaporto",
  profile:"Profilo",stats:"Statistiche",casual:"Casual",hardcore:"Hardcore",rounds:"Round",
  btn_collect:"Colleziona",btn_back:"Torna al menu",btn_next:"Avanti →",
  btn_again:"Gioca ancora",btn_menu:"Menu principale",btn_adapt:"Adatta",
  spotter_title:"\u{1F697} Spotter di viaggio",
  spotter_hint:"Hai visto una targa? Registrala subito!",
  spotter_all:"Tutti i paesi",spotter_unknown:"Targa sconosciuta",
  spotter_not_in:"non in",spotter_but_in:"ma in",
  album_title:"\u{1F4D4} Raccolta targhe",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mappa",
  album_empty_country:"Niente da {country} ancora — usa lo Spotter!",
  album_empty:"Niente ancora raccolto!\nGioca alle targhe UE o usa lo Spotter.",
  album_codes:"codici",
  hl_higher:"⬆️ Di più / Più lungo / Più grande",hl_lower:"⬇️ Di meno / Più corto / Più piccolo",
  hl_more:"⬆️ Più abitanti",hl_less:"⬇️ Meno abitanti",
  loc_detected:"Sei in {country}",loc_adapt:"Adatta",
  q_city:"In quale paese si trova questa città?",q_flag:"Quale paese ha questa bandiera?",
  q_capital:"A quale paese appartiene questa capitale?",q_river:"In quale paese scorre questo fiume?",
  q_landmark:"In quale paese si trova questo monumento?",q_park:"In quale paese si trova questo parco nazionale?",
  q_unesco:"In quale paese si trova questo sito UNESCO?",q_citymark:"A quale città appartiene questo monumento?",
  q_subway:"In quale città si trova questa metro?",q_flagsel:"Quale bandiera appartiene a…",
  q_rcapital:"Qual è la capitale di…?",q_rcity:"Quale città si trova in…?",
  q_rriver:"Quale fiume scorre attraverso…?",q_outline:"Quale paese ha questa forma?",
  q_food:"Da quale paese viene questo piatto?",q_brand:"Da quale paese viene questo marchio?",
  q_currency:"A quale paese appartiene questa valuta?",q_curr_real:"Quale valuta ha…",
  q_pop_compare:"Più o meno abitanti?",
  q_hl_pop:"Più abitanti di {a}?",q_hl_river:"Più lungo di {a}?",q_hl_area:"Più grande di {a}?",
  q_neighbor:"Quale paese confina con…?",q_neighbor_not:"NON confina con…?",
  q_plates_casual:"Da quale paese viene questa targa?",q_plates_hard:"Identificare la regione — nessun indizio!",
  q_river_real:"Attraverso quale paese scorre questo fiume?",q_map_guess:"Trova il paese sulla mappa",
  fb_correct:"✓ Corretto! +{pts}",fb_wrong:"✗ Sbagliato → {ans}",fb_time:"⏱ Tempo! → {ans}",
  plates_more:"+{n} altri",pct_complete:"{pct}% completato",
  spotter_dup:"📋 {code} ({country}) già raccolto!",
  map_unavail:"Mappa non disponibile",map_loading:"Caricamento mappa…",
  q_subway_km:"Quanto è lungo il metrò … (km)?",q_subway_lines:"Quante linee metro ha …?"
},
nl:{
  play:"SPELEN",again:"OPNIEUW SPELEN",menu:"Hoofdmenu",board:"Ranglijst",pass:"Paspoort",
  profile:"Profiel",stats:"Statistieken",casual:"Casual",hardcore:"Hardcore",rounds:"Rondes",
  btn_collect:"Verzamelen",btn_back:"Terug naar menu",btn_next:"Volgende →",
  btn_again:"Opnieuw spelen",btn_menu:"Hoofdmenu",btn_adapt:"Aanpassen",
  spotter_title:"\u{1F697} Reisspotter",
  spotter_hint:"Kenteken gezien? Noteer het nu!",
  spotter_all:"Alle landen",spotter_unknown:"Onbekend kenteken",
  spotter_not_in:"niet in",spotter_but_in:"maar in",
  album_title:"\u{1F4D4} Kentekenalbum",album_list:"\u{1F4DD} Lijst",album_map:"\u{1F5FA} Kaart",
  album_empty_country:"Nog niets uit {country} — gebruik de Spotter!",
  album_empty:"Nog niets verzameld!\nSpeel EU-kentekens of gebruik de Spotter.",
  album_codes:"codes",
  hl_higher:"⬆️ Meer / Langer / Groter",hl_lower:"⬇️ Minder / Korter / Kleiner",
  hl_more:"⬆️ Meer inwoners",hl_less:"⬇️ Minder inwoners",
  loc_detected:"Je bent in {country}",loc_adapt:"Aanpassen",
  q_city:"In welk land ligt deze stad?",q_flag:"Welk land heeft deze vlag?",
  q_capital:"Bij welk land hoort deze hoofdstad?",q_river:"In welk land ligt deze rivier?",
  q_landmark:"In welk land staat dit monument?",q_park:"In welk land ligt dit nationaal park?",
  q_unesco:"In welk land ligt dit UNESCO-erfgoed?",q_citymark:"Bij welke stad hoort dit monument?",
  q_subway:"In welke stad is deze metro?",q_flagsel:"Welke vlag hoort bij…",
  q_rcapital:"Wat is de hoofdstad van…?",q_rcity:"Welke stad ligt in…?",
  q_rriver:"Welke rivier stroomt door…?",q_outline:"Welk land heeft deze vorm?",
  q_food:"Uit welk land komt dit gerecht?",q_brand:"Uit welk land komt dit merk?",
  q_currency:"Bij welk land hoort deze munt?",q_curr_real:"Welke munt heeft…",
  q_pop_compare:"Meer of minder inwoners?",
  q_hl_pop:"Meer inwoners dan {a}?",q_hl_river:"Langer dan {a}?",q_hl_area:"Groter dan {a}?",
  q_neighbor:"Welk land grenst aan…?",q_neighbor_not:"Grenst NIET aan…?",
  q_plates_casual:"Uit welk land komt dit kenteken?",q_plates_hard:"Identificeer de regio — geen hint!",
  q_river_real:"Door welk land stroomt deze rivier?",q_map_guess:"Vind het land op de kaart",
  fb_correct:"✓ Correct! +{pts}",fb_wrong:"✗ Fout → {ans}",fb_time:"⏱ Tijd! → {ans}",
  plates_more:"+{n} meer",pct_complete:"{pct}% voltooid",
  spotter_dup:"📋 {code} ({country}) al verzameld!",
  map_unavail:"Kaart niet beschikbaar",map_loading:"Kaart laden…",
  q_subway_km:"Hoe lang is het metronetwerk … (km)?",q_subway_lines:"Hoeveel metrolijnen heeft …?"
},
pt:{
  play:"JOGAR",again:"JOGAR NOVAMENTE",menu:"Menu principal",board:"Classificação",pass:"Passaporte",
  profile:"Perfil",stats:"Estatísticas",casual:"Casual",hardcore:"Hardcore",rounds:"Rodadas",
  btn_collect:"Coletar",btn_back:"Voltar ao menu",btn_next:"Próximo →",
  btn_again:"Jogar novamente",btn_menu:"Menu principal",btn_adapt:"Adaptar",
  spotter_title:"\u{1F697} Spotter de viagem",
  spotter_hint:"Viu uma placa? Registre agora!",
  spotter_all:"Todos os países",spotter_unknown:"Placa desconhecida",
  spotter_not_in:"não em",spotter_but_in:"mas em",
  album_title:"\u{1F4D4} Coleção de placas",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Nada de {country} ainda — use o Spotter!",
  album_empty:"Nada coletado ainda!\nJogue placas UE ou use o Spotter.",
  album_codes:"códigos",
  hl_higher:"⬆️ Mais / Mais longo / Maior",hl_lower:"⬇️ Menos / Mais curto / Menor",
  hl_more:"⬆️ Mais habitantes",hl_less:"⬇️ Menos habitantes",
  loc_detected:"Você está em {country}",loc_adapt:"Adaptar",
  q_city:"Em qual país fica esta cidade?",q_flag:"Qual país tem esta bandeira?",
  q_capital:"A qual país pertence esta capital?",q_river:"Em qual país fica este rio?",
  q_landmark:"Em qual país fica este monumento?",q_park:"Em qual país fica este parque nacional?",
  q_unesco:"Em qual país fica este sítio UNESCO?",q_citymark:"A qual cidade pertence este monumento?",
  q_subway:"Em qual cidade fica este metrô?",q_flagsel:"Qual bandeira pertence a…",
  q_rcapital:"Qual é a capital de…?",q_rcity:"Qual cidade fica em…?",
  q_rriver:"Qual rio corre por…?",q_outline:"Qual país tem esta forma?",
  q_food:"De qual país vem este prato?",q_brand:"De qual país vem esta marca?",
  q_currency:"A qual país pertence esta moeda?",q_curr_real:"Qual moeda tem…",
  q_pop_compare:"Mais ou menos habitantes?",
  q_hl_pop:"Mais habitantes que {a}?",q_hl_river:"Mais longo que {a}?",q_hl_area:"Maior que {a}?",
  q_neighbor:"Qual país faz fronteira com…?",q_neighbor_not:"NÃO faz fronteira com…?",
  q_plates_casual:"De qual país é esta placa?",q_plates_hard:"Identificar a região — sem dica!",
  q_river_real:"Por qual país corre este rio?",q_map_guess:"Encontre o país no mapa",
  fb_correct:"✓ Correto! +{pts}",fb_wrong:"✗ Errado → {ans}",fb_time:"⏱ Tempo! → {ans}",
  plates_more:"+{n} mais",pct_complete:"{pct}% completo",
  spotter_dup:"📋 {code} ({country}) já coletado!",
  map_unavail:"Mapa não disponível",map_loading:"Carregando mapa…",
  q_subway_km:"Qual o comprimento da rede de metro … (km)?",q_subway_lines:"Quantas linhas de metro tem …?"
},
ro:{
  play:"JOACĂ",again:"JOACĂ DIN NOU",menu:"Meniu principal",board:"Clasament",pass:"Pașaport",
  profile:"Profil",stats:"Statistici",casual:"Casual",hardcore:"Hardcore",rounds:"Runde",
  btn_collect:"Colectează",btn_back:"Înapoi la meniu",btn_next:"Următor →",
  btn_again:"Joacă din nou",btn_menu:"Meniu principal",btn_adapt:"Adaptează",
  spotter_title:"\u{1F697} Spotter de călătorie",
  spotter_hint:"Ai văzut o plăcuță? Înregistreaz-o acum!",
  spotter_all:"Toate țările",spotter_unknown:"Plăcuță necunoscută",
  spotter_not_in:"nu în",spotter_but_in:"dar în",
  album_title:"\u{1F4D4} Colecție de plăcuțe",album_list:"\u{1F4DD} Listă",album_map:"\u{1F5FA} Hartă",
  album_empty_country:"Nimic din {country} încă — folosește Spotter-ul!",
  album_empty:"Nimic colectat încă!\nJoacă plăcuțe UE sau folosește Spotter-ul.",
  album_codes:"coduri",
  hl_higher:"⬆️ Mai mult / Mai lung / Mai mare",hl_lower:"⬇️ Mai puțin / Mai scurt / Mai mic",
  hl_more:"⬆️ Mai mulți locuitori",hl_less:"⬇️ Mai puțini locuitori",
  loc_detected:"Ești în {country}",loc_adapt:"Adaptează",
  q_city:"În ce țară se află acest oraș?",q_flag:"Ce țară are acest steag?",
  q_capital:"Cărui țări aparține această capitală?",q_river:"În ce țară curge acest râu?",
  q_landmark:"În ce țară se află acest monument?",q_park:"În ce țară se află acest parc național?",
  q_unesco:"În ce țară se află acest sit UNESCO?",q_citymark:"Cărui oraș aparține acest monument?",
  q_subway:"În ce oraș se află acest metrou?",q_flagsel:"Ce steag aparține lui…",
  q_rcapital:"Care este capitala lui…?",q_rcity:"Ce oraș se află în…?",
  q_rriver:"Ce râu curge prin…?",q_outline:"Ce țară are această formă?",
  q_food:"Din ce țară vine acest preparat?",q_brand:"Din ce țară vine acest brand?",
  q_currency:"Cărui țări aparține această monedă?",q_curr_real:"Ce monedă are…",
  q_pop_compare:"Mai mulți sau mai puțini locuitori?",
  q_hl_pop:"Mai mulți locuitori decât {a}?",q_hl_river:"Mai lung decât {a}?",q_hl_area:"Mai mare decât {a}?",
  q_neighbor:"Ce țară se învecinează cu…?",q_neighbor_not:"NU se învecinează cu…?",
  q_plates_casual:"Din ce țară este această plăcuță?",q_plates_hard:"Identificați regiunea — fără indiciu!",
  q_river_real:"Prin ce țară curge acest râu?",q_map_guess:"Găsește țara pe hartă",
  fb_correct:"✓ Corect! +{pts}",fb_wrong:"✗ Greșit → {ans}",fb_time:"⏱ Timp! → {ans}",
  plates_more:"+{n} mai mult",pct_complete:"{pct}% complet",
  spotter_dup:"📋 {code} ({country}) deja colectat!",
  map_unavail:"Hartă indisponibilă",map_loading:"Se êncarcă harta…",
  q_subway_km:"Cât de lungă este rețeaua de metrou … (km)?",q_subway_lines:"Câte linii de metrou are …?"
},
hu:{
  play:"JÁTÉK",again:"ÚJRA JÁTSZANI",menu:"Főmenü",board:"Rangsor",pass:"Útlevél",
  profile:"Profil",stats:"Statisztikák",casual:"Könnyű",hardcore:"Nehéz",rounds:"Körök",
  btn_collect:"Gyűjt",btn_back:"Vissza a főmenübe",btn_next:"Tovább →",
  btn_again:"Újra játszani",btn_menu:"Főmenü",btn_adapt:"Módosít",
  spotter_title:"\u{1F697} Utazó Spotter",
  spotter_hint:"Rendszámot láttál? Jegyezd fel azonnal!",
  spotter_all:"Összes ország",spotter_unknown:"Ismeretlen rendszám",
  spotter_not_in:"nem szerepel",spotter_but_in:"de szerepel",
  album_title:"\u{1F4D4} Rendszám Album",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Térkép",
  album_empty_country:"Még semmi {country}-ból — használd a Spotter-t!",
  album_empty:"Még semmi összegyűjtve!\nJátssz EU rendszámokat vagy használd a Spotter-t.",
  album_codes:"kódok",
  hl_higher:"⬆️ Több / Hosszabb / Nagyobb",hl_lower:"⬇️ Kevesebb / Rövidebb / Kisebb",
  hl_more:"⬆️ Több lakos",hl_less:"⬇️ Kevesebb lakos",
  loc_detected:"Jelenleg itt tartózkodik: {country}",loc_adapt:"Módosít",
  q_city:"Melyik országban van ez a város?",q_flag:"Melyik ország zászlaja ez?",
  q_capital:"Melyik ország fővárosa ez?",q_river:"Melyik országban folyik ez a folyó?",
  q_landmark:"Melyik országban van ez az emlékmű?",q_park:"Melyik országban van ez a nemzeti park?",
  q_unesco:"Melyik országban van ez az UNESCO-helyszín?",q_citymark:"Melyik városhoz tartozik ez az emlékmű?",
  q_subway:"Melyik városban van ez a metró?",q_flagsel:"Melyik zászló tartozik…-hoz",
  q_rcapital:"Mi a fővárosa…-nak?",q_rcity:"Melyik város van…-ban?",
  q_rriver:"Melyik folyó folyik át…-on?",q_outline:"Melyik ország van ebben az alakban?",
  q_food:"Melyik országból származik ez az étel?",q_brand:"Melyik országból származik ez a márka?",
  q_currency:"Melyik ország pénzneme ez?",q_curr_real:"Melyik pénzneme van…-nak",
  q_pop_compare:"Több vagy kevesebb lakos?",
  q_hl_pop:"Több lakos, mint {a}?",q_hl_river:"Hosszabb, mint {a}?",q_hl_area:"Nagyobb, mint {a}?",
  q_neighbor:"Melyik ország határos…-val?",q_neighbor_not:"NEM határos…-val?",
  q_plates_casual:"Melyik ország rendszáma ez?",q_plates_hard:"Azonosítsa a régiót — nincs tipp!",
  q_river_real:"Melyik országon folyik át ez a folyó?",q_map_guess:"Keresse meg az országot a térképen",
  fb_correct:"✓ Helyes! +{pts}",fb_wrong:"✗ Rossz → {ans}",fb_time:"⏱ Idő! → {ans}",
  plates_more:"+{n} több",pct_complete:"{pct}% kész",
  spotter_dup:"📋 {code} ({country}) már összegyűjtve!",
  map_unavail:"Térkép nem elérhető",map_loading:"Térkép betöltése…",
  q_subway_km:"Milyen hosszú a metróhálózat … (km)?",q_subway_lines:"Hány metróvonal van …?"
},
cs:{
  play:"HRÁT",again:"HRÁT ZNOVU",menu:"Hlavní menu",board:"Žebříček",pass:"Pas",
  profile:"Profil",stats:"Statistiky",casual:"Casual",hardcore:"Hardcore",rounds:"Kola",
  btn_collect:"Sbírat",btn_back:"Zpět do menu",btn_next:"Další →",
  btn_again:"Hrát znovu",btn_menu:"Hlavní menu",btn_adapt:"Přizpůsobit",
  spotter_title:"\u{1F697} Cestovní Spotter",
  spotter_hint:"Viděl jsi SPZ? Zapiš ji hned!",
  spotter_all:"Všechny země",spotter_unknown:"Neznámá SPZ",
  spotter_not_in:"není v",spotter_but_in:"ale je v",
  album_title:"\u{1F4D4} Album SPZ",album_list:"\u{1F4DD} Seznam",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Zatím nic z {country} — použij Spotter!",
  album_empty:"Zatím nic neshromážděno!\nHraj EU SPZ nebo použij Spotter.",
  album_codes:"kódy",
  hl_higher:"⬆️ Více / Delší / Větší",hl_lower:"⬇️ Méně / Kratší / Menší",
  hl_more:"⬆️ Více obyvatel",hl_less:"⬇️ Méně obyvatel",
  loc_detected:"Jsi v {country}",loc_adapt:"Přizpůsobit",
  q_city:"Ve které zemi leží toto město?",q_flag:"Která země má tuto vlajku?",
  q_capital:"Které zemi patří toto hlavní město?",q_river:"Ve které zemi teče tato řeka?",
  q_landmark:"Ve které zemi se nachází tato památka?",q_park:"Ve které zemi se nachází tento národní park?",
  q_unesco:"Ve které zemi se nachází toto UNESCO dědictví?",q_citymark:"Ke kterému městu patří tato památka?",
  q_subway:"Ve kterém městě je toto metro?",q_flagsel:"Která vlajka patří k…",
  q_rcapital:"Jaké je hlavní město…?",q_rcity:"Které město leží v…?",
  q_rriver:"Která řeka protéká…?",q_outline:"Která země má tento tvar?",
  q_food:"Ze které země pochází toto jídlo?",q_brand:"Ze které země pochází tato značka?",
  q_currency:"Které zemi patří tato měna?",q_curr_real:"Jakou měnu má…",
  q_pop_compare:"Více nebo méně obyvatel?",
  q_hl_pop:"Více obyvatel než {a}?",q_hl_river:"Delší než {a}?",q_hl_area:"Větší než {a}?",
  q_neighbor:"Která země sousedí s…?",q_neighbor_not:"NESOUSEDÍ s…?",
  q_plates_casual:"Ze které země je tato SPZ?",q_plates_hard:"Určete region — žádná nápověda!",
  q_river_real:"Přes kterou zemi teče tato řeka?",q_map_guess:"Najdi zemi na mapě",
  fb_correct:"✓ Správně! +{pts}",fb_wrong:"✗ Chybně → {ans}",fb_time:"⏱ Čas! → {ans}",
  plates_more:"+{n} dalších",pct_complete:"{pct}% hotovo",
  spotter_dup:"📋 {code} ({country}) již sbíráno!",
  map_unavail:"Mapa není k dispozici",map_loading:"Načítání mapy…",
  q_subway_km:"Jak dlouhé je metro … (km)?",q_subway_lines:"Kolik metrových linek má …?"
},
sk:{
  play:"HRAŤ",again:"HRAŤ ZNOVA",menu:"Hlavné menu",board:"Rebríček",pass:"Pas",
  profile:"Profil",stats:"Štatistiky",casual:"Casual",hardcore:"Hardcore",rounds:"Kolá",
  btn_collect:"Zbierať",btn_back:"Späť do menu",btn_next:"Ďalej →",
  btn_again:"Hrať znova",btn_menu:"Hlavné menu",btn_adapt:"Prispôsobiť",
  spotter_title:"\u{1F697} Cestovný Spotter",
  spotter_hint:"Videl si EČV? Zaznač ju hneď!",
  spotter_all:"Všetky krajiny",spotter_unknown:"Neznáma EČV",
  spotter_not_in:"nie je v",spotter_but_in:"ale je v",
  album_title:"\u{1F4D4} Album EČV",album_list:"\u{1F4DD} Zoznam",album_map:"\u{1F5FA} Mapa",
  album_empty_country:"Zatiaľ nič z {country} — použi Spotter!",
  album_empty:"Zatiaľ nič nezbierane!\nHraj EÚ EČV alebo použi Spotter.",
  album_codes:"kódy",
  hl_higher:"⬆️ Viac / Dlhší / Väčší",hl_lower:"⬇️ Menej / Kratší / Menší",
  hl_more:"⬆️ Viac obyvateľov",hl_less:"⬇️ Menej obyvateľov",
  loc_detected:"Si v {country}",loc_adapt:"Prispôsobiť",
  q_city:"V ktorej krajine leží toto mesto?",q_flag:"Ktorá krajina má túto vlajku?",
  q_capital:"Ktorej krajine patrí toto hlavné mesto?",q_river:"V ktorej krajine tečie táto rieka?",
  q_landmark:"V ktorej krajine sa nachádza táto pamiatka?",q_park:"V ktorej krajine sa nachádza tento národný park?",
  q_unesco:"V ktorej krajine sa nachádza toto UNESCO dedičstvo?",q_citymark:"Ktorému mestu patrí táto pamiatka?",
  q_subway:"V ktorom meste je toto metro?",q_flagsel:"Ktorá vlajka patrí k…",
  q_rcapital:"Aké je hlavné mesto…?",q_rcity:"Ktoré mesto leží v…?",
  q_rriver:"Ktorá rieka preteká cez…?",q_outline:"Ktorá krajina má tento tvar?",
  q_food:"Z ktorej krajiny pochádza toto jedlo?",q_brand:"Z ktorej krajiny pochádza táto značka?",
  q_currency:"Ktorej krajine patrí táto mena?",q_curr_real:"Akú menu má…",
  q_pop_compare:"Viac alebo menej obyvateľov?",
  q_hl_pop:"Viac obyvateľov ako {a}?",q_hl_river:"Dlhší ako {a}?",q_hl_area:"Väčší ako {a}?",
  q_neighbor:"Ktorá krajina susedí s…?",q_neighbor_not:"NESUSEDÍ s…?",
  q_plates_casual:"Z ktorej krajiny je táto EČV?",q_plates_hard:"Identifikujte región — žiadna nápoveda!",
  q_river_real:"Cez ktorú krajinu tečie táto rieka?",q_map_guess:"Nájdi krajinu na mape",
  fb_correct:"✓ Správne! +{pts}",fb_wrong:"✗ Nesprávne → {ans}",fb_time:"⏱ Čas! → {ans}",
  plates_more:"+{n} ďalších",pct_complete:"{pct}% hotovo",
  spotter_dup:"📋 {code} ({country}) už zozbierané!",
  map_unavail:"Mapa nie je dostupná",map_loading:"Načítávanie mapy…",
  q_subway_km:"Aká dlhá je sieť metra … (km)?",q_subway_lines:"Koľko liniek metra má …?"
},
hr:{
  play:"IGRAJ",again:"IGRAJ PONOVO",menu:"Glavni izbornik",board:"Ljestvica",pass:"Putovnica",
  profile:"Profil",stats:"Statistike",casual:"Casual",hardcore:"Hardcore",rounds:"Runde",
  btn_collect:"Sakupi",btn_back:"Natrag na izbornik",btn_next:"Sljedeće →",
  btn_again:"Igraj ponovo",btn_menu:"Glavni izbornik",btn_adapt:"Prilagodi",
  spotter_title:"\u{1F697} Putni Spotter",
  spotter_hint:"Vidio registraciju? Zabilježi odmah!",
  spotter_all:"Sve države",spotter_unknown:"Nepoznata registracija",
  spotter_not_in:"nije u",spotter_but_in:"ali je u",
  album_title:"\u{1F4D4} Album registracija",album_list:"\u{1F4DD} Popis",album_map:"\u{1F5FA} Karta",
  album_empty_country:"Još ništa iz {country} — koristi Spotter!",
  album_empty:"Još ništa skupljeno!\nIgraj EU registracije ili koristi Spotter.",
  album_codes:"kodovi",
  hl_higher:"⬆️ Više / Duže / Veće",hl_lower:"⬇️ Manje / Kraće / Manje",
  hl_more:"⬆️ Više stanovnika",hl_less:"⬇️ Manje stanovnika",
  loc_detected:"Nalazite se u {country}",loc_adapt:"Prilagodi",
  q_city:"U kojoj se državi nalazi ovaj grad?",q_flag:"Koja država ima ovu zastavu?",
  q_capital:"Kojoj državi pripada ovaj glavni grad?",q_river:"U kojoj državi teče ova rijeka?",
  q_landmark:"U kojoj se državi nalazi ovaj spomenik?",q_park:"U kojoj se državi nalazi ovaj nacionalni park?",
  q_unesco:"U kojoj se državi nalazi ovo UNESCO nasljeđe?",q_citymark:"Kojemu gradu pripada ovaj spomenik?",
  q_subway:"U kojemu gradu je ovaj metro?",q_flagsel:"Koja zastava pripada…",
  q_rcapital:"Koji je glavni grad…?",q_rcity:"Koji grad se nalazi u…?",
  q_rriver:"Koja rijeka teče kroz…?",q_outline:"Koja država ima ovaj oblik?",
  q_food:"Iz koje države dolazi ovo jelo?",q_brand:"Iz koje države dolazi ovaj brand?",
  q_currency:"Kojoj državi pripada ova valuta?",q_curr_real:"Koju valutu ima…",
  q_pop_compare:"Više ili manje stanovnika?",
  q_hl_pop:"Više stanovnika od {a}?",q_hl_river:"Duže od {a}?",q_hl_area:"Veće od {a}?",
  q_neighbor:"Koja država graniči s…?",q_neighbor_not:"NE graniči s…?",
  q_plates_casual:"Iz koje države je ova registracija?",q_plates_hard:"Identificirajte regiju — nema naznake!",
  q_river_real:"Kroz koju državu teče ova rijeka?",q_map_guess:"Pronađi državu na karti",
  fb_correct:"✓ Točno! +{pts}",fb_wrong:"✗ Pogrešno → {ans}",fb_time:"⏱ Kraj vremena! → {ans}",
  plates_more:"+{n} više",pct_complete:"{pct}% dovršeno",
  spotter_dup:"📋 {code} ({country}) već skupljeno!",
  map_unavail:"Karta nije dostupna",map_loading:"Učitavanje karte…",
  q_subway_km:"Koliko duga je mreža metroa … (km)?",q_subway_lines:"Koliko linija metroa ima …?"
},
sl:{
  play:"IGRAJ",again:"IGRAJ ZNOVA",menu:"Glavni meni",board:"Lestvica",pass:"Potni list",
  profile:"Profil",stats:"Statistike",casual:"Casual",hardcore:"Hardcore",rounds:"Runde",
  btn_collect:"Zberi",btn_back:"Nazaj v meni",btn_next:"Naprej →",
  btn_again:"Igraj znova",btn_menu:"Glavni meni",btn_adapt:"Prilagodi",
  spotter_title:"\u{1F697} Potovalni Spotter",
  spotter_hint:"Si videl tablico? Zapiši jo takoj!",
  spotter_all:"Vse države",spotter_unknown:"Neznana tablica",
  spotter_not_in:"ni v",spotter_but_in:"ampak je v",
  album_title:"\u{1F4D4} Album tablic",album_list:"\u{1F4DD} Seznam",album_map:"\u{1F5FA} Karta",
  album_empty_country:"Še nič iz {country} — uporabi Spotter!",
  album_empty:"Še nič zbrano!\nIgraj EU tablice ali uporabi Spotter.",
  album_codes:"kode",
  hl_higher:"⬆️ Več / Daljši / Večji",hl_lower:"⬇️ Manj / Krajši / Manjši",
  hl_more:"⬆️ Več prebivalcev",hl_less:"⬇️ Manj prebivalcev",
  loc_detected:"Ste v {country}",loc_adapt:"Prilagodi",
  q_city:"V kateri državi leži to mesto?",q_flag:"Katera država ima to zastavo?",
  q_capital:"Kateri državi pripada to glavno mesto?",q_river:"V kateri državi teče ta reka?",
  q_landmark:"V kateri državi se nahaja ta znamenitost?",q_park:"V kateri državi se nahaja ta narodni park?",
  q_unesco:"V kateri državi se nahaja ta UNESCO dediščina?",q_citymark:"Kateremu mestu pripada ta znamenitost?",
  q_subway:"V katerem mestu je ta metro?",q_flagsel:"Katera zastava pripada…",
  q_rcapital:"Kakšno je glavno mesto…?",q_rcity:"Katero mesto leži v…?",
  q_rriver:"Katera reka teče skozi…?",q_outline:"Katera država ima to obliko?",
  q_food:"Iz katere države prihaja ta jed?",q_brand:"Iz katere države prihaja ta znamka?",
  q_currency:"Kateri državi pripada ta valuta?",q_curr_real:"Kakšno valuto ima…",
  q_pop_compare:"Več ali manj prebivalcev?",
  q_hl_pop:"Več prebivalcev kot {a}?",q_hl_river:"Daljši kot {a}?",q_hl_area:"Večji kot {a}?",
  q_neighbor:"Katera država meji na…?",q_neighbor_not:"NE meji na…?",
  q_plates_casual:"Iz katere države je ta tablica?",q_plates_hard:"Identificirajte regijo — brez namiga!",
  q_river_real:"Skozi katero državo teče ta reka?",q_map_guess:"Poišči državo na karti",
  fb_correct:"✓ Pravilno! +{pts}",fb_wrong:"✗ Napačno → {ans}",fb_time:"⏱ Čas! → {ans}",
  plates_more:"+{n} več",pct_complete:"{pct}% dokončano",
  spotter_dup:"📋 {code} ({country}) že zbrano!",
  map_unavail:"Karta ni na voljo",map_loading:"Nalaganje karte…",
  q_subway_km:"Kako dolgo je metrojsko omrežje … (km)?",q_subway_lines:"Koliko metrojskih linij ima …?"
},
bg:{
  play:"ИГРАЙ",again:"ИГРАЙ ОТНОВО",menu:"Главно меню",board:"Класация",pass:"Паспорт",
  profile:"Профил",stats:"Статистики",casual:"Лесен",hardcore:"Труден",rounds:"Рунди",
  btn_collect:"Събери",btn_back:"Обратно в менюто",btn_next:"Напред →",
  btn_again:"Играй отново",btn_menu:"Главно меню",btn_adapt:"Адаптирай",
  spotter_title:"\u{1F697} Пътен Спотър",
  spotter_hint:"Видял табела? Запиши я веднага!",
  spotter_all:"Всички страни",spotter_unknown:"Непозната табела",
  spotter_not_in:"не е в",spotter_but_in:"но е в",
  album_title:"\u{1F4D4} Албум с табели",album_list:"\u{1F4DD} Списък",album_map:"\u{1F5FA} Карта",
  album_empty_country:"Нищо от {country} все още — използвай Спотъра!",
  album_empty:"Все още нищо събрано!\nИграй ЕС табели или използвай Спотъра.",
  album_codes:"кодове",
  hl_higher:"⬆️ Повече / По-дълго / По-голямо",hl_lower:"⬇️ По-малко / По-кратко / По-малко",
  hl_more:"⬆️ Повече жители",hl_less:"⬇️ По-малко жители",
  loc_detected:"Намирате се в {country}",loc_adapt:"Адаптирай",
  q_city:"В коя страна се намира този град?",q_flag:"Коя страна има това знаме?",
  q_capital:"На коя страна принадлежи тази столица?",q_river:"В коя страна тече тази река?",
  q_landmark:"В коя страна се намира тази забележителност?",q_park:"В коя страна се намира този национален парк?",
  q_unesco:"В коя страна се намира това ЮНЕСКО наследство?",q_citymark:"На кой град принадлежи тази забележителност?",
  q_subway:"В кой град е това метро?",q_flagsel:"Кое знаме принадлежи на…",
  q_rcapital:"Каква е столицата на…?",q_rcity:"Кой град се намира в…?",
  q_rriver:"Коя река тече през…?",q_outline:"Коя страна има тази форма?",
  q_food:"От коя страна идва това ястие?",q_brand:"От коя страна идва тази марка?",
  q_currency:"На коя страна принадлежи тази валута?",q_curr_real:"Каква валута има…",
  q_pop_compare:"Повече или по-малко жители?",
  q_hl_pop:"Повече жители от {a}?",q_hl_river:"По-дълга от {a}?",q_hl_area:"По-голяма от {a}?",
  q_neighbor:"Коя страна граничи с…?",q_neighbor_not:"НЕ граничи с…?",
  q_plates_casual:"От коя страна е тази табела?",q_plates_hard:"Идентифицирайте региона — без подсказка!",
  q_river_real:"През коя страна тече тази река?",q_map_guess:"Намери страната на картата",
  fb_correct:"✓ Правилно! +{pts}",fb_wrong:"✗ Грешно → {ans}",fb_time:"⏱ Времето изтече! → {ans}",
  plates_more:"+{n} oщe",pct_complete:"{pct}% завършено",
  spotter_dup:"📋 {code} ({country}) вечe събрано!",
  map_unavail:"Картата не е достъпна",map_loading:"Зареждане на картата…",
  q_subway_km:"Колко дълга е метрото … (km)?",q_subway_lines:"Колко метролинии има …?"
},
el:{
  play:"ΠΑΙΞΕ",again:"ΠΑΙΞΕ ΞΑΝΑ",menu:"Κύριο μενού",board:"Κατάταξη",pass:"Διαβατήριο",
  profile:"Προφίλ",stats:"Στατιστικά",casual:"Εύκολο",hardcore:"Δύσκολο",rounds:"Γύροι",
  btn_collect:"Συλλογή",btn_back:"Πίσω στο μενού",btn_next:"Επόμενο →",
  btn_again:"Παίξε ξανά",btn_menu:"Κύριο μενού",btn_adapt:"Προσαρμογή",
  spotter_title:"\u{1F697} Spotter Ταξιδιού",
  spotter_hint:"Είδες πινακίδα; Καταχώρησέ την τώρα!",
  spotter_all:"Όλες οι χώρες",spotter_unknown:"Άγνωστη πινακίδα",
  spotter_not_in:"δεν είναι σε",spotter_but_in:"αλλά σε",
  album_title:"\u{1F4D4} Συλλογή πινακίδων",album_list:"\u{1F4DD} Λίστα",album_map:"\u{1F5FA} Χάρτης",
  album_empty_country:"Τίποτα από {country} ακόμα — χρησιμοποίησε το Spotter!",
  album_empty:"Δεν έχεις συλλέξει τίποτα ακόμα!\nΠαίξε πινακίδες ΕΕ ή χρησιμοποίησε το Spotter.",
  album_codes:"κωδικοί",
  hl_higher:"⬆️ Περισσότερο / Μεγαλύτερο / Μεγαλύτερο",hl_lower:"⬇️ Λιγότερο / Μικρότερο / Μικρότερο",
  hl_more:"⬆️ Περισσότεροι κάτοικοι",hl_less:"⬇️ Λιγότεροι κάτοικοι",
  loc_detected:"Βρίσκεστε στην/στο {country}",loc_adapt:"Προσαρμογή",
  q_city:"Σε ποια χώρα βρίσκεται αυτή η πόλη;",q_flag:"Ποια χώρα έχει αυτή τη σημαία;",
  q_capital:"Σε ποια χώρα ανήκει αυτή η πρωτεύουσα;",q_river:"Σε ποια χώρα βρίσκεται αυτό το ποτάμι;",
  q_landmark:"Σε ποια χώρα βρίσκεται αυτό το μνημείο;",q_park:"Σε ποια χώρα βρίσκεται αυτό το εθνικό πάρκο;",
  q_unesco:"Σε ποια χώρα βρίσκεται αυτό το μνημείο UNESCO;",q_citymark:"Σε ποια πόλη ανήκει αυτό το μνημείο;",
  q_subway:"Σε ποια πόλη βρίσκεται αυτό το μετρό;",q_flagsel:"Ποια σημαία ανήκει στη…",
  q_rcapital:"Ποια είναι η πρωτεύουσα της/του…;",q_rcity:"Ποια πόλη βρίσκεται στη/στο…;",
  q_rriver:"Ποιο ποτάμι διαρρέει τη/το…;",q_outline:"Ποια χώρα έχει αυτό το σχήμα;",
  q_food:"Από ποια χώρα προέρχεται αυτό το πιάτο;",q_brand:"Από ποια χώρα προέρχεται αυτή η μάρκα;",
  q_currency:"Σε ποια χώρα ανήκει αυτό το νόμισμα;",q_curr_real:"Ποιο νόμισμα έχει η/ο…",
  q_pop_compare:"Περισσότεροι ή λιγότεροι κάτοικοι;",
  q_hl_pop:"Περισσότεροι κάτοικοι από τη/τον {a};",q_hl_river:"Μεγαλύτερο από τη/τον {a};",q_hl_area:"Μεγαλύτερη από τη/τον {a};",
  q_neighbor:"Ποια χώρα συνορεύει με τη/το…;",q_neighbor_not:"ΔΕΝ συνορεύει με τη/το…;",
  q_plates_casual:"Από ποια χώρα είναι αυτή η πινακίδα;",q_plates_hard:"Αναγνωρίστε την περιοχή — χωρίς υπόδειξη!",
  q_river_real:"Μέσα από ποια χώρα διαρρέει αυτό το ποτάμι;",q_map_guess:"Βρες τη χώρα στον χάρτη",
  fb_correct:"✓ Σωστό! +{pts}",fb_wrong:"✗ Λάθος → {ans}",fb_time:"⏱ Τέλος χρόνου! → {ans}",
  plates_more:"+{n} ακόμα",pct_complete:"{pct}% ολοκληρώθηκε",
  spotter_dup:"📋 {code} ({country}) ήδη συλλέχθηκε!",
  map_unavail:"Χάρτης μη διαθέσιμος",map_loading:"Φόρτωση χάρτη…",
  q_subway_km:"Πόσο μακρύ είναι το μετρό … (km)?",q_subway_lines:"Πόσες γραμμές μετρό έχει …?"
},
da:{
  play:"SPIL",again:"SPIL IGEN",menu:"Hovedmenu",board:"Rangliste",pass:"Pas",
  profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Runder",
  btn_collect:"Samle",btn_back:"Tilbage til menu",btn_next:"Næste →",
  btn_again:"Spil igen",btn_menu:"Hovedmenu",btn_adapt:"Tilpas",
  spotter_title:"\u{1F697} Rejse-Spotter",
  spotter_hint:"Set en nummerplade? Notér den nu!",
  spotter_all:"Alle lande",spotter_unknown:"Ukendt nummerplade",
  spotter_not_in:"ikke i",spotter_but_in:"men i",
  album_title:"\u{1F4D4} Nummerplade-album",album_list:"\u{1F4DD} Liste",album_map:"\u{1F5FA} Kort",
  album_empty_country:"Intet fra {country} endnu — brug Spotter!",
  album_empty:"Intet indsamlet endnu!\nSpil EU-nummerplader eller brug Spotter.",
  album_codes:"koder",
  hl_higher:"⬆️ Mere / Længere / Større",hl_lower:"⬇️ Mindre / Kortere / Mindre",
  hl_more:"⬆️ Flere indbyggere",hl_less:"⬇️ Færre indbyggere",
  loc_detected:"Du er i {country}",loc_adapt:"Tilpas",
  q_city:"I hvilket land ligger denne by?",q_flag:"Hvilket land har dette flag?",
  q_capital:"Hvilke land tilhører denne hovedstad?",q_river:"I hvilket land løber denne flod?",
  q_landmark:"I hvilket land ligger dette monument?",q_park:"I hvilket land ligger denne nationalpark?",
  q_unesco:"I hvilket land ligger dette UNESCO-sted?",q_citymark:"Hvilken by tilhører dette monument?",
  q_subway:"I hvilken by er denne metro?",q_flagsel:"Hvilket flag tilhører…",
  q_rcapital:"Hvad er hovedstaden i…?",q_rcity:"Hvilken by ligger i…?",
  q_rriver:"Hvilken flod løber gennem…?",q_outline:"Hvilket land har denne form?",
  q_food:"Fra hvilket land kommer denne ret?",q_brand:"Fra hvilket land kommer dette mærke?",
  q_currency:"Hvilket land tilhører denne valuta?",q_curr_real:"Hvilken valuta har…",
  q_pop_compare:"Flere eller færre indbyggere?",
  q_hl_pop:"Flere indbyggere end {a}?",q_hl_river:"Længere end {a}?",q_hl_area:"Større end {a}?",
  q_neighbor:"Hvilket land grænser op til…?",q_neighbor_not:"Grænser IKKE op til…?",
  q_plates_casual:"Fra hvilket land er denne nummerplade?",q_plates_hard:"Identificér regionen — ingen hint!",
  q_river_real:"Gennem hvilket land løber denne flod?",q_map_guess:"Find landet på kortet",
  fb_correct:"✓ Korrekt! +{pts}",fb_wrong:"✗ Forkert → {ans}",fb_time:"⏱ Tid! → {ans}",
  plates_more:"+{n} mere",pct_complete:"{pct}% fuldført",
  spotter_dup:"📋 {code} ({country}) allerede indsamlet!",
  map_unavail:"Kort ikke tilgængeligt",map_loading:"Indlæser kort…",
  q_subway_km:"Hvor lang er metronetværket … (km)?",q_subway_lines:"Hvor mange metrolinjer har …?"
},
sv:{
  play:"SPELA",again:"SPELA IGEN",menu:"Huvudmeny",board:"Rankningslista",pass:"Pass",
  profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Rundor",
  btn_collect:"Samla",btn_back:"Tillbaka till menyn",btn_next:"Nästa →",
  btn_again:"Spela igen",btn_menu:"Huvudmeny",btn_adapt:"Anpassa",
  spotter_title:"\u{1F697} Resespotter",
  spotter_hint:"Sett en skylt? Notera den nu!",
  spotter_all:"Alla länder",spotter_unknown:"Okänd skylt",
  spotter_not_in:"inte i",spotter_but_in:"men i",
  album_title:"\u{1F4D4} Skyltalbum",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Karta",
  album_empty_country:"Inget från {country} ännu — använd Spotter!",
  album_empty:"Inget samlat ännu!\nSpela EU-skyltar eller använd Spotter.",
  album_codes:"koder",
  hl_higher:"⬆️ Mer / Längre / Större",hl_lower:"⬇️ Mindre / Kortare / Mindre",
  hl_more:"⬆️ Fler invånare",hl_less:"⬇️ Färre invånare",
  loc_detected:"Du är i {country}",loc_adapt:"Anpassa",
  q_city:"I vilket land ligger den här staden?",q_flag:"Vilket land har den här flaggan?",
  q_capital:"Vilket land tillhör den här huvudstaden?",q_river:"I vilket land flödar den här floden?",
  q_landmark:"I vilket land finns det här monumentet?",q_park:"I vilket land finns den här nationalparken?",
  q_unesco:"I vilket land finns det här UNESCO-arvet?",q_citymark:"Vilken stad tillhör det här monumentet?",
  q_subway:"I vilken stad finns den här tunnelbanan?",q_flagsel:"Vilken flagga tillhör…",
  q_rcapital:"Vad är huvudstaden i…?",q_rcity:"Vilken stad finns i…?",
  q_rriver:"Vilken flod rinner genom…?",q_outline:"Vilket land har den här formen?",
  q_food:"Från vilket land kommer den här rätten?",q_brand:"Från vilket land kommer det här märket?",
  q_currency:"Vilket land tillhör den här valutan?",q_curr_real:"Vilken valuta har…",
  q_pop_compare:"Fler eller färre invånare?",
  q_hl_pop:"Fler invånare än {a}?",q_hl_river:"Längre än {a}?",q_hl_area:"Större än {a}?",
  q_neighbor:"Vilket land gränsar till…?",q_neighbor_not:"Gränsar INTE till…?",
  q_plates_casual:"Från vilket land är den här skylten?",q_plates_hard:"Identifiera regionen — inget tips!",
  q_river_real:"Genom vilket land flödar den här floden?",q_map_guess:"Hitta landet på kartan",
  fb_correct:"✓ Rätt! +{pts}",fb_wrong:"✗ Fel → {ans}",fb_time:"⏱ Tid! → {ans}",
  plates_more:"+{n} till",pct_complete:"{pct}% klart",
  spotter_dup:"📋 {code} ({country}) redan insamlat!",
  map_unavail:"Karta ej tillgänglig",map_loading:"Laddar karta…",
  q_subway_km:"Hur lång är tunnelbanenätet … (km)?",q_subway_lines:"Hur många tunnelbanelinjer har …?"
},
fi:{
  play:"PELAA",again:"PELAA UUDELLEEN",menu:"Päävalikko",board:"Tulostaulukko",pass:"Passi",
  profile:"Profiili",stats:"Tilastot",casual:"Helppo",hardcore:"Vaikea",rounds:"Kierrokset",
  btn_collect:"Kerää",btn_back:"Takaisin päävalikkoon",btn_next:"Seuraava →",
  btn_again:"Pelaa uudelleen",btn_menu:"Päävalikko",btn_adapt:"Muokkaa",
  spotter_title:"\u{1F697} Matkaspotter",
  spotter_hint:"Näitkö rekisterikilven? Kirjaa se heti!",
  spotter_all:"Kaikki maat",spotter_unknown:"Tuntematon rekisterikilpi",
  spotter_not_in:"ei kohteessa",spotter_but_in:"mutta kohteessa",
  album_title:"\u{1F4D4} Rekisterikilpialbumi",album_list:"\u{1F4DD} Luettelo",album_map:"\u{1F5FA} Kartta",
  album_empty_country:"Ei vielä mitään kohteesta {country} — käytä Spotteria!",
  album_empty:"Ei vielä kerätty mitään!\nPelaa EU-rekisterikilpiä tai käytä Spotteria.",
  album_codes:"koodit",
  hl_higher:"⬆️ Enemmän / Pidempi / Suurempi",hl_lower:"⬇️ Vähemmän / Lyhyempi / Pienempi",
  hl_more:"⬆️ Enemmän asukkaita",hl_less:"⬇️ Vähemmän asukkaita",
  loc_detected:"Olet kohteessa {country}",loc_adapt:"Muokkaa",
  q_city:"Missä maassa tämä kaupunki sijaitsee?",q_flag:"Minkä maan tämä lippu on?",
  q_capital:"Mille maalle tämä pääkaupunki kuuluu?",q_river:"Missä maassa tämä joki sijaitsee?",
  q_landmark:"Missä maassa tämä nähtävyys sijaitsee?",q_park:"Missä maassa tämä kansallispuisto sijaitsee?",
  q_unesco:"Missä maassa tämä UNESCO-kohde sijaitsee?",q_citymark:"Mille kaupungille tämä nähtävyys kuuluu?",
  q_subway:"Missä kaupungissa tämä metro on?",q_flagsel:"Mikä lippu kuuluu…",
  q_rcapital:"Mikä on… pääkaupunki?",q_rcity:"Mikä kaupunki sijaitsee…?",
  q_rriver:"Mikä joki virtaa läpi…?",q_outline:"Minkä maan muoto tämä on?",
  q_food:"Mistä maasta tämä ruoka tulee?",q_brand:"Mistä maasta tämä merkki tulee?",
  q_currency:"Minkä maan valuutta tämä on?",q_curr_real:"Mikä valuutta on…",
  q_pop_compare:"Enemmän vai vähemmän asukkaita?",
  q_hl_pop:"Enemmän asukkaita kuin {a}?",q_hl_river:"Pidempi kuin {a}?",q_hl_area:"Suurempi kuin {a}?",
  q_neighbor:"Mikä maa rajoittuu…?",q_neighbor_not:"EI rajoitu…?",
  q_plates_casual:"Minkä maan rekisterikilpi tämä on?",q_plates_hard:"Tunnista alue — ei vihjettä!",
  q_river_real:"Minkä maan läpi tämä joki virtaa?",q_map_guess:"Etsi maa kartalta",
  fb_correct:"✓ Oikein! +{pts}",fb_wrong:"✗ Väärin → {ans}",fb_time:"⏱ Aika! → {ans}",
  plates_more:"+{n} lisää",pct_complete:"{pct}% valmis",
  spotter_dup:"📋 {code} ({country}) jo kerätty!",
  map_unavail:"Kartta ei saatavilla",map_loading:"Ladataan karttaa…",
  q_subway_km:"Kuinka pitkä on metroverkosto … (km)?",q_subway_lines:"Kuinka monta metrolinjaa on …?"
},
et:{
  play:"MÄNGI",again:"MÄNGI UUESTI",menu:"Peamenüü",board:"Edetabel",pass:"Pass",
  profile:"Profiil",stats:"Statistika",casual:"Lihtne",hardcore:"Raske",rounds:"Voorud",
  btn_collect:"Kogu",btn_back:"Tagasi menüüsse",btn_next:"Järgmine →",
  btn_again:"Mängi uuesti",btn_menu:"Peamenüü",btn_adapt:"Kohanda",
  spotter_title:"\u{1F697} Reisispotter",
  spotter_hint:"Nägid numbrimärki? Kirjuta kohe üles!",
  spotter_all:"Kõik riigid",spotter_unknown:"Tundmatu numbrimärk",
  spotter_not_in:"ei ole",spotter_but_in:"aga on",
  album_title:"\u{1F4D4} Numbrimärkide album",album_list:"\u{1F4DD} Nimekiri",album_map:"\u{1F5FA} Kaart",
  album_empty_country:"Veel midagi {country} — kasuta Spotterit!",
  album_empty:"Veel midagi kogutud!\nMängi EL-i numbrimärke või kasuta Spotterit.",
  album_codes:"koodid",
  hl_higher:"⬆️ Rohkem / Pikem / Suurem",hl_lower:"⬇️ Vähem / Lühem / Väiksem",
  hl_more:"⬆️ Rohkem elanikke",hl_less:"⬇️ Vähem elanikke",
  loc_detected:"Oled {country}",loc_adapt:"Kohanda",
  q_city:"Millises riigis see linn asub?",q_flag:"Millise riigi lipp see on?",
  q_capital:"Millisele riigile see pealinn kuulub?",q_river:"Millises riigis see jõgi voolab?",
  q_landmark:"Millises riigis see vaatamisväärsus asub?",q_park:"Millises riigis see rahvuspark asub?",
  q_unesco:"Millises riigis see UNESCO objekt asub?",q_citymark:"Millisele linnale see vaatamisväärsus kuulub?",
  q_subway:"Millises linnas see metroo on?",q_flagsel:"Milline lipp kuulub…",
  q_rcapital:"Mis on… pealinn?",q_rcity:"Milline linn asub…?",
  q_rriver:"Milline jõgi voolab läbi…?",q_outline:"Millisel riigil on see kuju?",
  q_food:"Millisest riigist see roog pärineb?",q_brand:"Millisest riigist see bränd pärineb?",
  q_currency:"Millisele riigile see valuuta kuulub?",q_curr_real:"Mis valuuta on…",
  q_pop_compare:"Rohkem või vähem elanikke?",
  q_hl_pop:"Rohkem elanikke kui {a}?",q_hl_river:"Pikem kui {a}?",q_hl_area:"Suurem kui {a}?",
  q_neighbor:"Milline riik piirneb…?",q_neighbor_not:"EI piirne…?",
  q_plates_casual:"Millisest riigist see numbrimärk on?",q_plates_hard:"Tuvasta piirkond — vihjeta!",
  q_river_real:"Läbi millise riigi see jõgi voolab?",q_map_guess:"Leia riik kaardilt",
  fb_correct:"✓ Õige! +{pts}",fb_wrong:"✗ Vale → {ans}",fb_time:"⏱ Aeg! → {ans}",
  plates_more:"+{n} veel",pct_complete:"{pct}% täidetud",
  spotter_dup:"📋 {code} ({country}) juba kogutud!",
  map_unavail:"Kaart pole saadaval",map_loading:"Kaardi laadimine…",
  q_subway_km:"Kui pikk on metroovõrk … (km)?",q_subway_lines:"Kui palju metroliine on …?"
},
lv:{
  play:"SPĒLĒT",again:"SPĒLĒT VĒLREIZ",menu:"Galvenā izvēlne",board:"Vērtējums",pass:"Pase",
  profile:"Profils",stats:"Statistika",casual:"Viegls",hardcore:"Grūts",rounds:"Kārtas",
  btn_collect:"Savākt",btn_back:"Atpakaļ uz izvēlni",btn_next:"Tālāk →",
  btn_again:"Spēlēt vēlreiz",btn_menu:"Galvenā izvēlne",btn_adapt:"Pielāgot",
  spotter_title:"\u{1F697} Ceļojuma Spotter",
  spotter_hint:"Redzēji numura zīmi? Reģistrē to tagad!",
  spotter_all:"Visas valstis",spotter_unknown:"Nezināma numura zīme",
  spotter_not_in:"nav",spotter_but_in:"bet ir",
  album_title:"\u{1F4D4} Numuru zīmju albums",album_list:"\u{1F4DD} Saraksts",album_map:"\u{1F5FA} Karte",
  album_empty_country:"Vēl nekas no {country} — izmanto Spotter!",
  album_empty:"Vēl nekas savākts!\nSpēlē ES numura zīmes vai izmanto Spotter.",
  album_codes:"kodi",
  hl_higher:"⬆️ Vairāk / Garāks / Lielāks",hl_lower:"⬇️ Mazāk / Īsāks / Mazāks",
  hl_more:"⬆️ Vairāk iedzīvotāju",hl_less:"⬇️ Mazāk iedzīvotāju",
  loc_detected:"Atrodaties {country}",loc_adapt:"Pielāgot",
  q_city:"Kurā valstī atrodas šī pilsēta?",q_flag:"Kuras valsts šis karogs?",
  q_capital:"Kurai valstij pieder šī galvaspilsēta?",q_river:"Kurā valstī tek šī upe?",
  q_landmark:"Kurā valstī atrodas šis piemineklis?",q_park:"Kurā valstī atrodas šis nacionālais parks?",
  q_unesco:"Kurā valstī atrodas šis UNESCO mantojums?",q_citymark:"Kurai pilsētai pieder šis piemineklis?",
  q_subway:"Kurā pilsētā atrodas šis metro?",q_flagsel:"Kurš karogs pieder…",
  q_rcapital:"Kāda ir… galvaspilsēta?",q_rcity:"Kurā pilsētā atrodas…?",
  q_rriver:"Kura upe tek caur…?",q_outline:"Kurai valstij ir šāda forma?",
  q_food:"No kuras valsts nāk šis ēdiens?",q_brand:"No kuras valsts nāk šis zīmols?",
  q_currency:"Kurai valstij pieder šī valūta?",q_curr_real:"Kāda valūta ir…",
  q_pop_compare:"Vairāk vai mazāk iedzīvotāju?",
  q_hl_pop:"Vairāk iedzīvotāju nekā {a}?",q_hl_river:"Garāka nekā {a}?",q_hl_area:"Lielāka nekā {a}?",
  q_neighbor:"Kura valsts robežojas ar…?",q_neighbor_not:"NAV robežas ar…?",
  q_plates_casual:"No kuras valsts ir šī numura zīme?",q_plates_hard:"Identificēt reģionu — bez padoma!",
  q_river_real:"Caur kuru valsti tek šī upe?",q_map_guess:"Atrodi valsti kartē",
  fb_correct:"✓ Pareizi! +{pts}",fb_wrong:"✗ Nepareizi → {ans}",fb_time:"⏱ Laiks beidzies! → {ans}",
  plates_more:"+{n} vairāk",pct_complete:"{pct}% pabeigts",
  spotter_dup:"📋 {code} ({country}) jau savākts!",
  map_unavail:"Karte nav pieejama",map_loading:"Karte ielādē…",
  q_subway_km:"Cik garš ir metro tīkls … (km)?",q_subway_lines:"Cik metro līniju ir …?"
},
lt:{
  play:"ŽAISTI",again:"ŽAISTI IŠ NAUJO",menu:"Pagrindinis meniu",board:"Reitingas",pass:"Pasas",
  profile:"Profilis",stats:"Statistika",casual:"Lengvas",hardcore:"Sunkus",rounds:"Raundai",
  btn_collect:"Rinkti",btn_back:"Atgal į meniu",btn_next:"Kitas →",
  btn_again:"Žaisti iš naujo",btn_menu:"Pagrindinis meniu",btn_adapt:"Pritaikyti",
  spotter_title:"\u{1F697} Kelionės Spotter",
  spotter_hint:"Matei numerį? Užrašyk dabar!",
  spotter_all:"Visos šalys",spotter_unknown:"Nežinomas numeris",
  spotter_not_in:"nėra",spotter_but_in:"bet yra",
  album_title:"\u{1F4D4} Numerių albumas",album_list:"\u{1F4DD} Sąrašas",album_map:"\u{1F5FA} Žemėlapis",
  album_empty_country:"Dar nieko iš {country} — naudok Spotter!",
  album_empty:"Dar nieko surinkta!\nŽaisk ES numerius arba naudok Spotter.",
  album_codes:"kodai",
  hl_higher:"⬆️ Daugiau / Ilgesnis / Didesnis",hl_lower:"⬇️ Mažiau / Trumpesnis / Mažesnis",
  hl_more:"⬆️ Daugiau gyventojų",hl_less:"⬇️ Mažiau gyventojų",
  loc_detected:"Esate {country}",loc_adapt:"Pritaikyti",
  q_city:"Kurioje šalyje yra šis miestas?",q_flag:"Kurios šalies ši vėliava?",
  q_capital:"Kuriai šaliai priklauso ši sostinė?",q_river:"Kurioje šalyje teka ši upė?",
  q_landmark:"Kurioje šalyje yra šis paminklas?",q_park:"Kurioje šalyje yra šis nacionalinis parkas?",
  q_unesco:"Kurioje šalyje yra šis UNESCO paveldas?",q_citymark:"Kuriam miestui priklauso šis paminklas?",
  q_subway:"Kuriame mieste yra šis metro?",q_flagsel:"Kuri vėliava priklauso…",
  q_rcapital:"Kokia yra… sostinė?",q_rcity:"Koks miestas yra…?",
  q_rriver:"Kuri upė teka per…?",q_outline:"Kuri šalis turi šią formą?",
  q_food:"Iš kurios šalies yra šis patiekalas?",q_brand:"Iš kurios šalies yra šis prekės ženklas?",
  q_currency:"Kuriai šaliai priklauso ši valiuta?",q_curr_real:"Kokia valiuta yra…",
  q_pop_compare:"Daugiau ar mažiau gyventojų?",
  q_hl_pop:"Daugiau gyventojų nei {a}?",q_hl_river:"Ilgesnis nei {a}?",q_hl_area:"Didesnis nei {a}?",
  q_neighbor:"Kuri šalis ribojasi su…?",q_neighbor_not:"NERIBOJASI su…?",
  q_plates_casual:"Iš kurios šalies yra šis numeris?",q_plates_hard:"Nustatyti regioną — be užuominos!",
  q_river_real:"Per kurią šalį teka ši upė?",q_map_guess:"Rask šalį žemėlapyje",
  fb_correct:"✓ Teisingai! +{pts}",fb_wrong:"✗ Neteisingai → {ans}",fb_time:"⏱ Laikas! → {ans}",
  plates_more:"+{n} daugiau",pct_complete:"{pct}% baigta",
  spotter_dup:"📋 {code} ({country}) jau surinkta!",
  map_unavail:"Žemėlapis neprieinamas",map_loading:"Kraunamas žemėlapis…",
  q_subway_km:"Kiek ilgas metro tinklas … (km)?",q_subway_lines:"Kiek metro linijų yra …?"
},
mt:{
  play:"ILGĦAB",again:"ILGĦAB MILL-ĠDID",menu:"Menu Prinċipali",board:"Klassifika",pass:"Passaport",
  profile:"Profil",stats:"Statistiċi",casual:"Casual",hardcore:"Hardcore",rounds:"Rawnd",
  btn_collect:"Iġbor",btn_back:"Lura għall-menu",btn_next:"Li Jmiss →",
  btn_again:"Ilgħab mill-ġdid",btn_menu:"Menu Prinċipali",btn_adapt:"Adatta",
  spotter_title:"\u{1F697} Spotter tal-Vjaġġ",
  spotter_hint:"Rajt pjanċa? Irreġistraha issa!",
  spotter_all:"Pajjiżi kollha",spotter_unknown:"Pjanċa mhux magħrufa",
  spotter_not_in:"mhux fi",spotter_but_in:"imma fi",
  album_title:"\u{1F4D4} Kollezzjoni tal-Pjanċi",album_list:"\u{1F4DD} Lista",album_map:"\u{1F5FA} Mappa",
  album_empty_country:"Xejn minn {country} s'issa — uża s-Spotter!",
  album_empty:"Xejn miġbur s'issa!\nIlgħab il-pjanċi tal-UE jew uża s-Spotter.",
  album_codes:"kodiċi",
  hl_higher:"⬆️ Aktar / Itwal / Akbar",hl_lower:"⬇️ Inqas / Iqsar / Iżgħar",
  hl_more:"⬆️ Aktar abitanti",hl_less:"⬇️ Inqas abitanti",
  loc_detected:"Qiegħed fi {country}",loc_adapt:"Adatta",
  q_city:"F'liema pajjiż tinsab din il-belt?",q_flag:"Liema pajjiż għandu din il-bandiera?",
  q_capital:"Lil liema pajjiż tappartjeni din il-kapitali?",q_river:"F'liema pajjiż jgħaddi dan ix-xmara?",
  q_landmark:"F'liema pajjiż tinsab din il-wieqfa?",q_park:"F'liema pajjiż jinsab dan il-park nazzjonali?",
  q_unesco:"F'liema pajjiż jinsab dan is-sit UNESCO?",q_citymark:"Lil liema belt tappartjeni din il-wieqfa?",
  q_subway:"F'liema belt jinsab dan il-metro?",q_flagsel:"Liema bandiera tappartjeni lil…",
  q_rcapital:"X'inhi l-kapitali ta'…?",q_rcity:"Liema belt tinsab fi…?",
  q_rriver:"Liema xmara tgħaddi minn…?",q_outline:"Liema pajjiż għandu din il-forma?",
  q_food:"Minn liema pajjiż ġej dan l-ikel?",q_brand:"Minn liema pajjiż ġej dan il-brand?",
  q_currency:"Lil liema pajjiż tappartjeni din il-munita?",q_curr_real:"X'munita għandu…",
  q_pop_compare:"Aktar jew inqas abitanti?",
  q_hl_pop:"Aktar abitanti minn {a}?",q_hl_river:"Itwal minn {a}?",q_hl_area:"Akbar minn {a}?",
  q_neighbor:"Liema pajjiż jibbordjja ma'…?",q_neighbor_not:"MA jibbordjjax ma'…?",
  q_plates_casual:"Minn liema pajjiż hija din il-pjanċa?",q_plates_hard:"Identifika r-reġjun — l-ebda indikazzjoni!",
  q_river_real:"Minn liema pajjiż jgħaddi dan ix-xmara?",q_map_guess:"Sib il-pajjiż fuq il-mappa",
  fb_correct:"✓ Korretti! +{pts}",fb_wrong:"✗ Ħażin → {ans}",fb_time:"⏱ Ħin! → {ans}",
  plates_more:"+{n} aktar",pct_complete:"{pct}% lest",
  spotter_dup:"📋 {code} ({country}) diġà miġbur!",
  map_unavail:"Mappa mhux disponibbli",map_loading:"Qed jġħabbi l-mappa…",
  q_subway_km:"Kemm hi twila n-netwerk tal-metro … (km)?",q_subway_lines:"Kemm għandha linji tal-metro …?"
},
ga:{
  play:"IMIR",again:"IMIR ARÍS",menu:"Príomh-roghchlár",board:"Clár na mBuaiteoirí",pass:"Pas",
  profile:"Próifíl",stats:"Staitisticí",casual:"Éasca",hardcore:"Deacair",rounds:"Babhtaí",
  btn_collect:"Bailigh",btn_back:"Ar ais go dtí an roghchlár",btn_next:"Ar Aghaidh →",
  btn_again:"Imir arís",btn_menu:"Príomh-roghchlár",btn_adapt:"Oiriúnaigh",
  spotter_title:"\u{1F697} Spotter Taistil",
  spotter_hint:"Chonaic tú pláta? Taifeadaigh anois é!",
  spotter_all:"Gach tír",spotter_unknown:"Pláta anaithnid",
  spotter_not_in:"níl i",spotter_but_in:"ach tá i",
  album_title:"\u{1F4D4} Cnuasach Pláta",album_list:"\u{1F4DD} Liosta",album_map:"\u{1F5FA} Léarscáil",
  album_empty_country:"Fós aon rud ó {country} — úsáid an Spotter!",
  album_empty:"Fós aon rud bailithe!\nImir pláta AE nó úsáid an Spotter.",
  album_codes:"cóid",
  hl_higher:"⬆️ Níos mó / Níos faide / Níos mó",hl_lower:"⬇️ Níos lú / Níos giorra / Níos lú",
  hl_more:"⬆️ Níos mó cónaitheoirí",hl_less:"⬇️ Níos lú cónaitheoirí",
  loc_detected:"Tá tú i {country}",loc_adapt:"Oiriúnaigh",
  q_city:"Cén tír ina bhfuil an chathair seo?",q_flag:"Cén tír a bhfuil an bhratach seo aige?",
  q_capital:"Cén tír ar leis an phríomhchathair seo?",q_river:"Cén tír ina ritheann an abhainn seo?",
  q_landmark:"Cén tír ina bhfuil an séadchomhartha seo?",q_park:"Cén tír ina bhfuil an páirc náisiúnta seo?",
  q_unesco:"Cén tír ina bhfuil an suíomh UNESCO seo?",q_citymark:"Cén chathair ar leis an séadchomhartha seo?",
  q_subway:"Cén chathair ina bhfuil an meitreal seo?",q_flagsel:"Cén bhratach a bhaineann le…",
  q_rcapital:"Cad is príomhchathair de…?",q_rcity:"Cén chathair atá i…?",
  q_rriver:"Cén abhainn a ritheann trí…?",q_outline:"Cén tír a bhfuil an cruth seo aige?",
  q_food:"Cén tír as ar tháinig an mias seo?",q_brand:"Cén tír as ar tháinig an branda seo?",
  q_currency:"Cén tír ar leis an airgeadra seo?",q_curr_real:"Cén airgeadra atá ag…",
  q_pop_compare:"Níos mó nó níos lú cónaitheoirí?",
  q_hl_pop:"Níos mó cónaitheoirí ná {a}?",q_hl_river:"Níos faide ná {a}?",q_hl_area:"Níos mó ná {a}?",
  q_neighbor:"Cén tír a bhfuil teorainn le…?",q_neighbor_not:"NÍL teorainn le…?",
  q_plates_casual:"Cén tír ar as an pláta seo?",q_plates_hard:"Aithin an réigiún — gan leid!",
  q_river_real:"Trí cén tír a ritheann an abhainn seo?",q_map_guess:"Aimsigh an tír ar an léarscáil",
  fb_correct:"✓ Ceart! +{pts}",fb_wrong:"✗ Mícheart → {ans}",fb_time:"⏱ Am! → {ans}",
  plates_more:"+{n} níos mó",pct_complete:"{pct}% críochnaithe",
  spotter_dup:"📋 {code} ({country}) bailithe cheana!",
  map_unavail:"Léarscáil nach bhfuil ar fáil",map_loading:"Ag lódáil léarscáil…",
  q_subway_km:"Cé chomh fada leis an ngréasán meitreó … (km)?",q_subway_lines:"Cé mhéad líne meitreó atá ag …?"
}
};
/* t(key, vars) — translate + interpolate */
function t(key,vars){
  const lang=(typeof S!=='undefined'&&S.language)||localStorage.getItem('gq_lang')||'de';
  let s=(LANG[lang]&&LANG[lang][key])||(LANG.en&&LANG.en[key])||(LANG.de&&LANG.de[key])||key;
  if(!s)return key;  /* never return undefined */
  if(vars)Object.keys(vars).forEach(k=>{const rv=vars[k]??"-";s=s.replace(new RegExp('\\{'+k+'\\}','g'),String(rv));});
  return s;
}
/* Backwards-compat alias */
function T(k){return t(k);}
/* setLanguage — persists choice, marks as manual override */
function setLanguage(lang){
  if(typeof S!=='undefined')S.language=lang;
  localStorage.setItem('gq_lang',lang);
  localStorage.setItem('geoquest_lang_manual','1');
  render();
}
/* getCountryName(cc, lang) — Intl.DisplayNames for all 25 locales */
function getCountryName(cc,lang){
  if(!cc||typeof cc!=="string")return cc||"";
  try{
    const locMap={de:'de-DE',en:'en-GB',pl:'pl-PL',fr:'fr-FR',es:'es-ES',it:'it-IT',
      nl:'nl-NL',pt:'pt-PT',ro:'ro-RO',hu:'hu-HU',cs:'cs-CZ',sk:'sk-SK',hr:'hr-HR',
      sl:'sl-SI',bg:'bg-BG',el:'el-GR',da:'da-DK',sv:'sv-SE',fi:'fi-FI',et:'et-EE',
      lv:'lv-LV',lt:'lt-LT',mt:'mt-MT',ga:'ga-IE'};
    const locale=locMap[lang]||'en-GB';
    return new Intl.DisplayNames([locale],{type:'region'}).of(cc.toUpperCase())||cc;
  }catch(e){return cc;}
}
/* displayCountry(name) — translate country display name for current language */
function displayCountry(name){
  if(!name||typeof name!=="string")return name||"";
  const lang=(typeof S!=='undefined'&&S.language)||localStorage.getItem('gq_lang')||'de';
  const co=COUNTRIES.find(c=>c.c===name);
  if(!co)return name;
  return getCountryName(co.cc,lang);
}

/* SEEDED RNG */
let rngSeed=null,rngState=0;
function initRng(seed){rngSeed=seed>>>0;rngState=rngSeed;}
function seededRand(){rngState=(rngState+0x6D2B79F5)>>>0;let t=Math.imul(rngState^rngState>>>15,rngState|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296;}
function rng(){return rngSeed\!==null?seededRand():Math.random();}

let PLATES_DATA=[],CURR_REAL=[],CAPS_POP=[],RIVERS_REAL=[],NEIGHBORS={},AREA_DATA=[];

const CITIES=PLACEHOLDER_CJ;
/* Build CAPS_POP from aggregated city populations per country */
(function(){const m={};CITIES.forEach(c=>{if(!m[c.c])m[c.c]=0;m[c.c]+=c.pop;});CAPS_POP=Object.entries(m).map(([c,pop])=>({c,pop})).filter(x=>x.pop>500000);})();
const COUNTRIES=[
  {c:"Afghanistan",cc:"af",ct:"Asia",sr:"Southern Asia"},{c:"Algeria",cc:"dz",ct:"Africa",sr:"Northern Africa"},
  {c:"Angola",cc:"ao",ct:"Africa",sr:"Middle Africa"},{c:"Argentina",cc:"ar",ct:"South America",sr:"South America"},
  {c:"Australia",cc:"au",ct:"Oceania",sr:"Australia and New Zealand"},{c:"Austria",cc:"at",ct:"Europe",sr:"Western Europe"},
  {c:"Bangladesh",cc:"bd",ct:"Asia",sr:"Southern Asia"},{c:"Belgium",cc:"be",ct:"Europe",sr:"Western Europe"},
  {c:"Bolivia",cc:"bo",ct:"South America",sr:"South America"},{c:"Botswana",cc:"bw",ct:"Africa",sr:"Southern Africa"},
  {c:"Brazil",cc:"br",ct:"South America",sr:"South America"},{c:"Bulgaria",cc:"bg",ct:"Europe",sr:"Eastern Europe"},
  {c:"Cambodia",cc:"kh",ct:"Asia",sr:"Southeast Asia"},{c:"Canada",cc:"ca",ct:"North America",sr:"Northern America"},
  {c:"Chile",cc:"cl",ct:"South America",sr:"South America"},{c:"China",cc:"cn",ct:"Asia",sr:"Eastern Asia"},
  {c:"Colombia",cc:"co",ct:"South America",sr:"South America"},{c:"Costa Rica",cc:"cr",ct:"North America",sr:"Central America"},
  {c:"Croatia",cc:"hr",ct:"Europe",sr:"Southern Europe"},{c:"Cuba",cc:"cu",ct:"North America",sr:"Caribbean"},
  {c:"Czech Republic",cc:"cz",ct:"Europe",sr:"Eastern Europe"},{c:"Denmark",cc:"dk",ct:"Europe",sr:"Northern Europe"},
  {c:"DR Congo",cc:"cd",ct:"Africa",sr:"Middle Africa"},{c:"Ecuador",cc:"ec",ct:"South America",sr:"South America"},
  {c:"Egypt",cc:"eg",ct:"Africa",sr:"Northern Africa"},{c:"Estonia",cc:"ee",ct:"Europe",sr:"Northern Europe"},
  {c:"Ethiopia",cc:"et",ct:"Africa",sr:"Eastern Africa"},{c:"Finland",cc:"fi",ct:"Europe",sr:"Northern Europe"},
  {c:"France",cc:"fr",ct:"Europe",sr:"Western Europe"},{c:"Germany",cc:"de",ct:"Europe",sr:"Western Europe"},
  {c:"Ghana",cc:"gh",ct:"Africa",sr:"Western Africa"},{c:"Greece",cc:"gr",ct:"Europe",sr:"Southern Europe"},
  {c:"Guatemala",cc:"gt",ct:"North America",sr:"Central America"},{c:"Hungary",cc:"hu",ct:"Europe",sr:"Eastern Europe"},
  {c:"Iceland",cc:"is",ct:"Europe",sr:"Northern Europe"},{c:"India",cc:"in",ct:"Asia",sr:"Southern Asia"},
  {c:"Indonesia",cc:"id",ct:"Asia",sr:"Southeast Asia"},{c:"Iran",cc:"ir",ct:"Asia",sr:"Southern Asia"},
  {c:"Iraq",cc:"iq",ct:"Asia",sr:"Western Asia"},{c:"Ireland",cc:"ie",ct:"Europe",sr:"Northern Europe"},
  {c:"Israel",cc:"il",ct:"Asia",sr:"Western Asia"},{c:"Italy",cc:"it",ct:"Europe",sr:"Southern Europe"},
  {c:"Ivory Coast",cc:"ci",ct:"Africa",sr:"Western Africa"},{c:"Japan",cc:"jp",ct:"Asia",sr:"Eastern Asia"},
  {c:"Jordan",cc:"jo",ct:"Asia",sr:"Western Asia"},{c:"Kazakhstan",cc:"kz",ct:"Asia",sr:"Central Asia"},
  {c:"Kenya",cc:"ke",ct:"Africa",sr:"Eastern Africa"},{c:"Laos",cc:"la",ct:"Asia",sr:"Southeast Asia"},
  {c:"Latvia",cc:"lv",ct:"Europe",sr:"Northern Europe"},{c:"Lithuania",cc:"lt",ct:"Europe",sr:"Northern Europe"},
  {c:"Malaysia",cc:"my",ct:"Asia",sr:"Southeast Asia"},{c:"Mali",cc:"ml",ct:"Africa",sr:"Western Africa"},
  {c:"Mexico",cc:"mx",ct:"North America",sr:"Central America"},{c:"Mongolia",cc:"mn",ct:"Asia",sr:"Eastern Asia"},
  {c:"Morocco",cc:"ma",ct:"Africa",sr:"Northern Africa"},{c:"Myanmar",cc:"mm",ct:"Asia",sr:"Southeast Asia"},
  {c:"Namibia",cc:"na",ct:"Africa",sr:"Southern Africa"},{c:"Nepal",cc:"np",ct:"Asia",sr:"Southern Asia"},
  {c:"Netherlands",cc:"nl",ct:"Europe",sr:"Western Europe"},{c:"New Zealand",cc:"nz",ct:"Oceania",sr:"Australia and New Zealand"},
  {c:"Nigeria",cc:"ng",ct:"Africa",sr:"Western Africa"},{c:"Norway",cc:"no",ct:"Europe",sr:"Northern Europe"},
  {c:"Pakistan",cc:"pk",ct:"Asia",sr:"Southern Asia"},{c:"Paraguay",cc:"py",ct:"South America",sr:"South America"},
  {c:"Peru",cc:"pe",ct:"South America",sr:"South America"},{c:"Philippines",cc:"ph",ct:"Asia",sr:"Southeast Asia"},
  {c:"Poland",cc:"pl",ct:"Europe",sr:"Eastern Europe"},{c:"Portugal",cc:"pt",ct:"Europe",sr:"Southern Europe"},
  {c:"Romania",cc:"ro",ct:"Europe",sr:"Eastern Europe"},{c:"Russia",cc:"ru",ct:"Europe",sr:"Eastern Europe"},
  {c:"Saudi Arabia",cc:"sa",ct:"Asia",sr:"Western Asia"},{c:"Senegal",cc:"sn",ct:"Africa",sr:"Western Africa"},
  {c:"Serbia",cc:"rs",ct:"Europe",sr:"Southern Europe"},{c:"Singapore",cc:"sg",ct:"Asia",sr:"Southeast Asia"},
  {c:"Slovakia",cc:"sk",ct:"Europe",sr:"Eastern Europe"},{c:"South Africa",cc:"za",ct:"Africa",sr:"Southern Africa"},
  {c:"South Korea",cc:"kr",ct:"Asia",sr:"Eastern Asia"},{c:"Spain",cc:"es",ct:"Europe",sr:"Southern Europe"},
  {c:"Sri Lanka",cc:"lk",ct:"Asia",sr:"Southern Asia"},{c:"Sudan",cc:"sd",ct:"Africa",sr:"Northern Africa"},
  {c:"Sweden",cc:"se",ct:"Europe",sr:"Northern Europe"},{c:"Switzerland",cc:"ch",ct:"Europe",sr:"Western Europe"},
  {c:"Taiwan",cc:"tw",ct:"Asia",sr:"Eastern Asia"},{c:"Tanzania",cc:"tz",ct:"Africa",sr:"Eastern Africa"},
  {c:"Thailand",cc:"th",ct:"Asia",sr:"Southeast Asia"},{c:"Turkey",cc:"tr",ct:"Europe",sr:"Western Asia"},
  {c:"UAE",cc:"ae",ct:"Asia",sr:"Western Asia"},{c:"Uganda",cc:"ug",ct:"Africa",sr:"Eastern Africa"},
  {c:"Ukraine",cc:"ua",ct:"Europe",sr:"Eastern Europe"},{c:"United Kingdom",cc:"gb",ct:"Europe",sr:"Northern Europe"},
  {c:"United States",cc:"us",ct:"North America",sr:"Northern America"},{c:"Uruguay",cc:"uy",ct:"South America",sr:"South America"},
  {c:"Venezuela",cc:"ve",ct:"South America",sr:"South America"},{c:"Vietnam",cc:"vn",ct:"Asia",sr:"Southeast Asia"},
  {c:"Zambia",cc:"zm",ct:"Africa",sr:"Eastern Africa"},{c:"Zimbabwe",cc:"zw",ct:"Africa",sr:"Eastern Africa"},
];
const CAPITALS=PLACEHOLDER_CAPJ;
const RIVERS=PLACEHOLDER_RJ;
const LANDMARKS=PLACEHOLDER_LMJ;
const NATIONAL_PARKS=PLACEHOLDER_NPJ;
const UNESCO_SITES=PLACEHOLDER_UNJ;
const CITY_LANDMARKS=PLACEHOLDER_CLJ;
const SUBWAYS=PLACEHOLDER_SWJ;
const FOOD_DATA=PLACEHOLDER_FJ;
const BRANDS_DATA=PLACEHOLDER_BJ;
const CURRENCIES_DATA=PLACEHOLDER_CUJ;

const REGIONS=[
  {name:"Europa",cc:["fr","de","it","es","gb","pt","nl","be","ch","at","se","no","dk","fi","pl","cz","hu","ro","gr","ua","ru","tr","rs","hr","ie","bg","sk","is","ee","lv","lt"]},
  {name:"Ostasien",cc:["cn","jp","kr","tw","mn"]},
  {name:"Sued-/Suedostasien",cc:["in","pk","bd","th","vn","id","my","ph","sg","kh","mm","lk","np","la","af"]},
  {name:"Naher Osten & Zentralasien",cc:["sa","ir","iq","il","jo","ae","kz"]},
  {name:"Afrika",cc:["ng","et","eg","cd","za","ke","tz","gh","ma","dz","sd","ao","ci","sn","ug","zw","tn","na","bw","zm","ml"]},
  {name:"Amerika",cc:["us","ca","mx","cu","gt","cr","br","ar","co","pe","cl","ve","ec","uy","bo","py"]},
  {name:"Ozeanien",cc:["au","nz"]},
];

const MODES=[
  {id:"city",    icon:"\u{1F3D9}",title:"Stadt \u2192 Land",       group:"pure_geo",prompt:"In welchem Land liegt \u2026"},
  {id:"flag",    icon:"\u{1F6A9}",title:"Flagge \u2192 Land",      group:"pure_geo",prompt:"Welches Land zeigt diese Flagge?"},
  {id:"capital", icon:"\u{1F3DB}",title:"Hauptstadt \u2192 Land",  group:"pure_geo",prompt:"Zu welchem Land geh\u00f6rt diese Hauptstadt?"},
  {id:"river",   icon:"\u{1F30A}",title:"Fluss \u2192 Land",       group:"pure_geo",prompt:"In welchem Land liegt dieser Fluss?"},
  {id:"landmark",icon:"\u{1F5FD}",title:"Sehenswuerdigkeit",       group:"pure_geo",prompt:"In welchem Land liegt diese Sehenswuerdigkeit?"},
  {id:"park",    icon:"\u{1F33F}",title:"Nationalpark",            group:"pure_geo",prompt:"In welchem Land liegt dieser Nationalpark?"},
  {id:"unesco",  icon:"\u{1FA3A}",title:"UNESCO Welterbe",         group:"pure_geo",prompt:"In welchem Land liegt dieses UNESCO-Erbe?"},
  {id:"citymark",icon:"\u{1F306}",title:"Wahrzeichen \u2192 Stadt",group:"pure_geo",prompt:"In welcher Stadt liegt dieses Wahrzeichen?"},
  {id:"subway",  icon:"\u{1F687}",title:"U-Bahn-Netz",            group:"pure_geo",prompt:"Stadtverkehr-Experte"},
  {id:"flagsel", icon:"\u{1F38C}",title:"Land \u2192 Flagge",      group:"pure_geo",prompt:"Welche Flagge geh\u00f6rt zu \u2026"},
  {id:"rcapital",icon:"\u{1F3DF}",title:"Land \u2192 Hauptstadt",  group:"pure_geo",prompt:"Was ist die Hauptstadt von \u2026"},
  {id:"rcity",   icon:"\u{1F3E2}",title:"Land \u2192 Stadt",       group:"pure_geo",prompt:"Welche Stadt liegt in \u2026"},
  {id:"rriver",  icon:"\u{1F4A7}",title:"Land \u2192 Fluss",       group:"pure_geo",prompt:"Welcher Fluss fliesst durch \u2026"},
  {id:"outline", icon:"\u{1F5FA}",title:"L\u00e4nder-Umrisse",      group:"lifestyle",prompt:"Welches Land hat diese Form?"},
  {id:"food",    icon:"\u{1F37D}",title:"Gericht \u2192 Land",      group:"lifestyle",prompt:"Aus welchem Land kommt dieses Gericht?"},
  {id:"brand",   icon:"\u{1F3F7}",title:"Marke \u2192 Land",        group:"lifestyle",prompt:"Aus welchem Land kommt diese Marke?"},
  {id:"currency",icon:"\u{1F4B1}",title:"W\u00e4hrung \u2192 Land",group:"lifestyle",prompt:"Zu welchem Land geh\u00f6rt diese W\u00e4hrung?"},
  {id:"plate_casual",icon:"\u{1F697}",title:"EU-Kennzeichen",      group:"eu_plates",prompt:"Woher kommt dieses Kennzeichen?"},
  {id:"plate_hard",  icon:"\u{1F6A6}",title:"Kennzeichen Pro",     group:"eu_plates",prompt:"Region erkennen \u2014 kein Tipp\!"},
  {id:"curr_real",  icon:"\u{1F4B5}",title:"Land \u2192 W\u00e4hrung",group:"lifestyle",prompt:"Welche W\u00e4hrung hat …"},
  {id:"pop_compare",icon:"\u{1F465}",title:"Mehr Einwohner?",          group:"lifestyle",prompt:"Hat [Land B] mehr oder weniger Einwohner?"},
  {id:"river_real", icon:"\u{1F30A}",title:"Fluss \u2192 Land",       group:"pure_geo", prompt:"Durch welches Land flie\u00dft dieser Fluss?"},
  /* Phase 30 */
  {id:"hl_pop",   icon:"\u{1F465}",title:"H/L Einwohner",  group:"hl_compare",prompt:"Mehr Einwohner?"},
  {id:"hl_river", icon:"\u{1F30A}",title:"H/L Flussl\u00e4nge", group:"hl_compare",prompt:"L\u00e4ngerer Fluss?"},
  {id:"hl_area",  icon:"\u{1F5FA}",title:"H/L Landfl\u00e4che",  group:"hl_compare",prompt:"Gr\u00f6\u00dferes Land?"},
  {id:"neighbor", icon:"\u{1F91D}",title:"Grenzg\u00e4nger",     group:"neighbors", prompt:"Grenzt an\u2026?"},
  /* Phase 34 */
  {id:"map_guess",icon:"\u{1F5FA}",title:"Finde das Land",group:"map_mode",prompt:"Klick auf das gesuchte Land"},
];

const MODE_CATS={
  pure_geo:{label:"Pure Geo",icon:"\u{1F30D}",modes:["city","flag","capital","river","landmark","park","unesco","citymark","subway","flagsel","rcapital","rcity","rriver","river_real"],cost:0},
  lifestyle:{label:"Kultur & Lifestyle",icon:"\u{1F3A8}",modes:["outline","food","brand","currency","curr_real","pop_compare"],cost:1000},
  eu_plates:{label:"EU-Kennzeichen",icon:"\u{1F697}",modes:["plate_casual","plate_hard"],cost:500},
  hl_compare:{label:"Higher / Lower",icon:"\u2b06\ufe0f",modes:["hl_pop","hl_river","hl_area"],cost:0},
  neighbors:{label:"Nachbarl\u00e4nder",icon:"\u{1F91D}",modes:["neighbor"],cost:0},
  map_mode:{label:"Weltkarte",icon:"\u{1F5FA}",modes:["map_guess"],cost:0},
};

/* Phase 28: New real-data mode generators */
function genCurrRealQ(){
  if(!CURR_REAL||!CURR_REAL.length)return null;
  const _fcc=_rfilt(COUNTRIES,2);const _ccc=new Set(_fcc.map(x=>x.cc));
  const _crPool=CURR_REAL.filter(x=>_ccc.has(ccFromCountry(x.c)));
  const _crSrc=_crPool.length>=2?_crPool:CURR_REAL;
  const idx=~~(Math.random()*_crSrc.length);
  const cor=_crSrc[idx];
  /* Show only currency name+ISO — NOT country name (would give away the answer) */
  const dis=CURR_REAL.filter((_,i)=>i!==idx).sort(()=>Math.random()-.5).slice(0,3).map(x=>x.n+" ("+x.iso+")");
  const ans=cor.n+" ("+cor.iso+")";
  return{type:"curr_real",prompt:"Welche W\u00e4hrung hat …",subj:cor.c,ans,opts:sh([ans,...dis]),meta:cor.n,lid:cor.c,cc:ccFromCountry(cor.c)};
}
function genPopCompareQ(){
  if(!CAPS_POP||CAPS_POP.length<2)return null;
  const _fpp=_rfilt(COUNTRIES,4);const _cpp=new Set(_fpp.map(x=>x.cc));
  let pool=CAPS_POP.filter(x=>x.pop>500000&&_cpp.has(ccFromCountry(x.c)));
  if(pool.length<2)pool=CAPS_POP.filter(x=>x.pop>500000);if(pool.length<2)return null;
  const ai=~~(Math.random()*pool.length);
  let bi=~~(Math.random()*pool.length);
  while(bi===ai)bi=~~(Math.random()*pool.length);
  const a=pool[ai],b=pool[bi];
  const ans=b.pop>a.pop?"more":"less";
  const wrong=b.pop>a.pop?"less":"more";
  const aPopStr=(a.pop/1e6).toFixed(1)+" Mio.";
  return{type:"pop_compare",prompt:t("q_pop_compare"),subj:{nameA:a.c,popA:aPopStr,nameB:b.c},ans,opts:[ans,wrong],meta:"",lid:b.c,cc:ccFromCountry(b.c)};
}
function genRiverRealQ(){
  if(!RIVERS_REAL||!RIVERS_REAL.length)return null;
  const _frr=_rfilt(COUNTRIES,2);const _ccr2=new Set(_frr.map(x=>x.cc));
  const _rrPool=RIVERS_REAL.filter(r=>_ccr2.has(ccFromCountry(r.c)));
  const _rrSrc=_rrPool.length>=1?_rrPool:RIVERS_REAL;
  const idx=~~(Math.random()*_rrSrc.length);
  const cor=_rrSrc[idx];
  const countries=[...new Set(RIVERS_REAL.map(r=>r.c))];
  const dis=countries.filter(c=>c!==cor.c).sort(()=>Math.random()-.5).slice(0,3);
  const meta=cor.len>0?cor.len+" km":"";
  return{type:"river_real",prompt:t("q_river_real"),subj:cor.n,ans:cor.c,opts:sh([cor.c,...dis]),meta,lid:cor.n,cc:ccFromCountry(cor.c)};
}

/* Phase 30 — Default neighbor map (fallback when neighbors.json is empty/broken) */
const _DEFAULT_NEIGHBORS={
  "Deutschland":["Frankreich","Belgien","Niederlande","Luxemburg","Schweiz","Österreich","Tschechien","Polen","Dänemark"],
  "Frankreich":["Deutschland","Belgien","Luxemburg","Schweiz","Italien","Spanien","Andorra","Monaco"],
  "Polen":["Deutschland","Tschechien","Slowakei","Ukraine","Belarus","Litauen","Russland"],
  "Österreich":["Deutschland","Schweiz","Liechtenstein","Italien","Slowenien","Ungarn","Slowakei","Tschechien"],
  "Schweiz":["Deutschland","Frankreich","Italien","Österreich","Liechtenstein"],
  "Spanien":["Frankreich","Andorra","Portugal"],
  "Portugal":["Spanien"],
  "Italien":["Frankreich","Schweiz","Österreich","Slowenien","San Marino"],
  "Russland":["Norwegen","Finnland","Estland","Lettland","Belarus","Ukraine","Georgien","Kasachstan","China","Mongolei","Nordkorea"],
  "China":["Russland","Mongolei","Kasachstan","Kirgisistan","Tadschikistan","Afghanistan","Pakistan","Indien","Nepal","Bhutan","Myanmar","Laos","Vietnam","Nordkorea"],
  "Indien":["Pakistan","China","Nepal","Bhutan","Bangladesh","Myanmar"],
  "Brasilien":["Venezuela","Guyana","Kolumbien","Peru","Bolivien","Paraguay","Argentinien","Uruguay"],
  "USA":["Kanada","Mexiko"],
  "Kanada":["USA"],
  "Mexiko":["USA","Guatemala","Belize"],
  "Argentinien":["Chile","Bolivien","Paraguay","Brasilien","Uruguay"],
  "Ukraine":["Russland","Belarus","Polen","Slowakei","Ungarn","Rumänien","Moldawien"],
  "Belarus":["Russland","Ukraine","Polen","Litauen","Lettland"],
  "Türkei":["Griechenland","Bulgarien","Georgien","Armenien","Aserbaidschan","Iran","Irak","Syrien"],
  "Iran":["Türkei","Irak","Afghanistan","Pakistan","Turkmenistan","Aserbaidschan","Armenien"],
  "Afghanistan":["Iran","Pakistan","Tadschikistan","Turkmenistan","Usbekistan","China"],
  "Pakistan":["Indien","Afghanistan","Iran","China"],
  "Irak":["Türkei","Syrien","Jordanien","Saudi-Arabien","Kuwait","Iran"],
  "Syrien":["Türkei","Irak","Jordanien","Libanon","Israel"],
  "Saudi-Arabien":["Jordanien","Irak","Kuwait","Bahrain","Katar","VAE","Oman","Jemen"],
  "Ägypten":["Israel","Sudan","Libyen"],
  "Sudan":["Ägypten","Libyen","Tschad","Zentralafrikanische Republik","Südsudan","Äthiopien","Eritrea"],
  "Äthiopien":["Eritrea","Dschibuti","Somalia","Kenia","Sudan","Südsudan"],
  "Nigeria":["Benin","Niger","Kamerun","Tschad"],
  "Demokratische Republik Kongo":["Republik Kongo","Angola","Sambia","Tansania","Ruanda","Burundi","Uganda","Zentralafrikanische Republik","Südsudan"],
  "Südafrika":["Namibia","Botswana","Simbabwe","Mosambik","Eswatini","Lesotho"],
  "Kenia":["Äthiopien","Somalia","Tansania","Uganda","Südsudan"],
  "Ungarn":["Österreich","Slowakei","Ukraine","Rumänien","Serbien","Kroatien","Slowenien"],
  "Rumänien":["Ungarn","Ukraine","Moldawien","Bulgarien","Serbien"],
  "Griechenland":["Albanien","Nordmazedonien","Bulgarien","Türkei"],
  "Schweden":["Norwegen","Finnland","Dänemark"],
  "Norwegen":["Schweden","Finnland","Russland"],
  "Finnland":["Schweden","Norwegen","Russland","Estland"],
  "Kolumbien":["Venezuela","Brasilien","Peru","Ecuador","Panama"],
  "Peru":["Ecuador","Kolumbien","Brasilien","Bolivien","Chile"],
  "Bolivien":["Peru","Chile","Argentinien","Paraguay","Brasilien"],
  "Chile":["Peru","Bolivien","Argentinien"],
  "Venezuela":["Kolumbien","Brasilien","Guyana"],
  "Indonesien":["Malaysia","Papua-Neuguinea","Osttimor"],
  "Thailand":["Myanmar","Laos","Kambodscha","Malaysia"],
  "Vietnam":["China","Laos","Kambodscha"],
  "Myanmar":["Indien","Bangladesh","China","Laos","Thailand"],
  "Kasachstan":["Russland","China","Kirgisistan","Usbekistan","Turkmenistan"],
  "Marokko":["Algerien","Mauretanien","Spanien"],
  "Algerien":["Marokko","Tunesien","Libyen","Niger","Mali","Mauretanien"],
  "Tunesien":["Algerien","Libyen"],
  "Tschechien":["Deutschland","Polen","Slowakei","Österreich"],
  "Slowakei":["Tschechien","Polen","Ukraine","Ungarn","Österreich"],
  "Bulgarien":["Rumänien","Serbien","Nordmazedonien","Griechenland","Türkei"],
  "Serbien":["Ungarn","Rumänien","Bulgarien","Nordmazedonien","Kosovo","Montenegro","Bosnien","Kroatien"],
  "Kroatien":["Slowenien","Ungarn","Serbien","Bosnien","Montenegro"],
  "Slowenien":["Italien","Österreich","Ungarn","Kroatien"],
};
function genHLPopQ(){
  if(\!CAPS_POP||CAPS_POP.length<2)return null;
  const _fcp=_rfilt(COUNTRIES,4);const _ccp=new Set(_fcp.map(x=>x.cc));
  let pool=CAPS_POP.filter(x=>x.pop>500000&&_ccp.has(ccFromCountry(x.c)));
  if(pool.length<2)pool=CAPS_POP.filter(x=>x.pop>500000);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=(p)=>p>=1e9?(p/1e9).toFixed(2)+" Mrd.":p>=1e6?(p/1e6).toFixed(1)+" Mio.":(p/1e3).toFixed(0)+" Tsd.";
  const ans=b.pop>a.pop?"higher":"lower";
  return{type:"hl_pop",prompt:t("q_hl_pop",{a:a.c}),nameA:a.c,valA:fmt(a.pop),nameB:b.c,valB:fmt(b.pop),ans,opts:["higher","lower"],lid:b.c,cc:ccFromCountry(b.c)};
}
function genHLRiverQ(){
  if(\!RIVERS_REAL||RIVERS_REAL.length<2)return null;
  const _fcr=_rfilt(COUNTRIES,4);const _ccr=new Set(_fcr.map(x=>x.cc));
  let pool=RIVERS_REAL.filter(r=>r.len>100&&_ccr.has(ccFromCountry(r.c)));
  if(pool.length<2)pool=RIVERS_REAL.filter(r=>r.len>100);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const ans=b.len>a.len?"higher":"lower";
  return{type:"hl_river",prompt:t("q_hl_river",{a:a.n}),nameA:a.n,valA:a.len+" km",nameB:b.n,valB:b.len+" km",ans,opts:["higher","lower"],lid:b.n,cc:ccFromCountry(b.c)};
}
function genHLAreaQ(){
  if(\!AREA_DATA||AREA_DATA.length<2)return null;
  const _fca=_rfilt(COUNTRIES,4);const _cca=new Set(_fca.map(x=>x.cc));
  let pool=AREA_DATA.filter(x=>_cca.has(ccFromCountry(x.c)));
  if(pool.length<2)pool=AREA_DATA.slice();if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=(x)=>x>=1e6?(x/1e6).toFixed(2)+" Mio. km²":(x/1000).toFixed(0)+" Tsd. km²";
  const ans=b.area>a.area?"higher":"lower";
  return{type:"hl_area",prompt:t("q_hl_area",{a:a.c}),nameA:a.c,valA:fmt(a.area),nameB:b.c,valB:fmt(b.area),ans,opts:["higher","lower"],lid:b.c,cc:ccFromCountry(b.c)};
}
function genNeighborQ(){
  const nb=NEIGHBORS;const valid=Object.keys(nb).filter(c=>nb[c]&&nb[c].length>=2);if(\!valid.length)return null;
  const country=valid[~~(rng()*valid.length)];const neighborList=nb[country];
  const allC=Object.keys(nb);const nonNb=allC.filter(c=>c\!==country&&\!neighborList.includes(c));if(\!nonNb.length)return null;
  const type2=rng()>.5;
  if(type2&&neighborList.length>=2){
    const ans=nonNb[~~(rng()*nonNb.length)];
    const dis=neighborList.slice().sort(()=>rng()-.5).slice(0,2);
    return{type:"neighbor",prompt:"Grenzt NICHT an\u2026?",subj:country,ans,opts:sh([ans,...dis]),lid:country+'|'+ans,cc:ccFromCountry(country)||''};
  }else{
    const ans=neighborList[~~(rng()*neighborList.length)];
    const dis=nonNb.slice().sort(()=>rng()-.5).slice(0,3);
    return{type:"neighbor",prompt:"Welches Land grenzt an\u2026?",subj:country,ans,opts:sh([ans,...dis.slice(0,3)]),lid:country+'|'+ans,cc:ccFromCountry(country)||''};
  }
}

/* ═══════════════════════════════════════════════════════════════════════
   PHASE 33 — REALTIME 1vs1 MULTIPLAYER  (Supabase Broadcast)
   ═══════════════════════════════════════════════════════════════════════ */

/* Helpers */
function mpCode(){let c="";const chars="ABCDEFGHJKLMNPQRSTUVWXYZ23456789";for(let i=0;i<4;i++)c+=chars[~~(Math.random()*chars.length)];return c;}
function mpLog(...a){console.log("[MP]",...a);}

/* Close and clean up current channel */
function mpLeave(){
  if(S.mp?.channel)try{S.mp.channel.unsubscribe();}catch(e){}
  S.mp=null;S.mpModal=false;render();
}

/* Send a broadcast on the current channel */
function mpSend(event,payload){
  if(\!S.mp?.channel)return;
  S.mp.channel.send({type:"broadcast",event,payload});
}

/* Countdown then start */
function mpCountdown(seed,mode){
  let t=3;
  S.mp.phase="countdown";S.mp.countdown=t;render();
  const iv=setInterval(()=>{
    t--;S.mp.countdown=t;
    if(t<=0){
      clearInterval(iv);
      S.mpModal=false;
      /* Phase 33 Teil 2: keep channel alive for in-game score sync */
      const _ch=S.mp.channel,_oppName=S.mp.oppName||"Gegner";
      window.mpGameCh=_ch;
      _ch.on("broadcast",{event:"score_update"},({payload})=>{
        S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;render();
      }).on("broadcast",{event:"game_over"},({payload})=>{
        S.mpOppFinal=payload;
        if(S.ph==="gameover")render();
      });
      S.mp=null;
      /* Sync start — same seed on both sides */
      initRng(seed);
      startGame(mode||"city");
      /* Tag session as multiplayer */
      S.mpSeed=seed;S.mpOpponent=_oppName;
      S.mpOppScore=0;S.mpOppRd=0;S.mpOppFinal=null;
    }else render();
  },1000);
}

/* HOST: create room */
function mpCreate(){
  if(\!sb){showToast("Supabase nicht verbunden\!");return;}
  const code=mpCode();
  let channel;
  try{
    channel=sb.channel("room_"+code,{config:{broadcast:{self:false}}});
  }catch(e){
    showToast("\u26a0\ufe0f Verbindungsfehler: "+e.message);
    console.error("mpCreate channel error:",e);
    return;
  }
  S.mp={role:"host",code,channel,phase:"waiting",myReady:false,oppReady:false,oppName:null};
  render();

  channel
    .on("broadcast",{event:"player_joined"},({payload})=>{
      mpLog("guest joined:",payload);
      S.mp.oppName=payload.name||"Gast";
      S.mp.phase="ready";
      render();
      /* Acknowledge the join */
      mpSend("host_ack",{name:sbProfile?.username||"Host"});
    })
    .on("broadcast",{event:"player_ready"},({payload})=>{
      mpLog("guest ready");
      S.mp.oppReady=true;render();
      if(S.mp.myReady&&S.mp.oppReady){
        const seed=~~(Math.random()*1e9);
        const mode=S.mode||"city";
        mpSend("game_start",{seed,mode});
        mpCountdown(seed,mode);
      }
    })
    .on("broadcast",{event:"game_start"},()=>{/* host ignores own game_start */})
    .subscribe((status)=>{
      mpLog("host channel status:",status);
      if(status==="SUBSCRIBED")render();
    });
}

/* GUEST: join room */
function mpJoin(code){
  if(\!sb){showToast("Supabase nicht verbunden\!");return;}
  if(\!code||code.length<4){showToast("Bitte gültigen Code eingeben\!");return;}
  const uc=code.toUpperCase().trim();
  let channel;
  try{
    channel=sb.channel("room_"+uc,{config:{broadcast:{self:false}}});
  }catch(e){
    showToast("\u26a0\ufe0f Verbindungsfehler: "+e.message);
    return;
  }
  S.mp={role:"guest",code:uc,channel,phase:"joining",myReady:false,oppReady:false,oppName:null};
  render();

  channel
    .on("broadcast",{event:"host_ack"},({payload})=>{
      mpLog("host ack:",payload);
      S.mp.oppName=payload.name||"Host";
      S.mp.phase="ready";render();
    })
    .on("broadcast",{event:"player_ready"},()=>{
      S.mp.oppReady=true;render();
    })
    .on("broadcast",{event:"game_start"},({payload})=>{
      mpLog("game_start received:",payload);
      mpCountdown(payload.seed,payload.mode);
    })
    .subscribe((status)=>{
      mpLog("guest channel status:",status);
      if(status==="SUBSCRIBED"){
        mpSend("player_joined",{name:sbProfile?.username||"Spieler"});
        render();
      }
    });
}

/* Ready button */
function mpReady(){
  S.mp.myReady=true;render();
  mpSend("player_ready",{name:sbProfile?.username||"Ich"});
  /* Host: if guest was already ready */
  if(S.mp.role==="host"&&S.mp.oppReady){
    const seed=~~(Math.random()*1e9);
    const mode=S.mode||"city";
    mpSend("game_start",{seed,mode});
    mpCountdown(seed,mode);
  }
}

/* Render the full lobby modal */
function renderMultiplayerLobby(){
  const mp=S.mp;

  /* ── Phase: initial (no room yet) ────────────────────────── */
  if(\!mp){
    const joinInput=S._mpJoinCode||"";
    return`<div class="scr">
      <div style="text-align:center;margin-bottom:1.4rem;padding-top:.5rem">
        <div class="mp-lobby-title">\u2694\ufe0f Live 1vs1 Duell</div>
        <div style="color:var(--text3);font-size:.8rem;margin-top:.25rem">Spiele live gegen einen Freund</div>
      </div>
      <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.4rem;margin-bottom:1rem;text-align:center">
        <div style="font-size:2.5rem;margin-bottom:.5rem">\u{1F3E0}</div>
        <div style="font-weight:900;font-size:1rem;color:var(--text);margin-bottom:.35rem">Spiel erstellen</div>
        <div style="color:var(--text3);font-size:.78rem;margin-bottom:.9rem">Generiere einen Code und lade einen Freund ein</div>
        <button class="btn-p" style="width:100%" onclick="mpCreate()">➕ Neues Spiel erstellen</button>
      </div>
      <div style="background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.4rem;text-align:center">
        <div style="font-size:2.5rem;margin-bottom:.5rem">\u{1F517}</div>
        <div style="font-weight:900;font-size:1rem;color:var(--text);margin-bottom:.35rem">Mit Code beitreten</div>
        <div style="color:var(--text3);font-size:.78rem;margin-bottom:.9rem">Gib den 4-stelligen Code deines Freundes ein</div>
        <div style="display:flex;gap:8px">
          <input type="text" maxlength="4" placeholder="z.B. A7B2" value="${esc(joinInput)}"
            oninput="S._mpJoinCode=this.value.toUpperCase();this.value=this.value.toUpperCase()"
            style="flex:1;font-size:1.2rem;font-weight:900;text-align:center;letter-spacing:4px;text-transform:uppercase">
          <button class="btn-p" style="width:auto;padding:.6rem 1.2rem" onclick="mpJoin(S._mpJoinCode)">▶</button>
        </div>
      </div>
      <button class="mp-back-btn" onclick="S.mpModal=false;render()">\u2b05\ufe0f Zurück zum Hauptmenü</button>
    </div>`;
  }

  /* ── Phase: host waiting for guest ───────────────────────── */
  if(mp.phase==="waiting"){
    return`<div class="scr" style="text-align:center">
      <button class="mp-back-btn" style="margin-bottom:.5rem" onclick="mpLeave()">\u2b05\ufe0f Abbrechen</button>
      <div style="clear:both;padding-top:.5rem"></div>
      <div style="font-size:3rem;margin:1rem 0">\u{1F4F1}</div>
      <h2 style="font-size:1.3rem;font-weight:900;color:var(--text);margin-bottom:.5rem">Warte auf Gegner…</h2>
      <p style="color:var(--text3);font-size:.82rem;margin-bottom:1.4rem">Gib diesen Code an deinen Freund:</p>
      <div style="display:inline-block;background:var(--bg3);border:3px solid #7c3aed;border-radius:16px;padding:1rem 2rem;font-size:3rem;font-weight:900;letter-spacing:10px;color:#7c3aed;margin-bottom:1rem">${esc(mp.code)}</div>
      <p style="color:var(--text3);font-size:.74rem">Verbunden — Channel aktiv</p>
      <div style="margin-top:1.5rem;display:flex;justify-content:center">
        <div class="spinner"></div>
      </div>
    </div>`;
  }

  /* ── Phase: guest joining ─────────────────────────────────── */
  if(mp.phase==="joining"){
    return`<div class="scr" style="text-align:center">
      <div style="font-size:3rem;margin:2rem 0">\u{1F50D}</div>
      <h2 style="font-size:1.2rem;font-weight:900;color:var(--text)">Verbinde mit Raum ${esc(mp.code)}…</h2>
      <div style="margin-top:1.5rem;display:flex;justify-content:center"><div class="spinner"></div></div>
    </div>`;
  }

  /* ── Phase: both in room — ready check ───────────────────── */
  if(mp.phase==="ready"){
    const myR=mp.myReady,oppR=mp.oppReady;
    return`<div class="scr" style="text-align:center">
      <button class="mp-back-btn" style="margin-bottom:.5rem" onclick="mpLeave()">\u2b05\ufe0f Abbrechen</button>
      <div style="clear:both;padding-top:.5rem"></div>
      <div style="font-size:2.5rem;margin:.6rem 0">\u{1F7E2}</div>
      <h2 style="font-size:1.2rem;font-weight:900;color:var(--text);margin-bottom:.3rem">Gegner gefunden\!</h2>
      <p style="color:var(--text3);font-size:.8rem;margin-bottom:1.2rem">Gegner: <strong>${esc(mp.oppName||"Unbekannt")}</strong></p>
      <div style="display:flex;gap:12px;justify-content:center;margin-bottom:1.4rem">
        <div style="background:var(--bg2);border:2px solid ${myR?"#10b981":"var(--border)"};border-radius:12px;padding:.75rem 1.2rem;min-width:100px">
          <div style="font-size:1.3rem">${myR?"✅":"⏳"}</div>
          <div style="font-size:.72rem;color:var(--text3);margin-top:4px">Du</div>
        </div>
        <div style="font-size:1.4rem;align-self:center;color:var(--text3)">VS</div>
        <div style="background:var(--bg2);border:2px solid ${oppR?"#10b981":"var(--border)"};border-radius:12px;padding:.75rem 1.2rem;min-width:100px">
          <div style="font-size:1.3rem">${oppR?"✅":"⏳"}</div>
          <div style="font-size:.72rem;color:var(--text3);margin-top:4px">${esc(mp.oppName||"Gegner")}</div>
        </div>
      </div>
      ${myR?`<div style="color:var(--text3);font-size:.82rem">Warte auf ${esc(mp.oppName||"Gegner")}…</div>`
           :`<button class="btn-p" style="width:100%;font-size:1.1rem" onclick="mpReady()">\u{1F3C1} Bereit\!</button>`}
    </div>`;
  }

  /* ── Phase: countdown ────────────────────────────────────── */
  if(mp.phase==="countdown"){
    return`<div class="scr" style="text-align:center;padding-top:30%">
      <div style="font-size:6rem;font-weight:900;color:#7c3aed;line-height:1">${mp.countdown}</div>
      <div style="color:var(--text2);font-size:1rem;margin-top:.8rem">Spiel startet…</div>
    </div>`;
  }

  return`<div class="scr"><button onclick="mpLeave()">← ${t("btn_back")}</button></div>`;
}

/* ACHIEVEMENTS */
const ACHIEVEMENTS=[
  {id:"first_blood", icon:"\u{1F3AF}", title:"Erster Treffer",    desc:"Erste richtige Antwort", check:(S,h)=>h.some(g=>g.correct>0)},
  {id:"streak5",     icon:"\u{1F525}", title:"On Fire",           desc:"Streak von 5 erreicht",  check:(S,h)=>h.some(g=>g.best_streak>=5)},
  {id:"streak10",    icon:"\u{1F4A5}", title:"Legendar",          desc:"Streak von 10 erreicht", check:(S,h)=>h.some(g=>g.best_streak>=10)},
  {id:"perfect",     icon:"\u{1F947}", title:"Makellos",          desc:"10/10 in einer Runde",   check:(S,h)=>h.some(g=>g.correct===10&&g.rounds===10)},
  {id:"globetrotter",icon:"\u{1F30D}", title:"Globetrotter",      desc:"20 Laender gestempelt",  check:(S,h)=>{const m=loadMastery();return Object.values(m).filter(v=>getMasteryRank(v.v,v.p)).length>=20;}},
  {id:"daily3",      icon:"\u{1F4C5}", title:"Daily Habit",       desc:"3 Daily Challenges",     check:(S,h)=>getDailyStreakCount()>=3},
  {id:"plates_ace",  icon:"\u{1F697}", title:"Kennzeichen-Ass",   desc:"Kennzeichen-Runde gespielt",check:(S,h)=>h.some(g=>g.mode==="plate_casual"||g.mode==="plate_hard")},
  {id:"hc_victory",  icon:"\u{1F94B}", title:"Hardcore-Sieger",   desc:"Hardcore-Runde >1500 Pkt",check:(S,h)=>h.some(g=>g.score>1500&&g.mode&&(localStorage.getItem("gq_hc_"+g.date)||g.diff==="hardcore"))},
];

function getDailyStreakCount(){
  let count=0;const today=new Date();
  for(let i=0;i<30;i++){const d=new Date(today);d.setDate(d.getDate()-i);const k="gq_daily_"+d.toISOString().slice(0,10);if(localStorage.getItem(k))count++;else break;}
  return count;
}

function loadUnlocked(){return _gqLoad("gq_unlocked",["pure_geo"]);}
function saveUnlocked(arr){_gqSave("gq_unlocked",arr);}
function isCategoryUnlocked(catId){return true;/* TEST MODE — all categories unlocked */}
function buyCategory(catId){
  if(!sb||!sbUser?.id){showToast("Bitte einloggen\!"); return;}
  const cat=MODE_CATS[catId];if(!cat)return;
  const coins=sbProfile?.geo_coins||0;
  if(coins<cat.cost){showToast("Zu wenig GeoCoins\!");return;}
  if(sbProfile)sbProfile.geo_coins=coins-cat.cost;
  const arr=loadUnlocked();if(\!arr.includes(catId))arr.push(catId);saveUnlocked(arr);
  if(sb&&sbUser){sb.rpc("spend_coins",{p_user_id:sbUser.id,p_amount:cat.cost}).then(r=>{if(r.data!=null&&sbProfile)sbProfile.geo_coins=r.data;},()=>{});}
  showConfetti();S.lockModal=null;render();
}
function showConfetti(){
  const colors=["#f59e0b","#10b981","#60a5fa","#f472b6","#a78bfa","#34d399"];
  for(let i=0;i<60;i++){const d=document.createElement("div");d.className="confetti-piece";d.style.left=Math.random()*100+"vw";d.style.background=colors[i%colors.length];d.style.animationDelay=Math.random()*1.5+"s";d.style.borderRadius=Math.random()>.5?"50%":"2px";document.body.appendChild(d);setTimeout(()=>d.remove(),3000);}
}
function renderLockModal(catId){
  const cat=MODE_CATS[catId];if(\!cat)return"";
  const coins=sbProfile?.geo_coins||0;const enough=coins>=cat.cost;
  return`<div class="modal-overlay" onclick="if(event.target===this){S.lockModal=null;render()}">
    <div class="modal-box">
      <div style="font-size:2.5rem;margin-bottom:.5rem">${cat.icon}</div>
      <div style="font-size:1.1rem;font-weight:900;margin-bottom:4px;color:var(--text)">${cat.label}</div>
      <div style="color:var(--text3);font-size:.82rem;margin-bottom:1rem">Diese Kategorie freischalten</div>
      <div style="background:var(--bg3);border-radius:12px;padding:.85rem;margin-bottom:1rem;text-align:center">
        <div style="color:var(--text3);font-size:.68rem;margin-bottom:3px">KOSTEN</div>
        <div style="font-size:1.8rem;font-weight:900;color:#fbbf24">\u{1F4B0} ${cat.cost.toLocaleString()}</div>
        <div style="font-size:.7rem;color:${enough?"#34d399":"#f87171"};margin-top:4px">${enough?"Du hast genug Coins \u2713":"Du hast nur "+coins+" Coins"}</div>
      </div>
      ${sbProfile?.is_premium?`<div style="color:#34d399;font-size:.82rem;margin-bottom:.85rem">\u{1F451} Premium: Diese Kategorie ist kostenlos\!</div>`:""}
      <button class="btn-p" onclick="buyCategory('${catId}')" ${(\!enough&&\!sbProfile?.is_premium)?"disabled":""}>
        ${sbProfile?.is_premium?"Kostenlos freischalten":"\u{1F4B0} "+cat.cost+" Coins ausgeben"}
      </button>
      <button class="btn-g" style="margin-bottom:0" onclick="S.payModal=true;S.lockModal=null;render()">\u{1F4B3} GeoCoins kaufen</button>
      <button class="btn-g" style="margin-bottom:0" onclick="S.lockModal=null;render()">Schlie\u00dfen</button>
    </div>
  </div>`;
}

/* POWER-UPS (Phase 26) */
function loadPU(){return _gqLoad("gq_pu",{});}
function savePU(d){_gqSave("gq_pu",d);}
function getPUCount(type){return(loadPU()[type]||0);}
function addPU(type,qty){const d=loadPU();d[type]=(d[type]||0)+qty;savePU(d);}
function useFiveO(){
  if(S.sel\!==null||S.half_removed)return;
  const pu=loadPU();if(\!(pu.five0>0)){showToast("Kein 50/50-Joker mehr\!");return;}
  pu.five0--;savePU(pu);
  const wrong=S.q.opts.filter(o=>o\!==S.q.ans);
  const toRemove=sh([...wrong]).slice(0,2);
  S.q.opts=S.q.opts.filter(o=>o===S.q.ans||\!toRemove.includes(o));
  S.half_removed=true;render();
}
function useFreeze(){
  if(S.freezeActive)return;
  const pu=loadPU();
  if(\!(pu.freeze>0)){showToast("Kein Zeit-Stopp mehr\!");return;}
  if(S.ph\!=="playing"&&S.ph\!=="feedback")return;
  pu.freeze--;savePU(pu);
  clearInterval(tIv);S.freezeActive=true;
  const bar=document.querySelector(".tbar");if(bar)bar.classList.add("frozen");
  render();
  setTimeout(()=>{
    if(S.ph\!=="playing"&&S.ph\!=="feedback"){S.freezeActive=false;return;}
    S.freezeActive=false;
    const b2=document.querySelector(".tbar");if(b2)b2.classList.remove("frozen");
    if(S.ph==="playing"&&S.sel===null){
      tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();if(S.tm<=0){clearInterval(tIv);answer(null);}else render();},1000);
    }
  },10000);
}

const ROUNDS=10,BASE=100,TB=10;
const TIERS=[
  {m:10,x:3.0,l:"\u{1F525}\u{1F525}\u{1F525} LEGEND\u00c4R \u2014 3\u00d7"},
  {m:5, x:2.0,l:"\u{1F525}\u{1F525} ON FIRE \u2014 2\u00d7"},
  {m:3, x:1.5,l:"\u{1F525} HEISS \u2014 1.5\u00d7"},
  {m:0, x:1.0,l:""},
];

/* SUPABASE */
let sb=null,sbUser=null,sbProfile=null,sbStamps=new Set();
/* CURR_REAL, CAPS_POP, RIVERS_REAL populated by loadGameData() */
/* Helper: country name → cc */
function ccFromCountry(name){const c=COUNTRIES.find(x=>x.c===name);return c?c.cc:null;}
function flagOf(name){const cc=ccFromCountry(name);return cc?`<img src="https://flagcdn.com/w40/${cc}.png" style="height:22px;vertical-align:middle;border-radius:2px" alt="${name}" onerror="this.style.display='none'">`:"";}

const sbOK=SUPABASE_URL.includes("supabase.co");
if(sbOK){
  try{
    sb=window.supabase.createClient(SUPABASE_URL,SUPABASE_ANON);
    initAuth();
  }catch(e){
    console.error("Supabase init failed:",e);
    setTimeout(()=>showToast("\u26a0\ufe0f Supabase-Verbindung fehlgeschlagen: "+e.message),1200);
  }
}

async function initAuth(){
  if(\!sb)return;
  const{data:{session}}=await sb.auth.getSession();
  if(session){sbUser=session.user;await loadProfile();}
  else{const{data,error}=await sb.auth.signInAnonymously();if(\!error){sbUser=data.user;await loadProfile();}}
}
async function loadProfile(){
  if(\!sb||\!sbUser)return;
  const{data}=await sb.from("profiles").select("*").eq("id",sbUser.id).single();
  sbProfile=data;
  /* Admin privileges handled server-side via Supabase trigger */
  const{data:stamps}=await sb.from("user_stamps").select("stamp_id,stamps(country_code)").eq("user_id",sbUser.id);
  if(stamps)stamps.forEach(s=>s.stamps&&sbStamps.add(s.stamps.country_code));
  render();
}
/* Helper: get display name */
function getDisplayName(){return sbProfile?.username||localStorage.getItem("gq_username")||null;}

async function saveUsername(n){
  if(!n.trim())return;
  const u=n.trim().slice(0,20);
  if(sbOK&&sb&&sbUser){await sb.from("profiles").update({username:u}).eq("id",sbUser.id);}
  if(!sbProfile)sbProfile={};
  sbProfile={...sbProfile,username:u};
  try{localStorage.setItem("gq_username",u);}catch(e){}
  S.newUsername="";
  showToast("\u2713 Name gespeichert: "+u);
  render();
}

/* Phase 27: Migrate guest localStorage data to real account */
async function migrateGuestToAccount(uid){
  if(!sb||!uid)return;
  const mastery=loadMastery();
  let bonusCoins=0;
  Object.values(mastery).forEach(m=>{
    const r=getMasteryRank(m.v,m.p);
    if(r==="gold")bonusCoins+=20;
    else if(r==="silver")bonusCoins+=5;
    else if(r==="bronze")bonusCoins+=1;
  });
  const totalCoins=(sbProfile?.geo_coins||0)+bonusCoins;
  try{const _cr=await sb.rpc("add_coins",{p_user_id:uid,p_amount:bonusCoins});if(_cr.data!=null&&sbProfile)sbProfile.geo_coins=_cr.data;}catch(_){}
  if(sbProfile)sbProfile.geo_coins=totalCoins;
  const masteryCC=Object.keys(mastery).filter(cc=>getMasteryRank(mastery[cc].v,mastery[cc].p));
  for(const cc of masteryCC){
    sb.rpc("upsert_stamp",{p_user_id:uid,p_country_code:cc,p_perfect:mastery[cc].p>0}).then(()=>{},()=>{});
  }
}

/* Phase 27: Register */
async function doRegister(){
  if(!sb){showToast("Supabase nicht verbunden");return;}
  const email=S.authEmail.trim();
  const pw=S.authPassword;
  const uname=S.authUsername.trim().slice(0,20);
  if(!email||!pw||!uname){S.authError="Bitte alle Felder ausf\u00fcllen.";render();return;}
  if(pw.length<6){S.authError="Passwort mind. 6 Zeichen.";render();return;}
  if(pw!==S.authConfirm){S.authError="Die Passwörter stimmen nicht überein.";render();return;}
  S.authLoading=true;S.authError="";render();
  try{
    const{data,error}=await sb.auth.signUp({email,password:pw,options:{data:{username:uname}}});
    if(error){
      const _em=error.message||"";
      S.authError=
        _em.includes("already registered")||_em.includes("already been registered")?"Diese E-Mail ist bereits registriert.":
        _em.includes("Password should be")||_em.includes("password")?"Passwort zu schwach (mind. 6 Zeichen).":
        _em.includes("valid email")||_em.includes("invalid format")||_em.includes("Unable to validate email")?"Bitte eine gültige E-Mail-Adresse eingeben.":
        _em.includes("rate limit")||_em.includes("too many")?"Zu viele Versuche. Bitte kurz warten.":
        _em||"Registrierung fehlgeschlagen.";
      S.authLoading=false;render();return;
    }
    const uid=data.user?.id;
    if(!uid){S.authError="Registrierung fehlgeschlagen.";S.authLoading=false;render();return;}
    // Save username locally immediately
    try{localStorage.setItem("gq_username",uname);}catch(e){}
    // Upsert profile (fire & forget errors)
    const{error:_upErr}=await sb.from("profiles").upsert({id:uid,username:uname});
    sbUser=data.user;
    sbProfile={...(sbProfile||{}),username:uname,geo_coins:100,id:uid};
    if(data.session)sb.rpc("add_coins",{p_user_id:uid,p_amount:100}).then(()=>{},()=>{});
    // Migrate guest data in background (don't await to avoid hanging)
    migrateGuestToAccount(uid).catch(()=>{});
    S.authLoading=false;S.authEmail="";S.authPassword="";S.authConfirm="";S.authUsername="";S.authError="";
    // If email confirmation required (session is null), show info message
    if(!data.session){
      showToast("\uD83D\uDCE7 Best\u00e4tigungsmail gesendet! Bitte E-Mail pr\u00fcfen.");
    } else {
      showToast("\uD83C\uDF89 Willkommen, "+uname+"! Fortschritt gesichert.");
      // Full profile load only if already confirmed
      loadProfile().catch(()=>{});
    }
    render();
  }catch(err){
    const _em=err.message||"";
    S.authError=
      _em.includes("already registered")||_em.includes("already been registered")?"Diese E-Mail ist bereits registriert.":
      _em.includes("valid email")||_em.includes("invalid format")?"Bitte eine gültige E-Mail-Adresse eingeben.":
      _em||"Unbekannter Fehler.";
    S.authLoading=false;
    render();
  }
}

/* Phase 27: Login */
async function doLogin(){
  if(!sb){showToast("Supabase nicht verbunden");return;}
  const email=S.authEmail.trim();
  const pw=S.authPassword;
  if(!email||!pw){S.authError="E-Mail und Passwort eingeben.";render();return;}
  S.authLoading=true;S.authError="";render();
  const{data,error}=await sb.auth.signInWithPassword({email,password:pw});
  if(error){S.authError=error.message==="Invalid login credentials"?"E-Mail oder Passwort falsch.":error.message;S.authLoading=false;render();return;}
  sbUser=data.user;
  await loadProfile();
  S.authLoading=false;S.authEmail="";S.authPassword="";S.authConfirm="";S.authError="";
  S.tab="home";
  render();
}

/* Phase 27: Logout */
async function doLogout(){
  if(!sb)return;
  await sb.auth.signOut();
  sbUser=null;sbProfile=null;sbStamps=new Set();
  try{localStorage.removeItem("gq_username");}catch(e){}
  /* Reset UI state — prevents stale mid-game or modal views after logout */
  S.ph="menu";S.tab="home";S.mpModal=false;S.payModal=false;S.lockModal=null;
  S.authEmail="";S.authPassword="";S.authConfirm="";S.authError="";
  const{data}=await sb.auth.signInAnonymously();
  if(data)sbUser=data.user;
  render();
}
async function saveSession(mode,score,bs,correct,durationMs){
  /* Sanity-cap score before submitting — max honest = ROUNDS*(BASE+12*TB)*3*3 */
  const _maxScore=Math.ceil(ROUNDS*(BASE+12*TB)*3*3*1.1);
  score=Math.min(score,_maxScore);
  bs=Math.min(bs,ROUNDS);
  correct=Math.min(correct,ROUNDS);
  /* Phase 33 Teil 2: notify opponent at game end */
  if(window.mpGameCh&&S.mpOpponent){
    window.mpGameCh.send({type:"broadcast",event:"game_over",
      payload:{score,name:sbProfile?.username||"Ich",correct}}).then(()=>{},()=>{});
    window.mpGameCh=null;
  }
  if(!sb||!sbUser?.id)return;
  await sb.from("game_sessions").insert({user_id:sbUser.id,mode,score,best_streak:bs,rounds:ROUNDS,accuracy:Math.round(correct/ROUNDS*100),username:sbProfile?.username||null});
  /* Use RPC to prevent client-side score tampering */
  await sb.rpc("add_score",{p_user_id:sbUser.id,p_score:score,p_coins:Math.floor(score/100),p_rounds:ROUNDS,p_duration_ms:durationMs||0});
  if(sbProfile){sbProfile.total_score=(sbProfile.total_score||0)+score;sbProfile.games_played=(sbProfile.games_played||0)+1;}
}
async function fetchLeaderboard(mode){
  if(\!sb)return[];
  const{data}=await sb.from("leaderboard_weekly").select("*").eq("mode",mode).order("rank",{ascending:true}).limit(30);
  return data||[];
}

/* MASTERY */
function loadMastery(){return _gqLoad("gq_mastery",{});}
function saveMastery(d){_gqSave("gq_mastery",d);}
function getMasteryRank(v,p){if(v>=15||p>=3)return"gold";if(v>=5||p>=1)return"silver";if(v>=1)return"bronze";return null;}
function getTravelRank(n){return n>=50?"Weltbuerger":n>=30?"Globetrotter":n>=15?"Weltenbummler":n>=5?"Reisender":"Einheimischer";}
function checkMastery(){
  const mastery=loadMastery();const answers=S.sessionAnswers||[];const isPerfect=S.correct===ROUNDS;
  const newlyUnlocked=[];
  const seen=new Set();
  answers.forEach(a=>{
    if(\!a.cc||\!a.correct)return;
    if(\!mastery[a.cc])mastery[a.cc]={v:0,p:0};
    mastery[a.cc].v++;
    if(isPerfect&&\!seen.has(a.cc)){mastery[a.cc].p++;seen.add(a.cc);}
  });
  if(isPerfect){
    const uniqueCC=[...new Set(answers.filter(a=>a.correct&&a.cc).map(a=>a.cc))];
    uniqueCC.forEach(cc=>{
      const m=mastery[cc];const rank=getMasteryRank(m.v,m.p);
      if(rank)newlyUnlocked.push({cc,rank});
      if(sbOK&&sbUser)syncStampSupabase(cc,true);
    });
  }else if(sbOK&&sbUser){
    const uniqueCC=[...new Set(answers.filter(a=>a.correct&&a.cc).map(a=>a.cc))];
    uniqueCC.forEach(cc=>syncStampSupabase(cc,false));
  }
  saveMastery(mastery);S.newStamps=newlyUnlocked;
}
function syncStampSupabase(cc,perfect){
  if(\!sb||\!sbUser)return;
  sb.rpc("upsert_stamp",{p_user_id:sbUser.id,p_country_code:cc,p_perfect:perfect}).then(()=>{},()=>{});
}

/* AUDIO */
let audioCtx=null,soundOn=true;
const SVG_VOL_ON=`<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/></svg>`;
const SVG_VOL_OFF=`<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/></svg>`;
function toggleSound(){soundOn=\!soundOn;document.getElementById("soundBtn").innerHTML=soundOn?SVG_VOL_ON:SVG_VOL_OFF;}
function getCtx(){if(\!audioCtx)audioCtx=new(window.AudioContext||window.webkitAudioContext)();if(audioCtx.state==="suspended")audioCtx.resume();return audioCtx;}
function playTone(f,type,dur,vol=0.2){if(\!soundOn)return;try{const c=getCtx(),o=c.createOscillator(),g=c.createGain();o.connect(g);g.connect(c.destination);o.type=type;o.frequency.setValueAtTime(f,c.currentTime);g.gain.setValueAtTime(vol,c.currentTime);g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+dur);o.start(c.currentTime);o.stop(c.currentTime+dur);}catch(e){}}
function soundCorrect(){[523,659,784].forEach((f,i)=>setTimeout(()=>playTone(f,"sine",.18,.2),i*60));}
function soundWrong(){playTone(300,"sawtooth",.15,.18);setTimeout(()=>playTone(220,"sawtooth",.2,.15),80);}
function soundStreak(l){if(\!soundOn)return;if(l>=10)[523,659,784,1047].forEach((f,i)=>setTimeout(()=>playTone(f,"sine",.25,.2),i*55));else if(l>=5)[523,659,784].forEach((f,i)=>setTimeout(()=>playTone(f,"triangle",.2,.18),i*60));else[523,659].forEach((f,i)=>setTimeout(()=>playTone(f,"sine",.15,.15),i*70));}
function soundWarn(){playTone(440,"square",.08,.1);}
function soundOver(){[392,330,262].forEach((f,i)=>setTimeout(()=>playTone(f,"sawtooth",.3,.2),i*120));}
function soundStamp(){[880,1047,1320].forEach((f,i)=>setTimeout(()=>playTone(f,"sine",.15,.15),i*80));}

/* STATE */
let S={
  ph:"menu",tab:"home",mode:"city",diff:"casual",
  sc:0,st:0,bs:0,rd:0,correct:0,tm:12,dur:12,
  q:null,sel:null,ok:null,pts:0,lid:null,
  lbData:[],lbLoading:false,scoreSaved:false,newUsername:"",
  sessionAnswers:[],newStamps:[],modal:null,
  obStep:-1,obLang:"de",obDiff:"casual",
  payModal:false,mpModal:false,mp:null,
  challenge:null,challengeSeed:null,
  pwaPrompt:null,
  lockModal:null,
  dailyDone:false,
  isDailyRun:false,
  challengeStarted:false,
  half_removed:false,
  freezeActive:false,
  filter:"all",
  fcIdx:0,fcFlipped:false,fcSearch:"",fcCountry:"all",
  darkMode:false,
  authMode:"login",authEmail:"",authPassword:"",authConfirm:"",authUsername:"",authError:"",authLoading:false,
  settingsModal:false,
  convModal:false,
  collectedPlates:loadCollectedPlates(),
  ligaData:[],ligaLoading:false,
  titleShop:false,
  language:localStorage.getItem("gq_lang")||"de",spotterInput:"",spotterMsg:"",spotterOk:null,albumView:"list",albumCountry:_smartDefaultCountry(),spotterCountry:_smartDefaultCountry(),
  collFilter:"all",collRarity:"all",collSearch:"",
};
let tIv=null,fTo=null,toastTo=null;

/* ── Phase 42: Anti-Cheat — Proxy wrapper for S in console ── */
(function(){
  const GUARDED=new Set(["sc","correct","st","bs","pts","collectedPlates","sbProfile"]);
  if(typeof Proxy==="undefined")return;
  try{
    const _real=S;
    const _p=new Proxy(_real,{
      set(t,k,v){
        if(GUARDED.has(k)){
          /* Check if call is from our own code (has game functions in stack) */
          const stk=(new Error()).stack||"";
          const trusted=["answer","startGame","mpCountdown","lq","nextRound",
            "checkMastery","spotterCollect","saveSession","loadData","initAuth"];
          const ok=trusted.some(fn=>stk.includes(fn));
          if(!ok){
            console.warn("%c🚫 GeoQuest: Schummeln erkannt! Feld '"+k+"' ist geschützt.",
              "color:#ef4444;font-weight:bold;font-size:14px");
            return true; /* silent block */
          }
        }
        t[k]=v;return true;
      }
    });
    /* Shadow window.S with the guarded proxy */
    Object.defineProperty(window,"S",{get:()=>_p,configurable:false,enumerable:false});
  }catch(e){}
})();


/* DARK MODE */
function applyTheme(){
  document.documentElement.setAttribute("data-theme",S.darkMode?"dark":"");
  try{localStorage.setItem("gq_dark",S.darkMode?"1":"0");}catch(e){}
}
(function initTheme(){try{S.darkMode=localStorage.getItem("gq_dark")==="1";}catch(e){}applyTheme();})();

/* HELPERS */
function sh(a){const b=[...a];for(let i=b.length-1;i>0;i--){const j=~~(Math.random()*(i+1));[b[i],b[j]]=[b[j],b[i]];}return b;}
function tier(s){return TIERS.find(t=>s>=t.m)||TIERS[3];}
function tc(){return S.tm>6?"#10b981":S.tm>3?"#f59e0b":"#ef4444";}
function pct(){return(S.tm/S.dur)*100;}
function showToast(msg){
  const old=document.getElementById("copy-toast");if(old)old.remove();
  const el=document.createElement("div");el.id="copy-toast";el.className="copy-toast";el.textContent=msg;
  document.body.appendChild(el);setTimeout(()=>el.remove(),2200);
}
function distractors(pool,matchFn,excludeFn,keyFn,n=2){
  const pref=pool.filter(x=>matchFn(x)&&\!excludeFn(x));
  const dp=pref.length>=n?pref:pool.filter(x=>\!excludeFn(x));
  const seen=new Set(),dis=[];
  for(const x of sh([...dp])){const k=keyFn(x);if(k\!==undefined&&\!seen.has(k)){seen.add(k);dis.push(k);if(dis.length===n)break;}}
  if(dis.length<n){for(const x of sh([...pool])){const k=keyFn(x);if(\!excludeFn(x)&&\!seen.has(k)){seen.add(k);dis.push(k);if(dis.length===n)break;}}}
  return dis;
}

/* GENERATORS */
function genCityQ(){
  const pf=S.diff==="hardcore"?0:200000;
  const pool=_rfilt(CITIES.filter(c=>c.pop>=pf&&c.id\!==S.lid),3);
  if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sub===cor.sub||x.cont===cor.cont,x=>x.c===cor.c,x=>x.c);
  return{type:"city",prompt:t("q_city"),subj:cor.n,ans:cor.c,opts:sh([cor.c,...dis]),meta:cor.cont+" \u00b7 "+(cor.pop/1e6).toFixed(1)+" Mio.",lid:cor.id,cc:cor.cc};
}
function genFlagQ(){
  const pool=_rfilt(COUNTRIES.filter(x=>x.cc\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sr===cor.sr||x.ct===cor.ct,x=>x.c===cor.c,x=>x.c);
  return{type:"flag",prompt:t("q_flag"),subj:cor.cc,ans:cor.c,opts:sh([cor.c,...dis]),meta:cor.ct,lid:cor.cc,cc:cor.cc};
}
function genCapitalQ(){
  const pool=_rfilt(CAPITALS.filter(x=>x.capital\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.country===cor.country,x=>x.country);
  return{type:"capital",prompt:t("q_capital"),subj:cor.capital,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.capital,cc:cor.cc};
}
/* Phase 62: region filter helpers */
function _regionOk(cc,cont){
  const f=S.filter;
  if(f==="all"||f==="eu_plates")return true;
  const c=cont||(COUNTRIES.find(x=>x.cc===cc)||{}).ct||"";
  if(f==="europe")return c==="Europe";
  if(f==="africa")return c==="Africa";
  if(f==="oceania")return c==="Oceania";
  if(f==="asia")return c==="Asia";
  if(f==="america")return c.includes("America");
  return true;
}
function _rfilt(pool,minLen){
  if(S.filter==="all"||S.filter==="eu_plates")return pool;
  const f=pool.filter(x=>_regionOk(x.cc,x.continent||x.ct||x.cont));
  return f.length>=minLen?f:pool;
}
/* Phase 62: region filter helpers */
function _regionOk(cc,cont){
  const f=S.filter;
  if(f==="all"||f==="eu_plates")return true;
  const c=cont||(COUNTRIES.find(x=>x.cc===cc)||{}).ct||"";
  if(f==="europe")return c==="Europe";
  if(f==="africa")return c==="Africa";
  if(f==="oceania")return c==="Oceania";
  if(f==="asia")return c==="Asia";
  if(f==="america")return c.includes("America");
  return true;
}
function _rfilt(pool,minLen){
  if(S.filter==="all"||S.filter==="eu_plates")return pool;
  const f=pool.filter(x=>_regionOk(x.cc,x.continent||x.ct||x.cont));
  return f.length>=minLen?f:pool;
}
/* Phase 62: region filter helpers */
function _regionOk(cc,cont){
  const f=S.filter;
  if(f==="all"||f==="eu_plates")return true;
  const c=cont||(COUNTRIES.find(x=>x.cc===cc)||{}).ct||"";
  if(f==="europe")return c==="Europe";
  if(f==="africa")return c==="Africa";
  if(f==="oceania")return c==="Oceania";
  if(f==="asia")return c==="Asia";
  if(f==="america")return c.includes("America");
  return true;
}
function _rfilt(pool,minLen){
  if(S.filter==="all"||S.filter==="eu_plates")return pool;
  const f=pool.filter(x=>_regionOk(x.cc,x.continent||x.ct||x.cont));
  return f.length>=minLen?f:pool;
}
/* Phase 62: region filter helpers */
function _regionOk(cc,cont){
  const f=S.filter;
  if(f==="all"||f==="eu_plates")return true;
  const c=cont||(COUNTRIES.find(x=>x.cc===cc)||{}).ct||"";
  if(f==="europe")return c==="Europe";
  if(f==="africa")return c==="Africa";
  if(f==="oceania")return c==="Oceania";
  if(f==="asia")return c==="Asia";
  if(f==="america")return c.includes("America");
  return true;
}
function _rfilt(pool,minLen){
  if(S.filter==="all"||S.filter==="eu_plates")return pool;
  const f=pool.filter(x=>_regionOk(x.cc,x.continent||x.ct||x.cont));
  return f.length>=minLen?f:pool;
}
/* Phase 62: region filter helpers */
function _regionOk(cc,cont){
  const f=S.filter;
  if(f==="all"||f==="eu_plates")return true;
  const c=cont||(COUNTRIES.find(x=>x.cc===cc)||{}).ct||"";
  if(f==="europe")return c==="Europe";
  if(f==="africa")return c==="Africa";
  if(f==="oceania")return c==="Oceania";
  if(f==="asia")return c==="Asia";
  if(f==="america")return c.includes("America");
  return true;
}
function _rfilt(pool,minLen){
  if(S.filter==="all"||S.filter==="eu_plates")return pool;
  const f=pool.filter(x=>_regionOk(x.cc,x.continent||x.ct||x.cont));
  return f.length>=minLen?f:pool;
}
/* Phase 62: region filter helpers */
function _regionOk(cc,cont){
  const f=S.filter;
  if(f==="all"||f==="eu_plates")return true;
  const c=cont||(COUNTRIES.find(x=>x.cc===cc)||{}).ct||"";
  if(f==="europe")return c==="Europe";
  if(f==="africa")return c==="Africa";
  if(f==="oceania")return c==="Oceania";
  if(f==="asia")return c==="Asia";
  if(f==="america")return c.includes("America");
  return true;
}
function _rfilt(pool,minLen){
  if(S.filter==="all"||S.filter==="eu_plates")return pool;
  const f=pool.filter(x=>_regionOk(x.cc,x.continent));
  return f.length>=minLen?f:pool;
}
function genRiverQ(){
  const pool=_rfilt(RIVERS.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(COUNTRIES,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"river",prompt:t("q_river"),subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genLandmarkQ(){
  const pool=_rfilt(LANDMARKS.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(COUNTRIES,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"landmark",prompt:t("q_landmark"),subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genParkQ(){
  const pool=_rfilt(NATIONAL_PARKS.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(COUNTRIES,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"park",prompt:t("q_park"),subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genUnescoQ(){
  const pool=_rfilt(UNESCO_SITES.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(COUNTRIES,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"unesco",prompt:t("q_unesco"),subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genCitymarkQ(){
  const pool=_rfilt(CITY_LANDMARKS.filter(x=>x.name\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(CITY_LANDMARKS,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.city===cor.city,x=>x.city);
  return{type:"citymark",prompt:t("q_citymark"),subj:cor.name,ans:cor.city,opts:sh([cor.city,...dis]),meta:cor.country,lid:cor.name,cc:cor.cc};
}
function genSubwayQ(){
  const pool=_rfilt(SUBWAYS.filter(x=>x.city\!==S.lid),3);if(pool.length<3)return null;
  const t=Math.floor(rng()*2);
  const cor=pool[~~(rng()*pool.length)];
  const dis3=distractors(pool,x=>x.country===cor.country||x.cc===cor.cc,x=>x.city===cor.city,x=>t===0?x.km:x.lines,2);
  const ansVal=t===0?cor.km:cor.lines;
  const prompt=t===0?"Wie lang ist das U-Bahn-Netz in \u2026 (km)?":"Wie viele U-Bahn-Linien hat \u2026?";
  const suffix=t===0?" km":" Linien";
  return{type:"subway",prompt,subj:cor.city,ans:String(ansVal),opts:sh([String(ansVal),...dis3.map(String)]),meta:cor.country+" \u00b7 "+suffix.trim(),lid:cor.city,cc:cor.cc};
}
function genFlagselQ(){
  const pool=_rfilt(COUNTRIES.filter(x=>x.cc\!==S.lid),4);if(pool.length<4)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sr===cor.sr||x.ct===cor.ct,x=>x.cc===cor.cc,x=>x.cc,3);
  return{type:"flagsel",prompt:t("q_flagsel"),subj:cor.c,ans:cor.cc,opts:sh([cor.cc,...dis]),meta:cor.ct,lid:cor.cc,cc:cor.cc};
}
function genRcapitalQ(){
  const pool=_rfilt(CAPITALS.filter(x=>x.country\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.capital===cor.capital,x=>x.capital);
  return{type:"rcapital",prompt:t("q_rcapital"),subj:cor.country,ans:cor.capital,opts:sh([cor.capital,...dis]),meta:cor.continent,lid:cor.country,cc:cor.cc};
}
function genRcityQ(){
  const pool=_rfilt(COUNTRIES.filter(x=>x.c\!==S.lid),3);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const cc2=CITIES.filter(c=>c.c===cor.c);if(\!cc2.length)return genRcityQ();
  const corCity=cc2[~~(rng()*cc2.length)];
  const dis=distractors(CITIES,x=>x.sub===corCity.sub||x.cont===corCity.cont,x=>x.c===cor.c,x=>x.n);
  return{type:"rcity",prompt:t("q_rcity"),subj:cor.c,ans:corCity.n,opts:sh([corCity.n,...dis]),meta:cor.ct,lid:cor.c,cc:cor.cc};
}
function genRriverQ(){
  const ctries=[...new Set(RIVERS.map(r=>r.country))].filter(c=>c\!==S.lid);if(\!ctries.length)return null;
  const corC=ctries[~~(rng()*ctries.length)];
  const cRivers=RIVERS.filter(r=>r.country===corC);
  const cor=cRivers[~~(rng()*cRivers.length)];
  const dis=distractors(RIVERS,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.country===corC,x=>x.name);
  return{type:"rriver",prompt:t("q_rriver"),subj:corC,ans:cor.name,opts:sh([cor.name,...dis]),meta:cor.continent,lid:corC,cc:cor.cc};
}
function genFoodQ(){
  if(\!FOOD_DATA.length)return null;
  const _fp=_rfilt(FOOD_DATA,3);const item=_fp[~~(rng()*_fp.length)];
  const corC=item.country;
  const dis=FOOD_DATA.filter(f=>f.country\!==corC).map(f=>f.country);
  const uniq=[...new Set(dis)];const picked=sh(uniq).slice(0,3);
  return{type:"food",prompt:t("q_food"),subj:item.dish,emoji:item.emoji,ans:corC,opts:sh([corC,...picked]),lid:item.cc,cc:item.cc};
}
function genBrandQ(){
  if(\!BRANDS_DATA.length)return null;
  const _bp=_rfilt(BRANDS_DATA,3);const item=_bp[~~(rng()*_bp.length)];
  const corC=item.country;
  const sameSub=BRANDS_DATA.filter(b=>b.sub===item.sub&&b.country\!==corC).map(b=>b.country);
  const fallback=BRANDS_DATA.filter(b=>b.country\!==corC).map(b=>b.country);
  const pool=[...new Set(sameSub.length>=3?sameSub:fallback)];
  const picked=sh(pool).slice(0,3);
  return{type:"brand",prompt:t("q_brand"),subj:item.brand,industry:item.industry,ans:corC,opts:sh([corC,...picked]),lid:item.cc,cc:item.cc};
}
function genCurrencyQ(){
  if(\!CURRENCIES_DATA.length)return null;
  const _cp=_rfilt(CURRENCIES_DATA,3);const item=_cp[~~(rng()*_cp.length)];
  const corC=item.country;
  const sameSub=CURRENCIES_DATA.filter(c=>c.sub===item.sub&&c.country\!==corC).map(c=>c.country);
  const fallback=CURRENCIES_DATA.filter(c=>c.country\!==corC).map(c=>c.country);
  const pool=[...new Set(sameSub.length>=3?sameSub:fallback)];
  const picked=sh(pool).slice(0,3);
  return{type:"currency",prompt:t("q_currency"),subj:item.currency,symbol:item.symbol,ans:corC,opts:sh([corC,...picked]),lid:item.cc,cc:item.cc};
}
function genOutlineQ(){
  const pool=_rfilt(COUNTRIES.filter(c=>c.cc&&c.cc.length===2),4);
  if(pool.length<4)return null;
  const sh2=arr=>{const a=[...arr];for(let i=a.length-1;i>0;i--){const j=~~(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
  const idx=~~(rng()*pool.length);const item=pool[idx];
  const corC=item.c;const corCC=item.cc;
  const dis=pool.filter(c=>c.cc\!==corCC).map(c=>c.c);
  const picked=sh2(dis).slice(0,3);
  return{type:"outline",prompt:t("q_outline"),subj:corCC,ans:corC,opts:sh2([corC,...picked]),lid:corCC,cc:corCC};
}
/* EU-KENNZEICHEN GENERATORS (Phase 23B) — smart same-country distractors */
function genPlateQ(hardcore){
  const pool=PLATES_DATA;
  if(\!pool||pool.length<5)return null;
  const cor=pool[~~(rng()*pool.length)];
  const sameCountry=pool.filter(p=>p.country===cor.country&&p.region\!==cor.region);
  const disPool=sameCountry.length>=3?sameCountry:pool.filter(p=>p.region\!==cor.region);
  const picked=sh([...disPool]).slice(0,3).map(p=>p.region);
  const opts=sh([cor.region,...picked]);
  const cc_map={Deutschland:"de",Österreich:"at",Schweiz:"ch",Polen:"pl",Frankreich:"fr",Italien:"it",Rumänien:"ro"};
  const cc=cc_map[cor.country]||"de";
  return{
    type:hardcore?"plate_hard":"plate_casual",
    prompt:hardcore?t("q_plates_hard"):t("q_plates_casual"),
    subj:cor.code,
    ans:cor.region,
    opts,
    meta:hardcore?"":cor.country+(cor.state?" \u00b7 "+cor.state:""),
    plateCountry:cor.country,
    lid:cor.code,
    cc,
  };
}

/* Phase 34: Map quiz countries */
const MAP_COUNTRIES=[{"cc":"fj","name":"Fiji"},{"cc":"tz","name":"Tanzania"},{"cc":"ca","name":"Canada"},{"cc":"us","name":"United States of America"},{"cc":"kz","name":"Kazakhstan"},{"cc":"uz","name":"Uzbekistan"},{"cc":"pg","name":"Papua New Guinea"},{"cc":"id","name":"Indonesia"},{"cc":"ar","name":"Argentina"},{"cc":"cl","name":"Chile"},{"cc":"cd","name":"Dem. Rep. Congo"},{"cc":"so","name":"Somalia"},{"cc":"ke","name":"Kenya"},{"cc":"sd","name":"Sudan"},{"cc":"td","name":"Chad"},{"cc":"ht","name":"Haiti"},{"cc":"do","name":"Dominican Rep."},{"cc":"ru","name":"Russia"},{"cc":"bs","name":"Bahamas"},{"cc":"no","name":"Norway"},{"cc":"za","name":"South Africa"},{"cc":"ls","name":"Lesotho"},{"cc":"mx","name":"Mexico"},{"cc":"uy","name":"Uruguay"},{"cc":"br","name":"Brazil"},{"cc":"bo","name":"Bolivia"},{"cc":"pe","name":"Peru"},{"cc":"co","name":"Colombia"},{"cc":"pa","name":"Panama"},{"cc":"cr","name":"Costa Rica"},{"cc":"ni","name":"Nicaragua"},{"cc":"hn","name":"Honduras"},{"cc":"sv","name":"El Salvador"},{"cc":"gt","name":"Guatemala"},{"cc":"bz","name":"Belize"},{"cc":"ve","name":"Venezuela"},{"cc":"gy","name":"Guyana"},{"cc":"sr","name":"Suriname"},{"cc":"fr","name":"France"},{"cc":"ec","name":"Ecuador"},{"cc":"jm","name":"Jamaica"},{"cc":"cu","name":"Cuba"},{"cc":"zw","name":"Zimbabwe"},{"cc":"bw","name":"Botswana"},{"cc":"na","name":"Namibia"},{"cc":"sn","name":"Senegal"},{"cc":"ml","name":"Mali"},{"cc":"mr","name":"Mauritania"},{"cc":"bj","name":"Benin"},{"cc":"ne","name":"Niger"},{"cc":"ng","name":"Nigeria"},{"cc":"cm","name":"Cameroon"},{"cc":"tg","name":"Togo"},{"cc":"gh","name":"Ghana"},{"cc":"ci","name":"Côte d'Ivoire"},{"cc":"gn","name":"Guinea"},{"cc":"gw","name":"Guinea-Bissau"},{"cc":"lr","name":"Liberia"},{"cc":"sl","name":"Sierra Leone"},{"cc":"bf","name":"Burkina Faso"},{"cc":"cf","name":"Central African Rep."},{"cc":"cg","name":"Congo"},{"cc":"ga","name":"Gabon"},{"cc":"gq","name":"Eq. Guinea"},{"cc":"zm","name":"Zambia"},{"cc":"mw","name":"Malawi"},{"cc":"mz","name":"Mozambique"},{"cc":"sz","name":"eSwatini"},{"cc":"ao","name":"Angola"},{"cc":"bi","name":"Burundi"},{"cc":"il","name":"Israel"},{"cc":"lb","name":"Lebanon"},{"cc":"mg","name":"Madagascar"},{"cc":"ps","name":"Palestine"},{"cc":"gm","name":"Gambia"},{"cc":"tn","name":"Tunisia"},{"cc":"dz","name":"Algeria"},{"cc":"jo","name":"Jordan"},{"cc":"ae","name":"United Arab Emirates"},{"cc":"qa","name":"Qatar"},{"cc":"kw","name":"Kuwait"},{"cc":"iq","name":"Iraq"},{"cc":"om","name":"Oman"},{"cc":"vu","name":"Vanuatu"},{"cc":"kh","name":"Cambodia"},{"cc":"th","name":"Thailand"},{"cc":"la","name":"Laos"},{"cc":"mm","name":"Myanmar"},{"cc":"vn","name":"Vietnam"},{"cc":"kp","name":"North Korea"},{"cc":"kr","name":"South Korea"},{"cc":"mn","name":"Mongolia"},{"cc":"in","name":"India"},{"cc":"bd","name":"Bangladesh"},{"cc":"bt","name":"Bhutan"},{"cc":"np","name":"Nepal"},{"cc":"pk","name":"Pakistan"},{"cc":"af","name":"Afghanistan"},{"cc":"tj","name":"Tajikistan"},{"cc":"kg","name":"Kyrgyzstan"},{"cc":"tm","name":"Turkmenistan"},{"cc":"ir","name":"Iran"},{"cc":"sy","name":"Syria"},{"cc":"am","name":"Armenia"},{"cc":"se","name":"Sweden"},{"cc":"by","name":"Belarus"},{"cc":"ua","name":"Ukraine"},{"cc":"pl","name":"Poland"},{"cc":"at","name":"Austria"},{"cc":"hu","name":"Hungary"},{"cc":"md","name":"Moldova"},{"cc":"ro","name":"Romania"},{"cc":"lt","name":"Lithuania"},{"cc":"lv","name":"Latvia"},{"cc":"ee","name":"Estonia"},{"cc":"de","name":"Germany"},{"cc":"bg","name":"Bulgaria"},{"cc":"gr","name":"Greece"},{"cc":"tr","name":"Turkey"},{"cc":"al","name":"Albania"},{"cc":"hr","name":"Croatia"},{"cc":"ch","name":"Switzerland"},{"cc":"lu","name":"Luxembourg"},{"cc":"be","name":"Belgium"},{"cc":"nl","name":"Netherlands"},{"cc":"pt","name":"Portugal"},{"cc":"es","name":"Spain"},{"cc":"ie","name":"Ireland"},{"cc":"nz","name":"New Zealand"},{"cc":"au","name":"Australia"},{"cc":"lk","name":"Sri Lanka"},{"cc":"cn","name":"China"},{"cc":"tw","name":"Taiwan"},{"cc":"it","name":"Italy"},{"cc":"dk","name":"Denmark"},{"cc":"gb","name":"United Kingdom"},{"cc":"is","name":"Iceland"},{"cc":"az","name":"Azerbaijan"},{"cc":"ge","name":"Georgia"},{"cc":"ph","name":"Philippines"},{"cc":"my","name":"Malaysia"},{"cc":"bn","name":"Brunei"},{"cc":"si","name":"Slovenia"},{"cc":"fi","name":"Finland"},{"cc":"sk","name":"Slovakia"},{"cc":"cz","name":"Czechia"},{"cc":"er","name":"Eritrea"},{"cc":"jp","name":"Japan"},{"cc":"py","name":"Paraguay"},{"cc":"ye","name":"Yemen"},{"cc":"sa","name":"Saudi Arabia"},{"cc":"cy","name":"Cyprus"},{"cc":"ma","name":"Morocco"},{"cc":"eg","name":"Egypt"},{"cc":"ly","name":"Libya"},{"cc":"et","name":"Ethiopia"},{"cc":"dj","name":"Djibouti"},{"cc":"ug","name":"Uganda"},{"cc":"rw","name":"Rwanda"},{"cc":"ba","name":"Bosnia and Herz."},{"cc":"mk","name":"Macedonia"},{"cc":"rs","name":"Serbia"},{"cc":"me","name":"Montenegro"},{"cc":"tt","name":"Trinidad and Tobago"},{"cc":"ss","name":"S. Sudan"}];

function genMapGuessQ(){
  if(\!MAP_COUNTRIES.length)return null;
  const idx=~~(Math.random()*MAP_COUNTRIES.length);
  const co=MAP_COUNTRIES[idx];if(\!co)return null;
  return{type:"map_guess",prompt:t("q_map_guess"),subj:co.name,
    ans:co.name,opts:[],meta:"",lid:co.cc,cc:co.cc};
}
const GEN={
  city:genCityQ,flag:genFlagQ,capital:genCapitalQ,river:genRiverQ,
  landmark:genLandmarkQ,park:genParkQ,unesco:genUnescoQ,citymark:genCitymarkQ,
  subway:genSubwayQ,flagsel:genFlagselQ,rcapital:genRcapitalQ,rcity:genRcityQ,
  rriver:genRriverQ,outline:genOutlineQ,food:genFoodQ,brand:genBrandQ,currency:genCurrencyQ,
  plate_casual:()=>genPlateQ(false),
  plate_hard:()=>genPlateQ(true),
  curr_real:genCurrRealQ,
  pop_compare:genPopCompareQ,
  river_real:genRiverRealQ,
  hl_pop:genHLPopQ,
  hl_river:genHLRiverQ,
  hl_area:genHLAreaQ,
  neighbor:genNeighborQ,
  map_guess:genMapGuessQ,
};

/* GAME LOOP */
function clr(){clearInterval(tIv);clearTimeout(fTo);}
function nextRound(){
  clr();
  const nr=S.rd+1;
  if(S.diff!=="survival"&&nr>=ROUNDS){
    S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();
    if(S.isDailyRun&&!isDailyDone()){markDailyDone(S.sc);if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+100;if(sb&&sbUser)sb.rpc("add_coins",{p_user_id:sbUser.id,p_amount:100}).then(r=>{if(r.data!=null&&sbProfile)sbProfile.geo_coins=r.data;},()=>{});}
    saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:ROUNDS,date:Date.now(),answers:S.sessionAnswers.map(a=>({cc:a.cc,correct:a.correct}))});
    if(sbOK)saveSession(S.mode,S.sc,S.bs,S.correct,Date.now()-(S.gameStartTime||Date.now())).then(()=>{S.scoreSaved=true;render();});
    render();
  }else{S.rd=nr;lq();}
}
function lq(){
  if(\!S.queueExtra)S.queueExtra=[];
  if(\!S.askedLids)S.askedLids=new Set();
  const dur=(S.diff==="hardcore"||S.diff==="survival")?8:12;
  /* Try up to 25 times to get a question whose lid hasn't appeared this round */
  let q=null,_att=0;
  while(_att<25){
    const _c=(GEN[S.mode]||genCityQ)();
    if(_c&&\!S.askedLids.has(_c.lid)){q=_c;break;}
    _att++;
  }
  /* Fallback: accept any valid question if pool is exhausted */
  if(\!q)q=(GEN[S.mode]||genCityQ)()||null;
  /* Duolingo casual: once normal round exhausted, pull retries */
  if(\!q&&S.diff==="casual"&&S.queueExtra.length>0)q=S.queueExtra.shift();
  if(\!q){S.ph="menu";render();return;}
  S.askedLids.add(q.lid);
  S.q=q;S.tm=dur;S.dur=dur;S.sel=null;S.ok=null;S.ph="playing";
  S.half_removed=false;S.freezeActive=false;
  render();
  tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();if(S.tm<=0){clearInterval(tIv);answer(null);}else render();},1000);
}

/* ── Phase 42: Index-based answer dispatch (hides answer strings from DOM) ── */
function answerByIdx(i){
  if(!S.q||!S.q.opts||i<0||i>=S.q.opts.length)return;
  answer(S.q.opts[i]);
}
function answer(a){
  if(S.sel\!==null)return;clr();
  const ok=a===S.q.ans;
  S.sel=a||"__t";S.ok=ok;
  if(S.q.cc)S.sessionAnswers.push({cc:S.q.cc,correct:ok});
  let pts=0;
  if(ok){const ns=S.st+1,t=tier(ns);const mm=S.diff==="hardcore"?3:S.diff==="survival"?2:1;pts=~~((BASE+S.tm*TB)*t.x*mm);S.sc+=pts;S.st=ns;S.bs=Math.max(S.bs,ns);S.correct++;soundCorrect();if(ns>=3)setTimeout(()=>soundStreak(ns),250);showPtsPopup(pts);if(navigator.vibrate)navigator.vibrate([50]);}
  else{S.st=0;soundWrong();if(navigator.vibrate)navigator.vibrate([100,50,100]);
    /* Survival: instant death on first wrong answer */
    if(S.diff==="survival"){
      clr();
      const sb_prev=parseInt(localStorage.getItem('gq_surv_best')||'0');
      const survived=S.rd;
      if(survived>sb_prev)localStorage.setItem('gq_surv_best',String(survived));
      S.survivalBest=Math.max(survived,sb_prev);
      S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();
      saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:survived,date:Date.now(),diff:"survival",answers:S.sessionAnswers.map(a=>({cc:a.cc,correct:a.correct}))});
      if(sbOK)saveSession(S.mode,S.sc,S.bs,S.correct,Date.now()-(S.gameStartTime||Date.now())).then(()=>{S.scoreSaved=true;render();});
      if(sb&&sbUser)sb.from("profiles").update({survival_best:Math.max(survived,sbProfile?.survival_best||0)}).eq("id",sbUser.id).then(()=>{},()=>{});
      S.pts=pts;S.lid=S.q.lid;render();
      return;
    }
    /* Duolingo casual: queue wrong question for retry */
    if(S.diff==="casual"&&\!S.q._retry){if(\!S.queueExtra)S.queueExtra=[];S.queueExtra.push({...S.q,_retry:true});}
  }
  /* Phase 43: collect plate with code::country key */
  if(ok&&(S.mode==="plate_casual"||S.mode==="plate_hard")&&S.q.subj){
    const _code=S.q.subj;
    const _pc=PLATES_DATA.find(p=>p.code===_code);
    if(_pc){
      const _key=collKey(_code,_pc.country);
      if(\!S.collectedPlates.includes(_key)){
        S.collectedPlates.push(_key);saveCollectedPlates(S.collectedPlates);
        const _allR=PLATES_DATA.filter(p=>p.code===_code&&p.country===_pc.country);
        showToast("⭐ Neu: "+_code+" — "+_pc.region+(_allR.length>1?" +"+(_allR.length-1)+" weitere":"")+"!");
      }
    }
  }
  S.pts=pts;S.lid=S.q.lid;S.ph="feedback";render();
  /* Phase 33 Teil 2 */
  if(window.mpGameCh&&S.mpOpponent){
    window.mpGameCh.send({type:"broadcast",event:"score_update",
      payload:{score:S.sc,rd:S.rd,correct:S.correct}}).then(()=>{},()=>{});
  }
  fTo=setTimeout(()=>{
    const nr=S.rd+1;
    if(S.diff\!=="survival"&&nr>=ROUNDS){
      S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();
      if(S.isDailyRun&&\!isDailyDone()){
        markDailyDone(S.sc);
        if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+100;
        if(sb&&sbUser)sb.rpc("add_coins",{p_user_id:sbUser.id,p_amount:100}).then(r=>{if(r.data!=null&&sbProfile)sbProfile.geo_coins=r.data;},()=>{});
      }
      saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:ROUNDS,date:Date.now(),answers:S.sessionAnswers.map(a=>({cc:a.cc,correct:a.correct}))});
      if(sbOK)saveSession(S.mode,S.sc,S.bs,S.correct,Date.now()-(S.gameStartTime||Date.now())).then(()=>{S.scoreSaved=true;render();});
      render();
    }else{S.rd=nr;lq();}
  },1700);
}
function startGame(m){
  clr();
  const survBest=parseInt(localStorage.getItem('gq_surv_best')||'0');
  Object.assign(S,{sc:0,st:0,bs:0,rd:0,correct:0,lid:null,ph:"playing",mode:m||S.mode,
    scoreSaved:false,convModal:false,sessionAnswers:[],newStamps:[],isDailyRun:false,challengeStarted:false,
    half_removed:false,freezeActive:false,queueExtra:[],askedLids:new Set(),
    survivalBest:survBest,gameStartTime:Date.now()});
  lq();
}
async function showLeaderboard(){S.ph="menu";S.tab="home";S.lbLoading=true;render();S.lbData=await fetchLeaderboard(S.mode);S.lbLoading=false;render();}

/* UTILS */
function showPtsPopup(pts){const el=document.createElement("div");el.className="pts-popup";el.textContent="+"+pts;el.style.cssText="left:50%;top:40%;transform:translateX(-50%)";document.body.appendChild(el);setTimeout(()=>el.remove(),950);}
function showStampToast(cc){
  clearTimeout(toastTo);const old=document.getElementById("stamp-toast");if(old)old.remove();
  const el=document.createElement("div");el.id="stamp-toast";el.className="stamp-toast";
  const cn=COUNTRIES.find(c=>c.cc===cc)?.c||cc.toUpperCase();
  el.innerHTML=`<img src="https://flagcdn.com/w40/${cc}.png" style="width:22px;height:auto;border-radius:2px"> Neuer Stempel: ${cn}`;
  document.body.appendChild(el);soundStamp();toastTo=setTimeout(()=>el.remove(),3000);
}
function showCopyToast(){
  const old=document.getElementById("copy-toast");if(old)old.remove();
  const el=document.createElement("div");el.id="copy-toast";el.className="copy-toast";el.textContent="\u2713 In Zwischenablage kopiert\!";
  document.body.appendChild(el);setTimeout(()=>el.remove(),2500);
}
function shareResult(){
  const grade=S.sc>=2800?"S":S.sc>=2200?"A":S.sc>=1500?"B":S.sc>=800?"C":"D";
  const stars="\u{1F525}".repeat(Math.min(5,Math.ceil(S.correct/2)));
  const text=`\u{1F30D} GeoQuest: ${S.sc.toLocaleString()} Punkte\! ${stars}\n${S.correct}/${ROUNDS} richtig \u2022 Streak: ${S.bs}\u00d7\nKannst du das toppen? \u{1F3C6}`;
  navigator.clipboard.writeText(text).then(showCopyToast).catch(()=>{});
}
/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */
function loadAd(){
  /* adsbygoogle.push({}); */
}
/* Phase 61: Viral share — Web Share API with clipboard fallback */
function shareGame(){
  const text=`Ich habe gerade ${S.sc.toLocaleString()} Punkte in GeoQuest erreicht\! Schaffst du mehr?`;
  const url=window.location.href;
  if(navigator.share){
    navigator.share({title:"GeoQuest",text,url}).catch(()=>{});
  }else{
    navigator.clipboard.writeText(text+" "+url)
      .then(()=>showToast(t("link_copied")||"Link kopiert\!"))
      .catch(()=>showToast("Link kopiert\!"));
  }
}
/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */
function loadAd(){
  /* adsbygoogle.push({}); */
}
/* Phase 61: Viral share — Web Share API with clipboard fallback */
function shareGame(){
  const text=`Ich habe gerade ${S.sc.toLocaleString()} Punkte in GeoQuest erreicht\! Schaffst du mehr?`;
  const url=window.location.href;
  if(navigator.share){
    navigator.share({title:"GeoQuest",text,url}).catch(()=>{});
  }else{
    navigator.clipboard.writeText(text+" "+url)
      .then(()=>showToast(t("link_copied")||"Link kopiert\!"))
      .catch(()=>showToast("Link kopiert\!"));
  }
}
/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */
function loadAd(){
  /* adsbygoogle.push({}); */
}
/* Phase 61: Viral share — Web Share API with clipboard fallback */
function shareGame(){
  const text=`Ich habe gerade ${S.sc.toLocaleString()} Punkte in GeoQuest erreicht\! Schaffst du mehr?`;
  const url=window.location.href;
  if(navigator.share){
    navigator.share({title:"GeoQuest",text,url}).catch(()=>{});
  }else{
    navigator.clipboard.writeText(text+" "+url)
      .then(()=>showToast(t("link_copied")||"Link kopiert\!"))
      .catch(()=>showToast("Link kopiert\!"));
  }
}
/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */
function loadAd(){
  /* adsbygoogle.push({}); */
}
/* Phase 61: Viral share — Web Share API with clipboard fallback */
function shareGame(){
  const text=`Ich habe gerade ${S.sc.toLocaleString()} Punkte in GeoQuest erreicht\! Schaffst du mehr?`;
  const url=window.location.href;
  if(navigator.share){
    navigator.share({title:"GeoQuest",text,url}).catch(()=>{});
  }else{
    navigator.clipboard.writeText(text+" "+url)
      .then(()=>showToast(t("link_copied")||"Link kopiert\!"))
      .catch(()=>showToast("Link kopiert\!"));
  }
}
/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */
function loadAd(){
  /* adsbygoogle.push({}); */
}
/* Phase 61: Viral share — Web Share API with clipboard fallback */
function shareGame(){
  const text=`Ich habe gerade ${S.sc.toLocaleString()} Punkte in GeoQuest erreicht\! Schaffst du mehr?`;
  const url=window.location.href;
  if(navigator.share){
    navigator.share({title:"GeoQuest",text,url}).catch(()=>{});
  }else{
    navigator.clipboard.writeText(text+" "+url)
      .then(()=>showToast(t("link_copied")||"Link kopiert\!"))
      .catch(()=>showToast("Link kopiert\!"));
  }
}
/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */
function loadAd(){
  /* adsbygoogle.push({}); */
}
/* Phase 61: Viral share — Web Share API with clipboard fallback */
function shareGame(){
  const text=`Ich habe gerade ${S.sc.toLocaleString()} Punkte in GeoQuest erreicht\! Schaffst du mehr?`;
  const url=window.location.href;
  if(navigator.share){
    navigator.share({title:"GeoQuest",text,url}).catch(()=>{});
  }else{
    navigator.clipboard.writeText(text+" "+url)
      .then(()=>showToast(t("link_copied")||"Link kopiert\!"))
      .catch(()=>showToast("Link kopiert\!"));
  }
}
/* Phase 60: Ad hook — swap in real adsbygoogle.push({}) when AdSense is live */
function loadAd(){
  /* adsbygoogle.push({}); */
}
/* Phase 61: Viral share — Web Share API with clipboard fallback */
function shareGame(){
  const text=`Ich habe gerade ${S.sc.toLocaleString()} Punkte in GeoQuest erreicht\! Schaffst du mehr?`;
  const url=window.location.href;
  if(navigator.share){
    navigator.share({title:"GeoQuest",text,url}).catch(()=>{});
  }else{
    navigator.clipboard.writeText(text+" "+url)
      .then(()=>showToast(t("link_copied")||"Link kopiert\!"))
      .catch(()=>showToast("Link kopiert\!"));
  }
}
function updateHdrGuest(){
  const hdr=document.getElementById("g-hdr");
  const _uname=sbProfile?.username||localStorage.getItem("gq_username")||null;
  if(hdr)hdr.innerHTML=`<span class="g-logo">GEO<span>QUEST</span></span><div class="g-stats">${_uname?`<span class="g-stat" style="color:#10b981">\uD83D\uDC64 ${esc(_uname)}</span>`:""}<span class="g-stat">\u{1F525} ${S.st}</span><span class="g-stat">\u{1F4B0} ${(sbProfile?.geo_coins||0).toLocaleString()}</span><button class="hdr-gear" onclick="S.settingsModal=!S.settingsModal;render()" title="Einstellungen">\u2699\ufe0f</button></div>`;
}
function stampHtml(cc,rank,rot){
  const cn=COUNTRIES.find(c=>c.cc===cc)?.c||cc.toUpperCase();
  return `<div class="stamp-cell" onclick="S.modal='${cc}';render()" title="${cn}"><div class="stamp-ink ${rank}" style="transform:rotate(${rot}deg)"><img class="stamp-flag" src="https://flagcdn.com/w40/${cc}.png" alt="${cn}" onerror="this.style.display='none'"><span>${cc.toUpperCase()}</span></div></div>`;
}

/* DAILY CHALLENGE */
function getDailyKey(){return"gq_daily_"+new Date().toISOString().slice(0,10);}


/* ── Phase 42: LocalStorage Checksums ── */
const _GQ_SALT="GQ®2025\u{1F30D}XKCD327";
function _fnv1a(s){
  let h=0x811c9dc5;
  for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=(h*0x01000193)>>>0;}
  return h.toString(36);
}
function _gqSave(key,data){
  const json=JSON.stringify(data);
  const cs=_fnv1a(json+_GQ_SALT);
  try{localStorage.setItem(key,JSON.stringify({d:data,c:cs}));}catch(e){}
}
function _gqLoad(key,fallback){
  try{
    const raw=localStorage.getItem(key);
    if(!raw)return fallback;
    const w=JSON.parse(raw);
    /* Support legacy plain format */
    if(w===null||typeof w!=="object"||!("d" in w))return w||fallback;
    const expected=_fnv1a(JSON.stringify(w.d)+_GQ_SALT);
    if(w.c!==expected){
      console.warn("GeoQuest: Integritätsfehler für",key,"— Daten zurückgesetzt");
      localStorage.removeItem(key);
      return fallback;
    }
    return w.d;
  }catch(e){return fallback;}
}

function _smartDefaultCountry(){
  /* Priority: new unified pref → old spotter key → navigator.language → fallback */
  const saved=localStorage.getItem("geoquest_pref_country")||localStorage.getItem("gq_spotter_country");
  if(saved&&saved!=="all")return saved;
  const lang=(navigator.language||"de-DE").toLowerCase();
  const langMap={
    "de-de":"Deutschland","de-at":"Österreich","de-ch":"Schweiz","de-li":"Liechtenstein",
    "fr-fr":"Frankreich","fr-be":"Belgien","fr-ch":"Schweiz","fr-lu":"Luxemburg",
    "nl-nl":"Niederlande","nl-be":"Belgien",
    "pl-pl":"Polen","it-it":"Italien","es-es":"Spanien","pt-pt":"Portugal",
    "cs-cz":"Tschechien","sk-sk":"Slowakei","hu-hu":"Ungarn","ro-ro":"Rumänien",
    "bg-bg":"Bulgarien","hr-hr":"Kroatien","sl-si":"Slowenien",
    "et-ee":"Estland","lv-lv":"Lettland","lt-lt":"Litauen",
    "fi-fi":"Finnland","sv-se":"Schweden","nb-no":"Norwegen","da-dk":"Dänemark",
    "el-gr":"Griechenland","tr-tr":"Türkei"
  };
  if(langMap[lang])return langMap[lang];
  /* Try just the language prefix (e.g. "de" for de-DE) */
  const prefix=lang.split("-")[0];
  const prefixMap={
    "de":"Deutschland","fr":"Frankreich","nl":"Niederlande","pl":"Polen",
    "it":"Italien","es":"Spanien","pt":"Portugal","cs":"Tschechien",
    "sk":"Slowakei","hu":"Ungarn","ro":"Rumänien","bg":"Bulgarien",
    "hr":"Kroatien","sl":"Slowenien","et":"Estland","lv":"Lettland",
    "lt":"Litauen","fi":"Finnland","sv":"Schweden","nb":"Norwegen","da":"Dänemark",
    "el":"Griechenland","tr":"Türkei"
  };
  return prefixMap[prefix]||"Deutschland";
}
function loadCollectedPlates(){return _gqLoad("gq_coll",[]);}
function saveCollectedPlates(arr){_gqSave("gq_coll",arr);}
function getRarity(code){
  if(!code)return"common";
  const c=code.trim().toUpperCase();
  const legendary=["WAT","CAS","AKU","BIR","HEB","HON","MEL","EUT","GUN","NAB","PEG","ABG","SCZ"];
  if(legendary.includes(c))return"legendary";
  if(c.length<=1)return"common";
  if(c.length===2)return"rare";
  if(c.length===3)return"epic";
  return"legendary";
}
function rarityLabel(r){return{common:"\u{1F7E2} Common",rare:"\u{1F535} Rare",epic:"\u{1F7E3} Epic",legendary:"\u{1F7E1} Legendary"}[r]||r;}
function rarityColor(r){return{common:"#10b981",rare:"#3b82f6",epic:"#8b5cf6",legendary:"#f59e0b"}[r]||"#999";}
function isDailyDone(){try{return\!\!JSON.parse(localStorage.getItem(getDailyKey())||"null");}catch(e){return false;}}
function markDailyDone(score){try{localStorage.setItem(getDailyKey(),JSON.stringify({score,ts:Date.now()}));}catch(e){}}
function getDailySeed(){
  const d=new Date().toISOString().slice(0,10).replace(/-/g,"");
  let h=0;for(let i=0;i<d.length;i++){h=(Math.imul(31,h)+d.charCodeAt(i))|0;}
  return Math.abs(h);
}
function getDailyCountdown(){
  const now=new Date(),midnight=new Date(now);
  midnight.setHours(24,0,0,0);
  let s=~~((midnight-now)/1000);
  const h=~~(s/3600);s%=3600;const m=~~(s/60);s%=60;
  return String(h).padStart(2,"0")+":"+String(m).padStart(2,"0")+":"+String(s).padStart(2,"0");
}
function startDailyChallenge(){
  const seed=getDailySeed();
  initRng(seed);
  S.mode="city";S.diff="casual";S.isDailyRun=true;
  Object.assign(S,{sc:0,st:0,bs:0,rd:0,correct:0,lid:null,ph:"playing",scoreSaved:false,sessionAnswers:[],newStamps:[],half_removed:false,freezeActive:false,queueExtra:[],askedLids:new Set(),gameStartTime:Date.now()});
  lq();
}
function renderDailyHero(){
  const done=isDailyDone();
  const stored=done?JSON.parse(localStorage.getItem(getDailyKey())||"null"):null;
  const cd=getDailyCountdown();
  if(done){
    return`<div class="daily-hero done">
      <div style="display:flex;align-items:center;gap:12px">
        <div style="font-size:2rem">\u{1F3C6}</div>
        <div>
          <div class="dh-title">Daily Challenge erledigt\!</div>
          <div class="dh-sub" style="color:var(--text2)">Score: <b>${stored?.score?.toLocaleString()||"?"}</b> \u00b7 Neue Challenge in <span style="font-family:monospace;color:#f59e0b">${cd}</span></div>
        </div>
      </div>
    </div>`;}
  return`<div class="daily-hero" onclick="startDailyChallenge()" role="button">
    <div style="display:flex;align-items:center;justify-content:space-between">
      <div style="display:flex;align-items:center;gap:12px">
        <div style="font-size:2.2rem">\u{1F4C5}</div>
        <div>
          <div class="dh-title">Daily Challenge</div>
          <div class="dh-sub">Endet in <span class="dh-cd">${cd}</span> \u00b7 +100 GeoCoins</div>
        </div>
      </div>
      <button class="dh-btn">Spielen</button>
    </div>
  </div>`;
}

/* RENDER — main dispatcher */
/* Phase 33 T2 helper: percentage for duell bar */
function duellPct(a,b){const mx=Math.max(a,b,1);return Math.round(a/mx*100);}

function render(){
  updateHdrGuest();
  const app=document.getElementById("app");if(\!app)return;

  /* Onboarding gate */
  const ob=loadOb();
  if(\!ob||\!ob.done){
    if(S.obStep<0)S.obStep=0;
    app.innerHTML=renderOnboarding(S.obStep);return;
  }
  if(S.mpModal){app.innerHTML=renderMultiplayerLobby();return;}
  if(S.payModal){app.innerHTML=renderPayModal();return;}
  if(S.lockModal){app.innerHTML=renderLockModal(S.lockModal);return;}

  /* Challenge welcome */
  if(CHALLENGE&&S.ph==="menu"&&\!S.challengeStarted){
    const ml=MODES.find(m=>m.id===CHALLENGE.mode)?.title||CHALLENGE.mode;
    app.innerHTML=`<div class="scr"><div style="background:var(--bg2);border-radius:20px;padding:1.5rem;text-align:center;margin-top:2rem">
      <div style="font-size:2rem;margin-bottom:.5rem">\u{1F3C6}</div>
      <div style="font-weight:900;font-size:1.2rem;margin-bottom:4px">Herausforderung\!</div>
      <div style="color:var(--text2);font-size:.82rem;margin-bottom:.85rem">Modus: ${ml}</div>
      <div style="background:var(--bg3);border-radius:12px;padding:.85rem;margin-bottom:1rem">
        <div style="color:var(--text3);font-size:.7rem;margin-bottom:3px">ZU SCHLAGEN</div>
        <div style="font-size:2.2rem;font-weight:900;color:#fbbf24">${CHALLENGE.oppScore.toLocaleString()}</div>
      </div>
      <button class="btn-p" onclick="S.challengeStarted=true;startChallenge(CHALLENGE)">\u{1F680} Annehmen</button>
      <button class="btn-g" onclick="S.challenge=null;render()">Ablehnen</button>
    </div></div>`;
    return;
  }

  /* Stamp detail modal */
  if(S.modal){
    const mastery=loadMastery();const m=mastery[S.modal]||{v:0,p:0};const rank=getMasteryRank(m.v,m.p);
    const cn=COUNTRIES.find(c=>c.cc===S.modal)?.c||S.modal.toUpperCase();
    const rl={gold:"\u{1F947} Gold",silver:"\u{1F948} Silber",bronze:"\u{1F949} Bronze"}[rank]||"Gesperrt";
    const rc={gold:"#d97706",silver:"#94a3b8",bronze:"#c2410c"}[rank]||"var(--text3)";
    app.innerHTML=`<div class="modal-overlay" onclick="if(event.target===this){S.modal=null;render()}"><div class="modal-box">
      <img src="https://flagcdn.com/w80/${S.modal}.png" style="height:44px;width:auto;border-radius:4px;margin-bottom:.75rem" onerror="this.style.display='none'">
      <div style="font-size:1.2rem;font-weight:900;color:var(--text);margin-bottom:4px">${cn}</div>
      <div style="font-size:.82rem;font-weight:700;color:${rc};margin-bottom:.85rem">${rl}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:1rem">
        <div style="background:var(--bg3);border-radius:10px;padding:.65rem;text-align:center"><div style="font-size:1.4rem;font-weight:900;color:#34d399">${m.v}</div><div style="font-size:.65rem;color:var(--text3)">Richtige Antworten</div></div>
        <div style="background:var(--bg3);border-radius:10px;padding:.65rem;text-align:center"><div style="font-size:1.4rem;font-weight:900;color:#fbbf24">${m.p}</div><div style="font-size:.65rem;color:var(--text3)">Perfekte Runden</div></div>
      </div>
      <button class="btn-p" style="margin-bottom:0" onclick="S.modal=null;render()">Schliessen</button>
    </div></div>`;
    return;
  }

  if(S.ph==="menu"){
    app.innerHTML=`<div class="scr">
      ${S.tab==="home"?renderHomeTab():""}
      ${S.tab==="lernen"?renderLernenTab():""}
      ${S.tab==="liga"?renderLigaTab():""}
      ${S.tab==="profil"?renderProfilTab():""}
      ${S.tab==="album"?renderCollectionScreen():""}
      ${S.settingsModal?renderSettingsModal():""}
    </div>${renderBottomNav()}`;
    return;
  }

  if(S.ph==="gameover"){
    const isSurv=S.diff==="survival";
    const survived=S.rd;const survBest=S.survivalBest||parseInt(localStorage.getItem('gq_surv_best')||'0');
    const isNewRecord=isSurv&&survived>=survBest&&survived>0;
    const g=S.sc>=2800?"S":S.sc>=2200?"A":S.sc>=1500?"B":S.sc>=800?"C":"D";
    const gc={S:"#fbbf24",A:"#34d399",B:"#60a5fa",C:"#fb923c",D:"#f87171"}[g];
    const ml=MODES.find(m=>m.id===S.mode)?.title||"";const mm=isSurv?2:S.diff==="hardcore"?3:1;
    const isGuest=sbOK&&\!sbProfile?.username;
    const mastery=loadMastery();const totalStamps=Object.values(mastery).filter(m=>getMasteryRank(m.v,m.p)).length;
    const stampBanners=S.newStamps.map(({cc,rank})=>{
      const cn=COUNTRIES.find(c=>c.cc===cc)?.c||cc.toUpperCase();
      const rl={gold:"\u{1F947} Gold-Stempel",silver:"\u{1F948} Silber-Stempel",bronze:"\u{1F949} Bronze-Stempel"}[rank]||"Stempel";
      return`<div class="new-stamp-banner"><img src="https://flagcdn.com/w40/${cc}.png" style="width:28px;height:auto;border-radius:3px" onerror="this.style.display='none'"><div><div style="color:#34d399;font-weight:900;font-size:.88rem">NEUER STEMPEL\!</div><div style="color:var(--text2);font-size:.78rem">${rl} \u2022 ${cn}</div></div></div>`;
    }).join("");
    const survivalPanel=isSurv?`
      ${isNewRecord?`<div style="background:linear-gradient(135deg,#7f1d1d,#991b1b);border:2px solid #ef4444;border-radius:12px;padding:.85rem;text-align:center;margin-bottom:.75rem">
        <div style="font-size:1.6rem">\ud83c\udfc6</div>
        <div style="color:#fca5a5;font-weight:900;font-size:.9rem">NEUER REKORD\!</div>
        <div style="color:#fef2f2;font-size:1.5rem;font-weight:900">${survived} Runden</div>
      </div>`:""}
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:.85rem">
        <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.5rem;font-weight:900;color:#ef4444">${survived}</div><div style="font-size:.64rem;color:var(--text3)">\u00dcberlebt</div></div>
        <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.5rem;font-weight:900;color:#fbbf24">${survBest}</div><div style="font-size:.64rem;color:var(--text3)">Rekord</div></div>
      </div>`:"";
    app.innerHTML=`<div class="scr">
      <div style="font-size:2.5rem;text-align:center">${isSurv?"\ud83d\udc80":"\u{1F3C6}"}</div>
      <h2 style="text-align:center;font-size:1.7rem;font-weight:900;color:var(--text);margin:3px 0">GAME OVER</h2>
      <p style="text-align:center;color:var(--text3);font-size:.78rem;margin-bottom:.85rem">${ml} \u00b7 ${isSurv?"Survival":ROUNDS+" Runden"}</p>
      ${stampBanners}
      <div style="background:var(--bg2);border-radius:16px;padding:1.5rem;margin-bottom:.85rem;text-align:center;border:1px solid var(--border)">
        ${isSurv?survivalPanel:`<div style="font-size:4rem;font-weight:900;line-height:1;color:${gc}">${g}</div>`}
        <div style="font-size:2rem;font-weight:900;color:var(--text);margin-top:5px">${S.sc.toLocaleString()}</div>
        <div style="color:var(--text3);font-size:.76rem;margin-bottom:.85rem">Punkte</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:8px;margin-bottom:.85rem">
          <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.3rem;font-weight:900;color:#34d399">${S.correct}${isSurv?"":"/"+ROUNDS}</div><div style="font-size:.64rem;color:var(--text3)">Richtige</div></div>
          <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.3rem;font-weight:900;color:${mm>1?"#f59e0b":"var(--text3)"}">${mm}\u00d7</div><div style="font-size:.64rem;color:var(--text3)">${isSurv?"Survival":S.diff==="hardcore"?"Hardcore":"Casual"}</div></div>
          <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.3rem;font-weight:900;color:#fb923c">${S.bs}\u00d7</div><div style="font-size:.64rem;color:var(--text3)">Streak</div></div>
          <div style="background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center"><div style="font-size:1.3rem;font-weight:900;color:#fbbf24">${isSurv?survived:~~(S.sc/ROUNDS)}</div><div style="font-size:.64rem;color:var(--text3)">${isSurv?"Runden":"\u00d8/Rd"}</div></div>
        </div>
        ${S.isDailyRun&&\!isDailyDone()?`<div style="background:linear-gradient(135deg,#052e16,#064e3b);border:1.5px solid #10b981;border-radius:12px;padding:.75rem;text-align:center;margin-bottom:.75rem">
          <div style="font-size:1.4rem">\u{1F3C6}</div>
          <div style="color:#34d399;font-weight:900;font-size:.9rem">Daily Challenge\!</div>
          <div style="color:#fbbf24;font-size:1rem;font-weight:900">+100 GeoCoins</div>
        </div>`:""}
        ${sbOK?`<div style="font-size:.76rem;color:${S.scoreSaved?"#34d399":"var(--text3)"}">${S.scoreSaved?"\u2713 Score gespeichert":"Speichere \u2026"}</div>`:""}
      </div>
      ${isGuest&&S.correct>0&&S.convModal?`<div class="conv-modal-bg" onclick="if(event.target===this){S.convModal=false;render()}">
  <div class="conv-modal">
    <div style="font-size:2rem;margin-bottom:.4rem">\u{1F4BE}</div>
    <div style="font-size:1rem;font-weight:900;color:var(--text);margin-bottom:.4rem">Fortschritt sichern!</div>
    <div style="color:var(--text2);font-size:.82rem;margin-bottom:1rem">Du hast dir ${S.sc.toLocaleString()} Punkte erarbeitet. Erstelle einen kostenlosen Account, damit deine Erfolge nicht verloren gehen.</div>
    <button class="btn-p" style="margin-bottom:.5rem" onclick="S.tab='profil';S.ph='menu';S.authMode='register';render()">\u{1F331} Account erstellen</button>
    <button class="btn-g" style="margin-bottom:0" onclick="S.convModal=false;render()">Sp\u00e4ter</button>
  </div>
</div>`:""}
      ${S.challenge?renderChallengeResult(S.challenge,S.sc,S.mode):""}
      <div id="ad-container-score" style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;text-align:center;color:var(--text3);font-size:.8rem">Danke, dass du GeoQuest spielst\! \u{1F499}</div>
      <div id="ad-container-score" style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;text-align:center;color:var(--text3);font-size:.8rem">Danke, dass du GeoQuest spielst\! \u{1F499}</div>
      <div id="ad-container-score" style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;text-align:center;color:var(--text3);font-size:.8rem">Danke, dass du GeoQuest spielst\! \u{1F499}</div>
      <div id="ad-container-score" style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;text-align:center;color:var(--text3);font-size:.8rem">Danke, dass du GeoQuest spielst\! \u{1F499}</div>
      <div id="ad-container-score" style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;text-align:center;color:var(--text3);font-size:.8rem">Danke, dass du GeoQuest spielst\! \u{1F499}</div>
      <div id="ad-container-score" style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;text-align:center;color:var(--text3);font-size:.8rem">Danke, dass du GeoQuest spielst\! \u{1F499}</div>
      <div id="ad-container-score" style="background:var(--bg2);border:1px solid var(--border);border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;text-align:center;color:var(--text3);font-size:.8rem">Danke, dass du GeoQuest spielst\! \u{1F499}</div>
      <button class="share-btn" onclick="shareResult()">\u{1F4CB} Ergebnis teilen</button>
      <button class="btn-share-viral" onclick="shareGame()">\u{1F4E4} Spiel teilen</button>
      <button class="btn-share-viral" onclick="shareGame()">\u{1F4E4} Spiel teilen</button>
      <button class="btn-share-viral" onclick="shareGame()">\u{1F4E4} Spiel teilen</button>
      <button class="btn-share-viral" onclick="shareGame()">\u{1F4E4} Spiel teilen</button>
      <button class="btn-share-viral" onclick="shareGame()">\u{1F4E4} Spiel teilen</button>
      <button class="btn-share-viral" onclick="shareGame()">\u{1F4E4} Spiel teilen</button>
      <button class="btn-share-viral" onclick="shareGame()">\u{1F4E4} Spiel teilen</button>
      <button class="btn-p" onclick="rngSeed=null;S.challenge=null;S.challengeStarted=false;startGame()">NOCHMAL</button>
      <button class="btn-g" onclick="S.ph='menu';S.tab='home';rngSeed=null;render()">Hauptmen\u00fc</button>
      ${S.mpOpponent?`
      <div class="mp-result-card">
        <div class="mp-result-title">\u2694\ufe0f Duell-Ergebnis</div>
        <div class="mp-result-row">
          <div class="mp-result-col mp-you">
            <div class="mp-result-name">Ich</div>
            <div class="mp-result-score">${S.sc.toLocaleString()}</div>
          </div>
          <div style="font-size:1.4rem;align-self:center;color:var(--text3)">vs</div>
          <div class="mp-result-col mp-opp">
            <div class="mp-result-name">${esc(S.mpOpponent)}</div>
            <div class="mp-result-score">${S.mpOppFinal?S.mpOppFinal.score.toLocaleString():'...'}</div>
          </div>
        </div>
        ${S.mpOppFinal
          ?`<div class="duell-final-bar">
              <div class="dfb-fill-you" style="width:${duellPct(S.sc,S.mpOppFinal.score)}%"></div>
              <div class="dfb-fill-opp" style="width:${duellPct(S.mpOppFinal.score,S.sc)}%"></div>
            </div>
            <div class="mp-result-verdict">${S.sc>S.mpOppFinal.score?'\u{1F3C6} Du gewinnst!':S.sc<S.mpOppFinal.score?'\u{1F614} Niederlage':'\u{1F91D} Unentschieden!'}</div>`
          :'<div class="mp-waiting">\u23f3 Warte auf Gegner\u2026<br><button class="btn-g" style="margin-top:.5rem;width:auto;padding:.35rem .9rem;font-size:.75rem" onclick="S.mpOpponent=null;render()">Trotzdem weiter</button></div>'}
      </div>`:""}
    </div>`;
    setTimeout(loadAd,100);
    return;
  }

  /* PLAYING / FEEDBACK */
  const{sc,st,bs,rd,tm,q,sel,ok,pts,mode,diff}=S;
  if(!q){S.ph="menu";S.q=null;render();return;}  /* guard: q not yet set */
  const col=tc(),p=pct(),_tr=tier(st);
  let qBody="";
  if(q.type==="flag"){
    qBody=`<div class="qprompt">${q.prompt}</div><div class="qflag"><img src="https://flagcdn.com/w160/${q.subj}.png" alt="Flagge" onerror="this.style.display='none'"></div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
  }else if(q.type==="outline"){
    qBody=`<div class="qprompt">${q.prompt}</div><div class="outline-wrap" id="gq-outline-svg"></div>`;
  }else if(q.type==="food"){
    qBody=`<div class="qprompt">${q.prompt}</div><div class="food-emoji">${q.emoji||"\u{1F37D}"}</div><div class="qmain">${q.subj}</div>`;
  }else if(q.type==="brand"){
    qBody=`<div class="qprompt">${q.prompt}</div><div style="text-align:center;color:#94a3b8;font-size:.68rem;margin:2px 0 4px">${q.industry||""}</div><div class="qmain" style="font-size:2.2rem">${q.subj}</div>`;
  }else if(q.type==="currency"){
    qBody=`<div class="qprompt">${q.prompt}</div><div style="text-align:center;margin:6px 0 2px"><span class="currency-symbol">${q.symbol||""}</span></div><div class="qmain">${q.subj}</div>`;
  }else if(q.type==="plate_casual"||q.type==="plate_hard"){
    qBody=`<div class="qprompt">${q.prompt}</div>
      <div style="text-align:center;margin:8px 0 10px">
        <div class="plate-badge">${q.subj}</div>
        ${q.type==="plate_casual"&&q.meta&&sel\!==null?`<div style="color:var(--text3);font-size:.75rem;margin-top:6px">${q.meta}</div>`:""}
      </div>`;
  }else if(q.type==="hl_pop"||q.type==="hl_river"||q.type==="hl_area"){
    /* Higher/Lower card + dedicated answer buttons (clean "higher"/"lower" keys) */
    const revB=sel\!==null;
    const hlIcon=q.type==="hl_pop"?"\u{1F465}":q.type==="hl_river"?"\u{1F4A7}":"\u{1F5FA}";
    const hlFbH=sel===null?"":ok&&q.ans==="higher"?"ok":"ng";
    const hlFbL=sel===null?"":ok&&q.ans==="lower"?"ok":"ng";
    const hlDis=sel\!==null?"disabled":"";
    qBody=`<div class="qprompt">${hlIcon} ${q.prompt}</div>
      <div class="hl-wrap">
        <div class="hl-card hl-known">
          <div class="hl-name">${q.nameA}</div>
          <div class="hl-val">${q.valA}</div>
        </div>
        <div class="hl-vs">\u{1F914}</div>
        <div class="hl-card hl-hidden${revB?" hl-revealed":""}">
          <div class="hl-name">${q.nameB}</div>
          <div class="hl-val">${revB?q.valB:"\u2753"}</div>
        </div>
      </div>
      <div class="hl-btn-row">
        <button class="hl-btn hl-higher${sel\!==null?(q.ans==="higher"?" ok":(sel==="higher"?" ng":" dm")):""}" ${hlDis} onclick="answer('higher')">${t("hl_higher")}</button>
        <button class="hl-btn hl-lower${sel\!==null?(q.ans==="lower"?" ok":(sel==="lower"?" ng":" dm")):""}" ${hlDis} onclick="answer('lower')">${t("hl_lower")}</button>
      </div>`;
  }else if(q.type==="curr_real"){
    /* Show country name; hide currency name (meta) until answered */
    qBody=`<div class="qprompt">${q.prompt}</div>
      <div class="qmain">${q.subj}</div>
      ${sel\!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
  }else if(q.type==="neighbor"){
    qBody=`<div class="qprompt" style="font-size:1rem">${q.prompt}</div>
      <div style="text-align:center;margin:10px 0 6px">
        <div class="qmain" style="font-size:2.2rem">${q.subj}</div>
        <div style="font-size:1.2rem;margin-top:4px">${flagOf(q.subj)}</div>
      </div>`;
  }else{
    qBody=`<div class="qprompt">${q.prompt}</div><div class="qmain">${q.subj}</div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
  }
  /* After-answer reveal for plate casual */
  let plateReveal="";
  if(sel\!==null&&(q.type==="plate_casual"||q.type==="plate_hard")){
    const pc=PLATES_DATA.find(p=>p.code===q.subj);
    if(pc)plateReveal=`<div style="text-align:center;color:var(--text2);font-size:.8rem;margin-top:4px">${pc.region} \u00b7 ${pc.country}${pc.state?" \u00b7 "+pc.state:""}</div>`;
  }
  /* Phase 34: Map-Guesser — early return, D3 map replaces answer buttons */
  if(q.type==="map_guess"){
    const mapFb=sel===null?"":ok
      ?`<div class="fb ok">\u2713 Richtig\! +${pts}</div>`
      :`<div class="fb ng">\u2717 Falsch \u2192 ${q.ans}</div>`;
    app.innerHTML=`<div class="scr map-scr">
      <div class="hud">
        <div style="display:flex;gap:8px;align-items:center">
          <div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>
          ${st>0?`<div class="pill-s"><div class="hlbl" style="color:#fb923c">STREAK</div><div class="hval-s">\u00d7${st}</div></div>`:""}
          ${S.mpOpponent?`<div class="pill" style="opacity:.7"><div class="hlbl" style="color:#8b5cf6">\u2694</div><div class="hval" style="color:#8b5cf6">${(S.mpOppScore||0).toLocaleString()}</div></div>`:""}
        </div>
        <div style="display:flex;align-items:center;gap:8px">
          ${diff==="survival"
            ?`<div style="text-align:right"><div class="hlbl" style="color:#ef4444">\ud83d\udc80 SURVIVAL</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">\u221e</span></div></div>`
            :`<div style="text-align:right"><div class="hlbl" style="color:var(--text3)">RUNDE</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">/${ROUNDS}</span></div></div>`}
          <button class="btn-cancel" onclick="clr();S.ph='menu';S.tab='home';render()">\u00d7</button>
        </div>
      </div>
      ${S.mpOpponent?`<div class="duell-bar-wrap" style="margin:0 0 4px"><div class="duell-lbl duell-you">Ich<span class="duell-score">${sc.toLocaleString()}</span></div><div class="duell-track"><div class="duell-fill-you" style="width:${duellPct(sc,S.mpOppScore||0)}%"></div><div class="duell-fill-opp" style="width:${duellPct(S.mpOppScore||0,sc)}%"></div></div><div class="duell-lbl duell-opp"><span class="duell-score">${(S.mpOppScore||0).toLocaleString()}</span>${esc(S.mpOpponent.slice(0,8))}</div></div>`:""}
      <div class="tbar${S.freezeActive?" frozen":""}"><div class="tfill" style="width:${p}%;background:${col}"></div></div>
      <div class="map-prompt">\u{1F5FA} Finde: <strong>${esc(q.subj)}</strong></div>
      <div id="gq-map-svg" class="map-container"></div>
      ${mapFb}
      ${sel\!==null?`<button class="btn-p map-weiter" onclick="clr();nextRound()">Weiter \u2192</button>`:""}
    </div>`;
    requestAnimationFrame(()=>drawWorldMap(q.ans,sel,ok));
    return;
  }
  /* topBar: shared HUD wrapper used by pop_compare early-return */
  const topBar=`<div class="scr"><div class="hud"><div style="display:flex;gap:8px;align-items:center"><div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>${st>0?`<div class="pill-s"><div class="hlbl" style="color:#fb923c">STREAK</div><div class="hval-s">×${st}</div></div>`:""}</div><div style="display:flex;align-items:center;gap:8px">${diff==="survival"?`<div style="text-align:right"><div class="hlbl" style="color:#ef4444">💀 SURVIVAL</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">∞</span></div></div>`:`<div style="text-align:right"><div class="hlbl" style="color:var(--text3)">RUNDE</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">/${ROUNDS}</span></div></div>`}<button class="btn-cancel" onclick="clr();S.ph='menu';S.tab='home';render()">×</button></div></div><div class="tbar${S.freezeActive?" frozen":""}"><div class="tfill" style="width:${p}%;background:${col}"></div></div>`;
  let answerHtml="";
  if(q.type==="flagsel"){
    const fb2=q.opts.map(cc=>{let cls="btn-flag";if(sel\!==null){if(cc===q.ans)cls+=" ok";else if(cc===sel)cls+=" ng";else cls+=" dm";}const flagEmoji=cc.toUpperCase().replace(/./g,c=>String.fromCodePoint(c.charCodeAt(0)+127397));
      return`<button class="${cls}" ${sel?"disabled":""} onclick="answer('${cc}')"><img src="https://flagcdn.com/w120/${cc}.png" alt="${cc}" onerror="this.outerHTML='<span class=flag-fb>'+flagEmoji+'</span>'"></button>`;}).join("");
    answerHtml=`<div class="flag-grid">${fb2}</div>`;
  }else{
    // Population comparison: special subj rendering
    if(q.type==="pop_compare"&&q.subj&&typeof q.subj==='object'){
      const pcDis=sel!==null?"disabled":"";
      const moreCls="hl-btn hl-higher"+(sel!==null?(q.ans==="more"?" ok":(sel==="more"?" ng":" dm")):"");
      const lessCls="hl-btn hl-lower"+(sel!==null?(q.ans==="less"?" ok":(sel==="less"?" ng":" dm")):"");
      const pcHtml=topBar+`
        <div class="pop-compare-wrap">
          <div class="pop-box">
            <div class="pop-country">${q.subj.nameA}</div>
            <div class="pop-value">${q.subj.popA}</div>
          </div>
          <div style="font-size:1.4rem;color:var(--text3)">vs</div>
          <div class="pop-box" style="border-color:#10b981">
            <div class="pop-country">${q.subj.nameB}</div>
            <div style="color:var(--text3);font-size:.78rem">?</div>
          </div>
        </div>
        <div style="color:var(--text3);font-size:.82rem;text-align:center;margin:.5rem 0">${q.prompt}</div>
        <div class="hl-btn-row">
          <button class="${moreCls}" ${pcDis} onclick="answer('more')">${t("hl_more")}</button>
          <button class="${lessCls}" ${pcDis} onclick="answer('less')">${t("hl_less")}</button>
        </div>
        ${sel\!==null?`<div class="meta-line">${q.meta||""}</div>`:""}
        ${sel\!==null?`<button class="btn-p" onclick="nextRound()">Weiter →</button>`:""}
      </div>`;
      app.innerHTML=pcHtml;return;
    }
    if(q.type==="hl_pop"||q.type==="hl_river"||q.type==="hl_area"){
      answerHtml="";
    }else{
      const btns=q.opts.map((o,i)=>{let cls="btn-a";const os=o.replace(/'/g,"\\'");if(sel\!==null){if(o===q.ans)cls+=" ok";else if(o===sel)cls+=" ng";else cls+=" dm";}const mk=sel?(o===q.ans?`<span>\u2713</span>`:o===sel?`<span>\u2717</span>`:""):"";return`<button class="${cls}" ${sel?"disabled":""} onclick="answerByIdx(${i})">${esc(displayCountry(o))}${mk}</button>`;}).join("");
      answerHtml=`<div class="answers">${btns}</div>`;
    }
  }
  let fb="";
  if(S.ph==="feedback"){const cls=ok?"fb ok":"fb ng";let al=q.ans;if(q.type==="flagsel"){const co=COUNTRIES.find(c=>c.cc===q.ans);al=co?co.c:q.ans;}const al_d=displayCountry(al);const msg=ok?t("fb_correct",{pts}):sel==="__t"?t("fb_time",{ans:al_d}):t("fb_wrong",{ans:al_d});fb=`<div class="${cls}">${msg}</div>${plateReveal}`;}
  /* Power-up bar (Phase 26) */
  const pu=loadPU();
  const puBar=`<div class="pu-bar">
    <button class="pu-btn${S.half_removed?" pu-used":""}" onclick="useFiveO()" ${(S.half_removed||(pu.five0||0)===0)?"disabled":""} title="50/50-Joker (${pu.five0||0} \u00fcbrig)">\u2702 50/50 <span style="font-size:.62rem">(${pu.five0||0})</span></button>
    <button class="pu-btn${S.freezeActive?" freeze-on":""}" onclick="useFreeze()" ${(S.freezeActive||(pu.freeze||0)===0)?"disabled":""} title="Zeit-Stopp (${pu.freeze||0} \u00fcbrig)">\u{1F9CA} Freeze <span style="font-size:.62rem">(${pu.freeze||0})</span></button>
  </div>`;
  app.innerHTML=`<div class="scr">
    <div class="hud">
      <div style="display:flex;gap:8px;align-items:center">
        <div class="pill"><div class="hlbl">SCORE</div><div class="hval">${sc.toLocaleString()}</div></div>
        ${st>0?`<div class="pill-s"><div class="hlbl" style="color:#fb923c">STREAK</div><div class="hval-s">\u00d7${st}</div></div>`:""}
      </div>
      <div style="display:flex;align-items:center;gap:8px">
        ${diff==="survival"
          ?`<div style="text-align:right"><div class="hlbl" style="color:#ef4444">\ud83d\udc80 SURVIVAL</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">\u221e</span></div></div>`
          :`<div style="text-align:right"><div class="hlbl" style="color:var(--text3)">RUNDE</div><div style="color:var(--text);font-weight:700;font-size:.9rem">${rd+1}<span style="color:var(--text3)">/${ROUNDS}</span></div></div>`}
        <button class="btn-cancel" onclick="clr();S.ph='menu';S.tab='home';render()">\u00d7</button>
      </div>
    </div>
    ${S.mpOpponent?`<div class="duell-bar-wrap"><div class="duell-lbl duell-you">Ich<span class="duell-score">${sc.toLocaleString()}</span></div><div class="duell-track"><div class="duell-fill-you" style="width:${duellPct(sc,S.mpOppScore||0)}%"></div><div class="duell-fill-opp" style="width:${duellPct(S.mpOppScore||0,sc)}%"></div></div><div class="duell-lbl duell-opp"><span class="duell-score">${(S.mpOppScore||0).toLocaleString()}</span>${esc(S.mpOpponent.slice(0,8))}</div></div>`:""}
    ${st>=3?`<div style="text-align:center;font-size:.76rem;font-weight:700;color:#fb923c;margin-bottom:6px">${_tr.l}</div>`:""}
    <div class="tbar${S.freezeActive?" frozen":""}"><div class="tfill" style="width:${p}%;background:${col}"></div></div>
    <div class="qcard">${qBody}<div class="qtimer" style="color:${col}">${tm}</div></div>
    ${sel===null?puBar:""}
    ${answerHtml}${fb}
  </div>`;
  /* Phase 35: draw country outline after DOM update */
  if(q.type==="outline")requestAnimationFrame(()=>drawCountryOutline(q.subj,"gq-outline-svg"));
}

/* Phase 35: draw single-country D3 silhouette for outline mode */
function drawCountryOutline(cc,targetId){
  const el=document.getElementById(targetId);
  if(\!el)return;
  if(typeof d3==='undefined'||typeof topojson==='undefined'||\!window.WORLD_TOPO){
    el.innerHTML='<span style="font-size:3rem">'+cc.toUpperCase()+'</span>';
    return;
  }
  const countries=topojson.feature(window.WORLD_TOPO,window.WORLD_TOPO.objects.countries);
  /* Map cc to TopoJSON name via MAP_COUNTRIES */
  const entry=MAP_COUNTRIES.find(x=>x.cc===cc);
  if(\!entry){el.innerHTML='<span style="font-size:1rem;color:var(--text3)">?</span>';return;}
  const feat=countries.features.find(f=>f.properties.name===entry.name);
  if(\!feat){el.innerHTML='<span style="font-size:1rem;color:var(--text3)">?</span>';return;}
  const W=el.clientWidth||200,H=el.clientHeight||140;
  const proj=d3.geoMercator().fitSize([W,H],feat);
  const path=d3.geoPath().projection(proj);
  d3.select(el).html('').append('svg')
    .attr('width','100%').attr('height','100%')
    .attr('viewBox',`0 0 ${W} ${H}`)
    .append('path')
    .datum(feat)
    .attr('d',path)
    .attr('fill','var(--text,#1e293b)')
    .attr('stroke','none');
}


/* Phase 34 — D3 World Map component */
function drawWorldMap(targetName,sel,ok){
  const container=document.getElementById('gq-map-svg');
  if(\!container||typeof d3==='undefined'||typeof topojson==='undefined'){
    if(container)container.innerHTML='<p style="color:var(--text3);text-align:center;padding:2rem">'+t('map_unavail')+'</p>';
    return;
  }
  if(\!window.WORLD_TOPO){
    container.innerHTML='<p style="color:var(--text3);text-align:center;padding:2rem">'+t('map_loading')+'</p>';
    return;
  }
  const W=container.clientWidth||(window.innerWidth||360),H=Math.min(W*.56,290);
  const svg=d3.select(container).html('').append('svg')
    .attr('width','100%').attr('height',H)
    .attr('viewBox',`0 0 ${W} ${H}`)
    .style('background','var(--bg2)');

  const proj=d3.geoNaturalEarth1().scale(W/6.2).translate([W/2,H/2]);
  const path=d3.geoPath().projection(proj);
  const countries=topojson.feature(window.WORLD_TOPO,window.WORLD_TOPO.objects.countries);

  const g=svg.append('g');

  /* Zoom + pan */
  const zoom=d3.zoom().scaleExtent([1,10])
    .on('zoom',ev=>{
      if(sel\!==null)return; /* lock zoom during feedback so user sees the result */
      g.attr('transform',ev.transform);
    });
  svg.call(zoom);

  /* Sphere backdrop */
  g.append('path').datum({type:'Sphere'}).attr('d',path)
    .attr('fill','#bfdbfe').attr('stroke','none');

  /* Country paths */
  g.selectAll('path.ctry')
    .data(countries.features)
    .enter().append('path')
    .attr('class','ctry')
    .attr('d',path)
    .attr('data-n',d=>d.properties.name)
    .attr('fill',d=>{
      const n=d.properties.name;
      if(sel\!==null){
        if(n===targetName)return'#10b981';
        if(n===sel&&\!ok)return'#ef4444';
        return'#d1d5db';
      }
      return'var(--bg3,#e2e8f0)';
    })
    .attr('stroke','var(--border,#94a3b8)')
    .attr('stroke-width',.35)
    .on('mouseover',function(_,d){
      if(sel\!==null)return;
      d3.select(this).attr('fill','#93c5fd');
    })
    .on('mouseout',function(_,d){
      if(sel\!==null)return;
      d3.select(this).attr('fill','var(--bg3,#e2e8f0)');
    })
    .on('click',function(ev,d){
      if(sel\!==null)return;
      ev.stopPropagation();
      answer(d.properties.name);
    });

  /* Pulse correct country after feedback */
  if(sel\!==null){
    const cp=g.selectAll('path.ctry').filter(d=>d.properties.name===targetName);
    let n=ok?2:4;
    function pulse(){
      if(n--<=0)return;
      cp.transition().duration(300).attr('fill','#6ee7b7')
        .transition().duration(300).attr('fill','#10b981').on('end',pulse);
    }
    pulse();
    /* Zoom to correct country */
    const feat=countries.features.find(d=>d.properties.name===targetName);
    if(feat){
      const[[x0,y0],[x1,y1]]=path.bounds(feat);
      const cw=x1-x0,ch=y1-y0;
      const s=Math.max(1,Math.min(8,.8/Math.max(cw/W,ch/H)));
      const tx=W/2-(x0+x1)/2*s,ty=H/2-(y0+y1)/2*s;
      svg.transition().duration(700)
        .call(zoom.transform,d3.zoomIdentity.translate(tx,ty).scale(s));
    }
  }
}


/* BOTTOM NAV */
function renderBottomNav(){
  const tabs=[
    {id:"home",   icon:"\u{1F3E0}", lbl:"Home"},
    {id:"lernen", icon:"\u{1F4DA}", lbl:"Lernen"},
    {id:"liga",   icon:"\u{1F3C6}", lbl:"Liga"},
    {id:"profil", icon:"\u{1F464}", lbl:"Profil"},
    {id:"album",  icon:"\u{1F4D4}", lbl:"Album"},
  ];
  return`<nav class="bottom-nav">${tabs.map(t=>`<button class="bn-item${S.tab===t.id?" active":""}" onclick="S.tab='${t.id}';render()"><span class="bn-icon">${t.icon}</span><span class="bn-lbl">${t.lbl}</span></button>`).join("")}</nav>`;
}


/* ─── Phase 43: Kennzeichen-Album ─────────────────────────────────────── */

/* Country name → English for world-110m matching */
const PLATE_COUNTRY_EN={
  "Deutschland":"Germany","Österreich":"Austria","Frankreich":"France",
  "Italien":"Italy","Spanien":"Spain","Polen":"Poland","Tschechien":"Czechia",
  "Ungarn":"Hungary","Schweiz":"Switzerland","Belgien":"Belgium",
  "Niederlande":"Netherlands","Dänemark":"Denmark","Schweden":"Sweden",
  "Norwegen":"Norway","Finnland":"Finland","Portugal":"Portugal",
  "Griechenland":"Greece","Rumänien":"Romania","Bulgarien":"Bulgaria",
  "Kroatien":"Croatia","Slowenien":"Slovenia","Slowakei":"Slovakia",
  "Luxemburg":"Luxembourg","Irland":"Ireland","Litauen":"Lithuania",
  "Lettland":"Latvia","Estland":"Estonia","Zypern":"Cyprus","Malta":"Malta",
  "Vereinigtes Königreich":"United Kingdom","Russland":"Russia",
  "Türkei":"Turkey","Ukraine":"Ukraine","Serbien":"Serbia",
  "Bosnien und Herzegowina":"Bosnia and Herzegovina"
};
function plateCountryToEn(c){return PLATE_COUNTRY_EN[c]||c;}

/* ── Collection key helpers ──────────────────────────────────────────────
   collectedPlates stores "CODE::Country" keys to handle cross-country dups
   e.g. "HD::Germany" and "HD::Romania" are separate entries
   ──────────────────────────────────────────────────────────────────────── */
function collKey(code,country){return code+"::"+country;}
function parseCollKey(k){const i=k.indexOf("::");return i<0?{code:k,country:"?"}:{code:k.slice(0,i),country:k.slice(i+2)};}
function isCollected(code,country){return S.collectedPlates.includes(collKey(code,country));}

/* Migrate old plain-code format → code::country */
function migrateCollectedPlates(){
  if(\!PLATES_DATA.length)return;
  let changed=false;
  S.collectedPlates=S.collectedPlates.map(entry=>{
    if(entry.includes("::"))return entry; /* already new format */
    const code=entry.toUpperCase();
    const matches=[...new Set(PLATES_DATA.filter(p=>p.code===code).map(p=>p.country))];
    if(matches.length===1){changed=true;return collKey(code,matches[0]);}
    if(matches.length>1){changed=true;return collKey(code,matches[0]);} /* take first if ambiguous */
    return null; /* unknown code — discard */
  }).filter(Boolean);
  /* Deduplicate */
  S.collectedPlates=[...new Set(S.collectedPlates)];
  if(changed)saveCollectedPlates(S.collectedPlates);
}

/* ── Unique deduped plate view per country ───────────────────────────────
   PLATES_DATA may have 61 rows for "HD" in Germany (61 municipalities).
   We want ONE entry per code per country in the album.
   ──────────────────────────────────────────────────────────────────────── */
function getUniquePlatesForCountry(country){
  /* Returns [{code, mainRegion, extraCount}] — one entry per unique code */
  const codeMap={};
  PLATES_DATA.filter(p=>p.country===country).forEach(p=>{
    if(\!codeMap[p.code])codeMap[p.code]={code:p.code,mainRegion:p.region,count:0};
    codeMap[p.code].count++;
  });
  return Object.values(codeMap).sort((a,b)=>a.code.localeCompare(b.code));
}

/* Total unique code::country combos (= album size) */
function totalUniquePlates(){
  const seen=new Set();
  PLATES_DATA.forEach(p=>seen.add(collKey(p.code,p.country)));
  return seen.size;
}

/* ── Spotter ─────────────────────────────────────────────────────────────*/
function spotterCollect(){
  const code=(S.spotterInput||"").toUpperCase().trim();
  if(\!code){S.spotterMsg="Bitte Kennzeichen eingeben\!";S.spotterOk=null;render();return;}
  const country=S.spotterCountry&&S.spotterCountry\!=="all"?S.spotterCountry:null;
  /* Find matching plates filtered by country if set */
  const candidates=PLATES_DATA.filter(p=>p.code===code&&(country===null||p.country===country));
  if(\!candidates.length){
    /* Check if code exists in other countries */
    const elsewhere=PLATES_DATA.filter(p=>p.code===code);
    if(elsewhere.length){
      const others=[...new Set(elsewhere.map(p=>p.country))].join(", ");
      S.spotterMsg="❓ '"+esc(code)+"' "+t("spotter_not_in")+" "+(country?displayCountry(country):t("spotter_all"))+" — "+t("spotter_but_in")+": "+esc(others);
    }else{
      S.spotterMsg="❌ "+t("spotter_unknown")+": "+esc(code);
    }
    S.spotterOk=false;render();return;
  }
  const mainPlate=candidates[0];
  const mainCountry=mainPlate.country;
  const key=collKey(code,mainCountry);
  if(S.collectedPlates.includes(key)){
    S.spotterMsg=t("spotter_dup",{code:esc(code),country:displayCountry(mainCountry)});S.spotterOk=null;
  }else{
    S.collectedPlates.push(key);saveCollectedPlates(S.collectedPlates);
    const extras=candidates.length-1;
    S.spotterMsg="\u{1F389} Neu: "+code+" — "+mainPlate.region+(extras?" +"+extras+" weitere":"")+"\!";
    S.spotterOk=true;soundStamp();
  }
  S.spotterInput="";render();
}

/* ── Real plate HTML ─────────────────────────────────────────────────────*/
function renderRealPlate(code,region,extra){
  return`<div class="real-plate">
    <div class="rp-eu-strip"><span class="rp-stars">★</span></div>
    <div class="rp-body">
      <div class="rp-code">${esc(code)}</div>
      ${region?`<div class="rp-region">${esc(region)}${extra>0?" "+t("plates_more",{n:extra}):""}</div>`:""}
    </div>
  </div>`;
}

/* ── Collection Screen ───────────────────────────────────────────────────*/
function renderCollectionScreen(){
  if(\!PLATES_DATA.length)return`<div class="panel" style="text-align:center;padding:2rem"><div style="font-size:2rem">⏳</div><p style="color:var(--text3);margin-top:.5rem">Kennzeichen-Daten werden geladen…</p></div>`;
  /* Run migration once per session */
  if(\!window._platesMigrated){window._platesMigrated=true;migrateCollectedPlates();}

  const coll=S.collectedPlates;
  const total=totalUniquePlates();
  const pct=Math.round(coll.length/Math.max(total,1)*100);
  const countries=[...new Set(PLATES_DATA.map(p=>p.country))].sort();
  const view=S.albumView||"list";
  const acF=S.albumCountry||"all";
  const sCountry=S.spotterCountry||"all";

  /* Achievements: all unique codes in a country collected */
  const achs=countries.filter(c=>{
    const uCodes=getUniquePlatesForCountry(c);
    return uCodes.length>0&&uCodes.every(u=>isCollected(u.code,c));
  });

  /* ── Spotter ── */
  const spotVal=S.spotterInput||"";
  const spotMsg=S.spotterMsg||"";
  const spotCol=S.spotterOk===true?"#10b981":S.spotterOk===false?"#ef4444":"var(--text3)";
  const spotter=`<div class="album-spotter">
    <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:.4rem">
      <span class="album-spotter-title">${t("spotter_title")}</span>
      <select class="spotter-country-sel" onchange="S.spotterCountry=this.value;S.albumCountry=this.value;localStorage.setItem('geoquest_pref_country',this.value);S.spotterMsg='';render()">
        <option value="all" ${sCountry==="all"?"selected":""}>\u{1F30D} ${t("spotter_all")}</option>
        ${countries.map(c=>`<option value="${esc(c)}" ${sCountry===c?"selected":""}>${esc(c)}</option>`).join("")}
      </select>
    </div>
    <div class="album-spotter-sub">${t("spotter_hint")}</div>
    <div style="display:flex;gap:8px">
      <input type="text" maxlength="5" placeholder="e.g. D / PL" value="${esc(spotVal)}"
        oninput="S.spotterInput=this.value.toUpperCase();this.value=this.value.toUpperCase();S.spotterMsg=''"
        class="spotter-input">
      <button class="btn-p" style="width:auto;padding:.5rem 1rem;margin-bottom:0" onclick="spotterCollect()">${t("btn_collect")}</button>
    </div>
    ${spotMsg?`<div style="font-size:.82rem;font-weight:700;text-align:center;color:${spotCol};padding:.35rem 0;margin-top:4px">${esc(spotMsg)}</div>`:""}
  </div>`;

  /* ── Progress ── */
  const progressBar=`<div class="album-progress-wrap">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px">
      <span style="font-weight:900;font-size:1rem">${t("album_title")}</span>
      <span style="font-size:.78rem;color:var(--text3)">${coll.length}&thinsp;/&thinsp;${total}</span>
    </div>
    <div class="coll-progress-wrap"><div class="coll-progress-bar" style="width:${pct}%"></div></div>
    <div style="text-align:right;font-size:.65rem;color:var(--text3);margin-top:2px">${t("pct_complete",{pct})}</div>
  </div>`;

  /* ── Achievements ── */
  const achBar=achs.length?`<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:.7rem">${achs.map(c=>`<span class="coll-ach">\u{1F3C6} ${esc(c)}-Experte</span>`).join("")}</div>`:"";

  /* ── Controls ── */
  const controls=`<div style="display:flex;gap:6px;margin-bottom:.7rem;align-items:center">
    <button class="view-toggle-btn${view==="list"?" active":""}" onclick="S.albumView='list';render()">${t("album_list")}</button>
    <button class="view-toggle-btn${view==="map"?" active":""}" onclick="S.albumView='map';render()">${t("album_map")}</button>
    <select style="margin-left:auto;background:var(--bg3);color:var(--text);border:1.5px solid var(--border);border-radius:8px;padding:.3rem .5rem;font-size:.76rem" onchange="S.albumCountry=this.value;S.spotterCountry=this.value;localStorage.setItem('geoquest_pref_country',this.value);render()">
      <option value="all" ${acF==="all"?"selected":""}>${t("spotter_all")}</option>
      ${countries.map(c=>`<option value="${esc(c)}" ${acF===c?"selected":""}>${esc(c)}</option>`).join("")}
    </select>
  </div>`;

  /* ── List view: deduplicated per code per country ── */
  let listContent="";
  if(view==="list"){
    const showCountries=acF==="all"?countries:[acF];
    listContent=showCountries.map(country=>{
      const uPlates=getUniquePlatesForCountry(country);
      const collHere=uPlates.filter(u=>isCollected(u.code,country));
      if(acF==="all"&&collHere.length===0)return"";
      const cPct=Math.round(collHere.length/Math.max(uPlates.length,1)*100);
      return`<div class="album-country-section">
        <div class="album-country-header">
          <span style="font-weight:900;font-size:.88rem">${esc(country)}</span>
          <span style="font-size:.72rem;color:var(--text3)">${collHere.length}&thinsp;/&thinsp;${uPlates.length} ${t("album_codes")}</span>
        </div>
        <div style="height:4px;background:var(--bg4);border-radius:2px;overflow:hidden;margin-bottom:.65rem">
          <div style="height:100%;width:${cPct}%;background:#10b981;border-radius:2px"></div>
        </div>
        ${collHere.length
          ?`<div class="real-plate-grid">${collHere.map(u=>renderRealPlate(u.code,u.mainRegion,u.count-1)).join("")}</div>`
          :`<div style="color:var(--text3);font-size:.75rem;text-align:center;padding:.5rem 0">${t("album_empty_country",{country:displayCountry(country)})}</div>`}
      </div>`;
    }).join("");
    if(\!listContent)listContent=`<div style="text-align:center;padding:2rem;color:var(--text3)">${t("album_empty").replace("\n","<br>")}</div>`;
  }

  const mapContent=view==="map"?`<div id="album-map-svg" class="album-map-container"></div>`:"";

  if(view==="map")requestAnimationFrame(()=>drawAlbumMap());

  const backBtn=`<button onclick="S.tab='home';render()" style="display:flex;align-items:center;gap:6px;background:none;border:none;color:var(--text3);font-size:.82rem;font-weight:700;cursor:pointer;padding:.3rem .1rem;margin-bottom:.6rem;letter-spacing:.3px;transition:color .15s" onmouseenter="this.style.color='var(--text)'" onmouseleave="this.style.color='var(--text3)'"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>${t('btn_back')}</button>`;
  return`<div>${backBtn}${spotter}${progressBar}${achBar}${controls}${listContent}${mapContent}</div>`;
}

/* ── Trophy Map ──────────────────────────────────────────────────────────*/
function drawAlbumMap(){
  const el=document.getElementById("album-map-svg");
  if(\!el||typeof d3==="undefined"||typeof topojson==="undefined"||\!window.WORLD_TOPO)return;

  const coll=S.collectedPlates;
  /* Collected countries (EN) → unique codes collected there */
  const collByCountryEn={};
  coll.forEach(key=>{
    const {code,country}=parseCollKey(key);
    const en=plateCountryToEn(country);
    if(\!collByCountryEn[en])collByCountryEn[en]=[];
    /* Only add unique codes */
    if(\!collByCountryEn[en].includes(code))collByCountryEn[en].push(code);
  });
  const collCountrySet=new Set(Object.keys(collByCountryEn));

  const W=el.clientWidth||(window.innerWidth-32)||360;
  const H=Math.min(W*0.58,280);
  const proj=d3.geoMercator().scale(W*0.95).center([12,52]).translate([W/2,H/2]);
  const geoPath=d3.geoPath().projection(proj);
  const countriesGeo=topojson.feature(window.WORLD_TOPO,window.WORLD_TOPO.objects.countries);

  d3.select(el).html("");
  const svg=d3.select(el).append("svg")
    .attr("width","100%").attr("height",H)
    .style("border-radius","12px").style("display","block")
    .style("background","#c8dff0");

  /* Graticule */
  svg.append("path").datum(d3.geoGraticule()())
    .attr("d",geoPath).attr("fill","none")
    .attr("stroke","#b0cce0").attr("stroke-width",.3);

  const g=svg.append("g");

  /* Country fills */
  g.selectAll("path.country").data(countriesGeo.features)
    .join("path").attr("class","country")
    .attr("d",geoPath)
    .attr("fill",d=>{
      const name=d.properties&&d.properties.name;
      return collCountrySet.has(name)?"#10b981":"#d4dfe8";
    })
    .attr("stroke","#fff").attr("stroke-width",.4);

  /* Pins at country centroids for collected countries */
  const pinData=countriesGeo.features.filter(d=>{
    return d.properties&&collCountrySet.has(d.properties.name);
  }).map(d=>{
    const name=d.properties.name;
    const c=geoPath.centroid(d);
    return{name,c,codes:collByCountryEn[name]||[]};
  }).filter(d=>d.c&&\!isNaN(d.c[0])&&\!isNaN(d.c[1]));

  /* Drop shadow filter */
  const defs=svg.append("defs");
  const filter=defs.append("filter").attr("id","pin-shadow");
  filter.append("feDropShadow").attr("dx",0).attr("dy",1).attr("stdDeviation",1.5).attr("flood-opacity",.35);

  const pinG=g.append("g").attr("class","pins");
  pinData.forEach(d=>{
    const pg=pinG.append("g")
      .attr("transform","translate("+d.c[0]+","+d.c[1]+")")
      .style("cursor","pointer")
      .on("click",function(ev){
        ev.stopPropagation();
        d3.select(el).selectAll(".map-popup").remove();
        /* Position popup near pin, avoid overflow */
        const rect=el.getBoundingClientRect();
        const px=Math.min(d.c[0]+8,W-180);
        const py=Math.max(d.c[1]-60,4);
        const pop=d3.select(el).append("div")
          .attr("class","map-popup")
          .style("left",px+"px").style("top",py+"px")
          .style("min-width","150px").style("max-width","200px");
        pop.append("button").attr("class","map-popup-close")
          .text("✕").on("click",()=>d3.select(el).selectAll(".map-popup").remove());
        pop.append("div").attr("class","map-popup-title")
          .text(d.name+" ("+d.codes.length+")");
        const grid=pop.append("div").attr("class","map-popup-grid");
        d.codes.slice(0,9).forEach(code=>{
          const plates=PLATES_DATA.filter(p=>p.code===code&&plateCountryToEn(p.country)===d.name);
          const region=plates.length?plates[0].region:"";
          const item=grid.append("div").attr("class","real-plate real-plate-sm");
          item.append("div").attr("class","rp-eu-strip")
            .append("span").attr("class","rp-stars").text("★");
          const body=item.append("div").attr("class","rp-body");
          body.append("div").attr("class","rp-code").text(code);
          if(plates.length>1)body.append("div").attr("class","rp-region").text("+"+(plates.length-1));
        });
        if(d.codes.length>9)pop.append("div")
          .style("font-size",".65rem").style("color","var(--text3)").style("margin-top","3px")
          .text(t("plates_more",{n:d.codes.length-9}));
      });

    /* Pin circle with glow */
    pg.append("circle").attr("r",7).attr("fill","#10b981")
      .attr("stroke","#fff").attr("stroke-width",1.5)
      .attr("filter","url(#pin-shadow)");
    /* Count badge */
    pg.append("text").attr("text-anchor","middle").attr("dy","0.35em")
      .attr("fill","#fff").attr("font-size","6px").attr("font-weight","bold")
      .attr("pointer-events","none")
      .text(d.codes.length>9?"9+":d.codes.length);
  });

  /* Click outside popup closes it */
  svg.on("click",()=>d3.select(el).selectAll(".map-popup").remove());

  /* Pan/zoom (on g group, not pins layer) */
  svg.call(d3.zoom().scaleExtent([1,10]).on("zoom",ev=>{
    g.attr("transform",ev.transform);
  }));
}

/* HOME TAB */
function renderHomeTab(){
  const FILTERS=[
    {id:"all",lbl:"Alle"},
    {id:"europe",lbl:"Europa"},
    {id:"asia",lbl:"Asien"},
    {id:"america",lbl:"Amerika"},
    {id:"africa",lbl:"Afrika"},
    {id:"oceania",lbl:"Ozeanien"},
    {id:"eu_plates",lbl:"\u{1F697} Kennzeichen"},
  ];
  function catMatchesFilter(catId){
    if(S.filter==="all")return true;
    if(S.filter==="eu_plates")return catId==="eu_plates";
    if(catId==="eu_plates")return false;
    return true;
  }
  const chips=FILTERS.map(f=>`<span class="chip${S.filter===f.id?" active":""}" onclick="S.filter='${f.id}';render()">${f.lbl}</span>`).join("");
  function catSection(catId){
    const cat=MODE_CATS[catId];const unlocked=isCategoryUnlocked(catId);
    if(\!catMatchesFilter(catId))return"";
    const catModes=MODES.filter(m=>cat.modes.includes(m.id));
    const cards=catModes.map(m=>{
      const active=S.mode===m.id;
      return`<div class="mode-card${active?" active":""}${\!unlocked?" locked-card":""}" onclick="${unlocked?"startGame('"+m.id+"')":"S.lockModal='"+catId+"';render()"}" role="button">
        <span class="mode-icon">${m.icon}</span><div class="mode-title">${m.title}</div>
      </div>`;
    }).join("");
    const lockOverlay=\!unlocked?`<div class="cat-lock-overlay" onclick="S.lockModal='${catId}';render()">
      <div style="text-align:center">
        <div style="font-size:2rem;margin-bottom:6px">\u{1F512}</div>
        <div style="color:var(--text);font-weight:900;font-size:.88rem">${cat.label}</div>
        <div style="color:var(--text2);font-size:.75rem;margin:4px 0 10px">\u{1F4B0} ${cat.cost.toLocaleString()} GeoCoins</div>
        <button class="btn-p" style="width:auto;padding:.4rem .9rem;font-size:.78rem;margin-bottom:0" onclick="event.stopPropagation();S.lockModal='${catId}';render()">Freischalten</button>
      </div>
    </div>`:"";
    return`<div style="margin-bottom:.75rem">
      <div class="cat-header"><div class="cat-title">${cat.icon} ${cat.label.toUpperCase()}</div>${\!unlocked?`<span style="color:#f59e0b;font-size:.65rem;font-weight:700">\u{1F4B0} ${cat.cost.toLocaleString()} Coins</span>`:`<span style="color:#10b981;font-size:.65rem">\u2713 Freigeschaltet</span>`}</div>
      <div style="position:relative"><div class="mode-grid" style="opacity:${unlocked?1:.4}">${cards}</div>${lockOverlay}</div>
    </div>`;
  }
  /* Phase 59: Dynamic Home Header */
  const _li=sbUser&&sbProfile?.username;
  const _un=sbProfile?.username||(sbUser?.email?.split('@')[0]||'Gast');
  const _gc=(sbProfile?.geo_coins||0).toLocaleString();
  const _hdr=_li
    ?`<div style="display:flex;align-items:center;justify-content:space-between;padding:.85rem 1rem .6rem;margin-bottom:.1rem">
        <div style="font-size:1.05rem;font-weight:700;color:var(--text)">Hallo, ${_un} \u{1F44B}</div>
        <div style="display:flex;align-items:center;gap:5px;background:var(--bg2);border-radius:20px;padding:.28rem .75rem;font-size:.82rem;font-weight:700;color:#f59e0b;border:1px solid rgba(245,158,11,.25)">\u{1FA99} ${_gc}</div>
      </div>`
    :`<div style="display:flex;align-items:center;justify-content:space-between;padding:.85rem 1rem .6rem;margin-bottom:.1rem">
        <div style="font-size:1.05rem;font-weight:700;color:var(--text)">Willkommen, Gast \u{1F30D}</div>
        <button onclick="S.tab='profil';render()" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);color:#fff;border:none;border-radius:20px;padding:.3rem .8rem;font-size:.72rem;font-weight:700;cursor:pointer;white-space:nowrap;box-shadow:0 2px 8px rgba(99,102,241,.35)">\u{1F510} Fortschritt sichern</button>
      </div>`;
  return`${_hdr}${renderDailyHero()}
    <div class="pvp-hero" onclick="S.mpModal=true;render()" role="button" aria-label="Live 1vs1 starten">
      <div style="display:flex;align-items:center;gap:14px">
        <div style="font-size:2.2rem">⚔️</div>
        <div>
          <div style="font-size:1rem;font-weight:900;color:#fff">Live 1vs1 Duell</div>
          <div style="font-size:.74rem;color:rgba(255,255,255,.75);margin-top:2px">Echtzeit gegen einen Freund spielen</div>
        </div>
        <div style="margin-left:auto;background:#7c3aed;color:#fff;border-radius:20px;padding:.3rem .85rem;font-size:.76rem;font-weight:700">▶ Spielen</div>
      </div>
    </div>
    <div class="filter-bar">${chips}</div>
    ${catSection("pure_geo")}
    ${catSection("lifestyle")}
    ${catSection("eu_plates")}
    <div style="background:var(--bg2);border:2px solid #3b82f6;border-radius:16px;padding:1rem;margin-bottom:.7rem;cursor:pointer;display:flex;align-items:center;gap:14px;box-shadow:0 2px 12px rgba(59,130,246,.15);transition:transform .15s,box-shadow .15s" onclick="S.tab='album';render()" onmousedown="this.style.transform='scale(.98)'" onmouseup="this.style.transform=''">
      <div style="width:44px;height:44px;background:linear-gradient(135deg,#1d4ed8,#3b82f6);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0">\u{1F4D4}</div>
      <div style="flex:1;min-width:0">
        <div style="font-weight:900;font-size:.9rem;color:var(--text)">Kennzeichen-Album & Spotter</div>
        <div style="font-size:.72rem;color:var(--text3);margin-top:2px">${S.collectedPlates.length} von ${totalUniquePlates()||"?"} gesammelt</div>
      </div>
      <div style="color:#3b82f6;font-size:1.1rem;font-weight:700">→</div>
    </div>
    ${catSection("hl_compare")}
    ${catSection("neighbors")}
    <div class="diff-toggle">
      <button class="diff-btn ${S.diff==="casual"?"active":""}" onclick="S.diff='casual';render()">Casual</button>
      <button class="diff-btn ${S.diff==="hardcore"?"active":""}" onclick="S.diff='hardcore';render()">Hardcore</button>
      <button class="diff-btn ${S.diff==="survival"?"active":""}" onclick="S.diff='survival';render()">\ud83d\udc80 Survival</button>
    </div>
    <p style="text-align:center;color:var(--text3);font-size:.7rem;margin:.3rem 0 .5rem">${
      S.diff==="casual"?"\u{1F7E2} Casual: Gro\u00dfe St\u00e4dte \u00b7 12s \u00b7 "+ROUNDS+" Runden":
      S.diff==="hardcore"?"\u{1F525} Hardcore: Alle St\u00e4dte \u00b7 8s \u00b7 "+ROUNDS+" Runden":
      "\u{1F480} Survival: Kein Fehler erlaubt \u00b7 8s \u00b7 \u221e Runden"
    }</p>
    <div style="height:5rem"></div>`;
}

/* LERNEN TAB — Flashcards (Phase 23C) */
function renderLernenTab(){
  const pool=(()=>{
    let p=PLATES_DATA;
    if(S.fcCountry\!=="all")p=p.filter(x=>x.country===S.fcCountry);
    if(S.fcSearch.trim())p=p.filter(x=>x.code.toLowerCase().includes(S.fcSearch.toLowerCase())||x.region.toLowerCase().includes(S.fcSearch.toLowerCase()));
    return p;
  })();
  if(\!pool.length)return`<div class="panel" style="text-align:center;padding:2rem"><div style="font-size:2rem">\u{1F50D}</div><p style="color:var(--text3);margin-top:.5rem">Keine Karten gefunden.</p></div>`;
  const idx=Math.min(S.fcIdx,pool.length-1);
  const card=pool[idx];
  const countries=[...new Set(PLATES_DATA.map(p=>p.country))].sort();
  return`<div>
    <div style="display:flex;gap:6px;margin-bottom:.65rem">
      <input type="text" placeholder="Suche Code oder Region\u2026" value="${S.fcSearch}" oninput="S.fcSearch=this.value;S.fcIdx=0;S.fcFlipped=false;render()" style="flex:1">
      <select style="background:var(--bg3);color:var(--text);border:1.5px solid var(--border);border-radius:8px;padding:.4rem .6rem;font-size:.82rem" onchange="S.fcCountry=this.value;S.fcIdx=0;S.fcFlipped=false;render()">
        <option value="all" ${S.fcCountry==="all"?"selected":""}>Alle L\u00e4nder</option>
        ${countries.map(c=>`<option value="${c}" ${S.fcCountry===c?"selected":""}>${c}</option>`).join("")}
      </select>
    </div>
    <div style="text-align:center;color:var(--text3);font-size:.72rem;margin-bottom:.65rem">${idx+1} / ${pool.length} Karten</div>
    <div class="flashcard${S.fcFlipped?" flipped":""}" onclick="S.fcFlipped=\!S.fcFlipped;render()">
      <div class="fc-front">
        <div class="fc-label">KENNZEICHEN</div>
        <div class="fc-plate">${card.code}</div>
        <div class="fc-hint">Tippen zum Umdrehen</div>
      </div>
      <div class="fc-back">
        <div class="fc-label">REGION</div>
        <div class="fc-region">${card.region}</div>
        <div class="fc-country">${card.country}${card.state?" \u00b7 "+card.state:""}</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;margin-top:.85rem">
      <button class="btn-g" style="margin-bottom:0;flex:1" onclick="S.fcIdx=Math.max(0,S.fcIdx-1);S.fcFlipped=false;render()" ${idx===0?"disabled":""}>\u2190 Zur\u00fcck</button>
      <button class="btn-p" style="margin-bottom:0;flex:1" onclick="S.fcIdx=Math.min(pool.length-1,S.fcIdx+1);S.fcFlipped=false;render()" ${idx>=pool.length-1?"disabled":""}>Weiter \u2192</button>
    </div>
    <button class="btn-g" style="margin-top:.5rem" onclick="S.fcIdx=~~(Math.random()*pool.length);S.fcFlipped=false;render()">\u{1F500} Zuf\u00e4llig</button>
  </div>`;
}

/* STATS TAB (Phase 23D + existing) */
function renderStatsTab(){
  const history=loadHistory();
  const mastery=loadMastery();
  const totalStamps=Object.values(mastery).filter(m=>getMasteryRank(m.v,m.p)).length;
  const rank=getTravelRank(totalStamps);

  /* Mastery tiles */
  const tileHtml=COUNTRIES.map(co=>{
    const m=mastery[co.cc]||{v:0,p:0};const r=getMasteryRank(m.v,m.p);
    const cls=r==="gold"?"mc-done":r==="silver"?"mc-learn":r==="bronze"?"mc-new":"";
    return`<div class="mc-tile${cls?" "+cls:""}" title="${co.c} \u00b7 ${m.v} richtig" onclick="S.modal='${co.cc}';render()"></div>`;
  }).join("");

  /* Achievements */
  const h=history;
  const achHtml=ACHIEVEMENTS.map(a=>{
    const unlocked=a.check(S,h);
    return`<div class="ach-card${unlocked?" unlocked":""}">
      <div class="ach-icon">${unlocked?a.icon:"\u{1F512}"}</div>
      <div class="ach-name">${a.title}</div>
      <div class="ach-desc">${a.desc}</div>
    </div>`;
  }).join("");

  /* Stats bars */
  if(\!history.length){
    return`<div class="panel" style="text-align:center"><div style="font-size:2rem">\u{1F4CA}</div><p style="color:var(--text3);font-size:.85rem;margin-top:.5rem">Noch keine Spielhistorie.</p></div>
    <div class="panel"><div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.5rem">ACHIEVEMENTS</div><div class="ach-grid">${achHtml}</div></div>
    <div class="panel"><div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.5rem">MASTERY MAP \u2014 ${totalStamps} L\u00e4nder</div><div class="mastery-tiles">${tileHtml}</div></div>`;
  }
  const modeAcc={};
  history.forEach(g=>{if(\!modeAcc[g.mode])modeAcc[g.mode]={c:0,t:0};modeAcc[g.mode].c+=g.correct;modeAcc[g.mode].t+=g.rounds;});
  const modeBars=MODES.map(m=>{const s=modeAcc[m.id];if(\!s||\!s.t)return"";const p=Math.round(s.c/s.t*100);return`<div class="stat-bar-row"><div class="stat-bar-lbl">${m.icon} ${m.title.slice(0,11)}</div><div class="stat-bar-track"><div class="stat-bar-fill ${p<50?"low":p<80?"mid":""}" style="width:${p}%"></div></div><div class="stat-bar-pct">${p}%</div></div>`;}).filter(Boolean).join("");
  const last10=history.slice(0,10).reverse();
  const maxSc=Math.max(...last10.map(g=>g.score),1);
  const W=300,H=72;
  const svgPts=last10.map((g,i)=>{const x=last10.length>1?i*(W/(last10.length-1)):W/2;const y=H-(g.score/maxSc)*(H-12)-6;return`${x.toFixed(1)},${y.toFixed(1)}`;}).join(" ");
  const svgDots=last10.map((g,i)=>{const x=last10.length>1?i*(W/(last10.length-1)):W/2;const y=H-(g.score/maxSc)*(H-12)-6;return`<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="4" fill="#10b981"/><text x="${x.toFixed(1)}" y="${(y-8).toFixed(1)}" text-anchor="middle" fill="var(--text3)" font-size="9">${g.score>=1000?(g.score/1000).toFixed(1)+"k":g.score}</text>`;}).join("");
  const lineChart=last10.length>=2?`<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:72px;margin-bottom:.75rem"><polyline fill="none" stroke="#10b981" stroke-width="2.5" stroke-linejoin="round" points="${svgPts}"/>${svgDots}</svg>`:`<p style="color:var(--text3);font-size:.8rem;text-align:center;margin-bottom:.75rem">Mind. 2 Spiele f\u00fcr Verlauf.</p>`;
  const ccAcc={};
  history.forEach(g=>{(g.answers||[]).forEach(a=>{if(\!a.cc)return;if(\!ccAcc[a.cc])ccAcc[a.cc]={c:0,t:0};ccAcc[a.cc].t++;if(a.correct)ccAcc[a.cc].c++;});});

  return`<div class="panel" style="text-align:center;padding:.85rem 1rem">
    <div style="font-size:2rem">\u{1F4D4}</div>
    <div style="font-weight:900;font-size:.95rem;color:var(--text)">${totalStamps} L\u00e4nder \u00b7 ${rank}</div>
  </div>
  <div class="panel"><div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.5rem">MASTERY MAP</div>
    <div style="font-size:.62rem;color:var(--text3);margin-bottom:.5rem"><span style="color:#10b981">\u25a0</span> Gold \u00b7 <span style="color:#3b82f6">\u25a0</span> Silber \u00b7 <span style="color:#f59e0b">\u25a0</span> Bronze</div>
    <div class="mastery-tiles">${tileHtml}</div>
  </div>
  <div class="panel"><div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.65rem">ACHIEVEMENTS</div><div class="ach-grid">${achHtml}</div></div>
  <div class="panel"><div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.75rem">GENAUIGKEIT PRO MODUS</div>${modeBars||`<p style="color:var(--text3);font-size:.8rem">Noch nicht genug Daten.</p>`}</div>
  <div class="panel"><div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.5rem">SCORE-VERLAUF</div>${lineChart}</div>`;
}

/* LIGA TAB — Leaderboard */
function renderLigaTab(){
  const isGuest=!sbUser?.email;
  return`<div style="font-size:1.1rem;font-weight:900;color:var(--text);margin-bottom:.75rem">\u{1F3C6} Liga</div>
  ${!sbOK?`<div class="panel"><p style="color:var(--text3);font-size:.85rem">Supabase nicht konfiguriert.</p></div>`:
    isGuest?`<div class="panel" style="text-align:center;padding:1.5rem">
      <div style="font-size:2rem;margin-bottom:.5rem">\u{1F464}</div>
      <div style="font-weight:700;color:var(--text);margin-bottom:.4rem">Melde dich an</div>
      <div style="color:var(--text3);font-size:.82rem;margin-bottom:1rem">Um in der Liga zu erscheinen und Punkte zu sammeln.</div>
      <button class="btn-p" onclick="S.tab='profil';S.authMode='login';render()">\u{1F511} Anmelden</button>
    </div>`:
    S.ligaLoading?`<div style="text-align:center;padding:2rem;color:var(--text3)">Laden \u2026</div>`:
    !S.ligaData.length?`<div class="panel"><p style="color:var(--text3)">Noch keine Eintr\u00e4ge.</p></div>`:
    `<div style="display:flex;gap:5px;margin-bottom:.75rem;flex-wrap:wrap">${MODES.slice(0,8).map(m=>`<button onclick="S.ligaMode='${m.id}';loadLiga()" style="flex:1;min-width:36px;background:${(S.ligaMode||'city')===m.id?'#10b981':'var(--bg3)'};color:${(S.ligaMode||'city')===m.id?'#fff':'var(--text2)'};border:1px solid var(--border);border-radius:7px;padding:.3rem .2rem;font-size:.8rem;cursor:pointer">${m.icon}</button>`).join('')}</div>
    <div class="panel" style="padding:.5rem">${S.ligaData.map((r,i)=>{
      const rc=i===0?'gold':i===1?'silver':i===2?'bronze':'';
      const isMe=sbUser&&r.user_id===sbUser.id;
      const title=r.equipped_title?`<span style="font-size:.62rem;color:#a78bfa;margin-left:4px">${r.equipped_title}</span>`:'';
      return`<div class="lb-row${isMe?' me':''}${i<5?' promo':''}"><span class="lb-rank ${rc}">${r.rank||i+1}</span><span class="lb-name">${r.username||'Anonym'}${title}</span><span class="lb-score">${Number(r.best_score||0).toLocaleString()}</span></div>`;
    }).join('')}</div>`}`;
}
async function loadLiga(){
  if(!sb)return;
  S.ligaLoading=true;render();
  const mode=S.ligaMode||'city';
  const{data}=await sb.from("leaderboard_weekly").select("*").eq("mode",mode).order("rank",{ascending:true}).limit(30);
  S.ligaData=data||[];S.ligaLoading=false;render();
}

/* PROFIL TAB — Auth + Passport + Stats */
function renderProfilTab(){
  return renderMehrTab()+renderStatsTab();
}

/* SETTINGS MODAL */
function renderSettingsModal(){
  return`<div class="modal-overlay" onclick="if(event.target===this){S.settingsModal=false;render()}"><div class="modal-box" style="max-width:320px">
    <div style="font-size:1.1rem;font-weight:900;margin-bottom:1rem">\u2699\ufe0f Einstellungen</div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.4rem">
      <div style="font-weight:700">\u{1F310} Sprache / Language</div>
      <select onchange="setLanguage(this.value)" style="font-size:.82rem;padding:.25rem .4rem;border-radius:8px;border:1.5px solid var(--border);background:var(--bg3);color:var(--text);cursor:pointer">
        ${[["de","Deutsch"],["en","English"],["fr","Français"],["es","Español"],["it","Italiano"],["nl","Nederlands"],["pt","Português"],["pl","Polski"],["ro","Română"],["hu","Magyar"],["cs","Čeština"],["sk","Slovenčina"],["hr","Hrvatski"],["sl","Slovenščina"],["bg","Български"],["el","Ελληνικά"],["da","Dansk"],["sv","Svenska"],["fi","Suomi"],["et","Eesti"],["lv","Latviešu"],["lt","Lietuvių"],["mt","Malti"],["ga","Gaeilge"]].map(([l,n])=>`<option value="${l}" ${S.language===l?"selected":""}>${n}</option>`).join("")}
      </select>
    </div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div style="font-weight:700">\u{1F4CD} Heimatregion</div>
      <span style="font-size:.78rem;color:#3b82f6;font-weight:700;cursor:pointer" onclick="localStorage.removeItem('geoquest_last_detected_country');showToast('Erkennung wird beim n\u00e4chsten Start wiederholt')">\u21ba Reset</span>
    </div>
    <div style="font-size:.76rem;color:var(--text2);margin-bottom:.75rem">${esc(localStorage.getItem('geoquest_pref_country')||'Nicht gesetzt (auto)')}</div>
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div style="font-weight:700">\u{1F319} Dark Mode</div>
      <button onclick="S.darkMode=!S.darkMode;applyTheme();render()" class="btn-g" style="width:auto;padding:.4rem .85rem;margin-bottom:0;font-size:.8rem">${S.darkMode?'An':'Aus'}</button>
    </div>
    ${sbUser?.email?`<button class="btn-g" style="margin-bottom:.5rem;color:#f87171;border-color:#f87171" onclick="if(confirm('Wirklich abmelden?'))doLogout()">\u{1F6AA} Abmelden</button>`:''}
    <button class="btn-g" style="margin-bottom:0" onclick="S.settingsModal=false;render()">Schlie\u00dfen</button>
  </div></div>`;
}

/* MEHR TAB — Profile + Passport + Shop + Settings (Phase 27) */
function renderMehrTab(){
  const mastery=loadMastery();
  const totalStamps=Object.values(mastery).filter(m=>getMasteryRank(m.v,m.p)).length;
  const rank=getTravelRank(totalStamps);
  const rots=[-12,-8,-5,-3,0,3,5,8,12,15,-15];
  const passGrid=COUNTRIES.map(co=>{const m=mastery[co.cc]||{v:0,p:0};const r=getMasteryRank(m.v,m.p);if(!r)return`<div class="stamp-cell locked" title="${co.c}"><span>?</span></div>`;const rot=rots[co.cc.charCodeAt(0)%rots.length];return stampHtml(co.cc,r,rot);}).join("");
  const regionBars=REGIONS.map(rg=>{
    const total=rg.cc.length;const done=rg.cc.filter(cc=>getMasteryRank((mastery[cc]||{v:0}).v,(mastery[cc]||{p:0}).p)).length;
    const pct2=total>0?Math.round(done/total*100):0;const complete=pct2===100;
    return`<div class="region-bar"><div class="region-bar-lbl"><span>${rg.name}${complete?` <span style="color:#f59e0b;font-size:.6rem">+500</span>`:""}</span><span>${done}/${total}</span></div><div class="region-bar-track"><div class="region-bar-fill${complete?" done":""}" style="width:${pct2}%"></div></div></div>`;
  }).join("");
  const pu=loadPU();
  const isAnon=!sbUser?.email;
  const hasName=!!(sbProfile?.username||localStorage.getItem("gq_username"));
  let authSection="";
  if(!sbOK){
    authSection=`<div class="auth-card" style="text-align:center"><p style="color:var(--text3);font-size:.85rem">Supabase nicht konfiguriert.</p></div>`;
  } else if(isAnon||!hasName){
    const isReg=S.authMode==="register";
    authSection=`<div class="auth-card">
      <div style="text-align:center;font-size:1.5rem;margin-bottom:.75rem">${isReg?"\uD83C\uDF31":"\uD83D\uDD11"}</div>
      <div style="font-size:1rem;font-weight:900;color:var(--text);text-align:center;margin-bottom:.3rem">${isReg?"Konto erstellen":"Anmelden"}</div>
      <div style="color:var(--text3);font-size:.78rem;text-align:center;margin-bottom:1rem">${isReg?"Dein Fortschritt wird gesichert.":"Willkommen zur\u00fcck!"}</div>
      <div class="auth-tabs">
        <button class="auth-tab${S.authMode==="login"?" active":""}" onclick="S.authMode='login';S.authError='';render()">Anmelden</button>
        <button class="auth-tab${S.authMode==="register"?" active":""}" onclick="S.authMode='register';S.authError='';render()">Registrieren</button>
      </div>
      ${S.authError?`<div class="auth-err">${S.authError}</div>`:""}
      ${isReg?`<div class="auth-field"><label>BENUTZERNAME</label><input type="text" placeholder="Dein Spielername" maxlength="20" value="${S.authUsername}" oninput="S.authUsername=this.value"></div>`:""}
      <div class="auth-field"><label>E-MAIL</label><input type="email" placeholder="deine@email.de" value="${S.authEmail}" oninput="S.authEmail=this.value"></div>
      <div class="auth-field"><label>PASSWORT</label><input type="password" placeholder="${isReg?"Mind. 6 Zeichen":"\u2022\u2022\u2022\u2022\u2022\u2022"}" value="${S.authPassword}" oninput="S.authPassword=this.value" onkeydown="if(event.key==='Enter'){${isReg?"doRegister":"doLogin"}();}"></div>
      ${isReg?`<div class="auth-field"><label>PASSWORT BESTÄTIGEN</label><input type="password" placeholder="Passwort wiederholen" value="${S.authConfirm}" oninput="S.authConfirm=this.value" onkeydown="if(event.key==='Enter')doRegister();"></div>`:""}
      <button class="btn-p" onclick="${isReg?"doRegister":"doLogin"}()" ${S.authLoading?"disabled":""}>
        ${S.authLoading?"Bitte warten \u2026":isReg?"\uD83C\uDF31 Konto erstellen &amp; Fortschritt sichern":"\uD83D\uDD11 Anmelden"}
      </button>
      ${isAnon&&isReg&&totalStamps>0?`<div style="background:rgba(16,185,129,.08);border:1px solid #10b981;border-radius:8px;padding:.5rem .75rem;font-size:.74rem;color:#10b981;margin-top:.25rem">\uD83D\uDCBE ${totalStamps} Stempel &amp; deine Punkte werden \u00fcbernommen.</div>`:""}
    </div>`;
  } else {
    const name=getDisplayName();
    authSection=`<div class="auth-card">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem">
        <div style="width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#10b981,#0891b2);display:flex;align-items:center;justify-content:center;font-size:1.3rem;font-weight:900;color:#fff;flex-shrink:0">${name?name[0].toUpperCase():"\uD83D\uDC64"}</div>
        <div><div style="font-size:1rem;font-weight:900;color:var(--text)">${name||"Spieler"}</div><div style="font-size:.72rem;color:var(--text3)">${sbUser?.email||"Gast-Konto"}</div></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;text-align:center;margin-bottom:1rem">
        <div style="background:var(--bg3);border-radius:10px;padding:.6rem"><div style="color:#34d399;font-size:1.2rem;font-weight:700">${(sbProfile?.total_score||0).toLocaleString()}</div><div style="color:var(--text3);font-size:.65rem">Punkte</div></div>
        <div style="background:var(--bg3);border-radius:10px;padding:.6rem"><div style="color:#60a5fa;font-size:1.2rem;font-weight:700">${sbProfile?.games_played||0}</div><div style="color:var(--text3);font-size:.65rem">Spiele</div></div>
        <div style="background:var(--bg3);border-radius:10px;padding:.6rem"><div style="color:#fbbf24;font-size:1.2rem;font-weight:700">${totalStamps}</div><div style="color:var(--text3);font-size:.65rem">Stempel</div></div>
      </div>
      ${sbProfile?.is_premium?`<div style="background:rgba(16,185,129,.1);border:1px solid #10b981;border-radius:8px;padding:.45rem .7rem;font-size:.74rem;color:#34d399;margin-bottom:.75rem">\uD83D\uDC51 Premium aktiv</div>`:""}
      <button class="btn-g" style="margin-bottom:0;color:#f87171;border-color:#f87171" onclick="if(confirm('Wirklich abmelden?'))doLogout()">\uD83D\uDEAA Abmelden</button>
    </div>`;
  }
  return`${authSection}
  <div style="background:linear-gradient(135deg,#1e3a5f,#0f172a);border-radius:18px;padding:1.2rem;text-align:center;margin-bottom:.85rem;border:2px solid #1e3a5f">
    <div style="font-size:2rem;margin-bottom:4px">\uD83D\uDCD4</div>
    <div style="color:#93c5fd;font-weight:900;font-size:1.05rem;letter-spacing:2px">REISEPASS</div>
    <div style="color:#60a5fa;font-size:.78rem;margin-top:3px">${totalStamps} Stempel \u00b7 ${rank}</div>
  </div>
  <div class="panel" style="padding:.85rem"><div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.65rem">REGIONEN-FORTSCHRITT</div>${regionBars}</div>
  <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:8px">ALLE L\u00c4NDER</div>
  <div class="stamp-grid">${passGrid}</div>
  <div class="panel" style="padding:.85rem;margin-top:.65rem">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div><div style="color:var(--text);font-weight:700;font-size:.85rem">\uD83D\uDCB0 GeoCoins</div><div style="color:#fbbf24;font-size:1.2rem;font-weight:900">${(sbProfile?.geo_coins||0).toLocaleString()}</div></div>
      <button class="btn-p" style="width:auto;padding:.5rem 1rem;font-size:.82rem;margin-bottom:0" onclick="S.payModal=true;render()">\uD83D\uDED2 Shop</button>
    </div>
    <div style="color:var(--text3);font-size:.68rem">Power-ups: <span style="color:var(--text)">50/50: ${pu.five0||0}</span> \u00b7 <span style="color:var(--text)">Freeze: ${pu.freeze||0}</span></div>
  </div>
  <div class="panel" style="padding:.85rem">
    <div style="color:var(--text3);font-size:.65rem;font-weight:700;letter-spacing:1px;margin-bottom:.65rem">EINSTELLUNGEN</div>
    <div style="display:flex;align-items:center;justify-content:space-between">
      <div style="color:var(--text);font-size:.88rem;font-weight:700">${S.darkMode?"\uD83C\uDF19 Dunkles Design":"\u2600\uFE0F Helles Design"}</div>
      <button onclick="S.darkMode=!S.darkMode;applyTheme();render()" class="btn-g" style="width:auto;padding:.4rem .85rem;margin-bottom:0;font-size:.8rem">Wechseln</button>
    </div>
  </div>`;
}

/* LEADERBOARD helper (used from home) */
function renderLeaderboard(lbData,lbLoading,mode){
  if(lbLoading)return`<div style="text-align:center;color:var(--text3);padding:1.5rem">Laden \u2026</div>`;
  if(\!sbOK)return`<div class="panel"><p style="color:var(--text3);font-size:.85rem">Verf\u00fcgbar nach Supabase-Setup.</p></div>`;
  if(\!lbData.length)return`<div class="panel"><p style="color:var(--text3);font-size:.85rem">Noch keine Eintr\u00e4ge.</p></div>`;
  const n=lbData.length;
  return`<div style="display:flex;gap:5px;margin-bottom:.75rem;flex-wrap:wrap">${MODES.map(m=>`<button onclick="S.mode='${m.id}';showLeaderboard()" style="flex:1;min-width:36px;background:${mode===m.id?"#10b981":"var(--bg3)"};color:${mode===m.id?"#fff":"var(--text2)"};border:1px solid var(--border);border-radius:7px;padding:.3rem .2rem;font-size:.8rem;font-weight:700;cursor:pointer">${m.icon}</button>`).join("")}</div>
    ${lbData.map((r,i)=>{const rc=i===0?"gold":i===1?"silver":i===2?"bronze":"";const isMe=sbUser&&r.user_id===sbUser.id;const isPromo=i<5;const isRel=i>=n-5;let cls="lb-row";if(isMe)cls+=" me";else if(isPromo)cls+=" promo";else if(isRel)cls+=" relg";return`<div class="${cls}"><span class="lb-rank ${rc}">${r.rank}</span><span class="lb-name">${esc(r.username||"Anonym")}${isMe?`<span style="color:#34d399;font-size:.7rem;margin-left:4px">Du</span>`:""}</span><span class="lb-score">${Number(r.best_score||0).toLocaleString()}</span></div>`;}).join("")}`;
}

/* GAME HISTORY */
function loadHistory(){return _gqLoad("gq_history",[]);}
function saveHistory(entry){const h=loadHistory();h.unshift(entry);if(h.length>60)h.length=60;_gqSave("gq_history",h);}

/* ONBOARDING */
function loadOb(){try{return JSON.parse(localStorage.getItem("gq_onboarding")||"null")}catch(e){return null}}
function finishOb(){
  const l=S.obLang||"de",d=S.obDiff||"casual";
  localStorage.setItem("gq_onboarding",JSON.stringify({done:true,lang:l,diff:d}));
  localStorage.setItem("gq_lang",l);
  S.diff=d;S.obStep=0;render();
}
function renderOnboarding(step){
  const dots=[0,1,2].map(i=>`<div class="ob-dot ${i===step?"active":""}"></div>`).join("");
  if(step===0)return`<div class="ob-overlay"><div class="ob-card">
    <div class="ob-emoji">\u{1F30D}</div>
    <div class="ob-title">Willkommen bei GeoQuest</div>
    <div class="ob-sub">Das Geografie-Quiz \u2014 sammle Stempel, steige in der Liga auf\!</div>
    <div class="ob-dots">${dots}</div>
    <p style="color:var(--text3);font-size:.7rem;font-weight:700;letter-spacing:1px;margin-bottom:.6rem">SPRACHE / LANGUAGE</p>
    <div class="ob-lang-grid">
      <div class="ob-lang ${S.obLang==="de"?"sel":""}" onclick="S.obLang='de';render()">\u{1F1E9}\u{1F1EA} Deutsch</div>
      <div class="ob-lang ${S.obLang==="en"?"sel":""}" onclick="S.obLang='en';render()">\u{1F1EC}\u{1F1E7} English</div>
    </div>
    <button class="btn-p" onclick="S.obStep=1;render()">Weiter \u2192</button>
    <button class="btn-g" style="margin-top:.3rem;margin-bottom:0;font-size:.82rem;color:var(--text3);background:transparent;border:none;text-decoration:underline" onclick="const ob=loadOb();if(!ob)localStorage.setItem('gq_onboarding',JSON.stringify({done:true,lang:'de',diff:'casual'}));S.obStep=0;S.tab='profil';S.authMode='login';render()">Ich habe bereits einen Account</button>
  </div></div>`;
  if(step===1)return`<div class="ob-overlay"><div class="ob-card">
    <div class="ob-emoji">\u{1F9E0}</div>
    <div class="ob-title">Schwierigkeitsgrad</div>
    <div class="ob-sub">W\u00e4hle deinen Stil. \u00c4nderbar jederzeit.</div>
    <div class="ob-dots">${dots}</div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:1rem">
      <div class="ob-lang ${S.obDiff==="casual"?"sel":""}" onclick="S.obDiff='casual';render()" style="padding:.9rem"><div style="font-size:1.6rem;margin-bottom:4px">\u{1F7E2}</div><div style="font-weight:900;font-size:.88rem">Casual</div><div style="color:var(--text3);font-size:.7rem;margin-top:3px">Gro\u00dfe St\u00e4dte \u2022 12 Sek.</div></div>
      <div class="ob-lang ${S.obDiff==="hardcore"?"sel":""}" onclick="S.obDiff='hardcore';render()" style="padding:.9rem"><div style="font-size:1.6rem;margin-bottom:4px">\u{1F525}</div><div style="font-weight:900;font-size:.88rem">Hardcore</div><div style="color:var(--text3);font-size:.7rem;margin-top:3px">Alle St\u00e4dte \u2022 8 Sek.</div></div>
    </div>
    <button class="btn-p" onclick="S.obStep=2;render()">Weiter \u2192</button>
    <button class="btn-g" style="margin-bottom:0" onclick="S.obStep=0;render()">\u2190 Zur\u00fcck</button>
  </div></div>`;
  return`<div class="ob-overlay"><div class="ob-card">
    <div class="ob-emoji">\u{1F9ED}</div>
    <div class="ob-title">Spielmodi</div>
    <div class="ob-sub">19 Modi, ein Ziel: Die Welt kennenlernen.</div>
    <div class="ob-dots">${dots}</div>
    <div style="margin-bottom:1rem">
      <div class="ob-mode-row"><div class="ob-mode-icon">\u{1F3D9}</div><div><div style="color:var(--text);font-weight:700;font-size:.83rem">Stadt \u2192 Land</div><div class="ob-mode-desc">Welchem Land geh\u00f6rt diese Stadt?</div></div></div>
      <div class="ob-mode-row"><div class="ob-mode-icon">\u{1F697}</div><div><div style="color:var(--text);font-weight:700;font-size:.83rem">EU-Kennzeichen</div><div class="ob-mode-desc">Woher kommt dieses Kennzeichen?</div></div></div>
      <div class="ob-mode-row"><div class="ob-mode-icon">\u{1F687}</div><div><div style="color:var(--text);font-weight:700;font-size:.83rem">U-Bahn-Netz</div><div class="ob-mode-desc">Linien und km der Metros.</div></div></div>
      <div style="color:var(--text3);font-size:.7rem;text-align:center;margin-top:4px">\u2026 und 16 weitere Modi</div>
    </div>
    <button class="btn-p" onclick="finishOb()">\u{1F680} Los geht's\!</button>
    <button class="btn-g" style="margin-bottom:0" onclick="S.obStep=1;render()">\u2190 Zur\u00fcck</button>
  </div></div>`;
}

/* CHALLENGE (Phase 16) */
const CHALLENGE=(()=>{try{const p=new URLSearchParams(location.search);const gq=p.get("gq");if(gq){const[s,o,m]=gq.split(":");const safeM=MODES.find(x=>x.id===m)?m:"city";return{seed:parseInt(s),oppScore:parseInt(o),mode:safeM};}}catch(e){}return null;})();
function generateChallengeLink(seed,score){
  const url=location.href.split("?")[0]+"?gq="+seed+":"+score+":"+S.mode;
  navigator.clipboard.writeText(url).then(showCopyToast).catch(()=>{});
}
function startChallenge(ch){
  initRng(ch.seed);
  Object.assign(S,{sc:0,st:0,bs:0,rd:0,correct:0,lid:null,ph:"playing",mode:ch.mode,scoreSaved:false,sessionAnswers:[],newStamps:[],challenge:ch,challengeSeed:ch.seed,half_removed:false,freezeActive:false});
  lq();
}
function renderChallengeResult(ch,myScore,mode){
  const myWin=myScore>ch.oppScore,tie=myScore===ch.oppScore;
  const ml=MODES.find(m=>m.id===mode)?.title||mode;
  return`<div class="ch-overlay"><div class="ch-card">
    <div style="font-size:1.5rem;font-weight:900;color:var(--text);margin-bottom:4px">${myWin?"\u{1F3C6} Gewonnen\!":tie?"\u{1F91D} Unentschieden":"\u{1F614} Knapp verpasst"}</div>
    <div style="color:var(--text3);font-size:.75rem;margin-bottom:.85rem">${ml}</div>
    <div class="ch-vs">
      <div class="ch-score-box"><div style="color:var(--text3);font-size:.65rem;margin-bottom:3px">Gegner</div><div style="font-size:1.6rem;font-weight:900;color:${\!myWin&&\!tie?"#34d399":"var(--text)"}">${ch.oppScore.toLocaleString()}</div></div>
      <div style="color:var(--text3);font-weight:900;font-size:1.1rem">VS</div>
      <div class="ch-score-box"><div style="color:#34d399;font-size:.65rem;margin-bottom:3px">Du</div><div style="font-size:1.6rem;font-weight:900;color:${myWin?"#34d399":tie?"#fbbf24":"var(--text)"}">${myScore.toLocaleString()}</div></div>
    </div>
    <button class="btn-p" onclick="generateChallengeLink(${S.challengeSeed||Date.now()},${myScore})">\u{1F517} Weitergeben</button>
    <button class="btn-g" onclick="S.challenge=null;rngSeed=null;S.ph='menu';S.tab='home';render()">Zum Menü</button>
  </div></div>`;
}

/* PAYMENT (Phase 17) */
async function processMockPayment(productId){
  const p=PAY_PRODUCTS.find(x=>x.id===productId);if(\!p)return;
  if(p.pu&&p.pu_qty){addPU(p.pu,p.pu_qty);S.payModal=false;render();showToast("✓ "+p.name+" hinzugefügt\!");return;}
  if(sbOK&&sbUser){
    if(p.coins>0){const _cr=await sb.rpc("add_coins",{p_user_id:sbUser.id,p_amount:p.coins});
      if(_cr.data!=null&&sbProfile)sbProfile.geo_coins=_cr.data;
      else if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+p.coins;}
    if(p.premium){const u=new Date();u.setMonth(u.getMonth()+(p.months||1));
      const _upd={is_premium:true,premium_until:u.toISOString()};
      await sb.from("profiles").update(_upd).eq("id",sbUser.id);
      if(sbProfile)Object.assign(sbProfile,_upd);}
  }
  S.payModal=false;render();showToast("✓ "+p.name+" aktiviert\!");
}
function renderPayModal(){
  const prem=sbProfile?.is_premium;
  const until=prem&&sbProfile?.premium_until?new Date(sbProfile.premium_until).toLocaleDateString("de-DE"):"";
  return`<div class="modal-overlay" onclick="if(event.target===this){S.payModal=false;render()}"><div class="modal-box" style="max-width:360px">
    <div style="font-size:1.2rem;font-weight:900;color:var(--text);margin-bottom:.35rem">\u{1F4B3} Shop</div>
    ${prem?`<div style="background:rgba(16,185,129,.1);border:1px solid #10b981;border-radius:8px;padding:.45rem .7rem;font-size:.74rem;color:#34d399;margin-bottom:.6rem">\u{1F451} Premium aktiv${until?" • bis "+until:""}</div>`:""}
    <div style="color:var(--text3);font-size:.7rem;margin-bottom:.7rem">${STRIPE_PK?"Stripe aktiv":"Testmodus — kein echtes Geld"}</div>
    ${PAY_PRODUCTS.map(p=>`<div class="pay-product${p.featured?" featured":""}" onclick="processMockPayment('${p.id}')"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px"><div class="pay-product-name">${p.name}${p.featured?" ⭐":""}</div><div class="pay-product-price">${p.price}</div></div><div class="pay-product-desc">${p.desc}</div></div>`).join("")}
    <button class="btn-g" style="margin-bottom:0;margin-top:.35rem" onclick="S.payModal=false;render()">Schließen</button>
  </div></div>`;
}

/* PWA (Phase 18) */

/* ── Dynamic Data Loader (Phase 30) ──────────────────────────────────────────────────── */
async function loadGameData(){
  const ov=document.createElement('div');
  ov.id='gq-loader';
  ov.style='position:fixed;inset:0;background:var(--bg,#f0f4f8);display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:9999;font-family:system-ui,sans-serif';
  ov.innerHTML='<div style="font-size:2.8rem;margin-bottom:.8rem">\u{1F30D}</div>'
    +'<div style="font-size:1rem;font-weight:700;color:var(--text,#1a2a3a);margin-bottom:.4rem">GeoQuest</div>'
    +'<div id="gq-ld-msg" style="font-size:.82rem;color:var(--text2,#64748b);margin-bottom:1rem">Lade globale Datenbank…</div>'
    +'<div style="width:200px;height:5px;background:var(--bg3,#e2e8f0);border-radius:3px;overflow:hidden">'
    +'<div id="gq-prog" style="height:100%;width:0%;background:#10b981;transition:width .3s ease;border-radius:3px"></div></div>';
  document.body.appendChild(ov);
  const prog=(p)=>{const el=document.getElementById('gq-prog');if(el)el.style.width=p+'%';};
  const msg=(t)=>{const el=document.getElementById('gq-ld-msg');if(el)el.textContent=t;};

  function sv(b,f){const x=b[f];if(\!x)return '';return x.value\!==undefined?x.value:x;}

  function parsePlates(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    return arr.map(b=>({code:sv(b,'code'),region:sv(b,'regionLabel')||sv(b,'region'),country:sv(b,'countryLabel')||sv(b,'country'),state:sv(b,'stateLabel')||sv(b,'state')||''})).filter(x=>x.code&&x.country);
  }
  function parseCurr(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const seen=new Set(),out=[];
    arr.forEach(b=>{
      const c=sv(b,'countryLabel'),n=sv(b,'currencyLabel'),iso=sv(b,'isoCode');
      const k=c+'|'+iso;
      if(iso&&iso.length===3&&\!seen.has(k)){seen.add(k);out.push({c,n,iso});}
    });
    return out;
  }
  function parseCaps(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const caps={};
    arr.forEach(b=>{
      const c=sv(b,'countryLabel'),cap=sv(b,'capitalLabel'),pop=parseInt(sv(b,'population'))||0;
      if(\!caps[c]||pop>caps[c].pop)caps[c]={c,cap,pop};
    });
    return Object.values(caps);
  }
  function parseRivers(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const seen=new Set(),out=[];
    arr.forEach(b=>{
      const n=sv(b,'riverLabel'),c=sv(b,'countryLabel'),key=n+'|'+c;
      const len=Math.round(parseFloat(sv(b,'length')||0)/1000);
      if(\!seen.has(key)&&len>0){seen.add(key);out.push({n,c,len});}
    });
    return out;
  }
  function parseNeighbors(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const map={};
    arr.forEach(b=>{
      const c=sv(b,'countryLabel')||sv(b,'country');
      const nb=sv(b,'neighborLabel')||sv(b,'neighbor')||sv(b,'neighbors');
      if(\!c)return;
      if(\!map[c])map[c]=[];
      if(nb&&nb.trim()){
        /* neighbors field may be comma-separated list or single value */
        const parts=nb.split(',').map(s=>s.trim()).filter(Boolean);
        parts.forEach(p=>{if(\!map[c].includes(p))map[c].push(p);});
      }
    });
    return map;
  }
  function parseArea(json){
    const arr=json&&json.results&&json.results.bindings?json.results.bindings:json;
    const best={};
    arr.forEach(b=>{
      const c=sv(b,'countryLabel')||sv(b,'country');
      const a=parseFloat(sv(b,'area')||sv(b,'areaValue')||0);
      if(\!c||\!a)return;
      /* keep smallest area per country (filters historical empires) */
      if(\!best[c]||a<best[c])best[c]=a;
    });
    return Object.entries(best)
      .filter(([,a])=>a>100&&a<2e7)
      .map(([c,area])=>({c,area:Math.round(area)}));
  }

  /* ── per-file graceful fetch ── */
  async function safeFetch(url,label,pct){
    try{
      msg(label);
      const r=await fetch(url);
      if(\!r.ok)throw new Error(r.status+' '+url);
      const j=await r.json();
      prog(pct);
      return j;
    }catch(ex){
      console.warn('GeoQuest: could not load '+url+':',ex.message);
      prog(pct);
      return null;
    }
  }
  const errors=[];
  const pRaw  =await safeFetch('./license_plates.json',  'Lade Kennzeichen…',  18)||[];
  const cRaw  =await safeFetch('./currencies.json',       'Lade Währungen…', 32)||[];
  const capRaw=await safeFetch('./capitals_population.json','Lade Hauptstädte…',48)||[];
  const rRaw  =await safeFetch('./rivers.json',           'Lade Flüsse…',    62)||[];
  const nbRaw =await safeFetch('./neighbors.json',        'Lade Nachbarländer…',78)||[];
  const arRaw =await safeFetch('./area.json',             'Lade Länderfächen…',92)||[];
  const topoRaw=await safeFetch('./world-110m.json',       'Lade Weltkarte…',98);
  if(topoRaw)window.WORLD_TOPO=topoRaw;

  PLATES_DATA = parsePlates(Array.isArray(pRaw)?pRaw:(pRaw?.results?.bindings||[]));
  CURR_REAL   = parseCurr(cRaw);
  CAPS_POP    = parseCaps(capRaw);
  RIVERS_REAL = parseRivers(rRaw);
  const nbMap = parseNeighbors(nbRaw);
  NEIGHBORS   = Object.keys(nbMap).filter(k=>nbMap[k]&&nbMap[k].length>0).length>=10?nbMap:_DEFAULT_NEIGHBORS;
  AREA_DATA   = parseArea(arRaw);

  prog(100);
  const loaded=[PLATES_DATA.length,'plates',CURR_REAL.length,'curr',CAPS_POP.length,'caps',RIVERS_REAL.length,'rivers',Object.keys(NEIGHBORS).length,'nb',AREA_DATA.length,'areas'];
  console.log('GeoQuest data:',loaded.join(' '));
  if(\!PLATES_DATA.length||\!CURR_REAL.length||\!CAPS_POP.length){
    /* core files missing — show toast after render but still render */
    setTimeout(()=>showToast('Fehler beim Laden einiger Datensätze.'),800);
  }
  await new Promise(r=>setTimeout(r,120));
  ov.remove();
}

if("serviceWorker"in navigator){
  try{
    const swSrc=`const CACHE='gq-v4';
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.add(self.location.href)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k\!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{if(e.request.method\!=='GET')return;e.respondWith(caches.match(e.request).then(r=>{if(r)return r;return fetch(e.request).then(res=>{if(res.ok){const rc=res.clone();caches.open(CACHE).then(c=>c.put(e.request,rc));}return res;}).catch(()=>caches.match(e.request)||new Response('Offline',{status:503}));}));});`;
    const blob=new Blob([swSrc],{type:"application/javascript"});
    navigator.serviceWorker.register(URL.createObjectURL(blob),{scope:"./"}).catch(()=>{});
  }catch(e){}
  window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();S.pwaPrompt=e;const b=document.getElementById("pwa-banner");if(b)b.style.display="flex";});
}
/* Phase 32: Tab-focus anti-cheat — timer keeps running in background */
document.addEventListener("visibilitychange",()=>{
  if(!document.hidden)return;          /* only fire when going hidden */
  if(S.ph!=="playing"||S.sel!==null)return; /* not mid-question */
  /* Record when tab was hidden; on return the setInterval fires catch-up */
  S._hiddenAt=Date.now();
});
document.addEventListener("visibilitychange",()=>{
  if(document.hidden)return;           /* only fire when becoming visible */
  if(S.ph!=="playing"||S.sel!==null||!S._hiddenAt)return;
  const elapsed=Math.ceil((Date.now()-S._hiddenAt)/1000);
  S._hiddenAt=null;
  if(elapsed>0){
    S.tm=Math.max(0,S.tm-elapsed);
    if(S.tm<=0){clearInterval(tIv);answer(null);}else render();
  }
});


/* ── Phase 46: Smart Location Detection (IP-based, silent) ─────────────── */
const _GQ_IP_DE_MAP={
  "Germany":"Deutschland","Austria":"Österreich","Switzerland":"Schweiz",
  "Liechtenstein":"Liechtenstein","France":"Frankreich","Belgium":"Belgien",
  "Netherlands":"Niederlande","Luxembourg":"Luxemburg","Italy":"Italien",
  "Spain":"Spanien","Portugal":"Portugal","Poland":"Polen",
  "Czech Republic":"Tschechien","Czechia":"Tschechien","Slovakia":"Slowakei",
  "Hungary":"Ungarn","Romania":"Rumänien","Bulgaria":"Bulgarien",
  "Croatia":"Kroatien","Slovenia":"Slowenien","Serbia":"Serbien",
  "Bosnia and Herzegovina":"Bosnien","Albania":"Albanien","Montenegro":"Montenegro",
  "North Macedonia":"Nordmazedonien","Greece":"Griechenland","Turkey":"Türkei",
  "Estonia":"Estland","Latvia":"Lettland","Lithuania":"Litauen",
  "Finland":"Finnland","Sweden":"Schweden","Norway":"Norwegen","Denmark":"Dänemark",
  "Iceland":"Island","Ireland":"Irland","United Kingdom":"Vereinigtes Königreich",
  "Russia":"Russland","Ukraine":"Ukraine","Belarus":"Weißrussland",
  "Moldova":"Moldau","Georgia":"Georgien","Armenia":"Armenien","Azerbaijan":"Aserbaidschan"
};
function locationBannerYes(c){
  localStorage.setItem('geoquest_pref_country',c);
  S.spotterCountry=c;S.albumCountry=c;
  showToast('✓ Region auf '+c+' gesetzt');
  render();
}
function showLocationBanner(c){
  const old=document.getElementById('gq-loc-toast');if(old)old.remove();
  const el=document.createElement('div');
  el.id='gq-loc-toast';el.className='gq-loc-toast';
  el.innerHTML=`<span style="font-size:.8rem;color:var(--text2)">\u{1F4CD} ${t('loc_detected',{country:c})}</span>`
    +`<button class="gq-loc-btn-yes" onclick="locationBannerYes('${c.replace(/'/g,"\\'")}');document.getElementById('gq-loc-toast')?.remove()">${t('loc_adapt')}</button>`;
  document.body.appendChild(el);
  const _tid=setTimeout(()=>{
    const t=document.getElementById('gq-loc-toast');if(\!t)return;
    t.classList.add('hiding');
    setTimeout(()=>t?.remove(),300);
  },7000);
  el.querySelector('.gq-loc-btn-yes').addEventListener('click',()=>clearTimeout(_tid),{once:true});
}
async function detectUserCountry(){
  try{
    const ctrl=new AbortController();
    const tid=setTimeout(()=>ctrl.abort(),6000);
    const res=await fetch('https://ipapi.co/json/',{signal:ctrl.signal,cache:'no-store'});
    clearTimeout(tid);
    if(\!res.ok)return;
    const d=await res.json();
    const enName=d.country_name||'';
    const deCountry=_GQ_IP_DE_MAP[enName]||enName;
    if(\!deCountry)return;
    /* Only show banner if country exists in PLATES_DATA (sanity check) */
    const known=\!PLATES_DATA.length||PLATES_DATA.some(p=>p.country===deCountry);
    const last=localStorage.getItem('geoquest_last_detected_country');
    localStorage.setItem('geoquest_last_detected_country',deCountry);
    /* Auto-set language unless user manually chose one */
    if(!localStorage.getItem('geoquest_lang_manual')){
      const _cc=(d.country_code||'').toUpperCase();
      const _ccMap={
        'AT':'de','DE':'de','CH':'de','LI':'de',
        'FR':'fr','BE':'fr','LU':'fr','MC':'fr',
        'ES':'es','AD':'es',
        'IT':'it','SM':'it','VA':'it',
        'NL':'nl',
        'PT':'pt',
        'PL':'pl',
        'RO':'ro','MD':'ro',
        'HU':'hu',
        'CZ':'cs',
        'SK':'sk',
        'HR':'hr','BA':'hr',
        'SI':'sl',
        'BG':'bg',
        'GR':'el','CY':'el',
        'DK':'da',
        'SE':'sv',
        'FI':'fi',
        'EE':'et',
        'LV':'lv',
        'LT':'lt',
        'MT':'mt',
        'IE':'en','GB':'en','US':'en','AU':'en','CA':'en','NZ':'en','ZA':'en'
      };
      const _al=_ccMap[_cc]||'en';
      S.language=_al;localStorage.setItem('gq_lang',_al);
    }
    if(known&&last!==deCountry){showLocationBanner(deCountry);}
  }catch(e){}
}

loadGameData().then(()=>{render();setTimeout(detectUserCountry,2000);}).catch((e)=>{console.error("loadGameData fatal:",e);document.getElementById("gq-loader")?.remove();render();});


'''

# ── Substitute build-time data placeholders into JS ─────────────────────────
JS = (JS
  .replace('PLACEHOLDER_CJ',  CJ)
  .replace('PLACEHOLDER_CAPJ', CAPJ)
  .replace('PLACEHOLDER_RJ',  RJ)
  .replace('PLACEHOLDER_LMJ', LMJ)
  .replace('PLACEHOLDER_NPJ', NPJ)
  .replace('PLACEHOLDER_UNJ', UNJ)
  .replace('PLACEHOLDER_CLJ', CLJ)
  .replace('PLACEHOLDER_SWJ', SWJ)
  .replace('PLACEHOLDER_FJ',  FJ)
  .replace('PLACEHOLDER_BJ',  BJ)
  .replace('PLACEHOLDER_CUJ', CUJ)
)
remaining = __import__('re').findall(r'PLACEHOLDER_\w+', JS)
if remaining:
    print('WARNING: unreplaced placeholders:', set(remaining))
else:
    print('All placeholders substituted OK')


# ── Assemble final HTML ────────────────────────────────────────────────────
_HTML_HEAD = '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>GeoQuest</title>
<link rel="manifest" href="manifest.json">
<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/dist/umd/supabase.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/topojson-client@3/dist/topojson-client.min.js"></script>
<style>
:root{--bg:#f0f4f8;--bg2:#ffffff;--bg3:#f8fafc;--bg4:#e2e8f0;--border:#e2e8f0;--text:#0f172a;--text2:#475569;--text3:#94a3b8;--accent:#10b981;--shadow:0 1px 8px rgba(0,0,0,.08);--qcard:#fff;--hdr-bg:#fff;--hdr-border:#e2e8f0}
[data-theme=dark]{--bg:#0f172a;--bg2:#1e293b;--bg3:#0a0f1e;--bg4:#334155;--border:#334155;--text:#f1f5f9;--text2:#94a3b8;--text3:#475569;--shadow:0 2px 20px rgba(0,0,0,.4);--qcard:#fff;--hdr-bg:#0a0f1e;--hdr-border:#1e293b}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:var(--bg);font-family:system-ui,-apple-system,sans-serif;color:var(--text);-webkit-tap-highlight-color:transparent;transition:background .25s,color .25s}
body{padding-top:50px;padding-bottom:68px}
#app{min-height:calc(100dvh - 118px);display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding:1rem 1rem .5rem}
.scr{width:100%;max-width:420px}
.panel{background:var(--bg2);border-radius:16px;padding:1.25rem;margin-bottom:1rem;box-shadow:var(--shadow);border:1px solid var(--border)}
input[type=text]{width:100%;background:var(--bg);color:var(--text);border:1.5px solid var(--border);border-radius:8px;padding:.5rem .75rem;font-size:.88rem}
input[type=text]:focus{outline:none;border-color:var(--accent)}
input[type=text]::placeholder{color:var(--text3)}
.g-header{position:fixed;top:0;left:0;right:0;height:50px;background:var(--hdr-bg);border-bottom:1.5px solid var(--hdr-border);display:flex;align-items:center;justify-content:space-between;padding:0 1rem;z-index:300;transition:background .25s}
.g-logo{font-size:1.15rem;font-weight:900;color:var(--text);letter-spacing:-.5px}
.g-logo span{color:#10b981}
.g-stats{display:flex;gap:8px;align-items:center}
.g-stat{background:var(--bg3);border:1px solid var(--border);border-radius:8px;padding:3px 9px;font-size:.78rem;font-weight:700;color:var(--text)}
.sound-btn{background:transparent;border:none;color:var(--text3);font-size:1rem;cursor:pointer;padding:4px;display:flex;align-items:center;width:28px;height:28px;border-radius:6px}
.sound-btn:hover{color:var(--text2);background:var(--bg3)}
.bottom-nav{position:fixed;bottom:0;left:0;right:0;height:62px;background:var(--bg2);border-top:1px solid var(--border);display:flex;z-index:300;transition:background .25s;padding-bottom:env(safe-area-inset-bottom)}
.bn-item{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;cursor:pointer;border:none;background:transparent;padding:0 2px;min-width:0}
.bn-icon{font-size:1.15rem;line-height:1}
.bn-lbl{font-size:.5rem;font-weight:700;letter-spacing:.2px;white-space:nowrap}
.bn-item.active .bn-icon,.bn-item.active .bn-lbl{color:#10b981}
.bn-item:not(.active) .bn-icon,.bn-item:not(.active) .bn-lbl{color:var(--text3)}
.filter-bar{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px;margin-bottom:.85rem;-webkit-overflow-scrolling:touch;scrollbar-width:none}
.filter-bar::-webkit-scrollbar{display:none}
.chip{white-space:nowrap;background:var(--bg3);border:1.5px solid var(--border);border-radius:20px;padding:.3rem .8rem;font-size:.72rem;font-weight:700;color:var(--text2);cursor:pointer;transition:all .15s;flex-shrink:0}
.chip.active{background:#10b981;border-color:#10b981;color:#fff}
.daily-hero{background:linear-gradient(135deg,#10b981 0%,#0891b2 100%);border-radius:18px;padding:1.1rem 1.1rem .9rem;margin-bottom:.85rem;color:#fff;cursor:pointer;box-shadow:0 4px 20px rgba(16,185,129,.3)}
.daily-hero.done{background:var(--bg2);border:1.5px solid #10b981;cursor:default;box-shadow:var(--shadow);color:var(--text)}
.daily-hero.done .dh-title{color:#10b981}
.dh-title{font-size:.95rem;font-weight:900;margin-bottom:2px}
.dh-sub{font-size:.72rem;opacity:.85}
.dh-cd{font-family:monospace;font-weight:700;font-size:.8rem}
.dh-btn{background:rgba(255,255,255,.25);border:none;border-radius:8px;color:#fff;padding:.3rem .7rem;font-size:.72rem;font-weight:700;cursor:pointer;white-space:nowrap}
.daily-hero.done .dh-btn{display:none}
.btn-p{width:100%;background:#10b981;color:#fff;border:none;border-radius:12px;padding:.9rem;font-size:1rem;font-weight:900;cursor:pointer;transition:background .15s,transform .1s;margin-bottom:.5rem}
.btn-p:hover{background:#059669}.btn-p:active{transform:scale(.97)}
.btn-p:disabled{background:var(--bg4);color:var(--text3);cursor:default}
.btn-g{width:100%;background:transparent;color:var(--text2);border:1.5px solid var(--border);border-radius:12px;padding:.7rem;font-size:.9rem;font-weight:700;cursor:pointer;transition:border-color .15s;margin-bottom:.5rem}
.btn-g:hover{border-color:var(--text3);color:var(--text)}
.btn-cancel{background:transparent;border:1.5px solid var(--border);color:var(--text3);border-radius:8px;padding:3px 10px;font-size:.78rem;font-weight:700;cursor:pointer}
.btn-cancel:hover{color:#f87171;border-color:#f87171}
.diff-toggle{display:flex;background:var(--bg3);border-radius:10px;padding:3px;margin-bottom:.75rem;border:1px solid var(--border)}
.diff-btn{flex:1;background:transparent;color:var(--text3);border:none;border-radius:8px;padding:.5rem;font-size:.82rem;font-weight:700;cursor:pointer;transition:background .15s,color .15s}
.diff-btn.active{background:var(--bg2);color:var(--text);box-shadow:var(--shadow)}
.mode-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:.6rem}
.mode-grid-4{display:grid;grid-template-columns:repeat(4,1fr);gap:5px;margin-bottom:.5rem}
.mode-grid-life{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-bottom:.5rem}
.mode-card{background:var(--bg2);border:2px solid var(--border);border-radius:12px;padding:.6rem .4rem;cursor:pointer;transition:border-color .15s,background .15s;text-align:center;box-shadow:var(--shadow)}
.mode-card:hover{border-color:#10b981;background:var(--bg3)}
.mode-card.mini{border-radius:9px;padding:.38rem .25rem}
.mode-card.mini .mode-icon{font-size:1.1rem;margin-bottom:2px}
.mode-card.mini .mode-title{font-size:.58rem}
.mode-card.life{border-radius:10px;padding:.48rem .3rem}
.mode-card.life .mode-icon{font-size:1.2rem;margin-bottom:2px}
.mode-card.life .mode-title{font-size:.62rem}
.mode-card.active{border-color:#10b981;background:rgba(16,185,129,.08)}
.mode-icon{font-size:1.4rem;margin-bottom:3px;display:block}
.mode-title{color:var(--text);font-size:.68rem;font-weight:700;line-height:1.2}
.mode-card.locked-card{opacity:.35;filter:grayscale(.8);pointer-events:none}
.cat-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:.45rem;margin-top:.5rem}
.cat-title{color:var(--text3);font-size:.62rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase}
.cat-lock-overlay{position:absolute;inset:-4px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:rgba(15,23,42,.72);border-radius:14px;z-index:10;cursor:pointer;gap:5px;backdrop-filter:blur(2px)}
.hud{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.pill{background:var(--bg2);border:1px solid var(--border);border-radius:10px;padding:5px 14px;box-shadow:var(--shadow)}
.pill-s{background:rgba(251,146,60,.1);border:1.5px solid rgba(251,146,60,.35);border-radius:10px;padding:5px 14px}
.hlbl{font-size:.6rem;font-weight:600;letter-spacing:1px;color:var(--text3)}
.hval{font-size:1.2rem;font-weight:900;color:var(--text);line-height:1.2}
.hval-s{font-size:1.2rem;font-weight:900;color:#fed7aa;line-height:1.2}
.tbar{height:6px;background:var(--bg4);border-radius:99px;overflow:hidden;margin-bottom:14px}
.tfill{height:100%;border-radius:99px;transition:width 1s linear,background .4s}
.tbar.frozen .tfill{background:#3b82f6 !important;transition:none}
.qcard{background:var(--qcard);border-radius:18px;padding:1.1rem 1.1rem 1rem;text-align:center;margin-bottom:10px;box-shadow:0 2px 24px rgba(0,0,0,.12)}
.qprompt{color:var(--text2);font-size:1rem;font-weight:500;line-height:1.3;margin-bottom:8px}
.qmain{color:var(--text);font-size:2.4rem;font-weight:900;line-height:1.2;margin-bottom:4px;word-break:break-word}
.qsub{color:var(--text);font-size:1.2rem;font-weight:700;margin-bottom:4px}
.qflag{margin:2px 0 8px;display:flex;justify-content:center;align-items:center;min-height:80px}
.qflag img{width:140px;height:auto;border-radius:6px;box-shadow:0 2px 12px rgba(0,0,0,.18)}
.qmeta{color:var(--text2);font-size:.88rem;margin-bottom:10px}
.qtimer{font-size:2.7rem;font-weight:900;line-height:1;transition:color .3s}
.answers{display:flex;flex-direction:column;gap:7px}
.btn-a{background:#fff;color:#0f172a;border:2px solid #e2e8f0;border-radius:13px;padding:.75rem 1rem;font-size:.95rem;font-weight:700;cursor:pointer;display:flex;justify-content:space-between;align-items:center;transition:border-color .12s,background .12s;width:100%;text-align:left;min-height:48px}
.btn-a:hover:not(:disabled){border-color:#10b981;background:#f0fdf4}
.btn-a.ok{background:#f0fdf4;border-color:#10b981;color:#065f46}
.btn-a.ng{background:#fff1f2;border-color:#f43f5e;color:#9f1239;animation:shake .35s ease}
.btn-a.dm{background:#f8fafc;border-color:#e2e8f0;color:#94a3b8;cursor:default}
.btn-a.half{opacity:.2;pointer-events:none;cursor:default}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
.flag-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.btn-flag{background:#fff;border:3px solid #e2e8f0;border-radius:12px;padding:8px 6px;cursor:pointer;width:100%;transition:border-color .12s}
.btn-flag img{width:100%;max-height:64px;object-fit:contain;display:block;border-radius:4px}
.btn-flag.ok{border-color:#10b981;background:#f0fdf4}
.btn-flag.ng{border-color:#f43f5e;background:#fff1f2;animation:shake .35s ease}
.btn-flag.dm{opacity:.45;cursor:default}
.pu-bar{display:flex;gap:6px;justify-content:center;margin-bottom:8px}
.pu-btn{background:var(--bg2);border:2px solid var(--border);border-radius:10px;padding:.3rem .65rem;font-size:.72rem;font-weight:700;cursor:pointer;color:var(--text2);transition:all .15s;display:flex;align-items:center;gap:4px}
.pu-btn:hover:not(:disabled){border-color:#10b981;color:var(--text)}
.pu-btn:disabled{opacity:.35;cursor:default}
.pu-btn.freeze-on{border-color:#3b82f6 !important;color:#3b82f6 !important;background:rgba(59,130,246,.1) !important}
.fb{margin-top:10px;border-radius:12px;padding:.7rem 1rem;text-align:center;font-weight:700;font-size:.86rem}
.fb.ok{background:#f0fdf4;color:#065f46;border:1.5px solid #10b981}
.fb.ng{background:#fff1f2;color:#9f1239;border:1.5px solid #f43f5e}
.pts-popup{position:fixed;font-size:1.4rem;font-weight:900;color:#10b981;pointer-events:none;animation:floatUp .9s ease-out forwards;z-index:999}
@keyframes floatUp{0%{opacity:1;transform:translateY(0) scale(1)}100%{opacity:0;transform:translateY(-80px) scale(1.3)}}
.go-card{background:var(--bg2);border-radius:16px;padding:1.5rem;margin-bottom:.85rem;text-align:center;box-shadow:var(--shadow);border:1px solid var(--border)}
.go-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:.85rem}
.go-tile{background:var(--bg3);border-radius:12px;padding:.75rem .5rem;text-align:center;border:1px solid var(--border)}
.go-tile-val{font-size:1.5rem;font-weight:900;line-height:1.1}
.go-tile-lbl{font-size:.64rem;color:var(--text3);margin-top:2px}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:500;display:flex;align-items:center;justify-content:center;padding:1rem}
.modal-box{background:var(--bg2);border-radius:20px;padding:1.5rem;max-width:320px;width:100%;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,.25)}
.unlock-box{background:var(--bg2);border:1.5px solid #7c3aed;border-radius:20px;padding:1.5rem;max-width:340px;width:100%;text-align:center}
.unlock-btn{width:100%;border:none;border-radius:12px;padding:.85rem;font-size:.92rem;font-weight:900;cursor:pointer;margin-bottom:.5rem;transition:background .15s}
.unlock-btn.coin{background:#f59e0b;color:#fff}.unlock-btn.coin:hover{background:#d97706}
.unlock-btn.premium{background:#7c3aed;color:#fff}.unlock-btn.premium:hover{background:#6d28d9}
.stamp-toast{position:fixed;left:50%;transform:translateX(-50%);background:var(--bg2);border:1.5px solid #10b981;border-radius:12px;padding:.6rem 1.1rem;display:flex;align-items:center;gap:8px;font-size:.85rem;font-weight:700;color:#10b981;z-index:1000;animation:toastIn .35s ease-out;bottom:68px}
.copy-toast{position:fixed;left:50%;transform:translateX(-50%);background:var(--bg2);border:1.5px solid #3b82f6;border-radius:12px;padding:.5rem 1rem;font-size:.8rem;font-weight:700;color:#60a5fa;z-index:1000;animation:toastIn .35s ease-out;bottom:68px}
@keyframes toastIn{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
.new-stamp-banner{background:linear-gradient(135deg,#f0fdf4,#ecfdf5);border:1.5px solid #10b981;border-radius:14px;padding:.85rem 1rem;margin-bottom:.6rem;display:flex;align-items:center;gap:10px;animation:stampPop .45s cubic-bezier(.175,.885,.32,1.275)}
@keyframes stampPop{0%{transform:scale(0) rotate(-12deg);opacity:0}100%{transform:scale(1) rotate(0);opacity:1}}
.passport-cover{background:linear-gradient(135deg,#1e3a5f,#0f172a);border-radius:18px;padding:1.2rem;text-align:center;margin-bottom:.85rem;border:2px solid #1e3a5f}
.region-bar{margin-bottom:6px}
.region-bar-lbl{display:flex;justify-content:space-between;font-size:.68rem;color:var(--text2);margin-bottom:3px}
.region-bar-track{height:7px;background:var(--bg3);border-radius:99px;overflow:hidden;border:1px solid var(--border)}
.region-bar-fill{height:100%;border-radius:99px;background:#10b981;transition:width .5s}
.region-bar-fill.done{background:#f59e0b}
.stamp-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-bottom:1rem}
.stamp-cell{aspect-ratio:1;display:flex;align-items:center;justify-content:center;border-radius:8px;cursor:pointer;position:relative;background:#f8f4ef}
.stamp-cell.locked{background:var(--bg3);border:1px dashed var(--border)}
.stamp-cell.locked span{color:var(--text3);font-size:1rem}
.stamp-ink{width:48px;height:48px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-direction:column;font-weight:900;font-size:.55rem;letter-spacing:.5px;opacity:.92;transition:transform .2s;pointer-events:none;mix-blend-mode:multiply}
.stamp-cell:hover .stamp-ink{transform:scale(1.12) rotate(-3deg) !important}
.stamp-ink.bronze{border:3px double #b45309;color:#92400e;background:radial-gradient(circle,rgba(180,83,9,.22) 50%,rgba(180,83,9,.06) 100%)}
.stamp-ink.silver{border:3px double #64748b;color:#334155;background:radial-gradient(circle,rgba(100,116,139,.2) 50%,rgba(100,116,139,.05) 100%)}
.stamp-ink.gold{border:4px double #b45309;color:#92400e;background:radial-gradient(circle,rgba(217,119,6,.3) 50%,rgba(217,119,6,.08) 100%);box-shadow:0 0 14px rgba(217,119,6,.3)}
.stamp-flag{width:28px;height:auto;border-radius:2px;margin-bottom:2px;opacity:.9}
.lb-row{display:flex;align-items:center;gap:10px;padding:.6rem .75rem;border-radius:10px;margin-bottom:5px;background:var(--bg2);border:1px solid var(--border)}
.lb-row.me{background:rgba(16,185,129,.08);border-color:#10b981}
.lb-row.promo{border-left:3px solid #10b981}
.lb-row.relg{border-left:3px solid #f43f5e}
.lb-rank{color:var(--text3);font-size:.8rem;font-weight:700;width:22px;text-align:center;flex-shrink:0}
.lb-rank.gold{color:#fbbf24}.lb-rank.silver{color:#94a3b8}.lb-rank.bronze{color:#fb923c}
.lb-name{color:var(--text);font-size:.88rem;font-weight:700;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.lb-score{color:#10b981;font-size:.88rem;font-weight:900}
.lb-zone{font-size:.6rem;font-weight:700;padding:2px 5px;border-radius:4px;margin-left:4px;flex-shrink:0}
.lb-zone.up{background:rgba(16,185,129,.15);color:#10b981}
.lb-zone.dn{background:rgba(244,63,94,.15);color:#f43f5e}
.stat-bar-row{display:flex;align-items:center;gap:8px;margin-bottom:8px}
.stat-bar-lbl{color:var(--text2);font-size:.72rem;font-weight:700;width:88px;flex-shrink:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.stat-bar-track{flex:1;height:12px;background:var(--bg3);border-radius:99px;overflow:hidden;border:1px solid var(--border)}
.stat-bar-fill{height:100%;border-radius:99px;background:#10b981;transition:width .6s}
.stat-bar-fill.mid{background:#f59e0b}.stat-bar-fill.low{background:#f43f5e}
.stat-bar-pct{font-size:.72rem;font-weight:700;color:var(--text);width:35px;flex-shrink:0;text-align:right}
.ach-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:1rem}
.ach-card{background:var(--bg2);border:1.5px solid var(--border);border-radius:12px;padding:.75rem;display:flex;align-items:center;gap:10px;box-shadow:var(--shadow)}
.ach-card.unlocked{border-color:#fbbf24;background:linear-gradient(135deg,#fffbeb,#fef3c7)}
[data-theme=dark] .ach-card.unlocked{background:linear-gradient(135deg,#1e1a00,#2d2500)}
.ach-icon{font-size:1.7rem;flex-shrink:0;line-height:1}
.ach-name{font-size:.72rem;font-weight:900;color:var(--text);line-height:1.2}
.ach-desc{font-size:.62rem;color:var(--text2);margin-top:1px}
.mastery-region-lbl{color:var(--text3);font-size:.6rem;font-weight:700;letter-spacing:1.5px;margin:10px 0 6px;text-transform:uppercase}
.mastery-tiles{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:4px}
.mc-tile{border-radius:6px;padding:3px 6px;font-size:.62rem;font-weight:700;display:flex;align-items:center;gap:3px;cursor:pointer;transition:transform .15s}
.mc-tile:hover{transform:scale(1.15)}
.mc-tile img{width:14px;height:auto;border-radius:1px}
.mc-new{background:var(--bg3);color:var(--text3);border:1px solid var(--border)}
.mc-learn{background:#fef3c7;color:#92400e;border:1px solid #fde68a}
.mc-done{background:#d1fae5;color:#065f46;border:1px solid #6ee7b7}
[data-theme=dark] .mc-learn{background:#2d2500;color:#fbbf24;border-color:#854d0e}
[data-theme=dark] .mc-done{background:#022c22;color:#34d399;border-color:#065f46}
.heat-grid{display:grid;grid-template-columns:repeat(9,1fr);gap:4px;margin-bottom:.5rem}
.heat-cell{aspect-ratio:1;border-radius:4px;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:.42rem;font-weight:700;color:rgba(255,255,255,.7);transition:transform .15s}
.heat-cell:hover{transform:scale(1.2)}.heat-cell.hg{background:#10b981}.heat-cell.hy{background:#f59e0b}.heat-cell.hr{background:#f43f5e}.heat-cell.hn{background:var(--bg4)}.heat-cell.he{background:var(--bg3)}
.fc-search{position:relative;margin-bottom:.75rem}
.fc-search input{padding-left:2rem}
.fc-search-icon{position:absolute;left:.65rem;top:50%;transform:translateY(-50%);color:var(--text3);font-size:.85rem;pointer-events:none}
.fc-nav{display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem}
.fc-counter{color:var(--text2);font-size:.8rem;font-weight:700}
.fc-arr{background:var(--bg2);border:1.5px solid var(--border);border-radius:8px;padding:.3rem .65rem;font-size:1rem;cursor:pointer;color:var(--text)}
.fc-arr:hover{border-color:var(--accent)}
.flashcard{background:var(--bg2);border-radius:18px;padding:1.75rem 1.5rem;text-align:center;box-shadow:var(--shadow);border:1px solid var(--border);min-height:180px;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;margin-bottom:.75rem;position:relative}
.fc-hint{font-size:.65rem;color:var(--text3);position:absolute;bottom:.7rem;right:.9rem}
.fc-front-lbl{font-size:.65rem;font-weight:700;letter-spacing:1.5px;color:var(--text3);text-transform:uppercase;margin-bottom:.5rem}
.fc-plate{font-size:2.5rem;font-weight:900;color:#0f172a;letter-spacing:2px;background:#f0f4f8;border:3px solid #334155;border-radius:10px;padding:.3rem 1rem;margin-bottom:.4rem;display:inline-block}
.fc-back-region{font-size:1.3rem;font-weight:900;color:var(--text);margin-bottom:.3rem}
.fc-back-state{font-size:.82rem;color:var(--text2)}
.fc-back-country{font-size:.75rem;color:#10b981;font-weight:700;margin-top:4px}
.fc-filter-bar{display:flex;gap:5px;overflow-x:auto;padding-bottom:2px;margin-bottom:.75rem;scrollbar-width:none}
.fc-filter-bar::-webkit-scrollbar{display:none}
.outline-wrap{display:flex;justify-content:center;align-items:center;min-height:130px;padding:.5rem 0;margin:4px 0 8px}
.outline-path{fill:#10b981;transition:fill .4s}
.outline-path.ok{fill:#10b981;filter:drop-shadow(0 0 10px rgba(16,185,129,.9))}
.outline-path.ng{fill:#f43f5e}
.food-emoji{font-size:3.5rem;line-height:1;margin:6px 0 10px;display:block;text-align:center}
.brand-logo{font-size:1.6rem;font-weight:900;color:#0f172a;background:#fff;border-radius:10px;padding:.4rem 1rem;display:inline-block;margin-bottom:8px}
.currency-symbol{font-size:2.8rem;font-weight:900;color:#f59e0b;line-height:1;margin:4px 0 6px;display:block;text-align:center}
.plate-badge{display:inline-block;background:#fff;border:3px solid #1e293b;border-radius:10px;padding:.45rem 1.5rem;font-size:4rem;font-weight:900;letter-spacing:4px;color:#1e293b;margin:8px 0 14px;box-shadow:0 3px 14px rgba(0,0,0,.18)}
.share-btn{background:var(--bg2);color:#60a5fa;border:1.5px solid var(--border);border-radius:10px;padding:.6rem 1rem;font-size:.82rem;font-weight:700;cursor:pointer;width:100%;margin-bottom:.5rem}
.share-btn:hover{border-color:#60a5fa}
.ob-overlay{position:fixed;inset:0;background:var(--bg3);z-index:900;display:flex;align-items:center;justify-content:center;padding:1.5rem}
.ob-card{background:var(--bg2);border-radius:20px;padding:1.75rem 1.5rem;max-width:360px;width:100%;text-align:center;box-shadow:var(--shadow)}
.ob-emoji{font-size:3rem;margin-bottom:.85rem}
.ob-title{color:var(--text);font-size:1.4rem;font-weight:900;margin-bottom:.5rem}
.ob-sub{color:var(--text2);font-size:.84rem;line-height:1.55;margin-bottom:1.1rem}
.ob-dots{display:flex;justify-content:center;gap:6px;margin-bottom:1.1rem}
.ob-dot{width:7px;height:7px;border-radius:50%;background:var(--bg4);transition:background .2s}
.ob-dot.active{background:#10b981}
.ob-lang-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:1rem}
.ob-lang{background:var(--bg3);border:2px solid var(--border);border-radius:12px;padding:.75rem;cursor:pointer;color:var(--text);font-weight:700;font-size:.9rem;transition:border-color .15s}
.ob-lang:hover{border-color:var(--text3)}.ob-lang.sel{border-color:#10b981;background:rgba(16,185,129,.08);color:#10b981}
.ob-mode-row{display:flex;align-items:center;gap:10px;background:var(--bg3);border-radius:10px;padding:.6rem .85rem;margin-bottom:7px;text-align:left}
.ob-mode-icon{font-size:1.3rem;flex-shrink:0}
.ob-mode-desc{font-size:.77rem;color:var(--text2);line-height:1.3}
.guest-hook{background:linear-gradient(135deg,#f5f3ff,#ede9fe);border:1.5px solid #7c3aed;border-radius:14px;padding:1rem;margin-bottom:.85rem}
[data-theme=dark] .guest-hook{background:linear-gradient(135deg,#1e1035,#0f172a)}
.pay-product{background:var(--bg3);border:2px solid var(--border);border-radius:12px;padding:.85rem;margin-bottom:8px;cursor:pointer;transition:border-color .15s;text-align:left}
.pay-product:hover{border-color:#10b981}.pay-product.featured{border-color:#7c3aed}
.pay-product-name{color:var(--text);font-weight:700;font-size:.88rem}
.pay-product-price{color:#10b981;font-weight:900;font-size:1.05rem;margin:.2rem 0}
.pay-product-desc{color:var(--text3);font-size:.72rem}
.confetti-piece{position:fixed;top:-12px;width:9px;height:9px;z-index:9999;animation:cfFall 2.2s ease-in forwards;pointer-events:none}
@keyframes cfFall{0%{transform:translateY(0) rotate(0deg) scale(1);opacity:1}100%{transform:translateY(105vh) rotate(720deg) scale(.5);opacity:0}}
.pwa-banner{position:fixed;bottom:60px;left:0;right:0;background:var(--bg2);border-top:1px solid var(--border);padding:.6rem 1rem;display:flex;align-items:center;justify-content:space-between;z-index:290;font-size:.78rem;color:var(--text2)}
.pwa-install-btn{background:#10b981;color:#fff;border:none;border-radius:8px;padding:5px 12px;font-size:.78rem;font-weight:700;cursor:pointer}
.ch-card{background:var(--bg2);border-radius:20px;padding:1.5rem;max-width:340px;width:100%;text-align:center}
.ch-vs{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;margin:1rem 0}
.ch-score-box{background:var(--bg3);border-radius:12px;padding:.85rem .5rem}
.settings-row{display:flex;align-items:center;justify-content:space-between;padding:.65rem 0;border-bottom:1px solid var(--border)}
.settings-row:last-child{border-bottom:none}
.toggle-switch{position:relative;width:42px;height:24px;flex-shrink:0}
.toggle-switch input{opacity:0;width:0;height:0}
.toggle-slider{position:absolute;inset:0;background:var(--bg4);border-radius:12px;cursor:pointer;transition:.3s}
.toggle-slider:before{content:"";position:absolute;height:18px;width:18px;left:3px;bottom:3px;background:#fff;border-radius:50%;transition:.3s}
.toggle-switch input:checked + .toggle-slider{background:#10b981}
.toggle-switch input:checked + .toggle-slider:before{transform:translateX(18px)}
.daily-banner{background:linear-gradient(135deg,#1e3a5f 0%,#1e293b 100%);border:1.5px solid #2563eb;border-radius:14px;padding:.75rem .9rem;margin-bottom:.65rem;cursor:pointer}
.daily-banner.done{border-color:#10b981;cursor:default;opacity:.8}
.daily-cd{font-family:monospace;color:#fbbf24;font-weight:700}
@media(max-width:360px){.qmain{font-size:1.65rem}.btn-a{font-size:.88rem;padding:.65rem .85rem}.qcard{padding:.9rem .9rem .8rem}.mode-grid-4{grid-template-columns:repeat(3,1fr)}.hud{margin-bottom:6px}.tbar{margin-bottom:10px}}
@media(max-height:620px){.qcard{padding:.8rem 1rem}.btn-a{min-height:44px;padding:.6rem .9rem;font-size:.88rem}.answers{gap:5px}.hud{margin-bottom:6px}.tbar{margin-bottom:8px}.qmain{font-size:1.65rem}}

/* Phase 27 — Auth Card */
.auth-card{background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.1rem;margin-bottom:.85rem}
.auth-tabs{display:flex;gap:4px;margin-bottom:.85rem;background:var(--bg3);border-radius:10px;padding:3px}
.auth-tab{flex:1;padding:.45rem;border:none;background:transparent;border-radius:8px;font-weight:700;font-size:.82rem;color:var(--text2);cursor:pointer;transition:.15s}
.auth-tab.active{background:var(--bg);color:var(--text);box-shadow:0 1px 4px rgba(0,0,0,.12)}
.auth-field{margin-bottom:.65rem}
.auth-field label{display:block;font-size:.6rem;font-weight:700;letter-spacing:1px;color:var(--text3);margin-bottom:.3rem}
.auth-field input{width:100%;box-sizing:border-box}
.auth-err{background:#fee2e2;border:1px solid #fca5a5;border-radius:8px;padding:.4rem .6rem;font-size:.76rem;color:#b91c1c;margin-bottom:.65rem}

/* Phase 28 */
.hdr-gear{background:none;border:none;font-size:1.1rem;cursor:pointer;padding:.2rem .4rem;margin-left:4px;line-height:1}
.conv-modal-bg{position:fixed;inset:0;background:rgba(0,0,0,.6);display:flex;align-items:center;justify-content:center;z-index:999;padding:1rem}
.conv-modal{background:var(--bg2);border-radius:18px;padding:1.4rem;max-width:340px;width:100%;text-align:center;border:2px solid #7c3aed}
.pop-compare-wrap{display:flex;align-items:center;justify-content:center;gap:12px;margin:1rem 0}
.pop-box{background:var(--bg3);border:2px solid var(--border);border-radius:14px;padding:.8rem 1rem;text-align:center;min-width:100px}
.pop-country{font-weight:900;font-size:1.3rem;color:var(--text);margin-bottom:.3rem}
.pop-value{color:#10b981;font-size:1rem;font-weight:700}

/* Phase 30 — Higher/Lower cards */
.hl-wrap{display:flex;align-items:center;justify-content:center;gap:10px;margin:10px 0 6px;flex-wrap:nowrap}
.hl-card{background:var(--bg3);border:2px solid var(--border);border-radius:14px;padding:.7rem .9rem;text-align:center;min-width:108px;max-width:160px;flex:1;transition:border-color .25s}
.hl-card.hl-known{border-color:#10b981}
.hl-card.hl-hidden{border-color:var(--border);opacity:.85}
.hl-card.hl-revealed{border-color:#3b82f6;opacity:1}
.hl-name{font-weight:900;font-size:1.1rem;color:var(--text);margin-bottom:.35rem;word-break:break-word;overflow-wrap:break-word;line-height:1.25}
.hl-val{color:#10b981;font-size:1.05rem;font-weight:700}
.hl-hidden .hl-val{color:var(--text3);font-size:1.4rem}
.hl-vs{font-size:1.5rem;flex-shrink:0;color:var(--text3)}
/* Phase 30 — Survival diff button */
.diff-btn.active[onclick*="survival"]{background:#7f1d1d;color:#fca5a5;border-color:#ef4444}

/* Phase 33 — Multiplayer */
.pvp-hero{background:linear-gradient(135deg,#1e1b4b 0%,#312e81 100%);border:1.5px solid #7c3aed;border-radius:14px;padding:.85rem 1rem;margin-bottom:.65rem;cursor:pointer;transition:opacity .15s}
.pvp-hero:active{opacity:.8}
.spinner{width:28px;height:28px;border:3px solid var(--border);border-top-color:#7c3aed;border-radius:50%;animation:spin .7s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}

/* ── Phase 34: Map Guesser ───────────────────────────────────── */
.map-scr{display:flex;flex-direction:column;padding-bottom:.5rem}
.map-prompt{text-align:center;font-size:1rem;font-weight:700;color:var(--text);
  padding:.5rem .8rem .35rem;letter-spacing:.01em}
.map-prompt strong{color:#3b82f6}
.map-container{flex:1;min-height:200px;max-height:300px;width:100%;
  background:var(--bg2);border-radius:14px;overflow:hidden;
  touch-action:pan-x pan-y;margin-bottom:.5rem}
.map-container svg{display:block;width:100%;height:100%}
.map-container .ctry{cursor:pointer;transition:fill .15s}
.map-weiter{margin:.25rem .8rem .4rem}

/* ── Phase 33 Teil 2: MP result card ────────────────────────── */
.mp-result-card{background:var(--bg2);border:1.5px solid var(--border);
  border-radius:18px;padding:1rem;margin:.75rem 0 .25rem;text-align:center}
.mp-result-title{font-size:.68rem;font-weight:800;letter-spacing:1.5px;
  color:var(--text3);text-transform:uppercase;margin-bottom:.75rem}
.mp-result-row{display:flex;justify-content:space-around;align-items:center;gap:.5rem}
.mp-result-col{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px}
.mp-result-name{font-size:.75rem;color:var(--text2);font-weight:600;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:90px}
.mp-result-score{font-size:1.65rem;font-weight:900;letter-spacing:-1px}
.mp-you .mp-result-score{color:#10b981}
.mp-opp .mp-result-score{color:#8b5cf6}
.mp-result-verdict{font-size:.95rem;font-weight:800;margin-top:.65rem;color:var(--text)}

/* ── Phase 33 T2: Duell Live-Bar ─────────────────────────────── */
.duell-bar-wrap{display:flex;align-items:center;gap:5px;
  padding:3px 8px 5px;margin-bottom:2px}
.duell-track{flex:1;height:6px;background:var(--bg3);border-radius:3px;
  overflow:hidden;display:flex}
.duell-fill-you{background:#10b981;height:100%;border-radius:3px 0 0 3px;
  transition:width .5s ease}
.duell-fill-opp{background:#8b5cf6;height:100%;border-radius:0 3px 3px 0;
  transition:width .5s ease;margin-left:auto}
.duell-lbl{font-size:.62rem;font-weight:700;color:var(--text3);
  display:flex;flex-direction:column;align-items:center;min-width:34px;line-height:1.2}
.duell-you{color:#10b981}
.duell-opp{color:#8b5cf6}
.duell-score{font-size:.7rem;font-weight:800;font-variant-numeric:tabular-nums}
/* final comparison bar on game-over */
.duell-final-bar{display:flex;height:10px;border-radius:5px;overflow:hidden;
  margin:.6rem 0 .4rem;background:var(--bg3)}
.dfb-fill-you{background:#10b981;transition:width .8s ease}
.dfb-fill-opp{background:#8b5cf6;margin-left:auto;transition:width .8s ease}
.mp-waiting{color:var(--text3);font-size:.82rem;margin-top:.5rem;line-height:1.6}

/* ── Phase 35: H/L dedicated buttons ─────────────────────────── */
.hl-btn-row{display:flex;flex-direction:column;gap:8px;margin:.6rem 0 .2rem;padding:0 .5rem}
.hl-btn{width:100%;padding:.7rem .5rem;border-radius:12px;border:2px solid var(--border);
  background:var(--bg2);color:var(--text);font-weight:700;font-size:.92rem;
  cursor:pointer;transition:background .15s,border-color .15s}
.hl-btn:not([disabled]):hover{background:var(--bg3)}
.hl-btn.ok{background:#d1fae5;border-color:#10b981;color:#065f46}
.hl-btn.ng{background:#fee2e2;border-color:#ef4444;color:#991b1b}
.hl-btn.dm{opacity:.45}
/* outline SVG container */
.outline-wrap{display:flex;align-items:center;justify-content:center;
  height:150px;width:100%;margin:6px auto}
.outline-wrap svg{max-height:150px;width:auto}
/* flag fallback */
.flag-fb{font-size:2.5rem;line-height:1;display:flex;align-items:center;justify-content:center;
  width:100%;height:100%}

/* ── Phase 36: MP Lobby polish ─────────────────────────────── */
.mp-lobby-title{
  font-size:1.9rem;font-weight:900;letter-spacing:-.5px;
  background:linear-gradient(135deg,#6366f1,#8b5cf6,#a855f7);
  -webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;color:transparent;
  display:inline-block;padding:0 4px}
.mp-back-btn{
  display:block;width:100%;margin-top:1rem;padding:.85rem;
  background:var(--bg3);color:var(--text2);border:1.5px solid var(--border);
  border-radius:14px;font-weight:700;font-size:.9rem;cursor:pointer;
  text-align:center;transition:background .15s}
.mp-back-btn:hover{background:var(--bg2)}

/* ── Phase 37-40: Kennzeichen-Album & Roadtrip-Spotter ── */
.coll-header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.4rem}
.coll-title{font-weight:900;font-size:1rem;color:var(--text)}
.coll-sub{font-size:.78rem;color:var(--text3)}
.coll-progress-wrap{height:8px;background:var(--bg3);border-radius:4px;overflow:hidden;margin-bottom:.25rem}
.coll-progress-bar{height:100%;background:linear-gradient(90deg,#10b981,#3b82f6);border-radius:4px;transition:width .6s ease}
.coll-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(72px,1fr));gap:7px;margin-bottom:1.5rem}
.coll-item{display:flex;flex-direction:column;align-items:center;gap:3px}
.coll-locked{opacity:.38;filter:grayscale(1)}
.coll-plate{font-size:.88rem;font-weight:900;letter-spacing:1px;border:2px solid #666;border-radius:6px;padding:4px 7px;text-align:center;min-width:46px;background:var(--bg2);transition:border-color .2s,color .2s}
.coll-region{font-size:.58rem;color:var(--text3);text-align:center;max-width:72px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.coll-dot{width:6px;height:6px;border-radius:50%}
.coll-ach{display:inline-flex;align-items:center;gap:4px;background:rgba(245,158,11,.12);border:1px solid #f59e0b;border-radius:20px;padding:3px 9px;font-size:.7rem;font-weight:700;color:#f59e0b}
/* Toast */
.gq-toast{position:fixed;bottom:90px;left:50%;transform:translateX(-50%);background:#1e293b;color:#f8fafc;padding:.55rem 1.1rem;border-radius:20px;font-size:.8rem;font-weight:600;z-index:9999;white-space:nowrap;max-width:92vw;box-shadow:0 4px 20px rgba(0,0,0,.4);pointer-events:none;animation:gqToastIn .22s ease}
@keyframes gqToastIn{from{opacity:0;transform:translateX(-50%) translateY(8px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}

/* Album shortcut banner in Home tab */
.album-shortcut{display:flex;align-items:center;justify-content:space-between;background:linear-gradient(135deg,#1e3a5f,#1e4080);border:1.5px solid #3b82f6;border-radius:14px;padding:.7rem 1rem;margin-bottom:.65rem;cursor:pointer;transition:opacity .15s;color:#fff;font-weight:700;font-size:.9rem}
.album-shortcut:active{opacity:.8}
.album-shortcut-count{font-size:.75rem;background:rgba(255,255,255,.15);border-radius:20px;padding:.2rem .65rem;font-weight:600}

/* ── Phase 41: Album Entry Button ── */
.album-entry-btn{display:flex;align-items:center;gap:12px;background:linear-gradient(135deg,#1e3a8a,#1d4ed8);border:1.5px solid #3b82f6;border-radius:14px;padding:.85rem 1rem;margin-bottom:.65rem;cursor:pointer;transition:opacity .15s}
.album-entry-btn:active{opacity:.8}

/* ── Phase 41: Spotter ── */
.album-spotter{background:var(--bg2);border:1.5px solid var(--border);border-radius:16px;padding:1.1rem;margin-bottom:.9rem}
.album-spotter-title{font-weight:900;font-size:.95rem;margin-bottom:2px}
.album-spotter-sub{color:var(--text3);font-size:.74rem;margin-bottom:.7rem}
.spotter-input{flex:1;font-size:1.6rem;font-weight:900;text-align:center;letter-spacing:5px;text-transform:uppercase;padding:.4rem .3rem;border-radius:8px;border:2px solid var(--border);background:var(--bg);color:var(--text);width:0}

/* ── Phase 41: Progress ── */
.album-progress-wrap{background:var(--bg2);border:1.5px solid var(--border);border-radius:14px;padding:.9rem;margin-bottom:.7rem}

/* ── Phase 41: View toggle ── */
.view-toggle-btn{background:var(--bg3);border:1.5px solid var(--border);border-radius:8px;padding:.35rem .8rem;font-size:.8rem;font-weight:700;color:var(--text3);cursor:pointer;transition:all .15s}
.view-toggle-btn.active{background:#10b981;border-color:#10b981;color:#fff}

/* ── Phase 41: Country sections (List view) ── */
.album-country-section{margin-bottom:1.1rem}
.album-country-header{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:.3rem}
.real-plate-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:7px;margin-bottom:.4rem}

/* ── Phase 41: Real license plate card ── */
.real-plate{display:flex;align-items:stretch;background:#fff;border:2px solid #1a1a1a;border-radius:5px;overflow:hidden;box-shadow:0 1px 4px rgba(0,0,0,.18);cursor:default;min-height:44px}
.real-plate-sm{min-height:34px}
.rp-eu-strip{width:16px;background:#003399;display:flex;flex-direction:column;align-items:center;justify-content:center;flex-shrink:0;padding:2px 0}
.rp-stars{color:#fc0;font-size:.45rem;line-height:1;display:block;text-align:center}
.rp-body{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:3px 6px}
.rp-code{font-size:1rem;font-weight:900;letter-spacing:2px;color:#111;font-family:'Arial Black',Arial,sans-serif;line-height:1}
.real-plate-sm .rp-code{font-size:.78rem;letter-spacing:1px}
.rp-region{font-size:.52rem;color:#555;letter-spacing:.3px;margin-top:1px;text-align:center;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

/* ── Phase 41: Map ── */
.album-map-container{width:100%;min-height:240px;border-radius:12px;overflow:hidden;position:relative;background:var(--bg3);margin-bottom:1rem}
.map-popup{position:absolute;background:var(--bg2);border:1.5px solid var(--border);border-radius:10px;padding:.6rem .7rem;box-shadow:0 4px 20px rgba(0,0,0,.25);z-index:50;pointer-events:auto;min-width:140px}
.map-popup-title{font-weight:900;font-size:.8rem;margin-bottom:.4rem;color:var(--text)}
.map-popup-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:4px;margin-bottom:2px}
.map-popup-close{position:absolute;top:5px;right:6px;background:none;border:none;
/* Location detection toast */
.gq-loc-toast{position:fixed;bottom:76px;left:50%;transform:translateX(-50%);z-index:9998;background:var(--bg2);border:1.5px solid #3b82f6;border-radius:24px;padding:.55rem .85rem .55rem .8rem;box-shadow:0 4px 18px rgba(0,0,0,.28);display:flex;align-items:center;gap:.6rem;white-space:nowrap;animation:locToastIn .3s cubic-bezier(.34,1.56,.64,1) both}
.gq-loc-toast.hiding{animation:locToastOut .3s ease forwards}
.gq-loc-btn-yes{background:#3b82f6;color:#fff;border:none;border-radius:14px;padding:.3rem .75rem;font-weight:700;font-size:.76rem;cursor:pointer;flex-shrink:0}
@keyframes locToastIn{from{opacity:0;transform:translateX(-50%) translateY(14px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
@keyframes locToastOut{to{opacity:0;transform:translateX(-50%) translateY(12px)}}
</style>
</head>
<body>
<div id="app"></div>
'''
_HTML_TAIL = '''</script>
</body>
</html>'''
# Inject fresh CSS from geoquest_css.txt (overrides the static CSS in _HTML_HEAD)
_si = _HTML_HEAD.find('<style>')
_se = _HTML_HEAD.find('</style>') + len('</style>')
if _si >= 0 and _se > _si:
    _HTML_HEAD = _HTML_HEAD[:_si] + '<style>\n' + CSS + '\n</style>' + _HTML_HEAD[_se:]
HTML = _HTML_HEAD + '<script>\n' + JS + '\n' + _HTML_TAIL
HTML = HTML.replace('\\!', '!')
out = 'GeoQuest.html'
with open(out, 'w', encoding='utf-8') as _f:
    _f.write(HTML)
print(f'Written: {len(HTML):,} chars → {out}')
