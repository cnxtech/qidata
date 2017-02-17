
# qidata
from qidata._metadata_objects import _QidataEnumMixin

_country_list=[
	"AFRICA__UNSPECIFIED",
	"AFRICA__ALGERIA",
	"AFRICA__ANGOLA",
	"AFRICA__BENIN",
	"AFRICA__BOTSWANA",
	"AFRICA__BURKINA",
	"AFRICA__BURUNDI",
	"AFRICA__CAMEROON",
	"AFRICA__CAPE_VERDE",
	"AFRICA__CENTRAL_AFRICAN_REPUBLIC",
	"AFRICA__CHAD",
	"AFRICA__COMOROS",
	"AFRICA__CONGO",
	"AFRICA__DEMOCRATIC_REPUBLIC_OF_CONGO",
	"AFRICA__DJIBOUTI",
	"AFRICA__EGYPT",
	"AFRICA__EQUATORIAL_GUINEA",
	"AFRICA__ERITREA",
	"AFRICA__ETHIOPIA",
	"AFRICA__GABON",
	"AFRICA__GAMBIA",
	"AFRICA__GHANA",
	"AFRICA__GUINEA",
	"AFRICA__GUINEA_BISSAU",
	"AFRICA__IVORY_COAST",
	"AFRICA__KENYA",
	"AFRICA__LESOTHO",
	"AFRICA__LIBERIA",
	"AFRICA__LIBYA",
	"AFRICA__MADAGASCAR",
	"AFRICA__MALAWI",
	"AFRICA__MALI",
	"AFRICA__MAURITANIA",
	"AFRICA__MAURITIUS",
	"AFRICA__MOROCCO",
	"AFRICA__MOZAMBIQUE",
	"AFRICA__NAMIBIA",
	"AFRICA__NIGER",
	"AFRICA__NIGERIA",
	"AFRICA__RWANDA",
	"AFRICA__SAO_TOME_AND_PRINCIPE",
	"AFRICA__SENEGAL",
	"AFRICA__SEYCHELLES",
	"AFRICA__SIERRA_LEONE",
	"AFRICA__SOMALIA",
	"AFRICA__SOUTH_AFRICA",
	"AFRICA__SOUTH_SUDAN",
	"AFRICA__SUDAN",
	"AFRICA__SWAZILAND",
	"AFRICA__TANZANIA",
	"AFRICA__TOGO",
	"AFRICA__TUNISIA",
	"AFRICA__UGANDA",
	"AFRICA__ZAMBIA",
	"AFRICA__ZIMBABWE",

	"ASIA__UNSPECIFIED",
	"ASIA__AFGHANISTAN",
	"ASIA__BAHRAIN",
	"ASIA__BANGLADESH",
	"ASIA__BHUTAN",
	"ASIA__BRUNEI",
	"ASIA__BURMA",
	"ASIA__CAMBODIA",
	"ASIA__CHINA",
	"ASIA__EAST_TIMOR",
	"ASIA__INDIA",
	"ASIA__INDONESIA",
	"ASIA__IRAN",
	"ASIA__IRAQ",
	"ASIA__ISRAEL",
	"ASIA__JAPAN",
	"ASIA__JORDAN",
	"ASIA__KAZAKHSTAN",
	"ASIA__NORTH_KOREA",
	"ASIA__SOUTH_KOREA",
	"ASIA__KUWAIT",
	"ASIA__KYRGYZSTAN",
	"ASIA__LAOS",
	"ASIA__LEBANON",
	"ASIA__MALAYSIA",
	"ASIA__MALDIVES",
	"ASIA__MONGOLIA",
	"ASIA__NEPAL",
	"ASIA__OMAN",
	"ASIA__PAKISTAN",
	"ASIA__PHILIPPINES",
	"ASIA__QATAR",
	"ASIA__RUSSIA",
	"ASIA__SAUDI_ARABIA",
	"ASIA__SINGAPORE",
	"ASIA__SRI_LANKA",
	"ASIA__SYRIA",
	"ASIA__TAJIKISTAN",
	"ASIA__THAILAND",
	"ASIA__TURKEY",
	"ASIA__TURKMENISTAN",
	"ASIA__UNITED_ARAB_EMIRATES",
	"ASIA__UZBEKISTAN",
	"ASIA__VIETNAM",
	"ASIA__YEMEN",

	"EUROPE__UNSPECIFIED",
	"EUROPE__ALBANIA",
	"EUROPE__ANDORRA",
	"EUROPE__ARMENIA",
	"EUROPE__AUSTRIA",
	"EUROPE__AZERBAIJAN",
	"EUROPE__BELARUS",
	"EUROPE__BELGIUM",
	"EUROPE__BOSNIA_AND_HERZEGOVINA",
	"EUROPE__BULGARIA",
	"EUROPE__CROATIA",
	"EUROPE__CYPRUS",
	"EUROPE__CZECH_REPUBLIC",
	"EUROPE__DENMARK",
	"EUROPE__ESTONIA",
	"EUROPE__FINLAND",
	"EUROPE__FRANCE",
	"EUROPE__GEORGIA",
	"EUROPE__GERMANY",
	"EUROPE__GREECE",
	"EUROPE__HUNGARY",
	"EUROPE__ICELAND",
	"EUROPE__IRELAND",
	"EUROPE__ITALY",
	"EUROPE__LATVIA",
	"EUROPE__LIECHTENSTEIN",
	"EUROPE__LITHUANIA",
	"EUROPE__LUXEMBOURG",
	"EUROPE__MACEDONIA",
	"EUROPE__MALTA",
	"EUROPE__MOLDOVA",
	"EUROPE__MONACO",
	"EUROPE__MONTENEGRO",
	"EUROPE__NETHERLANDS",
	"EUROPE__NORWAY",
	"EUROPE__POLAND",
	"EUROPE__PORTUGAL",
	"EUROPE__ROMANIA",
	"EUROPE__SAN_MARINO",
	"EUROPE__SERBIA",
	"EUROPE__SLOVAKIA",
	"EUROPE__SLOVENIA",
	"EUROPE__SPAIN",
	"EUROPE__SWEDEN",
	"EUROPE__SWITZERLAND",
	"EUROPE__UKRAINE",
	"EUROPE__UNITED_KINGDOM",
	"EUROPE__VATICAN_CITY",

	"NORTH_AMERICA__UNSPECIFIED",
	"NORTH_AMERICA__ANTIGUA_AND_BARBUDA",
	"NORTH_AMERICA__BAHAMAS",
	"NORTH_AMERICA__BARBADOS",
	"NORTH_AMERICA__BELIZE",
	"NORTH_AMERICA__CANADA",
	"NORTH_AMERICA__COSTA_RICA",
	"NORTH_AMERICA__CUBA",
	"NORTH_AMERICA__DOMINICA",
	"NORTH_AMERICA__DOMINICAN_REPUBLIC",
	"NORTH_AMERICA__EL_SALVADOR",
	"NORTH_AMERICA__GRENADA",
	"NORTH_AMERICA__GUATEMALA",
	"NORTH_AMERICA__HAITI",
	"NORTH_AMERICA__HONDURAS",
	"NORTH_AMERICA__JAMAICA",
	"NORTH_AMERICA__MEXICO",
	"NORTH_AMERICA__NICARAGUA",
	"NORTH_AMERICA__PANAMA",
	"NORTH_AMERICA__SAINT_KITTS_AND_NEVIS",
	"NORTH_AMERICA__SAINT_LUCIA",
	"NORTH_AMERICA__SAINT_VINCENT_AND_THE_GRENADINES",
	"NORTH_AMERICA__TRINIDAD_AND_TOBAGO",
	"NORTH_AMERICA__UNITED_STATES",

	"OCEANIA__UNSPECIFIED",
	"OCEANIA__AUSTRALIA",
	"OCEANIA__FIJI",
	"OCEANIA__KIRIBATI",
	"OCEANIA__MARSHALL_ISLANDS",
	"OCEANIA__MICRONESIA",
	"OCEANIA__NAURU",
	"OCEANIA__NEW_ZEALAND",
	"OCEANIA__PALAU",
	"OCEANIA__PAPUA_NEW_GUINEA",
	"OCEANIA__SAMOA",
	"OCEANIA__SOLOMON_ISLANDS",
	"OCEANIA__TONGA",
	"OCEANIA__TUVALU",
	"OCEANIA__VANUATU",

	"SOUTH_AMERICA__UNSPECIFIED",
	"SOUTH_AMERICA__ARGENTINA",
	"SOUTH_AMERICA__BOLIVIA",
	"SOUTH_AMERICA__BRAZIL",
	"SOUTH_AMERICA__CHILE",
	"SOUTH_AMERICA__COLOMBIA",
	"SOUTH_AMERICA__ECUADOR",
	"SOUTH_AMERICA__GUYANA",
	"SOUTH_AMERICA__PARAGUAY",
	"SOUTH_AMERICA__PERU",
	"SOUTH_AMERICA__SURINAME",
	"SOUTH_AMERICA__URUGUAY",
	"SOUTH_AMERICA__VENEZUELA",

	"UNSPECIFIED"
]


Country = _QidataEnumMixin("Country",_country_list)