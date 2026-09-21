# General Active Transportation Infrastructure Specification (GATIS) v2 DRAFT

## 1.0 Introduction

This specification (tentative working name “General Active Transportation Infrastructure Specification” or “GATIS”) seeks to establish a consistent national format for data that represents the physical transportation infrastructure used by those traveling via “active transportation” – walking, bicycling, micromobility devices (e.g. e-scooters or skateboards), and assistive mobility devices like wheelchairs.

This specification is the product of a national collaboration of public, private, and non-governmental participants originally convened by the U.S. Department of Transportation (U.S. DOT)’s Bureau of Transportation Statistics (BTS). It was created through a collaborative process and is maintained by ORGANIZATION through community consultation. The specification is fully voluntary, and any agency or other user may elect to adopt the specification at their own discretion.

### 1.1. Statutory Basis

BTS maintains the National Transportation Atlas Database (NTAD) as required in Statute under [Title 49 U.S.C. § 6309](https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title49-section6309&num=0&edition=prelim). The NTAD comprises a collection of national geospatial datasets of modal and intermodal transportation facilities and networks; flows of people, goods, vehicles, and crafts over the transportation networks across all modes; and social, economic, and environmental conditions that affect or are affected by the transportation networks. 

To date, the NTAD has lacked robust datasets of transportation facilities and networks for people traveling by active transportation. BTS convened the national collaboration due to its desire to establish a common format for active transportation infrastructure data that could facilitate the broader production and use of those data by a range of public, private, and non-governmental entities.

### 1.2 Goals

This specification intends to provide consistency and interoperability across multiple data producers, managers, and users within the United States. It is designed with active transportation travelers of all abilities in mind, and can be used in all contexts from rural, to suburban, to urban areas. 

The specification is designed to address gaps in existing standards and specifications by capturing the active transportation infrastructure attributes that are critical for preference-based routing, planning, engineering, and safety analyses, and improved asset tracking and maintenance, among other use cases. See [Term Definitions](#3.2-definitions) for a description of key terms.

### 1.3 Guiding Principles

[Guiding principles](https://github.com/dotbts/BPA/wiki/Guiding-Principles) shape the specification development and its ongoing evolution by specifying an intended purpose, audience, governance, and requirements. Voting members of the collaboration approved the guiding principles, and they may be revised or updated in the future as needed through the [Collaboration Framework](https://github.com/dotbts/BPA/blob/main/documents/drafts/CollaborationFramework.md) or any governance processes that might replace it in the future. The current guiding principles are listed in bold text below along with clarifying information about each:

1. **The specification is owned and openly governed by the community.**  
   * The specification is licensed under [CC0 1.0 Universal Public Domain](https://creativecommons.org/publicdomain/zero/1.0/deed.en).  
   * A defined governance process for this specification exists to guide changes and other processes (See [Governance](#6.0-governance))

2. **Data produced under the specification should be shared freely and openly with the community.**  
   * The specification should not be used to produce proprietary or private data   
   * A catalog of tools and code libraries facilitate use of this specification (See [Tools](#heading=h.2m3sj0s80z7v)). Existing and proposed tools include:   
     * Data sharing and conversion between open and proprietary formats  
     * Sample datasets that provide examples of how to use the specification

3. **The specification is designed to be as simple as possible, yet provide the ability to capture precise detail when available. It aims to enable technical and non-technical experts to effectively produce high quality data.**  
   * The specification defines four tiers of precision to facilitate broad adoption (See [Data Readiness Tiers](#heading=h.od3xilig28hr))  
     * Minimum requirements for creating and modifying data are a text editor and common web-based tools that can produce a GeoJSON  
     * Geographic Information System (GIS) and enterprise asset management tools can be used as well  
     * Users adopting the specification can increase their data precision over time, if desired   
   * The specification indicates required and optional fields for each tier of precision (See [Metadata](#3.1-metadata))  
     * A minimum set of required fields ensure attribute consistency and interoperability between datasets.  
     * Optional fields allow users to provide more detailed data if desired.  
     * New *required* fields may be added through the specification governance process, but must meet a high bar in recognition that doing so may require expensive manual data collection effort.   
   * One canonical validator exists (URL TBD), which should be considered the authority on what data passes and does not pass the specification. This validator will fill out many of the metadata fields with automatic or default values that users can edit.

4. **The specification prioritizes universal accessibility and the needs of all travelers, across a range of use cases.**  
   * The specification describes the infrastructure used for active transportation travelers in urban, suburban, and rural contexts. (See [Representing the Bicycle/ Pedestrian Environment](#heading=h.il2my3wdczv))  
     * For example: Walking infrastructure may include sidewalks, shared-use paths, paved shoulders, roadways, etc.  
   * Physical connections between various types of transportation infrastructure are positively identified.  
     * For example: Sidewalks on either side of an intersection, the curb ramps, and crosswalks are all connected.

5. **The specification describes objective qualities of infrastructure.**  
   * Specific measurements and objective terms are used instead of categorical values, to ensure data users can make preference-based decisions related to routing and analysis. (See [Representing the Bicycle/ Pedestrian Environment](#heading=h.il2my3wdczv))  
     * The specification does not include subjective categorical values like “accessible / not accessible.”  
     * Annotations for a sidewalk might include “width \= 60 inches” and “maximum cross-slope \= 2.1%.”  
     * Annotations for a sidewalk, shared-use path, or other footway might include “surface material \= asphalt.”

6. **The specification includes context that is useful for travelers and for information systems.**  
* This context for data users includes a metadata document with fields for data collection date, data collection methods, source data, relationships to other datasets, and data discoverability within catalogs and searches. (See [Metadata](#3.1-metadata))  
* The specification includes documented protocols for contributing and editing data in conformance with the specification. (See [Specification](#3.0-specification))  
    
7. **The specification is extensible, and designed to be interoperable or interchangeable with other trusted specifications to make maintenance and creation as easy as possible.**  
   * The specification can be extended by data creators as necessary to serve their needs, but minimum requirements must be met as indicated for each tier. (See [Data Readiness Tiers](#heading=h.od3xilig28hr))  
   * Extensions may be considered for incorporation in future versions of the specification, subject to the established governance protocols. (See [Governance](#6.0-governance))

### 1.4 Audience for This Document

The audience for this document includes anyone seeking to use this specification to leverage active transportation infrastructure data and/or improve its quality and usefulness. Anticipated users include both data producers and data consumers, such as:

* **Public Agencies**  
  * U.S. DOT and other federal agencies  
  * State and local Departments of Transportation (DOTs)  
  * State and local Departments of Public Works (DPWs)  
  * State and local Departments of Planning and Community Development  
  * Metropolitan and Regional Transportation Planning Organizations (MPOs, RTPOs)  
  * Transit and paratransit agencies  
      
* **Private Entities**  
  * Data aggregators and vendors  
  * Software developers  
  * Transportation planning and engineering companies  
      
* **Non-Governmental Organizations**  
  * Academic and research institutions  
  * Non-profit and advocacy organizations  
  * Members of the public

### 1.5 Anticipated Use Cases Of This Specification

The specification is designed to serve two use case categories, **Routing** and **Asset Management**, with many anticipated sub-applications. In line with existing governance processes, the specification may evolve to serve additional use cases with future revisions.

#### 1.5.1 Routing

Routing means that different components of the network (edges or nodes that represent roads, paths, sidewalks, etc.) are linked together in the data such that users can calculate or “model” pathways through the network according to certain rules. For example, a person who prefers to follow a low-stress bicycle route may only choose to travel along separated bikeways and roads with low volumes and vehicle speeds, or a person with a mobility or visual impairment may wish to find the routes that are suitable for wheelchair users or travelers using a cane.

Routing applications are typically used to model **how well a network provides access** to and from different parts of a region. One common application is modeling low-stress bike accessibility using [level of traffic stress](https://blog.altaplanning.com/level-of-traffic-stress-what-it-means-for-building-better-bike-networks-c4af9800b4ee) (LTS) ratings applied to along network segments and at intersection crossings. LTS can show which elementshow much of the network are is suitable for bicycle riders or pedestrians with different preferences; routing-based network analysis can   then show, and what kinds of destinations they can reach. Routing can also help model the different connections to and from specific destinations, such as transit stations and mobility hubs, medical, civic, and education facilities, parks and open spaces, and other locations of interest to people traveling by active transportation.

Another application is modeling where people with different **mobility preferences** can travel unimpeded. This is an important use case because any one impassable section of a route may require a detour or may make it impossible for such users to complete their trip. Accurate data is critical to understand where such conditions exist, especially if the modeling application is intended for user navigation. Navigation for people with visual, mobility, or other impairments requires detailed information about additional roadway features. Many of these features appear in the higher tiers of the specification.

In combination with demographic information data, such as from the U.S. Census and from commercial sources of business location datadata and land use data (location of jobs, retail, schools, etc.), routing analysis can help users analyze what destinations people from various origins can reach using assess the distribution of active transportation. Examples include determining accessibility to jobs or supermarkets by bike or by foot, accessibility to can be reached, or across different populations, including access by specific populations to specific destinations (e.g., school-aged children’s walking access to elementary schools by foot.). If further combinedIn combination with demographicCensus, land use, and roadway and transitmotor vehicle data, active transportation infrastructure data can support multimodal transportation modeling, allowing users to study people’s accessibility to destinations using transit, with active transportation for the first and last mile. the distribution of people and goodsusing on foot or by bicycle.using multiple modes of transportation in addition to freight and passenger vehicles.

Each of these examples demonstrate how routing applications support “gap analyses.” Gap analyses help users identify locations to prioritize or avoid when routing or navigating. They also help public agencies determine **where to plan and prioritize investment**, and which infrastructure improvements and traffic operation changes to program for design and implementation.

#### 1.5.2 Asset Management

Asset management use cases require **data on individual infrastructure elements**. These data may include attributes like location, dimension, operational characteristics, obstructions and condition. For example, a user may wish to know the location of all curb ramps, the length of all bike lanes, or the condition of all sidewalks in a given area. Asset management use cases are typically related to prioritizing maintenance, developing budget estimates, or measuring progress towards performance measure goals.

Asset management use cases often include programmatic-scale assessments of groups of infrastructure elements. Some applications may include simple inventories, such as the number of curb ramps that comply with Americans with Disabilities Act (ADA) requirements, the location of all sidewalk extensions or median refuges, or the percentage of roadway crossings with adequate pedestrian lighting. Other applications include the **evaluation of infrastructure conditions**, such as the surface quality of a shared use path, the visibility of bicycle lane markings, or the legibility of signage.

In combination with other data, such as traffic crashes or vehicle speed and operations (e.g., hard braking), asset management data for active transportation infrastructure can help users study the relationship between infrastructure and safety. In combination with land use and census data, it can help users evaluate how well infrastructure is maintained and what elements exist in different parts of a community.

#### 1.5.3 A Note on Network Routability

RIn rare cases, routing and asset management may have conflicting objectives. Asset management can be more flexible in representing active transportation infrastructure than routing because routing requires explicitly defined connections between active transportation infrastructure. For instance, tracking the locations of traffic calming treatments like curb-extensions or bulb outs are straightforward to map as an asset but become more complicated to represent as a routable network feature. This specification tries to anticipate these possible differences conflicts, but there may be certain active transportation-related features that are simply more efficient to represent separately from the as non-routable network routing features and characteristics. 

### 1.6 Acknowledgments

The following organizations and people were essential in the creation of this draft:

* The Co-Chairs of the National Collaboration on Bicycle, Pedestrian and Accessibility Infrastructure Data (NC-BPAID):   
  * Anat Caspi, Taskar Center for Accessible Technology, University of Washington  
  * Bahar Datashova, Texas A\&M Transportation Institute  
  * Jeff Whitfield, Physical Activity and Health Branch, Centers for Disease Control and Prevention  
* The Bureau of Transportation Statistics, U.S. Department of Transportation  
* The leaders of NC-BPAID’s Subgroups on Data Practices, Outreach, and Specification Development:   
  * Jonah Chiarenza, Volpe Center, U.S. Department of Transportation  
  * Ellwood Hanrahan, New York State Department of Transportation  
  * Jeff Maki, Public Works Office  
  * Paul Moser, Delaware Department of Transportation  
  * Krista Nordback, Highway Safety Research Center, University of North Carolina  
  * Josh Roll, Oregon State Department of Transportation  
  * Ryan Westrom, Citian  
* Members of the NC-BPAID collaboration who provided insights, ideas, and feedback on this draft  
* Members of the two task forces of the NC-BPAID Specification Development Subgroup, Intersections and Accessibility  
* Carl Fredlund and our peers at MobilityData  
* Volpe Center, U.S. Department of Transportation  
* Federal Highway Administration, U.S. Department of Transportation  
* National Highway Traffic Safety Administration, U.S. Department of Transportation  
* Developers and maintainers of other specifications who provided advice along the way, including OpenStreetMap and the OSM US Pedestrian Working Group, OpenSidewalks, Open Mobility Foundation, General Transit Feed Specification (GTFS) and Workzone Data Exchange  
* Last but not least, the individuals and organizations who are currently reviewing this draft and helping to take it to the next level. We appreciate you\!

## 

## 2.0. Specification Overview

This specification seeks to digitally represent bicycle, pedestrian, and accessibility infrastructure in the public right-of-way (shorthanded as active transportation infrastructure (ATI) throughout the rest of this document).

ATI includes but is not limited to: 

* Sidewalks  
* Curb ramps  
* Accessible Pedestrian sSignals  
* Crosswalks and crossbikes  
* RaisedCrossing islands  
* Bicycle lLanes  
* Cycle tracks (also known as separated bike lanes and protected bike lanes)  
* Multi-use paths  
* and many others

To some extent the specification also seeks to digitally represent roads because 1\) cyclists are allowed to cycle on most roads, 2\) pedestrians are sometimes allowed to walk on roads, and 3\) roads are barriers that pedestrians and cyclists must cross (two-lane v. nine-lanes), and knowing how ATI interacts with the road is crucial for connectivity and safety analyses, and 4\) demographic and land use data used for destination accessibility analysis is generally tied to road segments.

The specification draws on the Public Right-of-Way Accessibility Guidelines (PROWAG), OpenSidewalks, OpenStreetMap, and extensive discussions in the collaboration to create an extensive list of fields with which to precisely describe ATI. Note that while the specification draws from OpenSidewalks and OpenStreetMap, the terminology used to describe ATI has been modified to more closely reflect transportation engineering and planning practice in the United States and/or add clarity.

This specification is designed to be extensible to other specifications such as GTFS. Part of this means that the specification allows for explicit linking to other specifications but forbids duplicating features. Practically speaking, this specification includes features that directly connect to a GTFS stop id but do not include features that could be potentially represented in the GTFS dataset such as station entrances, escalators, etc. We highly recommend the creators of extended datasets like GTFS to complete all accessibility related fields. For GTFS, this means creating a complete Pathways dataset.

This specification may not provide an exhaustive list of all possible methods for representing and describing ATI, but the specification seeks to establish common practices and minimal requirements to help standardize the collection of these data and accomplish the overall goals of the specification.

### 

### 2.1 The Tier Model

Some data creators might be preparing ATI datasets from scratch while others will be working with existing datasets that may (or may not) easily translate to this specification. The Tier Model aims to meet data creators where they are by providing a minimum set of requirements and a suggested [roadmap](https://www.atlassian.com/agile/product-management/product-roadmaps) for increasing the completeness, timeliness, precision, and other aspects of the data creators’ existing bicycle and pedestrian data over time. The model also provides guidance on best practices for those creating new datasets.

There are four tiers numbered from 1 to 4 in order of increasing value. There is no certification schema or recognition for achieving a particular tier. Rather, the model is meant to be self-guided. Tiers are intended to be “mix and match” across different aspects. An organization may be at the Tier 2 level when it comes to precision, for example, but at Tier 4 when it comes to completeness of the data. This system was inspired in part by the [OSM US Pedestrian Working Group’s schema](https://wiki.openstreetmap.org/wiki/Foundation/Local_Chapters/United_States/Pedestrian_Working_Group/Schema).

The tier model applies to:

* Which attributes are required for ATI facilities. For instance, a sidewalk slope attribute is optional at Tier 1 but required at Tier 2 and beyond.   
* The routability of the prepared data.   
* How ATI should be digitally represented  
* Whether frequent updating is required How often the data is updated

Throughout the remainder of this document the tier model will be referenced whenever there is a spectrum of how a data creator can (or should) create data for the specification. 

In summary, at lower or earlier tiers:

* Data collection processes are focused on creating a complete inventory of assets that is exhaustive, but has few attributes that may not be complete  
* Data in the specification format is likely being used in conjunction with existing processes for use cases like project prioritization, but data is not likely routable or is routable within small “islands”  
* Geometry for ATI may be connected to the road, rather than being reflective of the real geometry of, for example, a sidewalk that runs alongside a road  
* Attribute values may not capture the complete variability in the field. For example, width may vary along the edge segment in the real world, while the data shows constant values.  
* Data is focused on one primary infrastructure type: e.g. bike paths *or* sidewalks.  
* Linking to other data sets is possible, but only spatially and inferentially. There are no shared identifiers that exist across datasets.  
* Data may only be partly vetted by the infrastructure owner, or only vetted by third parties.  
* Data is only a snapshot of any system of record. The data may be months old or more.

While at later tiers:

* Data collection processes are focused on completeness of attributes for each asset.   
* Data collectors likely received training and are using quality assurance and quality control processes that ensure minimal variance and maximum consistency across collectors. Collection technology may be highly accurate – for example, using LIDAR.  
* Data is contained within a single-source-of-truth database across the organization, and established organizational processes mandate the use of this single source of truth across analysis, reporting, and other use cases, as well as derivative products.  
* Data is routable via spatial attributes, metadata, and by attributes that convey the needs of travelers with a range of mobility profiles.   
* Geometries of ATI infrastructure are accurate, especially when they vary from the roadway. For example, a sidewalk adjacent to a road that deviates from the road to go around an obstruction is reflected in the data with distinct geometry.   
* Edges are segmented when attribute values (such as width) change significantly.   
* Complete, preference-based attributes on accessibility and the features of bicycle and pedestrian spaces are present in the data to enable modeling and routing based on traveler profiles.   
* Alternative networks are provided for routing applications to optionally switch between. For example, bicycles can be routed between bike facilities, streets, multi-use paths, and other appropriate spaces.   
* Linking to other datasets is enabled via identifiers stored within the data.  
* Data is fully vetted by the infrastructure owner.  
* APIs or other facilities exist to make edit suggestions to data when users discover errors.  
* Data is very recent, and pulled directly from a system of record.  
* Systems are in place to update the data set with changes in land use or transportation network (same time as tax lot map and road updates)

### 

### 2.2 Concepts and Terminology Used In This Document

This section introduces technical details and terminology of the specification. This section will be more general while subsequent sections will include more concrete details on how these terms and concepts apply to preparing specification data. 

#### 2.2.0 Core Geospatial Entities (“Features”)

The specification includes three types of core geospatial entities: **edges**, **nodes**, and **zones**. 

**Edges, nodes, and zones should all represent ATI that is part of the bicycle and pedestrian travel way**. For pedestrians, this includes features like sidewalks and crosswalks. For cyclists, this includes dedicated bicycle infrastructure, but it may also include roads since cyclists are classified as vehicles and often expected to ride in the roadway. 

Each entity has a type and attached fields that describe it (see Section 3.0).

| Type | [OGC Geospatial Format](https://gsp.humboldt.edu/Websites/BlueSpray/STUsersGuide/Scripting/Script_SimpleFeatures.html) | Description | Examples |
| :---- | :---- | :---- | :---- |
| Edge | LineString | A segmented line that connects two nodes (points) | Sidewalks, roads, multi-use paths, separated bike lanescycletracks |
| Node | Point | A point that connects two or more edges (linestrings) | Generic node, curb ramps, impediments |
| Zone | Polygon | A closed segmented line that connects at least three nodes (points) | Pedestrian zone, raisedcrossing islands |

#### 

#### 2.2.1 Relation Tables

In addition to the core geospatial entities, there are also **relation tables** that can reference two or more core geospatial entities (as a tuple) and relate attributes to those geospatial entities, just as geospatial entities can have attributes themselves.

Relation tables can be used to set attributes at intersections, for example, to model intersection treatments such as bicycle two-stage left turns and turn restrictions. 

***\[At this time, the specification does not explicitly define how to create or utilize relation tables. We expect to address this more fully in the second draft.\]***

#### 2.2.1 Routing

The core geospatial entities should form a network graph for routing. For the geospatial entities to be **routable**, entities should be **topologically connected**:

* **Edges should have endpoint-to-endpoint connectivity (Figure 1), possibly with a specified margin of error (i.e. below which points should be considered to overlap)**  
    
* **When two or more edges cross each other at-grade, they should all share a vertex or node at that intersection (Figure 1, right) if they are actually connected**

In addition to being topologically connected, a routable network can also come with explicit **network referencing fields**. This means that edges have two node-referencing fields (“from\_node\_id” and “to\_node\_id”) that can be used to construct and identify directions in a network graph, in addition to a unique edge ID. 

When using network referencing fields, the edges in the network should be segmented such that every intersection (where two or more edges meet at-grade) results in a new edge (see 2.1.1 Segmentation).

![][image1]  
Figure 1: Network graph representation

Above Tier 1, Tthe specification supportsstrongly encourages creates a creating routable networks to support detailed routing-based analysis and navigation for cyclists and pedestrians. Examples of rRouting-based analyses include able networks create explicit relationships between edges that allow data users to utilize the data for comfort and accessibility analysis, andanalysies, and also allow the identifyingication of edge “centrality” (a measure of, or the importance of a network an infrastructure element in providing access), and methods that optimize or prioritize network improvements. within a network. 

However, the specificationspe    cification acknowledges that developing routable networks is a time-consuming process, and that athe non-routable network can still support asset management. Generally, a topologically connected network would be **required** at Tier 3 and above. A network with networking referencing would be **required** at Tier 4\.

For new datasets, it is recommended that data be routable via graph metadata. 

| Data Aspect | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
| :---- | :---- | :---- | :---- | :---- |
| Routable via Spatial Topology | Optional; likely inconsistent across the dataset |  | Required; consistent within the dataset |  |
| Routable via Graph Metadata | Optional, but encouraged |  | Recommended | Required |
| Conflation (i.e. linking to other networks) | Optional; likely only spatially | Recommended; with ID values to a public dataset like OSM |  | Recommended; also with ID values to a system of record |

Zones are polygon features that contain metadata that, similar to an edge, help routing applications determine how or when to route between nodes within the zone. Routing applications may determine how to model zones “behind the scenes” in their implementations. For example, they may choose to create pairwise edges between all nodes contained within the zone to effectively collapse zones into edges, or they may handle them at request time using another logic of their choice.

#### 2.2.1 Directionality and the use of “left”, “right”, and “both”

Functionally, edges can be unidirectional, allowing travel in only one direction, or bidirectional. In addition all Eedges have a topological directionaare directional: their direction is defined by either the sequence of vertices that make up the edge or the network reference ids from the start node to the end node (if network reference ids are included). The attribute Edge **directionality** indicates which general travel directions are permitted on an edge with reference to its topological directionality. There are three values: **forward**, **backward**, and **both**.

| Allowed Travel Direction | Description | Example |
| :---- | :---- | :---- |
| Forward | Only forward travel (from the first vertex to the last vertex) | One-way bike laneroad, escalator |
| Backward | Only backward travel (from the last vertex to the first vertex). This value is only used to indicate exceptions such as contra-flow bike lanes on one-way roads. | Contra-flow bike lane on a one way road |
| Both | Travel is allowed in both directions | Sidewalks, stairs, two-way roads |

Certain fields such as “incline” are directional and depend on the direction traveled (uphill or downhill). These types of fields should always be referenced to the sequence of vertices to avoid confusion with the allowed directions.

As will be discussed in Section 2.3, certain ATI can be referenced in relation to a road. To accomplish this, three modifier fields (**left**, **right**, and **both**) are used in conjunction with an edge’s topological direction to establish where these features are in relation to the road. For instance, a sidewalk on the left side of the road (in reference to the sequence of vertices) would be marked as “sidewalk:left:presence=yes.” Similar to incline, the information would be opposite different when considering travel in going the opposite direction on the link (now the sidewalk would be on the right side).

#### 2.2.2 Edge Segmentation

Edge segmentation refers to how linear features edges are divided into parts in the dataset. While considerable flexibility is allowed, Tthis specification has two important constraints does not include specific recommendations on network segmentation. First, for tiers that require that the network be routable, edges should be segmented at intersections. Second, 

, but note that **edges can only support one set of attributes along their entire length**. Practically speaking, this means that modeling a change in sidewalk width, for example, requires creating two edges with the two different width values. Data creators working with a Linear Referencing System (LRS) dataset or a General Modeling Network Specification (GMNS) dataset with segment data on their links need to segment out their data to conform to this specification since thoese formats support attaching multiple sets of attributes to one geospatial feature. When providing a routable network, edges should be segmented at intersections as well.

**Important: apparent segmentation of a path’s geometry does not necessarily have to be represented in the data by edge note that the segmentation of an edge in the data does not necessarily have to reflect the segmentation of the geometry–for example, an “S”-shaped path that is consistent in width and other attributes may be represented in the data by a single  only have one edge (a polyline in an S shape), or it may be represented by multiple edges. in the data, yet may be segmented multiple times geometrically to form its “S” shape.**

### 2.3 Recommended Practices For Digitizing Bicycle, Pedestrian, and Accessibility Infrastructure {#2.3-recommended-practices-for-digitizing-bicycle,-pedestrian,-and-accessibility-infrastructure}

There are several different conventions for digitizing Active Transportation Infrastructure (ATI) spatial data that have emerged over the last two decades. See [https://github.com/dotbts/BPA/tree/main/resources/attribute\_tracker](https://github.com/dotbts/BPA/tree/main/resources/attribute_tracker) for an extensive list of existing ATI datasets.

Because many bicycle facilities, shared-use-paths/multi-use-paths, and sidewalks are built along, within, or around roadways (roadway aligned), one of the most common differences in representing ATI geospatially is whether these facilities are modeled as fields (attributes) on the roadway centerline or as separate geospatial features with their own true geographical locations and dedicated fields (attributes).

Figure 2 shows a schematic depicting this difference. The image on the left shows the existing conditions. The image in the center shows what is referred to as **Parallel Feature Network Representation**. It models sidewalks and crosswalks as their own separate features, each with its own centerlines. IBt models bicycle facilities that are physically separated from the road are likewise modeled as as separate features;  centerlines, while keeping however, conventional bicycle lanes and other facilities that are integrated in the road are not usually modeled as separate features, but instead as attributes of the road(for example, separated only by paint; see Section 2.3.1.0) represented as fields on a road centerline. The image on the right shows what is referred to as **Roadway Centerline Representation**, in which. This image models sidewalks and all bicycle facilities are modeled as attributes part of the road; there is no separate centerline for them. With roadway centerline representation, stand-alone paths (multi-use paths that do not run along a road) must be represented by their own roadway feature, which may requiring creating a new centerline geometry, as in  creating a new roadway featureexcept for one multi-use path that is separate from the roadway.

![][image2]  
![][image3]  
Figure 2: (left) aerial photo of streets, sidewalks, and bicycle paths (middle) network representation (right) roadway centerline representation

While the specification allows for both methods of representation, the specification advocates for data creators to move towards network representation for sidewalks, multi-use pathways, and some types of bicycle facilities (described in Section 2.3.1.0) to allow for more precision in describing the infrastructure and accomplishing the intended use cases of routing, navigation, and asset management. Network representation also allows for better spatial description and flagging of obstructions or impediments to accessible travel.

The next sections will provide general guidance on **Network Representation** and **Roadway Centerline Representation**. 

#### 2.3.0 Roadway Centerline Representation

Roadway Centerline Representation is a method of representing the presence and physical description of roadway-aligned bikeways, sidewalks, and other pathways using fields on a roadway centerline. Sidewalks and bike lanes aren’t always symmetrical across a road; a sidewalk may only exist on one side of the road but not the other side. Roadway centerline representation tracks both sides independently using the “left”, “right”, and “both” field modifiers (see Section 2.2.1). Left and right are **always** used in reference to the sequence of vertices that make up the edge (from beginning to end). Figure 3 demonstrates how the presence of sidewalks and shared-use paths on the left and right side of the roadway are tracked while Figure 4 demonstrates how the presence of bike lanes and shared-use paths on the left and right side of the roadway are tracked.

![][image4]  
![][image5]  
Figure 3: Road centerline representation of sidewalks  
![][image6]  
![][image7]  
Figure 4: Road centerline representation of bike lanes

In Roadway Centerline Representation, roadway-aligned ATI does not have its own spatial representation or separate geometric features. This reduces spatial precision and the ability to provide active transportation users with precise and customized routing.

#### 2.3.1 Parallel Feature Network Representation

Parallel Feature Network Representation provides a more comprehensive and detailed spatial description of bikeways, sidewalks, pathways, etc. Parallel Feature Network Representation also allows for geospatial representation of roadway crossings at crosswalks as edges. Figure 5 shows an example of network representation. In network representation, bike lanes are still represented on the road centerline (see next section).

While Parallel Feature representation offers many advantages, one drawback is that the relation to the parallel road segment is lost, unless the parallel road segment ID is included as an attribute of the parallel feature or the features are related through a relation table. 

There are some drawbacks to Network Representation. Representing network features separately removes the explicit association between them, and the added geometric complexity may complicate geospatial operations, map matching, or routing efforts. Additionally, there are some ATI features such as bike lanes that should not get their own dedicated feature.

![][image8]

![][image9]  
Figure 5: Network representation of sidewalks, and dedicated bike facilities, and roadway centerlines

##### 2.3.1.0 Exceptions to Parallel FeatureNetwork Representation

For ATI that is along, within, or around a road (roadway-aligned), there are a few exceptions in which it is **not recommended** to represent the ATI as a distinct separate spatial feature from the road centerline. The rule of thumb for deciding whether or not to draw a feature as a separate centerline (instead of representing it with fields on the road) is to ask if:

1) Is the ATI integrated into the road?  
   1) Is the path taken on ATI distinct from the path taken on the road centerline?  
   2) Are cars prevented from entering/crossing into the ATI?  
   3) Is there some obstacle (physical or legal) that prevents ATI users from transitioning between the road and the ATI? For example, a curb, a continuous concrete barrier, etc.   
2) Are there attributes of the ATI that would be too complicated to track on the road centerline?

For instance, 1\) sidewalks are usually not integrated into the road because a) sidewalks often meander, deviate, or depart the road, b) cars cannot easily access sidewalks, and c) sidewalks are typically separated from the road with a curb or a grass strip. It’s also 2\) complicated to track sidewalk attributes like running slope, cross slope, surface type, condition, etc. on the road centerline.

The one type of ATI facility that should be represented as a field on the road are bicycle facilities that are painted on the road with no physical accompanying separation. These are 1\) integrated with the road because a) they take the same path as the road and b) there is no meaningful obstacle (physical or legal) between the ATI and the road, and 2\) it’s not complicated to track the attributes of these bicycle facilities on the roadway centerline.

Exceptions to the rule for painted bike lanes

- Segments of bufferedprotected bike facilities that are paint protected  
- Bike crossings at protected intersections

## 

## 

## 3.0 Specification {#3.0-specification}

### 3.1 Files

All files must be in GeoJSON or JSON format, with attributes as feature properties.

Files:

* Nodes File  
  * Named “nodes.geojson”  
  * GeoJSON features must be POINT type  
* Edges File  
  * Named “edges.geojson”  
  * GeoJSON features must be LINE type (MULTILINE type is not supported)  
* Zones File  
  * Named “zones.geojson”  
  * GeoJSON features must be POLYGON type (MULTIPOLYGON type is not supported)  
* Points File  
  * Named “points.geojson”  
  * GeoJSON features must be POINT type  
* Metadata File  
  * Named “metadata.json”  
  * JSON

GATIS uses WGS84 (World Geodetic System 1984\) as its coordinate reference system (CRS). WGS84 is the default CRS for GeoJSON files.

### 3.2 Definitions {#3.2-definitions}

* Accessibility: is defined as ADA accessibility for people with disabilities unless otherwise noted.  
* Network Features: any data which represent a bicycle/pedestrian “way.” Network features can define a Routable Network or Graph (defined below). Network features can also include features which represent a physical impediment (like an obstruction) or features that represent routing restrictions (like a closure).  
* Non-Network Features: any data which are not physically located on a bicycle or pedestrian way, but which might be important for travelers to know about. Examples include street furniture, parklets, and drinking fountains.   
* Edges: a geospatial line that represents the path of travel between two nodes in a Routable Network or Graph. Within this specification, edges represent the centerlines of different pieces of linear-shaped infrastructure, such as sidewalks, bike lanes, and crossings.  
* Nodes: a geospatial point that represents the connection between two or more edges in a Routable Network or Graph. Within this specification, nodes most often indicate a particular type of infrastructure, such as a curb ramp or a transit stop.  
* Zones: a geospatial polygon that represents a defined area. Within this specification, zones are used to indicate areas such as parks and plazas where pedestrians may choose their path freely within the polygon space.   
* Attribute: a field or value that provides deeper information about a Feature. For example, the attribute “width” describes how wide a piece of infrastructure (like a bike lane or a curb ramp) is.  
* Field: treat as interchangeable with attribute.  
* Routable Network or Graph: A representation of relationships between Features, defined by Nodes and Edges. When these Nodes and Edges are connected correctly, a Router can use the Network or Graph to map out a travel path for a bicyclist or pedestrian. See 2.2.1 for a deeper explanation of what makes a network routable.   
* Spatial (Graph) Inference: Using the geospatial coordinate data about two or more Features to draw conclusions about their connectivity or the relationship between them. Within a Routable Network or Graph, if a Node and an Edge touch or are very close to each other, spatial inference can be used to conclude that the Features they represent are likely to be physically connected.  
* Metadata-based Graph Inference: Using Attributes about Features to draw conclusions about their connectivity or the relationship between them. For example, an analyst may use “to\_node” and “from\_node” attributes to determine that a traveler can connect from one Edge to another because both Edges are connected by the same Node.   
* (Graph) Post-Processing: Steps taken by an analyst to refine a Routable Network or Graph for their specific use case. Post-processing may assume connections between specific Features based on rules they establish, add or remove Features, or adjust the data to fit specific software or analytical needs, to give a few examples.  
* Router: A Router is a type of software designed to make calculations from a Routable Network or Graph and return a suggested route between the origin of a trip and the destination. Routers can be designed to return routes based on a range of criteria. For example, they can recommend and prioritize multiple routes, take information about specific travelers and attempt to optimize routes based on traveler needs, and optimize route choices based on factors such as faster travel time, shorter distance or reduced exposure to vehicle traffic. Routers are typically third-party software that take data created using these specifications as an input.  
* Edge Costs or Impedances: Within a Routable Network or Graph, all edges have a length. In addition, Eedges can be assigned costs or values based on how they may impact a traveler. These costs can be based on a range of Attributes, such as length (or distance traveled), travel time or exposure to vehicle traffic. A Router would use an Edge Cost to find the route or routes that best satisfy the needs of an individual traveler. 

### 3.3 Presence Descriptors Used In This Specification

A presence descriptor is a term used to describe whether a field or file should be included in a dataset. These are the presence descriptors used in this specification:

* **Optional** \- The field or file can be omitted from the dataset.  
* **Recommended** \- The field or file may be omitted from the dataset, but the specification encourages that it be included.  
* **Required** \- The field or file must be included in the dataset and contain a valid value for each record.  
* **Conditionally Required** \- The field or file must be included under conditions outlined in the field or file description.  
* **Conditionally Forbidden** \- The field or file must not be included under conditions outlined in the field or file description.

***NOTE: The presence descriptor of fields and/or files changes across tiers.***

### 3.4 Attribute Types Used In This Specification

* **Array\<Type\>** \- A JSON element consisting of an ordered sequence of zero or more values of the specified sub-type  
* **Boolean** \- One of two possible values, “yes” or “no”. In the [OpenStreetMap boolean](https://wiki.openstreetmap.org/wiki/Item:Q21937) format.  
* **Date** \- Where possible, a date should contain the year, month, and day, but month and year can be used if day is not available. In RFC 3339 format. *Example: 2018-09-13 for September 13th, 2018\.*  
* **Datetime** \- A datetime should contain the year, month, day, hour, minute, and second. Use 24-hour two-digit codes for hours. If lower values aren’t available, zeros may substitute (for example: 2025-07-07T12:00:00, filling minutes and seconds with zeros). In RFC 3339 format. *Example: 2018-09-13T13:23:14 for September 13th, 2018 at 1:23:14 pm.*  
* **Enum** \- An option from a set of predefined (or "enumerated") constants defined in the "Description" column. Values can be Text or Integer. *Example:* The *directionality* field can only be *forward*, *backward*, or *both*.  
* **ID** \- An ID field value. An ID is labeled "unique ID" when it must be unique within a file. IDs defined in one .txt file are often referenced in another .txt file. IDs that reference an ID in another table are labeled "foreign ID".  
  *Example: The edge\_id field in edges.geojson is a "unique ID". The node\_id field in edges.geojson is a "foreign ID referencing nodes.node\_id".*  
* **Float** \- A floating point number. Use floats for numbers that contain decimal values. Example: 4.12.  
* **Integer** \- A whole number, with no decimal values. Example: 4\.  
* **Text** \- A string of UTF-8 characters which must be human readable. Some text fields have recommended string values but allow for analysts to add other values as well, to increase standardization without being overly restrictive.  
* **URL** \- A fully qualified URL that includes http:// or https://. Any special characters in the URL must be correctly escaped. See the following [http://www.w3.org/Addressing/URL/4\_URI\_Recommentations.html](http://www.w3.org/Addressing/URL/4_URI_Recommentations.html) for a description of how to create fully qualified URL values.

All geospatial features, listed out in section 2.2.0, use the [Open Geospatial Consortium (OGC) Format](https://www.ogc.org/standards/). Refer to this section and the OGC guidelines for how to structure this data.

### 3.1 Metadata  {#3.1-metadata}

This section describes the elements for the metadata file. Note that metadata describes the dataset as a whole. Some attributes within this schema provide metadata about features (such as the “node\_to” and “node\_from” attributes for edges) which appear elsewhere in the specification. 

This metadata schema shares some attributes and commonalities with a few other schemas:

* [Data Catalog Application Profile for the USA (DCAT)](https://doi-do.github.io/dcat-us/#).  
* [Croissant Format Specification](https://docs.mlcommons.org/croissant/docs/croissant-spec.html).  
* [The Data Cards Playbook](https://sites.research.google/datacardsplaybook/).  
* [The Data Nutrition Project..](https://datanutrition.org/)  
* [OpenSidewalks Data Schema](https://github.com/OpenSidewalks/OpenSidewalks-Schema).

The validator will help to populate the following attributes: schema\_version, date\_created (using current datetime), ~~license (using Creative Commons Universal license URL),~~ geographic\_bounding\_box, keywords (default values), attribution (concatenation of Title, Publisher, Version, Data Download URL and License), date\_modified (using current datetime), and checksum (generation of MD5 hash). It can also help to populate the conforms\_to attribute by inserting URLs for specifications selected from a pre-populated list by the user.

| Name | Type | Description | Status | Tier | Metadata Type |
| :---- | :---- | :---- | :---- | :---- | :---- |
| title | Text | The title of the dataset, | Required | 1, 2, 3, 4 | Basic |
| version | Text | Version number for the current dataset using [semantic versioning](https://semver.org/). Format: MAJOR.MINOR.PATCH | Required | 2, 3, 4 | Basic |
| description | Text | A brief (1-2 sentence or similar) description of what’s in the dataset. | Required | 1, 2, 3, 4 | Basic |
| publisher | Text | Organization responsible for collecting and maintaining the data. | Required | 1, 2, 3, 4 | Basic |
| schema\_version | Text | The version of the NC-BPAID schema in use. Use current version here as default value. | Required | 1, 2, 3, 4 | Basic |
| date\_created | Datetime | The date when this dataset was initially created. | Required | 1, 2, 3, 4 | Basic |
| contact\_name | Text | The name of a person who can be contacted with questions or for further information about the data. | Optional | 1, 2, 3, 4 | Basic |
| contact\_info | Text | The email address or phone number to reach someone who can answer questions or provide further information about the data. | Required | 1, 2, 3, 4 | Basic |
| license | URL | The license under which the data is published for use. URL linking to the license agreement; default value [https://creativecommons.org/publicdomain/zero/1.0/](https://creativecommons.org/publicdomain/zero/1.0/). | Required | 1, 2, 3, 4 | Basic |
| geo\_bounding\_box | Polygon or MultiPolygon | Geospatial data describing the upper and lower latitudes and longitudes within which the data falls. | Optional | 1, 2, 3, 4 | Basic |
| keywords | Text | A set of single words or short phrases that describe the content of the data. | Required | 1, 2, 3, 4 | Basic |
| attribution | Text | Line of text that a data user can copy to properly cite the dataset. TASL format (Title, Author, Source, License) or academic format (ALA, Chicago) recommended. | Optional | 2, 3, 4 | Detailed |
| data\_download\_url | Text | Direct URL to begin downloading the data; should not require additional clicks or steps besides visiting the URL to begin download. | Optional | 2, 3, 4 | Detailed |
| data\_docs\_url | Text | URL to access a data documentation booklet or site covering methodologies and other technical aspects of the data. | Optional | 2, 3, 4 | Detailed |
| data\_dictionary\_url | Text | URL to access the data dictionary for the dataset, in PDF, HTML or JSON format. | Optional | 2, 3, 4 | Detailed |
| data\_service\_endpoint\_url | Text | URL to access the data via a data service, such as Data.gov (catalog.data.gov/dataset/…), ArcGIS Online (ex. Feature service or feature layer link) or Socrata. | Optional | 2, 3, 4 | Detailed |
| rights\_usage\_limits\_restricts | Text or URL | Text or a URL providing greater detail on how the data can and should be used, what rights are reserved, the scope of the data and any other useful information. Populate with either a text statement or with a URL linking to a text statement or policy. | Optional | 2, 3, 4 | Detailed |
| quality\_validation | Text or URL | Statement describing the methods used to ensure quality and to validate the data, providing quantitative results where possible; can be a link to a web page or tool containing more information. | Optional | 2, 3, 4 | Detailed |
| date\_modified | Datetime | The date when this dataset was last updated. | Required | 3, 4 | Data Collection & Maintenance |
| checksum | Text | An MD5 sum associated with the dataset in its current state, used to check if the data has changed since last accessed; new checksums should be generated each time the data is updated. | Optional | 3, 4 | Data Collection & Maintenance |
| freq\_cadence | Enum | How often the full data is updated – for example, when new lidar is collected or a new field study is conducted; do not use for minor updates (ex. Correcting a few rows). Use values from the [Dublin Core frequency specification](https://www.dublincore.org/specifications/dublin-core/collection-description/frequency/).  | Optional | 3, 4 | Data Collection & Maintenance |
| modification\_notes | Text | Text statement describing recent updates or modifications that regular users might want to know about. | Optional | 3, 4 | Data Collection & Maintenance |
| collection\_period\_start | Date | Beginning date of the period during which data was collected; approximation is acceptable. Include at least the month and the year if possible. | Optional; if frequency / cadence \= ‘continuous,’ leave blank | 3, 4 | Data Collection & Maintenance |
| collection\_period\_end | Date | Ending date of the period during which data was collected; approximation is acceptable. Include at least the month and the year if possible. | Optional; if frequency / cadence \= ‘continuous,’ leave blank | 3, 4 | Data Collection & Maintenance |
| collection\_method | Array (enum) | List of the methods used to collect and extract the data. Values: Satellite / aerial; LIDAR; field survey / manual; GPS survey; hand traced or tagged; AI interpretation; transformation from another format / database | Optional | 3, 4 | Data Collection & Maintenance |
| collection\_notes | Text | Text statement providing additional detail about data collection methods and approach, including selection, tools, and data processing. | Optional | 3, 4 | Data Collection & Maintenance |
| conforms\_to | Array (URL) | List of the URLs of other specifications to which attributes within the data also conform. | Optional | 3, 4 | Provenance & Relationships |
| source\_dataset | Text | Either a link or a citation (title, publisher and publication date) to the primary dataset used to create the data; in many cases, this data will be satellite or LIDAR data used for extracting transportation elements.  | Optional | 3, 4 | Provenance & Relationships |
| source\_dataset\_type | Enum  | The type of dataset listed under Primary Source Dataset URL or Citation.  Values: aerial / satellite, LIDAR, GPS, field / manual, other | Optional | 4 | Provenance & Relationships |
| addl\_sources | Text | List of URLs or citations for additional data sources used besides the primary data source – ie for blending, for extracting additional features, etc. | Optional | 4 | Provenance & Relationships |
| source\_notes | Text | Text note describing any additional information about data sources, including how they were collected, any known issues, and cleaning and processing.  | Optional | 4 | Provenance & Relationships |
| contributor\_consulted | Text | Text statement acknowledging people or organizations who contributed or who were consulted in creation of the dataset. | Optional | 4 | Provenance & Relationships |
| used\_by | Text | Text statement describing related datasets or projects – for example, if another organization takes this data and layers on additional features. Include URLs where possible. | Optional | 4 | Provenance & Relationships |
| funding\_organization | Text | Name of the organization(s) who provided funding to enable any part of the effort to produce the dataset. | Optional | 4 | Provenance & Relationships |

### 3.2 Nodes

#### 3.2.0 Node Types

This table lists all of the allowed node types in the specification.

#### Moved here: [https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=1871199758\#gid=1871199758](https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=1871199758#gid=1871199758) 

#### 3.2.1 Recommended and Required Fields for Nodes

This table gives an overview of the recommended and required fields for nodes based on the type of node. At higher tiers, more fields are added. For a full list of optional and forbidden fields see the [field spreadsheet](https://docs.google.com/spreadsheets/u/0/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit).

#### 3.2.1 Node Fields

The following table lists all node fields.

Moved here:  
[https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=1871199758\#gid=1871199758](https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=1871199758#gid=1871199758) 

### 

### 3.3 Edges {#3.3-edges}

#### 3.3.0 Edge Types

This table lists all of the allowed edge types in the specification.

#### Moved here: [https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=1152664813\#gid=1152664813](https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=1152664813#gid=1152664813) 

#### 

#### 3.3.1 Recommended and Required Fields for Edges

This table gives an overview of the recommended and required fields for edges based on the type of edge. At higher tiers, more fields are added. For a full list of optional and forbidden fields see the [field spreadsheet](https://docs.google.com/spreadsheets/u/0/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit).

| Edge Type | Tier | Required | Recommended |
| :---- | :---- | :---- | :---- |
| road | Tier 1 | edge\_id, street\_name, edge\_type, bikeway\_type |  |
|  | Tier 2 | edge\_id, street\_name, edge\_type, from\_node, to\_node, bikeway\_type, surface\_material, incline | separation\_permeable\_car, buffer\_width, traffic\_volume, posted\_speed\_limit, car\_freeflow\_speed, thru\_lanes, aux\_lanes, shoulder\_width, roadway\_centerline, bridge, status, issue, road\_speed, detectable\_warning |
|  | Tier 3 | edge\_id, street\_name, edge\_type, from\_node, to\_node, bikeway\_type, separation\_permeable\_car, bridge, surface\_material, status, incline, issue, detectable\_warning | buffer\_width, traffic\_volume, posted\_speed\_limit, car\_freeflow\_speed, thru\_lanes, aux\_lanes, shoulder\_width, roadway\_centerline, seasonal, traffic\_calming, curb\_height, road\_speed |
|  | Tier 4 | edge\_id, street\_name, edge\_type, from\_node, to\_node, bikeway\_type, separation\_permeable\_car, bridge, surface\_material, status, incline, issue, detectable\_warning | buffer\_width, traffic\_volume, posted\_speed\_limit, car\_freeflow\_speed, thru\_lanes, aux\_lanes, shoulder\_width, roadway\_centerline, seasonal, traffic\_calming, curb\_height, road\_speed |
| sidewalk | Tier 1 | edge\_id, road\_associated, edge\_type |  |
|  | Tier 2 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, width, surface\_material, incline | street\_name, status, pedestrian\_lane, ada\_compliance, issue, road\_speed, detectable\_warning |
|  | Tier 3 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, width, surface\_material, status, incline, cross\_slope, issue, detectable\_warning | street\_name, width\_min, bridge, surface\_quality, pedestrian\_lane, cross\_slope\_max, ada\_compliance, date\_built, check\_date, road\_speed |
|  | Tier 4 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, width, surface\_material, status, incline, cross\_slope, issue, detectable\_warning | street\_name, width\_min, bridge, surface\_quality, pedestrian\_lane, cross\_slope\_max, ada\_compliance, date\_built, check\_date, road\_speed |
| footpath | Tier 1 | edge\_id, edge\_type |  |
|  | Tier 2 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, incline | street\_name, status, ada\_compliance, issue, road\_speed, detectable\_warning |
|  | Tier 3 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, status, incline, cross\_slope, issue, detectable\_warning | road\_associated, street\_name, width\_min, bridge, surface\_quality, cross\_slope\_max, ada\_compliance, date\_built, check\_date, road\_speed |
|  | Tier 4 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, status, incline, cross\_slope, issue, detectable\_warning | road\_associated, street\_name, width\_min, bridge, surface\_quality, cross\_slope\_max, ada\_compliance, date\_built, check\_date, road\_speed |
| crossing | Tier 1 | edge\_id, edge\_type |  |
|  | Tier 2 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, incline, visual\_markings | street\_name, status, ada\_compliance, issue, road\_speed, rail, detectable\_warning |
|  | Tier 3 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, status, incline, cross\_slope, issue, rail, visual\_markings, detectable\_warning, ped\_traffic\_control | road\_associated, street\_name, width\_min, bridge, surface\_quality, cross\_slope\_max, ada\_compliance, date\_built, check\_date, traffic\_calming, road\_speed, vehicle\_traffic\_control , cross\_vehicle\_traffic\_control , ped\_protection |
|  | Tier 4 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, status, incline, cross\_slope, issue, rail, visual\_markings, detectable\_warning, ped\_traffic\_control | road\_associated, street\_name, width\_min, bridge, surface\_conditionquality, cross\_slope\_max, ada\_compliance, date\_built, check\_date, traffic\_calming, road\_speed, vehicle\_traffic\_control , cross\_vehicle\_traffic\_control , ped\_protection |
| raisedtraffic\_island | Tier 1 | edge\_id, edge\_type |  |
|  | Tier 2 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, incline | street\_name, status, ada\_compliance, issue, road\_speed, detectable\_warning |
|  | Tier 3 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, status, incline, cross\_slope, issue, detectable\_warning | street\_name, width\_min, bridge, surface\_quality, cross\_slope\_max, ada\_compliance, date\_built, check\_date, road\_speed |
|  | Tier 4 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, status, incline, cross\_slope, issue, detectable\_warning | street\_name, width\_min, bridge, surface\_quality, cross\_slope\_max, ada\_compliance, date\_built, check\_date, road\_speed |
| steps | Tier 1 | edge\_id, edge\_type |  |
|  | Tier 2 | edge\_id, edge\_type, from\_node, to\_node, surface\_material | status, ada\_compliance, issue, step\_count, handrail, bike\_runnelwheel\_channel, detectable\_warning |
|  | Tier 3 | edge\_id, edge\_type, from\_node, to\_node, surface\_material, status, issue, step\_count, handrail, wheel\_channel, detectable\_warning | surface\_quality, ada\_compliance |
|  | Tier 4 | edge\_id, edge\_type, from\_node, to\_node, surface\_material, status, issue, step\_count, handrail, wheel\_channel, detectable\_warning | surface\_quality, ada\_compliance |
| escalator | Tier 1 | edge\_id, edge\_type |  |
|  | Tier 2 | edge\_id, edge\_type, from\_node, to\_node, surface\_material | status, ada\_compliance, issue, detectable\_warning |
|  | Tier 3 | edge\_id, edge\_type, from\_node, to\_node, surface\_material, status, issue, detectable\_warning | surface\_quality, ada\_compliance |
|  | Tier 4 | edge\_id, edge\_type, from\_node, to\_node, surface\_material, status, issue, detectable\_warning | surface\_quality, ada\_compliance |
| bikeway | Tier 1 | edge\_id, road\_associated, edge\_type, bikeway\_type | separation\_elements, separation\_permeable\_car |
|  | Tier 2 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, width, bikeway\_type, separation\_elements, separation\_permeable\_car, surface\_material, incline | street\_name, facility\_name, bikeway\_grade\_separation, street\_parking\_buffer, bridge, status, issue, road\_speed, detectable\_warning |
|  | Tier 3 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, width, width\_min, bikeway\_type, bikeway\_grade\_separation, separation\_elements, separation\_permeable\_car, bridge, surface\_material, status, incline, issue, detectable\_warning | street\_name, facility\_name, buffer\_width, street\_parking, street\_parking\_buffer, surface\_quality, seasonal, date\_built, check\_date, road\_speed |
|  | Tier 4 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, width, width\_min, bikeway\_type, bikeway\_grade\_separation, separation\_elements, separation\_permeable\_car, bridge, surface\_material, status, incline, issue, detectable\_warning | street\_name, facility\_name, buffer\_width, street\_parking, street\_parking\_buffer, surface\_quality, seasonal, date\_built, check\_date, road\_speed |
| mutli\_use\_path | Tier 1 | edge\_id, road\_associated, edge\_type | separation\_elements, separation\_permeable\_car, ada\_compliance |
|  | Tier 2 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, width, separation\_elements, separation\_permeable\_car, surface\_material, incline, ada\_compliance | street\_name, facility\_name, street\_parking\_buffer, bridge, mup\_modal\_delineation, status, cross\_slope, issue, road\_speed, detectable\_warning |
|  | Tier 3 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, width, width\_min, separation\_elements, separation\_permeable\_car, bridge, surface\_material, status, incline, cross\_slope, ada\_compliance, issue, detectable\_warning | street\_name, facility\_name, buffer\_width, street\_parking, street\_parking\_buffer, mup\_modal\_delineation, surface\_quality, seasonal, cross\_slope\_max, date\_built, check\_date, road\_speed |
|  | Tier 4 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, width, width\_min, separation\_elements, separation\_permeable\_car, bridge, surface\_material, status, incline, cross\_slope, cross\_slope\_max, ada\_compliance, issue, detectable\_warning | street\_name, facility\_name, buffer\_width, street\_parking, street\_parking\_buffer, mup\_modal\_delineation, surface\_quality, seasonal, date\_built, check\_date, road\_speed |
| trail | Tier 1 | edge\_id, road\_associated, edge\_type |  |
|  | Tier 2 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, surface\_material, incline | street\_name, facility\_name, bridge, status, ada\_compliance, issue, road\_speed |
|  | Tier 3 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, bridge, surface\_material, status, incline, issue | street\_name, facility\_name, width\_min, surface\_quality, cross\_slope\_max, ada\_compliance, date\_built, check\_date, road\_speed, official |
|  | Tier 4 | edge\_id, road\_associated, edge\_type, from\_node, to\_node, bridge, surface\_material, status, incline, issue | street\_name, facility\_name, width\_min, surface\_quality, cross\_slope\_max, ada\_compliance, date\_built, check\_date, road\_speed, official |
| virtual\_link | Tier 1 | edge\_id, road\_associated, edge\_type |  |
|  | Tier 2 | edge\_id, road\_associated, edge\_type, from\_node, to\_node |  |
|  | Tier 3 | edge\_id, road\_associated, edge\_type, from\_node, to\_node |  |
|  | Tier 4 | edge\_id, road\_associated, edge\_type, from\_node, to\_node |  |
| ramp | Tier 2 | edge\_id, edge\_type, from\_node, to\_node, surface\_material | status, ada\_compliance |
|  | Tier 3 | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, status, incline | width\_min, surface\_issue, cross\_slope, cross\_slope\_max, ada\_compliance, impediment, handrail |
|  | Tier 4  | edge\_id, edge\_type, from\_node, to\_node, width, surface\_material, surface\_issue, status, incline, impediment, handrail | width\_min, cross\_slope, cross\_slope\_max, ada\_compliance |

#### 

#### 3.3.2 Edge Fields

Moved here:  
[https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=2090301280\#gid=2090301280](https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=2090301280#gid=2090301280) 

### 3.4 Points

#### 3.4.0 Point Types

This table lists all of the allowed point types in the specification.

Moved here: [https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=1180188504\#gid=1180188504](https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=1180188504#gid=1180188504) 

#### 3.4.1 Recommended and Required Fields for Points

This table gives an overview of the recommended and required fields for points based on the type of point. At higher tiers, more fields are added. For a full list of optional and forbidden fields see the [field spreadsheet](https://docs.google.com/spreadsheets/u/0/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit).

| Point Type | Tier | Required | Recommended |
| :---- | :---- | :---- | :---- |
| object | Tier 1 | point\_id, type |  |
|  | Tier 2 | point\_id, type |  |
|  | Tier 3 | point\_id, type | object\_type |
|  | Tier 4 | point\_id, type | object\_type |

#### 3.4.2 Point Fields

The following table lists all the point fields.

Moved to: [https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=970755666\#gid=970755666](https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=970755666#gid=970755666) 

### 3.4 Zones

#### 3.4.0 Zone Types

Moved here:  [https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=692767688\#gid=692767688](https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=692767688#gid=692767688) 

#### 3.4.1 Recommended and Required Fields for Zones

This table gives an overview of the recommended and required fields for zones based on the type of zone. At higher tiers, more fields are added. For a full list of optional and forbidden fields see the [field spreadsheet](https://docs.google.com/spreadsheets/u/0/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit).

| Zone Type | Tier | Required | Recommended |
| :---- | :---- | :---- | :---- |
| pedestrian | Tier 1 | zone\_id, type |  |
|  | Tier 2 | zone\_id, type |  |
|  | Tier 3 | zone\_id, type | surface\_material, facility\_name |
|  | Tier 4 | zone\_id, type | surface\_material, facility\_name |

#### 3.4.2 Zone Fields

The following table lists all the zone fields.

## Moved here:

[https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=175584085\#gid=175584085](https://docs.google.com/spreadsheets/d/1qs0x58V-Gcikm70AKxsXxKH7D4TL6z8FlBgf4P4kqJQ/edit?gid=175584085#gid=175584085) 

## 5.0 Changes From Prior Versions

*\[Because this is V 1.X, this section is a placeholder.\]*

### 5.1 Known Limitations and Work Currently In Development

*\[Because this is V 1.X, this section is a placeholder. Please see the Appendix for information on some potential attributes that may be added, and for a couple proposals for how to approach some of the more challenging topics in the specification.\]* 

## 6.0 Governance  {#6.0-governance}

This specification is managed by \[ORGANIZATION\] through community consultation. Please visit \[LINK\] to review the overarching governance process for the specification. 

**6.1 Localization**

This specification is deliberately designed to be extensible by anyone “locally” (i.e. on their own machine or within their own computing environment) with minimal to no effort. Allowing local flexibility is a deliberate decision to allow practitioners the ability to customize their own data workflow. We want this specification to be an enabler, not a roadblock to getting work done.

Anyone can add any attribute they want to a dataset. This specification’s validator will warn, but not fail on, new or unknown fields, assuming they do not conflict with named attributes that are already defined as part of the specification.

**6.2 Process for Changes**

This specification will continue to grow and evolve as data practices and our infrastructure evolve. It was launched by a multi-sector collaboration, and it is governed in deep consultation with the community of data producers and consumers who rely on it.

**6.2.1 Requesting a Change**

We intend to monitor the ways in which others extend the specification and pull best practices to inform future versions. **Please share your thoughts, limitations you’ve found and workarounds.** You can share them at \[LINK\].

Here are some helpful things to include in your feedback or change request:

* A description of your real world use case  
* A demonstration or description of the problem with the current specification  
* A description of the specific change you want to see   
* Your contact information

**6.2.2 Modifying the Specification**

Consistent with the guiding principles that inform our work, there is a process to modify the specification. A description of this process and who is involved in decision-making is maintained at \[LINK\].

The specifications are meant to be relatively easy to use for a range of stakeholders throughout the process from data collection to pipeline implementation to analysis and applications. Adding a new attribute raises the bar for specification users and requires updates.

When considering changes, demonstrated, real-world use will be considered as well as alignment with the [Guiding Principles](https://github.com/dotbts/BPA/wiki/Guiding-Principles).

## 

## 9.0 Related Specifications, References and Other Resources

**9.1 Related Specifications**

The following specifications have a relationship with bicycle, pedestrian, and accessibility infrastructure. This specification is designed to be easily interoperable with them, wherever possible.

| Specification | Description | Interoperability |
| :---- | :---- | :---- |
| [General Modeling Network Specification (GMNS)](http://zephyr-data-specs.github.io/GMNS/) | GMNS is an extensible specification aimed at describing the entire transportation space, including physical elements, traffic controls and time varying policy elements. It includes representations of the physical transportation space (e.g., links, lanes, intersections, sidewalks, points of interest along a link), traffic controls (including signals) and time-varying policy elements (e.g., part-time lanes, restrictions on link or lane usage). | Bicycle and pedestrian facilities may either be modeled as attributes of a road link or as their own links. Nodes and edges within this specification can be integrated and joined with GMNS data in many cases. |
| [Indoor Mapping Data Format (IMDF)](http://register.apple.com/resources/imdf/) | IMDF is primarily used to create accurate, geo-referenced digital maps of indoor spaces. It is often adopted for use in buildings like airports, malls, stadiums, arenas, and other complex indoor environments. | There are no explicit ties between IMDF and this specification, but IMDF could easily be used to continue to route through an indoor space. This specification can end a route at a transit stop (including station entrances and exits) or in front of other building types. |
| [OpenSidewalks](https://tcat.cs.washington.edu/opensidewalks/) | The OpenSidewalks schema is used to create an internationally distributed pedestrian/bike transport graph layer, including infrastructure data for accessibility, safety, and pedestrian preferences. It includes extended attributes for advanced accessibility and route planning features. It builds on OpenStreetMap's tagging schema and community mapper model. | Interoperability with this specification is high, and many of the same data structures are shared. |
| [OpenStreetMap (OSM)](http://openstreetmap.org/about) | OSM is a global, crowd-sourced database that includes data oninfrastructure across transportation and within other domains. OSM covers bicycle, pedestrian, and accessibility aspects in depth. | OSM and this specification have many shared data structures, and data is highly interoperable. See the [OSM US Pedestrian Working Group’s schema](https://wiki.openstreetmap.org/wiki/Foundation/Local_Chapters/United_States/Pedestrian_Working_Group/Schema) to learn more about pedestrian features. |
| [Overture Maps](http://overturemaps.org) | Overture is creating global, interoperable, open spatial data that covers many aspects of the transportation system.  | Overture data draws from OSM and uses many of their data structures, as well as layering on its own. |
| [Curb Data Specification (CDS)](https://www.openmobilityfoundation.org/about-cds/) | CDS expresses “dynamic curb zones” to improve parking, especially for delivery vehicles and passenger loading. It includes both defining on and off street parking/stopping/travel facilities (for any type of vehicle, bike, bus, robot, etc), and tracking events and usage metrics at these locations. | CDS and this specification have some connections at the curb space and objects in the right of way. CDS is a good source for real-time policy rules and occupancy data related to curb management, and tracking activity and usage. |
| [General Bike Feed Specification (GBFS)](https://gbfs.org/) | GBFS represents the availability of docked and free-floating bikeshare, scootershare, and carshare. It connects data from bikeshare systems to consumer journey planning apps.  | This specification maps out public bicycle facilities. With a little effort, features such as bikeshare stations and parking can be integrated into a routable network created using this specification. |
| [General Transit Feed Specification (GTFS)](https://gtfs.org/)  (plus extensions including \-RT, \-Pathways, \-Flex, \-Fares) | GTFS relays data from public transit agencies globally to provide public transportation information including stations, stops, routes and arrival information. GTFS-Pathways data is available for a subset of those agencies and describes the layout and accessibility of transit stations. | This specification includes GTFS agency\_ids and stop\_ids that can be used to pull in transit data from any available GTFS feed. |
| [National Bicycle Network (NBN)](https://data.transportation.gov/stories/s/National-Bicycle-Network/88zh-3rqb/) | NBN compiles bicycle route geospatial data for the U.S., based on data released by public agencies. It is managed by the Federal Highway Administration.  | Many of the data structures in this specification align with NBN data structures.  |

# 

# 

# 

# 

# 

# 

# Appendix

The following comprises work-in-progress content that was removed from the main body of this draft document. If useful, this material will be included in future document revision or via separate resources. It is included here to preserve the work and inform reviewers of the intent to cover these topics. Reviewers are invited to provide feedback on this content. As this material is work-in-progress, reviewers may wish to limit feedback to “this is helpful content, revise and include” or “this is not helpful content, omit,” and avoid more detailed editing.

## Intersections

Representing intersections is a critical part of modeling ATI networks. Different transportation modes, speeds, volumes, and movements intersect with one another at intersections. As such, intersections often represent key connections or barriers to continuous active transportation travel. The specification helps users represent intersection infrastructure at each tier, to ensure modeled infrastructure information accurately reflects how it contributes or detracts from ATI network connectivity.

We propose two approaches to modeling intersections for walking and bicycling: describing intersections with **Edges** and describing intersections with **Relation Tables**. 

### Describing Intersections with Edges

When using the **Network Representation** for sidewalks, for example, crosswalks are digitized with their own spatial geometry (edge\_type \= ‘crossing’), and represent the path one would take to cross the roadway. If the location of curb ramps are also known, this provides significant insight into the length and exposure of the crossing, and we can spatially infer information about the nature of the roadway configuration and traffic from the roadway edge which is being crossed. This is **describing an intersection with Edges**. 

![][image10]

Describing a crossing with an edge is helpful because it provides a unique feature in the edge table which can be used to evaluate stress, delay, or other impedance measures of crossing the roadway at a defined location, and contain attributes that describe these and other characteristics of the edge (e.g., crossing\_type \= ‘continental’; width \= ‘10 feet’).

Network representation makes it easier to understand where crossings and other edge features intersect. For example, where a crossing intersects a roadway centerline, the specification ensures the user can know how many lanes of traffic, traffic speed, and traffic volume on the intersecting edge a traveler using the crossing is exposed to.

### Describing Intersections with Relation Tables

When using the **Centerline Representation** to model bicycle infrastructure, for example, there is no spatial geometry to describe the exact location or path of how someone bicycling would travel through an intersection. The intersection is represented as the convergence intersecting roadway edges. Because there are no individually modeled intersection crossing elements, the relationship between the approaching and departing edges would need to be documented in another format, such as **a Relation Table**. A relation table contains a unique row to describe the attributes of the connection between different pairs of intersection approach and departure edges.  
![][image10]

Relation tables provide a flexible framework for describing how the physical or operational aspects of intersection edges affect the feasibility, comfort, or other characteristics of active  transportation connectivity through an intersection.

The primary drawback of describing an intersection with a Relation Table is the added level of complexity associated with developing and maintaining a relation table, outside of the other geospatial datasets describing edges, nodes, or points. However, automated workflows can be used for developing these relation tables and spatially associating other data to the table, making this a more manageable task.

## How to Model Common Bicycle Features

See [2.3 Recommended Practices For Digitizing Bicycle, Pedestrian, and Accessibility Infrastructure](#2.3-recommended-practices-for-digitizing-bicycle,-pedestrian,-and-accessibility-infrastructure) for basic explanations. The following section provides more detailed descriptions of how to model certain features. Examples include both **Network Representation** and **Roadway Centerline Representation**.

### Bicycle Facilities

#### Shared-Use PathsNon-Roadway-Aligned Bike Facilities

In all cases, **NShared-use paths** (also referred to as Non-Roadway-Aligned Bicycle Facilities) require a separate geometric feature to meaningfully represent them as a Network Representation. 

#### Roadway-Aligned Directional Bike Lanes

For bike lanes (F**or** Roadway-Aligned Bicycle Facilities)**,** there may be ambiguity about whether the bike facility is best represented as a separate geometric feature (Network Representation) or if it can be represented using attributes on the roadway centerline (Centerline Representation). 

Directional, Roadway Aligned bike lanes (where bike lanes are on both sides of the street, and follow the prevailing legal direction of travel) should be described with the Centerline Representation, using attributes of the roadway to physically describe the bike lane (see [3.3 Edges](#3.3-edges)). 

#### Roadway-Aligned, Separated, Bidirectional Bicycle FacilitiesSeparated Bike Lane, Bidirectional

**Separated bike lanes, also referred to as** Roadway-Aligned, Separated, Bidirectional Bicycle Facilities**,** describe a set of bicycle facilities that can be bi-directional or one-way. A group separated bike lanes are two-way bike lane located on one side of the street, and physically separated from automobile traffic. These facilities may be described with the Centerline Representation or the Network Representation. The Network Representation approach provides more detail than the Centerline Representation approach, which is likely important for modeling the characteristics of such facilities as part of a network. However, both representations are valid and supported. Below are some considerations regarding approach:

* Is crossing the road to access the bidirectional bike lane, in order to turn right, a high-stress maneuver which presents a barrier to low-stress cycling? If so, the bike lane should be described with the Network Representation using a separate geometric figure.   
* Is the separation between the bike lane impermeable to entry and exit of people bicycling at minor intersections, entrances, or destinations? If so, the bike lane should be described with the Network Representation using a separate geometric figure.

#### Roadway-Aligned Multi-Use Pathways (‘Sidepaths’)

Sidepaths, known in some groups as Roadway-Aligned multi-use pathways, known in some jurisdictions as Sidepaths, should be described with a separate geometric feature to meaningfully represent them using the Network Representation. Sidepaths are typically separated from the roadway by a curb, a grass buffer, or some other separation which is nominally impermeable to cars. Sidepaths which are not as separated from the roadway can be described using the Centerline Representation and edge attributes**.**

## Other Features

The following ideas for attributes are listed here to allow for reactions: 

* **Curb ramp landings.** The draft does not currently include whether landings at the top and bottom of curb ramps are present, and it does not include the attributes of these landings such as width and slope.  
* **Curb ramp geometry**. Additional details on curb ramp geometry, including blended transitions and cut-outs. Many other details about the navigability of curb ramps are included.  
* **Signage**. The draft doesn’t include a means of tracking signage that conveys information about closures, permitted uses and other key information. It also does not include a way to track the accessibility of this signage for a range of users.  
* **Traffic noise.** Some local and state governments may have edge-level data about traffic noise. An appropriate federal data source could not be identified. The draft has no attribute, but this data can be blended if available.  
* **Level of stress for bicyclists and pedestrians**. In the Guiding Principles and in our conversations, we’ve veered towards describing the infrastructure and avoiding subjective or modeled data. The attributes in the draft include common features for LTS models, and this was seen as the best way the specifications could contribute to LTS analysis. Should LTS be added to the second draft, it would include a link to the specific methodology used.  
* **Transit boarding / alighting areas**. Whether a transit stop is an entrance or exit. This attribute was in a version of the draft, but the tendency of this draft is to avoid duplication with other specifications and schemas. Because this attribute is within GTFS, it was removed.  
* **Crossings split at the point where traffic direction changes**. This could be used to add more detail to the crossings, such as how many lanes are crossed in each direction, and how bike infrastructure intersects with crossings.  
* **Forbidden turns**. The draft does not currently cover places where motor vehicles are not allowed to turn right or turn left. Adding this attribute could enhance understanding of pedestrian and bicyclist safety at intersections.

 

 

 

## Signals

Signal infrastructure – such as pedestrian push buttons, pedestrian detectors and signal poles that convey auditory or tactile information about the signal and its messaging – are important for accessible travel.

We’re considering two different approaches to signals. One approach attaches information about the signals to edges. The other treats signals as nodes.

In both approaches, the location being tracked is where pedestrians must go to interact with the signal – to push a signal button, to hear and trigger auditory messages, or to access tactile information. The location of the signal head itself is not tracked.

In both approaches, the following attributes that are used above for edges and nodes would also be tracked: 

* presence  
* date\_built  
* date\_checked  
* ada\_compliance  
* ada\_compliance\_date  
* ada\_compliance\_standard

We would also add the following four attributes specific to signals:

* features: Tactile vibration, tactile arrow, auditory walk indication, pushbutton locator tone, other auditory messaging, other  
* triggering: Pedestrian actuated / push button, pedestrian auto-detected, no actuation or detection, unknown  
* crossing\_time: Measured in seconds. If crossing time is not fixed, the minimum crossing time would be listed.  
* issue: Push button not working, broken / damaged, auditory signal not working, vibrotactile signal not working, poor volume, button height issue, no visual countdown, distance from walk path, other.

**Option \#1: Signals on Edges**

Data about signals could be added as attributes to crossing edges. Because there will be signal infrastructure at two or more points on an edge, there would need to be tagging to indicate which signal location is being referenced, so that issues can be associated with the correct infrastructure and any differences from different approaches can be marked correctly.

The benefit of this approach is that it relies on existing structures with the specifications, and hopefully keeps the overall data model a little simpler. It also helps to keep it clear which signals are associated with which crossings. 

**Option \#2: Signals as Points**

Signal locations could be identified as points, showing their exact location within the intersection space. A virtual link (a type of edge described above) could be used to associate the point with the correct crossing. This virtual link would not be routable. 

A buffer could be created around signal points and then used to add nodes to the network to enable routing. Doing so would put the node for the signal on the right location on the sidewalk edge, helping pedestrians to be routed to the signal on their way to the curb ramp, regardless of the direction from which they approach.

The benefits of this approach are being able to accurately mark the location of the signal infrastructure, and enabling routing directly to the signal location. The latter can help a range of travelers with different mobility profiles, including blind and low vision travelers, to be able to more easily navigate and take advantage of signals for comfortable, safe travel.

[image1]: <data:image stripped>

[image2]: <data:image stripped>

[image3]: <data:image stripped>

[image4]: <data:image stripped>

[image5]: <data:image stripped>

[image6]: <data:image stripped>

[image7]: <data:image stripped>

[image8]: <data:image stripped>

[image9]: <data:image stripped>

[image10]: <data:image stripped>