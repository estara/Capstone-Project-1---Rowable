CREATE TABLE public.boathouse (
    id integer NOT NULL,
    name text NOT NULL,
    address text NOT NULL,
    city text NOT NULL,
    state text NOT NULL,
    zip integer NOT NULL,
    lat numeric NOT NULL,
    lon numeric NOT NULL,
    notes text,
    nmax integer,
    smax integer,
    emax integer,
    wmax integer,
    fun_limit integer,
    activated boolean DEFAULT false NOT NULL,
    timezone text
);


--
-- Name: Boathouse_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Boathouse_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Boathouse_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Boathouse_ID_seq" OWNED BY public.boathouse.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username text NOT NULL,
    hashed_password text NOT NULL,
    email text NOT NULL,
    c_or_f text DEFAULT 'F'::character varying NOT NULL,
    registered_on date,
    confirmed boolean DEFAULT false NOT NULL,
    confirmed_on date,
    boathouses integer[]
);


--
-- Name: User_ID_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."User_ID_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: User_ID_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."User_ID_seq" OWNED BY public."user".id;


--
-- Name: boathouse id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.boathouse ALTER COLUMN id SET DEFAULT nextval('public."Boathouse_ID_seq"'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public."User_ID_seq"'::regclass);


--
-- Data for Name: boathouse; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.boathouse (id, name, address, city, state, zip, lat, lon, notes, nmax, smax, emax, wmax, fun_limit, activated, timezone) FROM stdin;
1	Alexandria Community Rowing	 One Madison Street	Alexandria	VA	22314	38.813040	-77.045340	\N	\N	\N	\N	\N	\N	f	\N
2	Amoskeag Rowing Club	101 MERRIMACK STREET	HOOKSETT	NH	3106	43.105220	-71.464180	\N	\N	\N	\N	\N	\N	f	\N
3	Ann Arbor Rowing Club	1325 Lake Shore Dr.	Ann Arbor	MI	48104	42.304660	-83.746460	\N	\N	\N	\N	\N	\N	f	\N
4	Annapolis Rowing Club	10 Sunset Dr.	Edgewater	MD	21037	38.957660	-76.552310	\N	\N	\N	\N	\N	\N	f	\N
5	Aqueduct Rowing Club	2855 Aqueduct Rd	Schenectady	NY	12309	42.779020	-73.843180	\N	\N	\N	\N	\N	\N	f	\N
6	Arkansas Boathouse Club	River Mountain Rd	Little Rock	AR	72223	34.798333	-92.385378	\N	\N	\N	\N	\N	\N	f	\N
7	Asheville Rowing Club	70 Fisherman's Trail	Arden	NC	28704	35.476882	-82.528536	\N	\N	\N	\N	\N	\N	f	\N
8	Augusta Rowing Club	101 Riverfront Dr	Augusta	GA	30901	33.46937	-81.943806	\N	\N	\N	\N	\N	\N	f	\N
9	Austin Rowing Club	74 Trinity St	Austin	TX	78701	30.2605631	-97.7439515	\N	\N	\N	\N	\N	\N	f	\N
10	Bainbridge Island Rowing Club	301 Shannon Dr SE	Bainbridge Island	WA	98110	47.622616	-122.518187	\N	\N	\N	\N	\N	\N	f	\N
11	Bair Island Aquatics Center	1450 Maple Street	Redwood City	CA	94063	37.534959	-122.21337	\N	\N	\N	\N	\N	\N	f	\N
12	Baltimore Rowing Club	3301 Waterview Avenue	Baltimore	MD	21230	39.2549944	-76.6244584	\N	\N	\N	\N	\N	\N	f	\N
13	Bay Area Rowing Club of Houston	5001 NASA Parkway	Seabrook	TX	77586	29.5660591	-95.0701564	\N	\N	\N	\N	\N	\N	f	\N
14	Bayou Rowers	2433 Hwy. 308	Thibodaux	LA	70301	29.8356228	-90.9492546	\N	\N	\N	\N	\N	\N	f	\N
16	Boulder Community Rowing	5565 N 51st Street	Boulder	CO	80301	40.0737305	-105.2392327	\N	\N	\N	\N	\N	\N	f	\N
17	Bucks County Rowing Association	901 Bridgetown Pike	Langhorne	PA	19047	40.201009	-74.913089	\N	\N	\N	\N	\N	\N	f	\N
18	Camp Randall Rowing Club	617 North Shore Drive	Madison	WI	53703	43.06478	-89.3911876	\N	\N	\N	\N	\N	\N	f	\N
19	Cape Cod Rowing Inc	460 Shootflying Hill Rd	Centerville	MA	2632	41.679782	-70.3507068	\N	\N	\N	\N	\N	\N	f	\N
20	Cape Fear River Rowing Club	3410 River Road	Wilmington	NC	28412	34.1706249	-77.9512016	\N	\N	\N	\N	\N	\N	f	\N
21	Capital Rowing Club	1900 M St SE	Washington	DC	20003	38.878868	-76.97515	\N	\N	\N	\N	\N	\N	f	\N
22	Carnegie Lake Rowing Association	Class of 1887 Boathouse	Princeton	NJ	8540	40.339508	-74.650664	\N	\N	\N	\N	\N	\N	f	\N
23	Carolina Masters Crew Club	457 State Rd 1937	Chapel Hill	NC	27516	35.9084728	-79.0948719	\N	\N	\N	\N	\N	\N	f	\N
24	Cascadilla Boat Club	Stewart Park	Ithaca	NY	14850	42.4602113	-76.5108611	\N	\N	\N	\N	\N	\N	f	\N
25	Catawba Yacht Club Rowing	19809 W. Youngblood Rd	Charlotte	NC	28278	35.0766217	-81.0564798	\N	\N	\N	\N	\N	\N	f	\N
26	Cazenovia Rowing Club	1485-1493 US-20	Cazenovia	NY	13035	42.9254986	-75.8702262	\N	\N	\N	\N	\N	\N	f	\N
27	Central Connecticut Rowing Club	35 Harbor Dr	Middletown	CT	6457	41.5594106	-72.6444744	\N	\N	\N	\N	\N	\N	f	\N
28	Central Pennsylvania Rowing Association	Marina Rd	Sunbury	PA	17801	40.879936	-76.790893	\N	\N	\N	\N	\N	\N	f	\N
29	CHAOS Rowing	565 FARRINGTON RD	APEX	NC	27523	35.7436796	-79.0075944	\N	\N	\N	\N	\N	\N	f	\N
30	Charleston Rowing Club	444 Needlerush Parkway	Mt Pleasant	SC	29464	32.8640625	-79.8348831	\N	\N	\N	\N	\N	\N	f	\N
31	Chautauqua Lake Rowing	18 Jones & Gifford Ave	Jamestown	NY	14701	42.100368	-79.2560696	\N	\N	\N	\N	\N	\N	f	\N
32	Chesapeake Boathouse	725 S. Lincoln Boulevard	Oklahoma City	OK	73129	35.4578708	-97.5067116	\N	\N	\N	\N	\N	\N	f	\N
40	GMS Rowing Center	172 Grove St	New Milford	CT	6776	41.5645088	-73.408293	\N	21	20	25	25	\N	t	America/New_York
33	Portland Boat Club	12940 NW Marina Way	Portland	OR	97231	45.6207036	-122.808624	\N	15	18	18	15	10	t	America/Los_Angeles
34	College Club Seattle	11 E Allison Street	Seattle	WA	98102	47.6490849	-122.3274111	10mph max for novice scullers	12	12	12	12	6	t	America/Los_Angeles
15	Boathouse Row	1 Boat House Row	Philadelphia	PA	19130	39.9695828	-75.1876317	\N	15	15	15	15	\N	t	America/New_York
37	Sarasota County Rowing Club	800 Blackburn Point	Osprey	FL	34229	27.180198	-82.4973666	\N	10	10	10	10	\N	t	America/New_York
38	Nathan Benderson Park	5851 Nathan Benderson Cir	Sarasota	FL	34235	27.3742443	-82.4500873	\N	12	12	8	8	\N	t	America/New_York
35	Orlando Rowing Club	2200 Lee Road	Orlando	FL	32810	28.5985021	-81.4161573	Stay east side of lake if wind out of east or south.	5	\N	5	\N	\N	t	America/New_York
39	Sagamore Rowing Association	3 West End Ave	Oyster Bay	NY	11771	40.8757798	-73.5413329	N wind has 2k stretch for waves to build.	12	16	12	18	\N	t	America/New_York
36	Gainesville Area Rowing	151 SE 74th Street	Gainesville	FL	32641	29.6504834	-82.2414612	NE winds make it hard to get off the dock.	8	8	8	8	5	t	America/New_York
41	University of Connecticut	124 Lake St	Coventry	CT	6238	41.7673256	-72.3103987	NW winds of 7mph is starting to whitecap at our docks, though if you can make it to the "cove" at the top, it's usually nice. Any S/SW wind is rowable.	7	30	\N	\N	\N	t	America/New_York
42	Mendota Rowing Club	622 E Gorham St	Madison	WI	53703	43.082215	-89.3842102	4 statute mile stretch for W to NNW making racing 1x rowing (more relevant: launching) really unproductive in winds greater than 7-8 mph. That is about the max for do-able (but why?) when the wind is WSW and N. Other wind directions permit a little higher velocity but care must be taken when the wind is SSW to NNE at greater than 10 because the landforms and buildings cast wind shadows that result in fun, unexpected, gusts, with little disturbance of the water surface. And of course in a strong (12+) E wind one can row most of the near shore, provided you remain aware of how much you are being blown off shore.	8	10	15	8	\N	t	America/Chicago
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public."user" (id, username, hashed_password, email, c_or_f, registered_on, confirmed, confirmed_on, boathouses) FROM stdin;
1	test	$2b$12$dwn1k8ScJX59VzNjkuAuY.99.P5wnGNITyNTzWT567QV7eAJaqv1S	test@testuser.com	imperial	2021-03-29	t	\N	{5,3,16}
\.


--
-- Name: Boathouse_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."Boathouse_ID_seq"', 44, true);


--
-- Name: User_ID_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."User_ID_seq"', 11, true);


--
-- Name: boathouse Boathouse_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.boathouse
    ADD CONSTRAINT "Boathouse_pkey" PRIMARY KEY (id);


--
-- Name: user User_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "User_email_key" UNIQUE (email);


--
-- Name: user User_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- Name: user User_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT "User_username_key" UNIQUE (username);


--
-- PostgreSQL database dump complete
--

