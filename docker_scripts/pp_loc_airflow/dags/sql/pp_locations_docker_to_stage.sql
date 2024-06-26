DROP TABLE stg_petrol_pump_locations.pump_locations;

create table stg_petrol_pump_locations.pump_locations as 
select
	*
from
	public.dblink
('server_docker_prod_pp',
	'SELECT 
	element_type,
	osmid,
	amenity,
	brand,
	"brand:wikidata",
	"brand:wikipedia",
	"name",
	"addr:city",
	"addr:country",
	"addr:housenumber",
	"addr:postcode",
	"addr:street",
	branch,
	opening_hours,
	"addr:suburb",
	"operator",
	"ref:linz:address_id",
	note,
	compressed_air,
	"fuel:diesel",
	"fuel:octane_91",
	"fuel:octane_95",
	phone,
	website,
	"source",
	wheelchair,
	"fuel:electricity",
	"fuel:lpg",
	"fuel:octane_98",
	self_service,
	official_name,
	"fuel:HGV_diesel",
	"payment:cash",
	"payment:girocard",
	"payment:mastercard",
	"payment:visa",
	shop,
	"name:mi",
	landuse,
	layer,
	"payment:credit_cards",
	building,
	height,
	diesel,
	"fuel:GTL_diesel",
	"fuel:cng",
	"fuel:e10",
	"fuel:e85",
	"source:geometry",
	"building:levels",
	"roof:shape",
	toilets,
	atm,
	cafe,
	car_wash,
	check_date,
	"payment:american_express",
	"payment:visa_debit",
	service,
	"contact:phone",
	"fuel:adblue",
	"fuel:octane_100",
	"payment:debit_cards",
	smoking,
	"operator:wikidata",
	start_date,
	ways,
	"type",
	CURRENT_TIMESTAMP AS INSERT_TIME,
	geometry,
	nodes
FROM public.pump_locations pl') 
as data(
element_type text,
	osmid int8,
	amenity text,
	brand text,
	"brand:wikidata" text,
	"brand:wikipedia" text,
	"name" text,
	"addr:city" text,
	"addr:country" text,
	"addr:housenumber" text,
	"addr:postcode" text,
	"addr:street" text,
	branch text,
	opening_hours text,
	"addr:suburb" text,
	"operator" text,
	"ref:linz:address_id" text,
	note text,
	compressed_air text,
	"fuel:diesel" text,
	"fuel:octane_91" text,
	"fuel:octane_95" text,
	phone text,
	website text,
	"source" text,
	wheelchair text,
	"fuel:electricity" text,
	"fuel:lpg" text,
	"fuel:octane_98" text,
	self_service text,
	official_name text,
	"fuel:HGV_diesel" text,
	"payment:cash" text,
	"payment:girocard" text,
	"payment:mastercard" text,
	"payment:visa" text,
	shop text,
	"name:mi" text,
	landuse text,
	layer text,
	"payment:credit_cards" text,
	building text,
	height text,
	diesel text,
	"fuel:GTL_diesel" text,
	"fuel:cng" text,
	"fuel:e10" text,
	"fuel:e85" text,
	"source:geometry" text,
	"building:levels" text,
	"roof:shape" text,
	toilets text,
	atm text,
	cafe text,
	car_wash text,
	check_date text,
	"payment:american_express" text,
	"payment:visa_debit" text,
	service text,
	"contact:phone" text,
	"fuel:adblue" text,
	"fuel:octane_100" text,
	"payment:debit_cards" text,
	smoking text,
	"operator:wikidata" text,
	start_date text,
	ways text,
	"type" text,
	INSERT_TIME TIMESTAMP,
	geometry public.geometry,
	nodes text
);
