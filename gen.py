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
const LANG={
  de:{play:"SPIELEN",again:"NOCHMAL",menu:"Hauptmen\u00fc",board:"Bestenliste",pass:"Reisepass",profile:"Profil",stats:"Statistik",casual:"Casual",hardcore:"Hardcore",rounds:"Runden"},
  en:{play:"PLAY",again:"PLAY AGAIN",menu:"Main Menu",board:"Leaderboard",pass:"Passport",profile:"Profile",stats:"Stats",casual:"Casual",hardcore:"Hardcore",rounds:"Rounds"},
};
function T(k){const l=localStorage.getItem("gq_lang")||"de";return(LANG[l]||LANG.de)[k]||k;}

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
  const idx=~~(Math.random()*CURR_REAL.length);
  const cor=CURR_REAL[idx];
  /* Show only currency name+ISO — NOT country name (would give away the answer) */
  const dis=CURR_REAL.filter((_,i)=>i!==idx).sort(()=>Math.random()-.5).slice(0,3).map(x=>x.n+" ("+x.iso+")");
  const ans=cor.n+" ("+cor.iso+")";
  return{type:"curr_real",prompt:"Welche W\u00e4hrung hat …",subj:cor.c,ans,opts:sh([ans,...dis]),meta:cor.n,lid:cor.c,cc:ccFromCountry(cor.c)};
}
function genPopCompareQ(){
  if(!CAPS_POP||CAPS_POP.length<2)return null;
  const pool=CAPS_POP.filter(x=>x.pop>500000);
  const ai=~~(Math.random()*pool.length);
  let bi=~~(Math.random()*pool.length);
  while(bi===ai)bi=~~(Math.random()*pool.length);
  const a=pool[ai],b=pool[bi];
  const ans=b.pop>a.pop?"more":"less";
  const wrong=b.pop>a.pop?"less":"more";
  const aPopStr=(a.pop/1e6).toFixed(1)+" Mio.";
  return{type:"pop_compare",prompt:"Mehr oder weniger Einwohner?",subj:{nameA:a.c,popA:aPopStr,nameB:b.c},ans,opts:[ans,wrong],meta:"",lid:b.c,cc:ccFromCountry(b.c)};
}
function genRiverRealQ(){
  if(!RIVERS_REAL||!RIVERS_REAL.length)return null;
  const idx=~~(Math.random()*RIVERS_REAL.length);
  const cor=RIVERS_REAL[idx];
  const countries=[...new Set(RIVERS_REAL.map(r=>r.c))];
  const dis=countries.filter(c=>c!==cor.c).sort(()=>Math.random()-.5).slice(0,3);
  const meta=cor.len>0?cor.len+" km":"";
  return{type:"river_real",prompt:"Durch welches Land flie\u00dft dieser Fluss?",subj:cor.n,ans:cor.c,opts:sh([cor.c,...dis]),meta,lid:cor.n,cc:ccFromCountry(cor.c)};
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
  const pool=CAPS_POP.filter(x=>x.pop>500000);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const fmt=(p)=>p>=1e9?(p/1e9).toFixed(2)+" Mrd.":p>=1e6?(p/1e6).toFixed(1)+" Mio.":(p/1e3).toFixed(0)+" Tsd.";
  const ans=b.pop>a.pop?"higher":"lower";
  return{type:"hl_pop",prompt:"Mehr Einwohner als "+a.c+"?",nameA:a.c,valA:fmt(a.pop),nameB:b.c,valB:fmt(b.pop),ans,opts:["higher","lower"],lid:b.c,cc:ccFromCountry(b.c)};
}
function genHLRiverQ(){
  if(\!RIVERS_REAL||RIVERS_REAL.length<2)return null;
  const pool=RIVERS_REAL.filter(r=>r.len>100);if(pool.length<2)return null;
  const ai=~~(rng()*pool.length);let bi=~~(rng()*pool.length);while(bi===ai)bi=~~(rng()*pool.length);
  const a=pool[ai],b=pool[bi];
  const ans=b.len>a.len?"higher":"lower";
  return{type:"hl_river",prompt:"Länger als "+a.n+"?",nameA:a.n,valA:a.len+" km",nameB:b.n,valB:b.len+" km",ans,opts:["higher","lower"],lid:b.n,cc:ccFromCountry(b.c)};
}
function genHLAreaQ(){
  if(\!AREA_DATA||AREA_DATA.length<2)return null;
  const ai=~~(rng()*AREA_DATA.length);let bi=~~(rng()*AREA_DATA.length);while(bi===ai)bi=~~(rng()*AREA_DATA.length);
  const a=AREA_DATA[ai],b=AREA_DATA[bi];
  const fmt=(x)=>x>=1e6?(x/1e6).toFixed(2)+" Mio. km²":(x/1000).toFixed(0)+" Tsd. km²";
  const ans=b.area>a.area?"higher":"lower";
  return{type:"hl_area",prompt:"Größer als "+a.c+"?",nameA:a.c,valA:fmt(a.area),nameB:b.c,valB:fmt(b.area),ans,opts:["higher","lower"],lid:b.c,cc:ccFromCountry(b.c)};
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

  return`<div class="scr"><button onclick="mpLeave()">← Zurück</button></div>`;
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

function loadUnlocked(){try{return JSON.parse(localStorage.getItem("gq_unlocked")||'["pure_geo"]');}catch(e){return["pure_geo"];}}
function saveUnlocked(arr){try{localStorage.setItem("gq_unlocked",JSON.stringify(arr));}catch(e){}}
function isCategoryUnlocked(catId){return true;/* TEST MODE — all categories unlocked */}
function buyCategory(catId){
  if(!sb||!sbUser?.id){showToast("Bitte einloggen\!"); return;}
  const cat=MODE_CATS[catId];if(!cat)return;
  const coins=sbProfile?.geo_coins||0;
  if(coins<cat.cost){showToast("Zu wenig GeoCoins\!");return;}
  if(sbProfile)sbProfile.geo_coins=coins-cat.cost;
  const arr=loadUnlocked();if(\!arr.includes(catId))arr.push(catId);saveUnlocked(arr);
  if(sb&&sbUser){sb.from("profiles").update({geo_coins:coins-cat.cost}).eq("id",sbUser.id).then(()=>{});}
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
function loadPU(){try{return JSON.parse(localStorage.getItem("gq_pu")||"{}")}catch(e){return{}}}
function savePU(d){try{localStorage.setItem("gq_pu",JSON.stringify(d))}catch(e){}}
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
  const pu=loadPU();if(\!(pu.freeze>0)){showToast("Kein Zeit-Stopp mehr\!");return;}
  pu.freeze--;savePU(pu);
  clearInterval(tIv);S.freezeActive=true;
  const bar=document.querySelector(".tbar");if(bar)bar.classList.add("frozen");
  render();
  setTimeout(()=>{
    S.freezeActive=false;
    const b2=document.querySelector(".tbar");if(b2)b2.classList.remove("frozen");
    tIv=setInterval(()=>{S.tm--;if(S.tm===3)soundWarn();if(S.tm<=0){clearInterval(tIv);answer(null);}else render();},1000);
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
  await sb.from("profiles").update({geo_coins:totalCoins}).eq("id",uid).catch(()=>{});
  if(sbProfile)sbProfile.geo_coins=totalCoins;
  const masteryCC=Object.keys(mastery).filter(cc=>getMasteryRank(mastery[cc].v,mastery[cc].p));
  for(const cc of masteryCC){
    sb.rpc("upsert_stamp",{p_user_id:uid,p_country_code:cc,p_perfect:mastery[cc].p>0}).catch(()=>{});
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
  S.authLoading=true;S.authError="";render();
  try{
    const{data,error}=await sb.auth.signUp({email,password:pw,options:{data:{username:uname}}});
    if(error){S.authError=error.message;S.authLoading=false;render();return;}
    const uid=data.user?.id;
    if(!uid){S.authError="Registrierung fehlgeschlagen.";S.authLoading=false;render();return;}
    // Save username locally immediately
    try{localStorage.setItem("gq_username",uname);}catch(e){}
    // Upsert profile (fire & forget errors)
    await sb.from("profiles").upsert({id:uid,username:uname,geo_coins:100}).catch(()=>{});
    sbUser=data.user;
    sbProfile={...(sbProfile||{}),username:uname,geo_coins:100,id:uid};
    // Migrate guest data in background (don't await to avoid hanging)
    migrateGuestToAccount(uid).catch(()=>{});
    S.authLoading=false;S.authEmail="";S.authPassword="";S.authUsername="";S.authError="";
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
    S.authError=err.message||"Unbekannter Fehler.";
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
  S.authLoading=false;S.authEmail="";S.authPassword="";S.authError="";
  S.tab="home";
  render();
}

/* Phase 27: Logout */
async function doLogout(){
  if(!sb)return;
  await sb.auth.signOut();
  sbUser=null;sbProfile=null;sbStamps=new Set();
  try{localStorage.removeItem("gq_username");}catch(e){}
  const{data}=await sb.auth.signInAnonymously();
  if(data)sbUser=data.user;
  render();
}
async function saveSession(mode,score,bs,correct,durationMs){
  /* Phase 33 Teil 2: notify opponent at game end */
  if(window.mpGameCh&&S.mpOpponent){
    window.mpGameCh.send({type:"broadcast",event:"game_over",
      payload:{score,name:sbProfile?.username||"Ich",correct}}).catch(()=>{});
    window.mpGameCh=null;
  }
  if(\!sb||\!sbUser)return;
  if(!sb||!sbUser?.id)return;
  await sb.from("game_sessions").insert({user_id:sbUser.id,mode,score,best_streak:bs,rounds:ROUNDS,accuracy:Math.round(correct/ROUNDS*100),username:sbProfile?.username||null});
  /* Use RPC to prevent client-side score tampering */
  await sb.rpc("add_score",{p_user_id:sbUser.id,p_score:score,p_coins:Math.floor(score/100),p_rounds:ROUNDS,p_duration_ms:durationMs||0}).catch(()=>{});
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
  sb.rpc("upsert_stamp",{p_user_id:sbUser.id,p_country_code:cc,p_perfect:perfect}).catch(()=>{});
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
  authMode:"login",authEmail:"",authPassword:"",authUsername:"",authError:"",authLoading:false,
  settingsModal:false,
  convModal:false,
  collectedPlates:loadCollectedPlates(),
  ligaData:[],ligaLoading:false,
  titleShop:false,
  spotterInput:"",spotterMsg:"",spotterOk:null,albumView:"list",albumCountry:_smartDefaultCountry(),spotterCountry:_smartDefaultCountry(),
  collFilter:"all",collRarity:"all",collSearch:"",
};
let tIv=null,fTo=null,toastTo=null;

/* ── Phase 42: Anti-Cheat — Proxy wrapper for S in console ── */
(function(){
  const GUARDED=new Set(["sc","correct","st","bs","collectedPlates","sbProfile"]);
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
  const pool=CITIES.filter(c=>c.pop>=pf&&c.id\!==S.lid);
  if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sub===cor.sub||x.cont===cor.cont,x=>x.c===cor.c,x=>x.c);
  return{type:"city",prompt:MODES[0].prompt,subj:cor.n,ans:cor.c,opts:sh([cor.c,...dis]),meta:cor.cont+" \u00b7 "+(cor.pop/1e6).toFixed(1)+" Mio.",lid:cor.id,cc:cor.cc};
}
function genFlagQ(){
  const pool=COUNTRIES.filter(x=>x.cc\!==S.lid);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sr===cor.sr||x.ct===cor.ct,x=>x.c===cor.c,x=>x.c);
  return{type:"flag",prompt:MODES[1].prompt,subj:cor.cc,ans:cor.c,opts:sh([cor.c,...dis]),meta:cor.ct,lid:cor.cc,cc:cor.cc};
}
function genCapitalQ(){
  const pool=CAPITALS.filter(x=>x.capital\!==S.lid);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.country===cor.country,x=>x.country);
  return{type:"capital",prompt:MODES[2].prompt,subj:cor.capital,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.capital,cc:cor.cc};
}
function genRiverQ(){
  const pool=RIVERS.filter(x=>x.name\!==S.lid);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(COUNTRIES,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"river",prompt:MODES[3].prompt,subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genLandmarkQ(){
  const pool=LANDMARKS.filter(x=>x.name\!==S.lid);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(COUNTRIES,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"landmark",prompt:MODES[4].prompt,subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genParkQ(){
  const pool=NATIONAL_PARKS.filter(x=>x.name\!==S.lid);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(COUNTRIES,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"park",prompt:MODES[5].prompt,subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genUnescoQ(){
  const pool=UNESCO_SITES.filter(x=>x.name\!==S.lid);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(COUNTRIES,x=>x.sr===cor.subregion||x.ct===cor.continent,x=>x.c===cor.country,x=>x.c);
  return{type:"unesco",prompt:MODES[6].prompt,subj:cor.name,ans:cor.country,opts:sh([cor.country,...dis]),meta:cor.continent,lid:cor.name,cc:cor.cc};
}
function genCitymarkQ(){
  const pool=CITY_LANDMARKS.filter(x=>x.name\!==S.lid);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(CITY_LANDMARKS,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.city===cor.city,x=>x.city);
  return{type:"citymark",prompt:MODES[7].prompt,subj:cor.name,ans:cor.city,opts:sh([cor.city,...dis]),meta:cor.country,lid:cor.name,cc:cor.cc};
}
function genSubwayQ(){
  const pool=SUBWAYS.filter(x=>x.city\!==S.lid);if(pool.length<3)return null;
  const t=Math.floor(rng()*2);
  const cor=pool[~~(rng()*pool.length)];
  const dis3=distractors(pool,x=>x.country===cor.country||x.cc===cor.cc,x=>x.city===cor.city,x=>t===0?x.km:x.lines,2);
  const ansVal=t===0?cor.km:cor.lines;
  const prompt=t===0?"Wie lang ist das U-Bahn-Netz in \u2026 (km)?":"Wie viele U-Bahn-Linien hat \u2026?";
  const suffix=t===0?" km":" Linien";
  return{type:"subway",prompt,subj:cor.city,ans:String(ansVal),opts:sh([String(ansVal),...dis3.map(String)]),meta:cor.country+" \u00b7 "+suffix.trim(),lid:cor.city,cc:cor.cc};
}
function genFlagselQ(){
  const pool=COUNTRIES.filter(x=>x.cc\!==S.lid);if(pool.length<4)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.sr===cor.sr||x.ct===cor.ct,x=>x.cc===cor.cc,x=>x.cc,3);
  return{type:"flagsel",prompt:MODES[9].prompt,subj:cor.c,ans:cor.cc,opts:sh([cor.cc,...dis]),meta:cor.ct,lid:cor.cc,cc:cor.cc};
}
function genRcapitalQ(){
  const pool=CAPITALS.filter(x=>x.country\!==S.lid);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const dis=distractors(pool,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.capital===cor.capital,x=>x.capital);
  return{type:"rcapital",prompt:MODES[10].prompt,subj:cor.country,ans:cor.capital,opts:sh([cor.capital,...dis]),meta:cor.continent,lid:cor.country,cc:cor.cc};
}
function genRcityQ(){
  const pool=COUNTRIES.filter(x=>x.c\!==S.lid);if(pool.length<3)return null;
  const cor=pool[~~(rng()*pool.length)];
  const cc2=CITIES.filter(c=>c.c===cor.c);if(\!cc2.length)return genRcityQ();
  const corCity=cc2[~~(rng()*cc2.length)];
  const dis=distractors(CITIES,x=>x.sub===corCity.sub||x.cont===corCity.cont,x=>x.c===cor.c,x=>x.n);
  return{type:"rcity",prompt:MODES[11].prompt,subj:cor.c,ans:corCity.n,opts:sh([corCity.n,...dis]),meta:cor.ct,lid:cor.c,cc:cor.cc};
}
function genRriverQ(){
  const ctries=[...new Set(RIVERS.map(r=>r.country))].filter(c=>c\!==S.lid);if(\!ctries.length)return null;
  const corC=ctries[~~(rng()*ctries.length)];
  const cRivers=RIVERS.filter(r=>r.country===corC);
  const cor=cRivers[~~(rng()*cRivers.length)];
  const dis=distractors(RIVERS,x=>x.subregion===cor.subregion||x.continent===cor.continent,x=>x.country===corC,x=>x.name);
  return{type:"rriver",prompt:MODES[12].prompt,subj:corC,ans:cor.name,opts:sh([cor.name,...dis]),meta:cor.continent,lid:corC,cc:cor.cc};
}
function genFoodQ(){
  if(\!FOOD_DATA.length)return null;
  const idx=~~(rng()*FOOD_DATA.length);const item=FOOD_DATA[idx];
  const corC=item.country;
  const dis=FOOD_DATA.filter(f=>f.country\!==corC).map(f=>f.country);
  const uniq=[...new Set(dis)];const picked=sh(uniq).slice(0,3);
  return{type:"food",prompt:MODES.find(m=>m.id==="food").prompt,subj:item.dish,emoji:item.emoji,ans:corC,opts:sh([corC,...picked]),lid:item.cc,cc:item.cc};
}
function genBrandQ(){
  if(\!BRANDS_DATA.length)return null;
  const idx=~~(rng()*BRANDS_DATA.length);const item=BRANDS_DATA[idx];
  const corC=item.country;
  const sameSub=BRANDS_DATA.filter(b=>b.sub===item.sub&&b.country\!==corC).map(b=>b.country);
  const fallback=BRANDS_DATA.filter(b=>b.country\!==corC).map(b=>b.country);
  const pool=[...new Set(sameSub.length>=3?sameSub:fallback)];
  const picked=sh(pool).slice(0,3);
  return{type:"brand",prompt:MODES.find(m=>m.id==="brand").prompt,subj:item.brand,industry:item.industry,ans:corC,opts:sh([corC,...picked]),lid:item.cc,cc:item.cc};
}
function genCurrencyQ(){
  if(\!CURRENCIES_DATA.length)return null;
  const idx=~~(rng()*CURRENCIES_DATA.length);const item=CURRENCIES_DATA[idx];
  const corC=item.country;
  const sameSub=CURRENCIES_DATA.filter(c=>c.sub===item.sub&&c.country\!==corC).map(c=>c.country);
  const fallback=CURRENCIES_DATA.filter(c=>c.country\!==corC).map(c=>c.country);
  const pool=[...new Set(sameSub.length>=3?sameSub:fallback)];
  const picked=sh(pool).slice(0,3);
  return{type:"currency",prompt:MODES.find(m=>m.id==="currency").prompt,subj:item.currency,symbol:item.symbol,ans:corC,opts:sh([corC,...picked]),lid:item.cc,cc:item.cc};
}
function genOutlineQ(){
  const pool=COUNTRIES.filter(c=>c.cc&&c.cc.length===2);
  if(pool.length<4)return null;
  const sh2=arr=>{const a=[...arr];for(let i=a.length-1;i>0;i--){const j=~~(rng()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
  const idx=~~(rng()*pool.length);const item=pool[idx];
  const corC=item.c;const corCC=item.cc;
  const dis=pool.filter(c=>c.cc\!==corCC).map(c=>c.c);
  const picked=sh2(dis).slice(0,3);
  return{type:"outline",prompt:MODES.find(m=>m.id==="outline").prompt,subj:corCC,ans:corC,opts:sh2([corC,...picked]),lid:corCC,cc:corCC};
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
    prompt:hardcore?"Region erkennen \u2014 kein Tipp\!":"Woher kommt dieses Kennzeichen?",
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
  return{type:"map_guess",prompt:"Finde das Land auf der Karte",subj:co.name,
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
    if(S.isDailyRun&&!isDailyDone()){markDailyDone(S.sc);if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+100;if(sb&&sbUser)sb.from("profiles").update({geo_coins:(sbProfile?.geo_coins||0)}).eq("id",sbUser.id).catch(()=>{});}
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
      if(sb&&sbUser)sb.from("profiles").update({survival_best:Math.max(survived,sbProfile?.survival_best||0)}).eq("id",sbUser.id).catch(()=>{});
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
      payload:{score:S.sc,rd:S.rd,correct:S.correct}}).catch(()=>{});
  }
  fTo=setTimeout(()=>{
    const nr=S.rd+1;
    if(S.diff\!=="survival"&&nr>=ROUNDS){
      S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();
      if(S.isDailyRun&&\!isDailyDone()){
        markDailyDone(S.sc);
        if(sbProfile)sbProfile.geo_coins=(sbProfile.geo_coins||0)+100;
        if(sb&&sbUser)sb.from("profiles").update({geo_coins:(sbProfile?.geo_coins||0)}).eq("id",sbUser.id).catch(()=>{});
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
      <button class="share-btn" onclick="shareResult()">\u{1F4CB} Ergebnis teilen</button>
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
    return;
  }

  /* PLAYING / FEEDBACK */
  const{sc,st,bs,rd,tm,q,sel,ok,pts,mode,diff}=S;
  const col=tc(),p=pct(),t=tier(st);
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
        <button class="hl-btn hl-higher${sel\!==null?(q.ans==="higher"?" ok":(sel==="higher"?" ng":" dm")):""}" ${hlDis} onclick="answer('higher')">\u2b06\ufe0f Mehr / L\u00e4nger / Gr\u00f6\u00dfer</button>
        <button class="hl-btn hl-lower${sel\!==null?(q.ans==="lower"?" ok":(sel==="lower"?" ng":" dm")):""}" ${hlDis} onclick="answer('lower')">\u2b07\ufe0f Weniger / K\u00fcrzer / Kleiner</button>
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
      return`${topBar}
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
          <button class="${moreCls}" ${pcDis} onclick="answer('more')">⬆️ Mehr Einwohner</button>
          <button class="${lessCls}" ${pcDis} onclick="answer('less')">⬇️ Weniger Einwohner</button>
        </div>
        ${sel\!==null?`<div class="meta-line">${q.meta||""}</div>`:""}
        ${sel\!==null?`<button class="btn-p" onclick="nextRound()">Weiter →</button>`:""}`;
    }
    if(q.type==="hl_pop"||q.type==="hl_river"||q.type==="hl_area"){
      answerHtml="";
    }else{
      const btns=q.opts.map((o,i)=>{let cls="btn-a";const os=o.replace(/'/g,"\\'");if(sel\!==null){if(o===q.ans)cls+=" ok";else if(o===sel)cls+=" ng";else cls+=" dm";}const mk=sel?(o===q.ans?`<span>\u2713</span>`:o===sel?`<span>\u2717</span>`:""):"";return`<button class="${cls}" ${sel?"disabled":""} onclick="answerByIdx(${i})">${esc(o)}${mk}</button>`;}).join("");
      answerHtml=`<div class="answers">${btns}</div>`;
    }
  }
  let fb="";
  if(S.ph==="feedback"){const cls=ok?"fb ok":"fb ng";let al=q.ans;if(q.type==="flagsel"){const co=COUNTRIES.find(c=>c.cc===q.ans);al=co?co.c:q.ans;}const msg=ok?`\u2713 Richtig\! +${pts}`:sel==="__t"?`\u23f1 Zeit\! \u2192 ${al}`:`\u2717 Falsch \u2192 ${al}`;fb=`<div class="${cls}">${msg}</div>${plateReveal}`;}
  /* Power-up bar (Phase 26) */
  const pu=loadPU();
  const puBar=`<div class="pu-bar">
    <button class="pu-btn${S.half_removed?" pu-used":""}" onclick="useFiveO()" title="50/50-Joker (${pu.five0||0} \u00fcbrig)">\u2702 50/50 <span style="font-size:.62rem">(${pu.five0||0})</span></button>
    <button class="pu-btn${S.freezeActive?" freeze-on":""}" onclick="useFreeze()" title="Zeit-Stopp (${pu.freeze||0} \u00fcbrig)">\u{1F9CA} Freeze <span style="font-size:.62rem">(${pu.freeze||0})</span></button>
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
    ${st>=3?`<div style="text-align:center;font-size:.76rem;font-weight:700;color:#fb923c;margin-bottom:6px">${t.l}</div>`:""}
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
    if(container)container.innerHTML='<p style="color:var(--text3);text-align:center;padding:2rem">Karte nicht verfügbar</p>';
    return;
  }
  if(\!window.WORLD_TOPO){
    container.innerHTML='<p style="color:var(--text3);text-align:center;padding:2rem">Kartendaten werden geladen…</p>';
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
      S.spotterMsg="❓ '"+code+"' nicht in "+(country||"Alle")+" — aber in: "+others;
    }else{
      S.spotterMsg="❌ Unbekanntes Kennzeichen: "+code;
    }
    S.spotterOk=false;render();return;
  }
  const mainPlate=candidates[0];
  const mainCountry=mainPlate.country;
  const key=collKey(code,mainCountry);
  if(S.collectedPlates.includes(key)){
    S.spotterMsg="\u{1F4CB} "+code+" ("+mainCountry+") bereits in der Sammlung\!";S.spotterOk=null;
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
      ${region?`<div class="rp-region">${esc(region)}${extra>0?" +"+extra+" weitere":""}</div>`:""}
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
      <span class="album-spotter-title">\u{1F697} Roadtrip-Spotter</span>
      <select class="spotter-country-sel" onchange="S.spotterCountry=this.value;S.albumCountry=this.value;localStorage.setItem('geoquest_pref_country',this.value);S.spotterMsg='';render()">
        <option value="all" ${sCountry==="all"?"selected":""}>\u{1F30D} Alle Länder</option>
        ${countries.map(c=>`<option value="${esc(c)}" ${sCountry===c?"selected":""}>${esc(c)}</option>`).join("")}
      </select>
    </div>
    <div class="album-spotter-sub">Kennzeichen gesehen? Sofort eintragen\!</div>
    <div style="display:flex;gap:8px">
      <input type="text" maxlength="5" placeholder="z.B. MÜ" value="${esc(spotVal)}"
        oninput="S.spotterInput=this.value.toUpperCase();this.value=this.value.toUpperCase();S.spotterMsg='';render()"
        class="spotter-input">
      <button class="btn-p" style="width:auto;padding:.5rem 1rem;margin-bottom:0" onclick="spotterCollect()">\u{1F50D} Sammeln</button>
    </div>
    ${spotMsg?`<div style="font-size:.82rem;font-weight:700;text-align:center;color:${spotCol};padding:.35rem 0;margin-top:4px">${spotMsg}</div>`:""}
  </div>`;

  /* ── Progress ── */
  const progressBar=`<div class="album-progress-wrap">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:5px">
      <span style="font-weight:900;font-size:1rem">\u{1F4D4} Kennzeichen-Album</span>
      <span style="font-size:.78rem;color:var(--text3)">${coll.length}&thinsp;/&thinsp;${total}</span>
    </div>
    <div class="coll-progress-wrap"><div class="coll-progress-bar" style="width:${pct}%"></div></div>
    <div style="text-align:right;font-size:.65rem;color:var(--text3);margin-top:2px">${pct}% vollständig</div>
  </div>`;

  /* ── Achievements ── */
  const achBar=achs.length?`<div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:.7rem">${achs.map(c=>`<span class="coll-ach">\u{1F3C6} ${esc(c)}-Experte</span>`).join("")}</div>`:"";

  /* ── Controls ── */
  const controls=`<div style="display:flex;gap:6px;margin-bottom:.7rem;align-items:center">
    <button class="view-toggle-btn${view==="list"?" active":""}" onclick="S.albumView='list';render()">\u{1F4DD} Liste</button>
    <button class="view-toggle-btn${view==="map"?" active":""}" onclick="S.albumView='map';render()">\u{1F5FA} Karte</button>
    <select style="margin-left:auto;background:var(--bg3);color:var(--text);border:1.5px solid var(--border);border-radius:8px;padding:.3rem .5rem;font-size:.76rem" onchange="S.albumCountry=this.value;S.spotterCountry=this.value;localStorage.setItem('geoquest_pref_country',this.value);render()">
      <option value="all" ${acF==="all"?"selected":""}>Alle Länder</option>
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
          <span style="font-size:.72rem;color:var(--text3)">${collHere.length}&thinsp;/&thinsp;${uPlates.length} Kürzel</span>
        </div>
        <div style="height:4px;background:var(--bg4);border-radius:2px;overflow:hidden;margin-bottom:.65rem">
          <div style="height:100%;width:${cPct}%;background:#10b981;border-radius:2px"></div>
        </div>
        ${collHere.length
          ?`<div class="real-plate-grid">${collHere.map(u=>renderRealPlate(u.code,u.mainRegion,u.count-1)).join("")}</div>`
          :`<div style="color:var(--text3);font-size:.75rem;text-align:center;padding:.5rem 0">Noch nichts aus ${esc(country)} gesammelt — spiele Kennzeichen oder nutze den Spotter!</div>`}
      </div>`;
    }).join("");
    if(\!listContent)listContent=`<div style="text-align:center;padding:2rem;color:var(--text3)">Noch nichts gesammelt\!<br><small>Spiele EU-Kennzeichen oder benutze den Spotter oben.</small></div>`;
  }

  const mapContent=view==="map"?`<div id="album-map-svg" class="album-map-container"></div>`:"";

  if(view==="map")requestAnimationFrame(()=>drawAlbumMap());

  const backBtn=`<button onclick="S.tab='home';render()" style="display:flex;align-items:center;gap:6px;background:none;border:none;color:var(--text3);font-size:.82rem;font-weight:700;cursor:pointer;padding:.3rem .1rem;margin-bottom:.6rem;letter-spacing:.3px;transition:color .15s" onmouseenter="this.style.color='var(--text)'" onmouseleave="this.style.color='var(--text3)'"><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>Zurück zum Hauptmenü</button>`;
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
          .text("+"+(d.codes.length-9)+" weitere");
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
  return`${renderDailyHero()}
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
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">
      <div style="font-weight:700">\u{1F4CD} Heimatregion</div>
      <span style="font-size:.78rem;color:#3b82f6;font-weight:700;cursor:pointer" onclick="localStorage.removeItem('geoquest_last_detected_country');showToast('Erkennung wird beim n\u00e4chsten Start wiederholt')">\u21ba Reset</span>
    </div>
    <div style="font-size:.76rem;color:var(--text2);margin-bottom:.75rem">${localStorage.getItem('geoquest_pref_country')||'Nicht gesetzt (auto)'}</div>
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
    const upd={geo_coins:(sbProfile?.geo_coins||0)+p.coins};
    if(p.premium){const u=new Date();u.setMonth(u.getMonth()+(p.months||1));upd.is_premium=true;upd.premium_until=u.toISOString();}
    await sb.from("profiles").update(upd).eq("id",sbUser.id);
    if(sbProfile)Object.assign(sbProfile,upd);
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
  el.innerHTML=`<span style="font-size:.8rem;color:var(--text2)">\u{1F4CD} Du bist in <strong style="color:var(--text)">${c}</strong></span>`
    +`<button class="gq-loc-btn-yes" onclick="locationBannerYes('${c.replace(/'/g,"\\'")}');document.getElementById('gq-loc-toast')?.remove()">Anpassen</button>`;
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

HTML = f"""<!DOCTYPE html>
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
{CSS}
</style>
</head>
<body>
<div id="app"></div>
<script>
{JS}
</script>
</body>
</html>"""

out = '/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/GeoQuest.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)
size = len(HTML)//1024
print(f'GeoQuest.html written: {size} KB')

# Post-process: fix \! -> ! (bash heredoc artifact)
raw = open(out,'rb').read()
fixed_raw = raw.replace(b'\x5c\x21', b'\x21')
open(out,'wb').write(fixed_raw)
cnt=fixed_raw.count(b'\x5c\x21')
print(f'Post-process: fixed {fixed_raw.count(b"!") } backslash-bang occurrences')
  