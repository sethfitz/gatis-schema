## ![][image1]

## 

**General Active Transportation Infrastructure Specification**

**Playbook**  
**v1.0**

**September 2026**

## What is GATIS?

The General Active Transportation Infrastructure Specification, or GATIS, provides a consistent national format for data that represents the physical transportation infrastructure used by those traveling via active transportation – walking, bicycling, micromobility devices (e.g. e-scooters or skateboards), and assistive mobility devices like wheelchairs. The goal of the specification is to enable data pooling across jurisdictions and datasets. It aims to capture attributes critical for mobility profile-based routing, asset tracking and maintenance, and other use cases.

This specification was developed by the National Collaboration on Bicycle, Pedestrian and Accessibility Infrastructure Data, made up of public, private, research, and non-governmental participants and originally convened by the U.S. Department of Transportation (U.S. DOT)’s Bureau of Transportation Statistics (BTS). The specification was created through a collaborative, consensus-based process and is maintained by \<ORGANIZATION\> through community consultation. The specification is voluntary, and any agency or other user may elect to adopt it at their own discretion.

### Statutory basis

BTS maintains the National Transportation Atlas Database (NTAD) as required in Statute under [Title 49 U.S.C. § 6309](https://uscode.house.gov/view.xhtml?req=granuleid:USC-prelim-title49-section6309&num=0&edition=prelim). The NTAD comprises a collection of national geospatial datasets of modal and intermodal transportation facilities and networks; flows of people, goods, vehicles, and crafts over the transportation networks across all modes; and social, economic, and environmental conditions that affect or are affected by the transportation networks. 

To date, the NTAD has lacked robust datasets of transportation facilities and networks for people traveling by active transportation. BTS convened the national collaboration due to its desire to establish a common format for active transportation infrastructure data that could facilitate the broader production and use of those data by a range of public, private, and non-governmental entities.

### The value of standardization

GATIS offers significant advantages for data producers and consumers by establishing a unified digital framework for active transportation data. By standardizing how we represent infrastructure like sidewalks, bike lanes, and curb ramps, organizations can move beyond fragmented datasets toward a cohesive national data ecosystem, and more easily pool data across jurisdictions for routing, safety analyses, and more.

#### Better quality and reliability

Standardization ensures that data definitions are consistent, significantly reducing the subjectivity that often plagues disparate datasets. Because GATIS uses specific, objective attributes, the resulting data is inherently more interpretable and precise. For example, GATIS uses numerical values for slope rather than subjective labels like "accessible" making it more adaptable to end users’ local quantitative thresholds to determine “accessibility” for a given use case. Furthermore, the GATIS Tier Model serves as a vital benchmark, allowing users to verify the technical capability and applicability of a dataset based on its level of precision and attribute completeness. 

#### More efficient and cost-effective

Implementing a common specification leads to faster integration with existing workflows, as technical teams no longer need to design unique data schemas for every project. This predictability saves time and money by minimizing the labor-intensive data cleaning and manipulation typically required to merge different datasets. Additionally, because the format is standardized, it becomes much easier to train staff and document processes, ensuring that institutional knowledge is preserved even as personnel change.

#### Greater power/capability and capacity

A standardized format unlocks deeper data usefulness, enabling sophisticated analysis and insights that are difficult to achieve with "siloed" data. GATIS facilitates easier data sharing within internal departments and across external agencies – supporting connected network data across municipal and state borders. For public agencies, this also makes it easier to procure data from commercial vendors or provide data to external partners, as everyone is operating on the same technical foundation. GATIS enables easier interoperability between active transportation infrastructure and other datasets, like motor vehicle, crash, public health, land use, and census data.

#### Support forward progress

GATIS provides a scalable framework that can grow alongside an organization’s needs and capabilities, moving from limited asset inventories to complete, routable networks. By establishing these clear national guidelines, the specification facilitates robust documentation and training. This collective approach ensures that the active transportation field continues to advance, creating a virtuous cycle of improved planning, analysis, research, and management that supports expanded active transportation facility design, project delivery, asset maintenance, and enhanced safety for travelers with a range of needs and using a range of modes.

## Who uses GATIS?

### Audience

The audience for this document includes anyone seeking to use this specification to leverage active transportation infrastructure data and/or improve its quality and usefulness. Anticipated users include both data producers and data consumers, such as:

* **Public Agencies**  
  * U.S. DOT and other federal agencies  
  * State and local Departments of Transportation (DOTs)  
  * State and local Departments of Public Works (DPWs)  
  * State and local Departments of Planning and Community Development  
  * State Departments of Health  
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

## Use Cases

GATIS enables agencies to organize their active transportation infrastructure data in a common, standard format. Once data is standardized, it can support many different use cases for a wide range of stakeholders. The extent to which these use cases can be realized depends on the completeness, quality, and maintenance of the underlying data. While this Playbook focuses on two example use cases, routing for travelers and asset management for agencies, GATIS can support many other applications, depending on an agency’s specific needs, priorities, and capabilities. 

The GATIS specification is designed to serve two primary use case categories: Routing and Asset Management. While these categories represent core functionality, the specification is designed to evolve and support additional sub-applications through novel use and future revisions.

### Routing Use Cases

Routing involves linking different network components—such as edges and nodes representing roads, sidewalks, and paths—so that users can calculate or “model” pathways through the network based on specific rules.

* **Profile-Based Routing:** GATIS helps users model routes for specific traveler needs or “profiles” that tell a routing engine which pathways to include, ensuring each connected edge and node meets the minimum criteria for that profile. Here are examples demonstrating how user profiles shape which network segments a routing engine includes or prioritizes when modeling a route:

  * **Kid-friendly bicycle routes:** A Safe Routes to School planner might want to identify routes that are conducive to children bicycling to school. GATIS could help identify roads with separated bicycle lanes that buffer cyclists from traffic, roads with low traffic volumes and vehicle speeds, off-street paths, protected intersections, and road crossings with cross-bike treatments and rectangular rapid flashing beacons or traffic signals.

  * **Accessible routes for a person with a physical disability:** An accessibility coordinator might seek to find routes for someone using a wheelchair. GATIS could help identify sidewalks and crosswalks with adequate clear width, slope and cross-slope, curb ramps, and pedestrian signal push buttons.

  * **Navigation for a person with specific mobility preferences:** A caregiver seeking directions to a playground in a new city might want to know what route to take while pushing a child in a stroller. GATIS could help identify the most direct route that only includes sidewalks and avoids steep hills.

* **Gap Analysis:** GATIS can also show where sections of a network are incompatible with a specific profile or infrastructure criteria (“gaps” in the network). Gap analyses help users identify and prioritize locations for investment based on their potential to expand or connect a series of uninterrupted routes.

  * **Investment prioritization:** As part of project scoping, a program manager might want to compare how potential design options might affect pedestrian access or bicycle connectivity across a neighborhood or region. GATIS could help model different investment scenarios at a project-by-project scale to demonstrate the relative impacts of different project scoping decisions. 

  * **Programmatic investment planning:** As part of planning for programmatic safety improvements, an analyst might want to identify all the high-stress gaps that interrupt otherwise low-stress bicycling routes in a municipality. GATIS could help identify and prioritize intersections and crossings for targeted safety upgrades to help reduce risks at key connection points in the network. 

* **Interoperable Data Analyses:** Gap analysis facilitates access modeling, to show how bridging certain gaps may affect the larger network. 

  * **Land-use Access:** Applications can evaluate how well a network connects the population to regional destinations. This allows planners to study accessibility to essential services like supermarkets, pharmacies, jobs, schools, and recreation. It also supports modeling "first and last mile" connections to transit stations, and increases the value of Level of Traffic Stress (LTS) ratings by showing which parts of a network are suitable for various active transportation users and what destinations they can reach.

  * **Multimodal Access:** Integrating active transportation infrastructure into roadway network data supports multimodal modeling. This can allow analysts to model and compare travel time, cost, and other metrics across multiple modes, and develop different scenarios based on changes to active transportation infrastructure.

  * **Safety Analysis:** Many safety analyses are plagued by poor contextual data. Improved active transportation data, when integrated with crash data, EMS data, or connected vehicle probe and event data (hard braking and acceleration, headlights and windshield wiper status, near-miss events, etc.), helps researchers assess the impact of more detailed infrastructure factors on crash events and outcomes.

### Asset Management

Asset management focuses on the characteristics of infrastructure elements themselves,either individually or in aggregate. GATIS supports asset management by providing data critical for maintenance, long-term planning, reporting, and evaluation.

* **Asset Inventory and Programmatic Assessments:** GATIS is designed to capture detailed attributes for assets, including their precise location, dimensions, operational characteristics, and current physical condition. This supports creating consistent multi-jurisdictional asset data and large-scale programmatic evaluations.

  * **Performance Management:** Simply reporting an accurate inventory of active transportation facilities can be challenging. Using a GATIS-formatted dataset, a complete streets section manager might produce quarterly reports on bicycle and pedestrian facilities by type, such as the ratio of painted, buffered, or fully separated bicycle lane miles to non-limited access road miles by direction, to demonstrate progress toward a municipal goal.

  * **Multi-jurisdictional Inventories:** Many multiuse trails cross municipal, county, or state boundaries and may lie within easements owned or maintained by transit, rail, or utility agencies. To maintain consistent information across such boundaries, a state or regional asset manager might aggregate available data from agencies, convert it to GATIS format, and contract with a vendor to validate, correct, and fill-in missing data to create a consistent trails asset inventory with precise dimensions, material type and condition, and wayside sign location and content information.

  * **ADA Transition Planning:** An ADA transition plan coordinator might run an annual report of crosswalk attributes and inventory dates, including their physical characteristics (slope, cross-slope, landing area dimensions, alignment with crosswalks) and the presence of signals and push-buttons, to measure ADA transition program progress and identify locations for reassessment.

  * **Systemic Safety Engineering:** A traffic engineer might analyze the spatial relationship between uncontrolled crosswalks and street lights, to pinpoint specific segments of the network for field assessment of adequate lighting for safe nighttime use.

* **Budgeting and Maintenance Prioritization:** Data on the surface quality of shared-use paths or the visibility of bike lane markings helps agencies develop budget estimates and prioritize maintenance tasks.

  * **Multi-year Budget Development:** A budget analyst might aggregate maintenance cost estimates based on GATIS-defined asset dimensions, surface material types, and historical bid data, to develop accurate multi-year budget requests for remarking pedestrian and bicycle roadway markings.

  * **Clustering Maintenance Tasks:** A maintenance supervisor might utilize GATIS sidewalk point data attributes (e.g., "cracking," "root damage") to cluster maintenance requests geographically, allowing crews to bundle repairs for multiple adjacent infrastructure segments in a single work order. 

  * **Separated Infrastructure Maintenance Scheduling:** An asset manager might produce a report of locations with separated bike lanes and multiuse paths to prioritize small-format street sweeping and plowing.

## The Structure of GATIS

### Overview

The [GATIS Explorer](https://dotbts.github.io/BPA/index.html) is the website where you can see and explore the specification. Should any questions arise, the version of the specification available through the GATIS Explorer is the authoritative version.

GATIS data is organized into what is referred to as a network graph – a set of geospatial lines and points that represent the paths travelers can follow. Many data producers already have network graphs for motor vehicles, with the line in the middle of the road space, or centerline, represented in their data with a geospatial line. Early in producing pedestrian data, GATIS data producers can attach data about sidewalks and other pedestrian infrastructure to roadway centerlines using attributes. But as pedestrian data collection advances, centerlines for sidewalks and crossings should be created instead, and data about pedestrian networks should shift over to these centerlines. Throughout GATIS, the bicycle network can be a mix of roadway centerlines and bicycle facility centerlines, since cyclists often ride on the roadway space with minimal or no separation. 

Several of the technical sections in this playbook provide further guidance, including the sections on Centerlines, Routing and Bike Networks. See Section 2.0 of the specification for further information on the files that make up GATIS data, the data types used, and what attributes are recommended or required at different tiers.

### Tier Model

Some data creators might be preparing active transportation datasets from scratch while others will be working with existing datasets that may (or may not) easily translate to this specification. The Tier Model aims to meet data creators where they are by providing a minimum set of requirements to enable common use cases and a suggested roadmap for increasing the completeness, routability, timeliness, precision, and other aspects of the data creators’ existing bicycle and pedestrian data over time. The model also provides guidance on best practices for those creating new datasets recognizing that organizational processes such as data governance is part of any successful data program.

There are four tiers numbered from 1 to 4 in order of increasing detail and completeness. There is no certification schema or recognition for achieving a particular tier. Rather, the model is meant to be self-guided. 

Tiers are intended to be “mix and match” across different modes: pedestrian data can be at one level, bike another for example. Similarly, an organization may be at the Tier 2 level when it comes to spatial precision, for example, but at Tier 4 when it comes to completeness of the attributes. This system was inspired in part by the [OSM US Pedestrian Working Group’s schema](https://wiki.openstreetmap.org/wiki/Foundation/Local_Chapters/United_States/Pedestrian_Working_Group/Schema).

As more use cases emerge and further user needs are uncovered, the tier system will be revised to provide further guidance to data creators and consumers. 

The creators of this specification recognize that readers may have further questions about the tier model and may desire further detail on specific questions or their own datasets or conventions, how to validate a tier level, etc.; we welcome these questions so that we can further develop this guidance in response to real user needs, and commit to further refining this concept and the specification as a whole as further user needs are uncovered.

#### Key Tier Dimensions:

##### Features

The tier model outlines what types of pedestrian, bicyclist and accessibility features are required or recommended at each level. For instance, a ramp edge is optional  at Tier 1, but required at Tier 3 and beyond. 

##### Routability

The tier model defines whether the data is routable and how. At tier 1, data is most likely not routable, but becomes routable with defined topology at tier 3, for example. 

##### Attribute completeness

The tier model outlines how complete any given features’ attributes are. At lower tiers, there will be gaps in attribute values, while moving towards tier 4 attributes will become more rich and complete. 

##### Geospatial precision

The tier model defines how accurate the geographic location (or precision) of the active transportation infrastructure data is, increasing in accuracy as one moves up through the tier levels. 

Table 1: Tier Model Summary

|  | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
| :---- | :---- | :---- | :---- | :---- |
| Features | Sidewalk/ crosswalk centerlines or road centerlines; curb ramps (as nodes); bikeways; multi-use paths | Sidewalk/ crosswalk centerlines; curb ramps; bikeways; multi-use paths; trails | Sidewalk ramps and landing zones as edges, traffic islands, steps, elevators, pedestrian zones, transit stops | \+ issue points |
| Routability  | May be routable | Routable with some user pre-processing | Routable at least via spatial topology | Routable via graph metadata (at minimum) |
| Attributes | Small defined set; Likely to have gaps | Larger attribute set; Complete or mostly complete across most attributes | Mostly complete, with more attributes | Very complete, with a rich set of attributes |
| Geospatial Precision | Lower  | Medium | Higher | Highest |

Throughout the remainder of this document, the tier model will be referenced whenever there is a spectrum of how a data creator can (or should) create data for the specification. 

In summary, at lower tiers:

* Data collection processes are focused on creating a complete inventory of assets that is exhaustive, but without a complete set of the attributes of each asset

* Data in the specification format is likely being used in conjunction with existing processes for use cases like project prioritization, but data is not likely routable or is routable within small “islands”

* Geometry for active transportation infrastructure may be connected to the road, rather than being reflective of the real geometry of, for example, a sidewalk that runs alongside a road

* Attribute values may not capture the complete variability in the field. For example, width may vary along the edge segment in the real world, while the data shows constant values.

* Data is focused on one primary infrastructure type: e.g. bike paths *or* sidewalks.

* Linking to other data sets is possible, but only spatially and inferentially. There are no shared identifiers that exist across datasets.

* Data may only be partly vetted by the infrastructure owner, or only vetted by third parties.

* Data is only a snapshot of any system of record. The data may be months old or more.

At higher tiers:

* Data collection processes are focused on completeness of attributes for each asset. 

* Data collectors likely received training and are using quality assurance and quality control processes that ensure minimal variance and maximum consistency across collectors. Collection technology may be highly accurate – for example, using LIDAR.

* Data is contained within a single-source-of-truth database across the organization, and established organizational processes mandate the use of this single source of truth across analysis, reporting, and other use cases, as well as derivative products.

* Data is routable via spatial attributes, metadata, and by attributes that convey the needs of travelers with a range of mobility profiles. 

* Geometries of active transportation infrastructure are accurate, especially when they vary from the roadway. For example, a sidewalk adjacent to a road that deviates from the road to go around an obstruction is reflected in the data with distinct geometry. 

* Edges are segmented when attribute values (such as width) change significantly. 

* Complete, preference-based attributes on accessibility and the features of bicycle and pedestrian spaces are present in the data to enable modeling and routing based on traveler profiles. 

* Alternative networks are provided for routing applications to optionally switch between. For example, bicycles can be routed between bike facilities, streets, multi-use paths, and other appropriate spaces. 

* Linking to other datasets is enabled via identifiers stored within the data.

* Data is fully vetted by the infrastructure owner.

* APIs or other facilities exist to make edit suggestions to data when users discover errors.

* Data is very recent, and pulled directly from a system of record.

### Data Management

GATIS data uses a feed format, where data producers periodically push new files to their feeds that contain their most up-to-date data. At this time, GATIS does not require a specific frequency of updates. Data producers may want to consider re-collecting or refreshing their data regularly (for example, yearly). They may also decide whether they want to push updates to their feed with minor data corrections or hold those corrections for a regular update (for example, quarterly). The tier model may incorporate the freshness of data at higher tiers in a future version.

There are several tools on the [GATIS Explorer](https://dotbts.github.io/BPA/index.html) to make it easier to create, manage and share GATIS data:

- The schema is available in GeoJSON/JSON, as well as in geodatabase format for easy use in ArcGIS.  
- Sample datasets appear on the GATIS Explorer that can help data producers answer questions about how to structure their data.  
- The GATIS Validator (prototype) can scan a dataset for compliance with the specification and flag any issues for correction.

### Using the Specification in Different Environments

#### For Publishing

The primary use of GATIS at this time is as a publishing specification – meaning that data producers may be using different specifications in-house to collect and manage their data, and convert their data into GATIS format in order to share it out in a format that can be readily ingested and merged with other GATIS datasets. Data producers may also choose to use GATIS as their in-house specification, but doing so is not a requirement.

#### For Coordinating among Agencies

GATIS can be used as a shared specification where government agencies or other organizations need to combine data across jurisdictional lines, or where state departments of transportation or metropolitan planning organizations are compiling data from local jurisdictions. The individual agencies could use GATIS or another specification as their in-house specification.

#### Working with a Contractor

Many contractors or vendors who help to collect data will also propose a schema for the data, adding cost and effort to the proposal. GATIS can be freely given out to contractors to ensure data comes back in a compatible format, and to reduce costs and streamline communication about what data to include. Because GATIS tiers specify what data should be included, selecting a specific tier for collections can help to ensure that the final data is useful for particular use cases such as safety analysis or granular routing applications. It’s preferable but not required to have the final data also be published in the GATIS format. 

# Specific Topics

## Additional Attributes Not in GATIS

GATIS aims to be comprehensive, but it does not cover every imaginable attribute. It also does not perfectly align with every local use case or need. Data producers may add any additional attributes that they desire to a GATIS dataset. 

The GATIS validator will not fail if it sees new or unknown attributes, so long as those attributes are named differently than the attributes that are already in GATIS. It will also not fail on unknown geospatial feature types. For example, an edge of a type not included in GATIS may be included in a GATIS edge file without that file failing the validator.

Attributes that are not in GATIS but appear in many GATIS datasets may be identified for inclusion in future updates to the specification. GATIS users are also encouraged to submit proposals of additions or modifications to the specification that would make it easier or more beneficial for them to use.

## Allowed and Prohibited Uses

GATIS has two attributes to convey who may travel on a piece of infrastructure: allowed\_uses and prohibited\_uses. Both are optional attributes on edges and zones. 

The prohibited\_uses attribute captures when a specific mode of travel is explicitly not allowed – for example, a trail might prohibit ebikes or certain classes of ebikes. 

The allowed\_uses attribute is not meant to be a list of every allowed use; rather, it is meant to capture allowed uses that are exceptions or might not be expected. GATIS avoids requiring every jurisdiction to provide a list of bikes, ebike classes and micromobility types that are allowed on every bike lane, or to indicate on every sidewalk edge that pedestrians may use the sidewalk. This information may be provided in cases where it adds clarity.

Allowed uses vary by locality. In some jurisdictions, for example, cyclists may choose to ride on sidewalks by default in all or most areas, and are asked to yield to pedestrians. In other jurisdictions cyclists may not use the sidewalk. GATIS enables jurisdictions that do allow cyclists to ride on sidewalks to add the types of bicycles and micromobility that are allowed on edges or in zones under allowed\_uses.

It is encouraged to fill out both allowed\_uses and prohibited\_uses where routing engines may need the information to successfully route all types of travelers. Routing engine developers should be aware that this data is not required and might not be filled out, and consider researching local regulations where they operate. They should also feel comfortable making common sense assumptions about the primary modes a piece of infrastructure was built for being allowed.

## Americans with Disabilities Act Data and Compliance

Within GATIS, the attributes “ada\_compliant\_with” and “ada\_compliance\_date” are recommended in tiers 2+. The attribute “ada\_compliant\_with” contains the name of the specific standard (such as PROWAG) that the infrastructure was found to be compliant with, while “ada\_compliance\_date” indicates the date that the compliance determination was made. If infrastructure is not found to be compliant, or if no information is available, these attributes remain blank. These attributes are not required, and data producers should consult with their compliance departments when determining what data to make publicly available. Because part of the intent of GATIS is to provide data that can help every traveler have a better traveling experience, GATIS’ creators hope that data producers will challenge themselves to release as much data as they possibly can, and continue progressing on ADA transition plans and infrastructure improvements.

The [Guiding Principles](https://github.com/dotbts/BPA/wiki/Guiding-Principles) for GATIS specify that “the specification describes objective qualities of infrastructure.” Many attributes in GATIS convey information that is a part of ADA assessment, such as width, incline and cross slope. Some of these attributes are required starting in tier 2\. Describing the infrastructure objectively is meant to help a range of travelers – from people with mobility devices to parents with small children to delivery robots – be served routes by routing engines that work for the way that they move. Breaking these attributes out separately helps travelers to be matched with specific routes. A person who walks with a cane, for example, may have their own specific limitations that cause them to struggle to traverse the steepest inclines allowable under the ADA. If routing engines have the specific incline available, they can help this person find flatter routes.

## Assigning IDs

In the future, each agency that submits a feed to the GATIS Registry will be assigned a GATIS publisher\_id, which appears in the Metadata JSON file. All GATIS publisher IDs will be four digits long and will not start with leading zeros.

Unique IDs for geospatial features (such as edge\_id and node\_id) should be assigned locally. They should be numeric without leading zeros, but otherwise it is up to the data producer to choose how to set numbering. If the data producer’s regular method of assigning unique IDs is numeric without leading zeros, these same IDs should be used for GATIS features.

For consumers of the data who want to combine multiple datasets, the GATIS publisher\_id for the data producer should be appended at the front of the unique ID for the geospatial feature. For example, if publisher\_id \= 1449 and edge\_id \= 12398, the ID for that feature would be 144912398\. Combining these IDs makes it possible to easily combine datasets while not conflating or confusing unique geospatial features that have the same edge\_id in the data producers’ in-house datasets.

## Associating Bicycle, Pedestrian and Accessibility Features with the Roadway

Within the Edges GeoJSON file, there are two fields used to associate bike and pedestrian infrastructure with a particular street for motor vehicles. One is street\_name, which is required in higher tiers for sidewalks and crossings so that routing engines can provide the information to users. The other is reference\_ids, which is optional and can be used to list out cross references to any other dataset that contains the same feature. Within the reference\_ids field, roadway networks such as Census Roads, ARNOLD and Overture can easily be linked. The Nodes, Points and Zones GeoJSON files do not contain the street\_name field, but they do contain the reference\_ids field.

Another option for associating GATIS features with specific roadways is to use the LRS extension, described in another section called “LRS Crosswalking.”

It’s recommended that bikeways that are on the roadway space and do not have any separation from the roadway other than paint be mapped on a roadway edge using left, right and both tags. See the sections on “Bike Networks” and “Left, Right and Both Tags” for more information.

A geospatial feature that is not associated with a roadway would not have a reference\_id to a roads dataset. It also would not have a bikeway left, right or both tag on a roadway edge. It might have an LRS reference in an LRS extension to mark entry and exit points or intersections, such as the entry to a multi-use path that diverges from the roadway but can be accessed from it. Data consumers may want to use geospatial visualization, buffering or some other algorithm to confirm that geospatial features are not near roadways, as there is not a perfect guarantee within GATIS data that a geospatial feature missing all of these markers is not roadway associated.

It is up to the data producer to decide whether to indicate a particular geospatial feature as being associated with a roadway. GATIS does not currently set a particular threshold or particular rules for making this determination. Generally, however, it recommends at higher tiers to fill out reference\_ids and street\_name where there is an association, as doing so enables safety analysis, routing, asset management and other use cases.

## Bike Networks

### Bike Facility Types

The facility types that are recommended in GATIS come from NACTO’s [Urban Bikeway Design Guide](https://nacto.org/publication/urban-bikeway-design-guide), AASHTO’s [Guide for the Development of Bicycle Facilities](https://www.fhwa.dot.gov/environment/bicycle_pedestrian/publications/), and FHWA Office of Safety’s [Bicycle Facility Types](https://www.fhwa.dot.gov/environment/bicycle_pedestrian/funding/before_after/bikeway.cfm), which are used by the [National Bikeway Network](https://data.transportation.gov/stories/s/National-Bicycle-Network/88zh-3rqb/). There are a couple types that do not appear in the suggested values for the bikeway\_type edge attribute in GATIS. One is multi-use path, which maps instead to the GATIS multi\_use\_path edge type that contains attributes relevant to other types of travelers. The other is a two-way separated bike lane, which is mapped in GATIS as bikeway\_type=”Separated Bike Lane,” plus directionality=”both.” This format is easier for routing engines to parse. The bikeway\_type attribute is a text attribute with recommended values, and GATIS users may add other values at their discretion.

### On-Road and Off-Road Feature Mapping

When a bikeway is on the road space and does not have physical separation, GATIS recommends mapping it on the road edge and attaching it to the roadway centerline, rather than creating a separate bikeway centerline. This choice helps to communicate to routing engines and travelers that the bikeway is unprotected and that cyclists in this space can likely expect to engage more frequently with moving vehicles. In most cases when bikeway\_type equals “Shared Lane” or “Paved Shoulder,” it should be placed on roadway edge rather than a bikeway edge. When bikeway\_type equals “Bike Lane” and the only separator between the cycling space and motor vehicles is paint, it should typically be placed on a roadway edge rather than a bikeway edge. 

While many jurisdictions have legal restrictions that prevent motor vehicles from entering bicycle facilities, the focus of GATIS is on mapping physical infrastructure. Decisions about how to map a facility should be made based on the physical infrastructure that is present.

The GATIS validator does not enforce any specific rules about when separate centerlines are used for bike facilities, and the specification recognizes that the range of ways in which bike facilities are designed creates cases where data producers must use their best judgment to convey their knowledge about local conditions.

The following questions may be helpful in deciding whether to create a separate centerline for a bike facility or to place it on a roadway centerline:

1. Is the bike facility integrated into the road? If so, place it on a roadway centerline.

   1. Is the path taken on the bike facility distinct from the path taken on the road centerline?

   2. Are cars prevented from entering or crossing into the bike facility by a physical barrier or obstacle, such as a concrete barrier or curb?

   3. Are cyclists prevented from entering or crossing into the roadway space by a physical barrier or obstacle, such as a concrete barrier or curb?

2. Are there attributes of the bike facility that would be too complicated to track on the road centerline, such as surface type changes, incline or surface condition? If so, put it on a separate centerline.

### Intersection Connectivity

The network graph structure of GATIS data requires that nodes be placed at every point where two or more edges intersect. Generic nodes should be inserted to fully connect bikeway edges and road edges that contain bicycle facilities. Where these edges don’t meet up perfectly, crossing edges can help to fill gaps. Another option is to utilize metadata routing, explained in this Playbook in the Routing section. Metadata routing relies on the from\_node and to\_node attributes to explain what geospatial features connect in the physical world. 

## Centerlines

Within geospatial data, a centerline shows where the middle line of a piece of infrastructure – such as a bike facility, sidewalk or road for motor vehicles – is located. Within GATIS, centerlines appear on both active transportation facilities and on road edges. 

In Tier 1, sidewalks may be tagged on the centerline of the adjacent road or have their own, separate centerlines, but in Tiers 2 and above, sidewalks must have their own centerlines. This enables better mapping of pedestrian infrastructure, because it is difficult to adequately map crossings and curb ramps on a roadway centerline. In Tier 1, data does not need to be fully connected and routable. In higher tiers it should be, though Tier 2 data can have some gaps and minor issues that a data user can correct.

In Tier 1, bike facilities can similarly be placed on the roadway centerline or have their own centerlines. In higher tiers, bike facilities should be placed on the roadway if there is no separation or only paint as separation from motor vehicle traffic, while bike facilities that are separated by hard barriers (like a concrete barrier) or are not next to the roadway should have their own, separate centerlines. With cases that are ambiguous, it is up to the judgment of the data creator which centerline placement is more useful. See the Bike Network section for more information.

When the road centerline is used, GATIS provides modifier attributes to describe active transportation facilities. For example, a bikeway can be described using attributes such as “bikeway:right:width” to apply the “width” attribute for edges to a bikeway on the right. See the section on “Left, Right and Both Tags” to learn more.

## Contestability and Corrections of Data

One of GATIS’ guiding principles is that “The specification includes context that is useful for travelers and for information systems,” with this sub-principle: “The specification is designed to allow for two-way data exchange so that users who identify errors may submit or suggest them for correction.” GATIS metadata, its feed structure and other aspects enable traceability of and accountability for the data. 

GATIS does not have a specific mechanism for users who identify errors to submit them for correction. Each GATIS data producer is encouraged to make a pathway for corrections available. [OpenStreetMap](https://openstreetmap.us/), [Mapillary](https://www.mapillary.com/), [AccessMap](https://tcat.cs.washington.edu/accessmap/), [ArcGIS Hub and Web AppBuilder](https://hub.arcgis.com/), and many other applications allow for posting of data with mechanisms to offer suggestions that can then be reviewed by the data producer before adoption. The Taskar Center for Accessible Technology at the University of Washington has developed the [AVIV ScoutRoute mobile application](https://tcat.cs.washington.edu/avivscoutroute/), which is currently in beta and enables travelers to submit corrections to pedestrian and accessibility data directly from the field. In the future, GATIS may provide more tools and/or recommendations to support data producers in accepting user corrections and contestations. 

## Curb Ramps

As tiers advance, GATIS recommends that data producers increase the level of detail they provide about the curb ramp and curb cut space to provide more details for travelers, asset maintenance and ADA accessibility analysis.

In tier 1, GATIS data in general does not need to be geospatially precise, and edges and nodes in the data might not fully connect. Tier 1 uses a curb\_ramp node to indicate the approximate location of the curb ramp.

In tier 2, GATIS data should be more geospatially precise, and edges and nodes in the data should be connected and mostly routable. Tier 2 uses a curb\_ramp node to indicate the ramp, but it is recommended to move that node closer to what will become the ramp\_to\_street\_transition node in higher tiers. This node marks the point where a pedestrian moves from protected pedestrian space into the roadway. Marking its location is important to safety and other analyses that consider the exact width of crossings, among other use cases. To shift the point, data producers may start to adopt the edges and nodes used to mark curb ramps in tiers 3 and 4, fill in with generic nodes and footways, and/or allow the locations of their linework to be slightly off of the actual centerline so that it can connect.

In tiers 3, GATIS data should have curb ramps mapped out in greater detail, which can be refined and expanded to all curb ramps in tier 4\. In these tiers, a curb\_ramp\_system\_id is created for each curb ramp area. This id ties together a curb ramp system made up of the following edges and nodes:

- Edges: curb\_ramp\_toplanding, which maps out the transition area from sidewalk space into curb ramp space; and curb\_ramp\_runslope, which maps out the sloped area of the ramp  
- Nodes: sidewalk\_to\_ramp\_transition, which maps out the point where a pedestrian enters the landing area at the top of a curb ramp; generic, which can be used to fill in connections between edges not otherwise connected; and ramp\_to\_street\_transition, which maps out the point where a pedestrian leaves the curb ramp and enters the street space.

The following illustration shows how these edges and nodes connect for a single ramp: 

![][image2]

There are many different configurations of curb ramp spaces. This same mapping system should also be used to map curb ramps and curb cuts on traffic islands, at larger driveways and in any other location where there is similar infrastructure. At times this may require a little creativity or problem-solving by the mapper.

## Data Feeds and Frequency

At this time, it is up to the data producer how often they want to push new GATIS files to their feeds. The GATIS tier model does not require a particular frequency of updates at any tier, recognizing that data collection can be expensive and access to resources for collection can vary. 

It is recommended that data producers in higher tiers consider more frequent collections, because data about issues, impediments and infrastructure condition in these tiers lose value when they are not current. Each data producer should have a sense of what frequency supports having good quality of information about current conditions.

## Directionality

Within geospatial data, a line or polyline (ie, a LineString) always has an order to how the various points making up the line are drawn. Consider the following line:

{

  "type": "LineString",

  "coordinates": \[

    \[-95.9325, 41.2529\],

    \[-95.9298, 41.2529\],

    \[-95.9252, 41.2529\]

  \]

}

The line originates at the point \[-95.9325, 41.2529\]; that is the point on the line that geospatial software will draw first. It ends at the point \[-95.9252, 41.2529\]. Within GATIS, the from\_node for an edge that followed this line would be the node closest to \[-95.9325, 41.2529\], and the to\_node would be the node closest to \[-95.9252, 41.2529\].

This line is a horizontal line that runs from an origin at its west end to a terminus at its east end. For the directionality attribute on edges, if we traveled eastward on this line, we would be moving “forward.” If we traveled westward on this line, we would be moving “backward.” Note that the directionality attribute describes the allowed direction of travel. Any edge with the values “forward” or “backward” is an edge that only allows one-way travel. This could be a one-way bike lane or an escalator, for example. Any edge with the value “both” allows two-way travel.

Attributes such as “incline” are also affected by the directionality of an edge. Within GATIS data, if the incline or slope is upward as a traveler moves in the “forward” direction for that edge, the incline value should be positive. If the incline or slope is downward as a traveler moves in the “forward” direction for that edge, the incline value should be negative. 

For left / right tagging within GATIS (discussed in “Left, Right and Both Tags”), a piece of infrastructure would be on the left side of the edge and tagged “left” if it were to the north of this edge, because it would be on our left hand side as we are traveling east, in the forward direction. The infrastructure would be tagged “right” if it were to the south. Any other left and right references within GATIS follow this same pattern.

You can view line geometry in the geometry attribute within any geospatial data. It’s also possible to extract the first and last points of a linear feature to help populate the “from\_node” and “to\_node” attributes in GATIS, by finding the node in the GATIS node file that is the closest to each of these points.

## Driveway Mapping

GATIS does not contain a particular edge or node type for driveways, but it does support and encourage mapping of driveways. Some jurisdictions map every driveway, including all residential driveways, for asset management and inventorying purposes. Other jurisdictions may want to map only larger driveways or driveways in commercial, industrial or mixed-use areas. GATIS suggests mapping out larger commercial and institutional driveways in tiers 3-4, but the GATIS validator will not verify whether this has been done.

To map a driveway in GATIS, use the crossing edge to represent the area where motor vehicle or other traffic may be intersected. Connect the crossing edge to nearby sidewalk, mixed-use path or other edges using curb ramp nodes in tiers 1-2, and using the full mapping of curb ramp elements in tiers 3-4. (See “Curb Ramps” for more details.) Where possible, include any inclines and cross slopes that vary along the pedestrian path, using the incline attribute on the curb\_ramp node (tiers 1-2) or the curb\_ramp\_runslope edge (tiers 3-4). Driveways may also contain footways, traffic calming features like bulb-outs, and other geospatial features that can be represented in existing GATIS formats.

In residential areas, some data producers may not be able to map every driveway. However, a sudden change in cross slope from a driveway can be a challenge or a hazard for many travelers. A simpler way to map this change where significant is by segmenting the edge. The expanse of the driveway in the pedestrian way can be represented by either a sidewalk or a crossing edge, with the correct value provided in cross\_slope. See “Edge Segmentation” for more info on segmentation when selected attributes change.

## Edge Costing / Edge Impedances

Edge costing, also called edge impedance, is a technique used with graph networks to weight edges within the network differently in order to choose routes that fit specific needs. For example, a traveler might want to choose a route that is as flat as possible if they are traveling with a stroller or a mobility device. An algorithm could be used to assign higher edge costs to segments that have steeper inclines, and lower edge costs to segments that have little to no incline. A routing engine could then prioritize the edges with the lowest cost for this traveler. Edge costs can be created using a range of algorithms and can combine multiple attributes and factors.

GATIS does not contain attributes for edge costing, but GATIS data is useful for a range of edge costing scenarios. Data with thorough coverage, completeness, and consistency of attributes helps to enable costing. 

## Edge Segmentation

To segment an edge means to separate it into two or more smaller edges, and place a node in between each of those edges to maintain a connected network graph. If there is a specific type of physical infrastructure between the new edges, use the respective node type. If there is not a specific type of physical infrastructure between the new edges, use a generic node.

Within GATIS data, edges should always be segmented at intersections. 

When a sidewalk, bike facility, roadway or other edge becomes a bridge, tunnel / underpass or skywalk / overpass, the edge should be segmented. Use the bridge, tunnel and skywalk attributes to indicate the type of infrastructure. Similarly, segment when the edge type changes – for example, when a sidewalk turns into a multi-use path.

GATIS also recommends segmenting edges when some attribute values change. This helps to keep the data precise and make changes visible to users. However, a heavily segmented network is slower to parse and to route, and it is more complicated for an analyst to work with. It is expected that tier 3 and 4 data will have some segmentation. The exact amount of segmentation and where to segment is up to the data producer. The GATIS validator does not perform any checks related to segmentation, and the amount of segmentation is not a part of the calculation of the data’s tier.

It is recommended in tiers 3 and 4 to segment edges when attributes that have a significant effect on travelers or on use of the data change. Some examples include directionality, width\_in, status, official, presence, bikeway\_type, separation\_permeable\_car, shoulder\_width\_in, mup\_modal\_delineation, prohibited\_uses, allowed\_uses, restricted\_access, surface\_material, pedestrian\_lane, incline and cross\_slope.

It is recommended to NOT segment for attributes that have a less significant effect on travelers. This is a bit subjective, and different decisions might be made in different jurisdictions for a range of reasons. Some examples of attributes that might not be worth segmenting for include height\_max\_passable\_in, width\_min\_passable\_in, curb\_height\_in, separation\_elements and street\_parking. When choosing a value to assign to the edge, choose the value that identifies the most potential challenge for a traveler – for example, the highest curb\_height\_in.

Edges are polylines, so they can come in different shapes. For example, a multi-use path could have an “S” curve. The various stretches along the “S” shape do not need to be segmented, because they can be captured in a polyline. Segmentation would need to occur only if attributes change along the length of the segment, or if there is an intersection.

## Events Extension

The Events Extension in GATIS exists to capture greater detail about the history of infrastructure and its maintenance – when it was built or taken down, when construction or improvements occurred, and when it was inspected for asset management or ADA purposes. It is an optional extension that is not required in any tier, but its use is beneficial to safety analysis and a range of planning activities. It is designed to capture data that already appears in many government agencies’ asset management datasets.

Each row in the Events Extension represents a single event, such as a construction project, an inspection, an opening or closing date. It does not contain any geospatial data, but rather links to the geospatial data in the Edge, Node, Zone and Point GeoJSON files. It is a JSON file.

It is up to the data producer which types of events to capture within the Events Extension. New event\_types can be freely added.

## Extensions

Extensions to the specification may be added over time to cover gaps identified in previous releases. Data producers may also choose to extend GATIS on their own, by creating extensions that capture their unique needs. If an extension begins to see use from many data producers, it may be adopted into the specification in future versions. Extensions do not appear in the GATIS Registry by default.

## Footways

The footway edge type is used for a few purposes. One of these purposes is, in tiers 1-2, to map any gaps between the sidewalk centerline and the curb\_ramp node in order to make the curb ramp space routable. Footways may also be used to create connectors in other places where they are needed, or to map out a footpath that cannot reasonably be mapped using the sidewalk, trail, multi\_use\_path or other edge types. 

Footways are also useful in converting data between GATIS and OpenStreetMap, which has a footway tag. Three of OSM’s footway values map specifically to other GATIS edge types: “footway=sidewalk” should map to GATIS’ sidewalk edge, “footway=crossing” should map to GATIS’ crossing edge, and “footway=traffic\_island” should map to GATIS traffic\_island edge. In many cases, OSM’s “footway=path” is probably best mapped to GATIS’ trail edge. Other uses of the “footway” or  “footway (plain)” tag in OSM can be mapped to the GATIS footway edge. This data from OSM includes edges such as accessible footpaths in parking lots, alleys and residential pathways. Because OSM mapping practices can sometimes vary across areas, it can be helpful to take the time to study the data and consider if these mappings fit your needs. 

Both OSM and GATIS use the footway edge to connect sidewalk centerlines with curb ramp nodes. GATIS places a generic node at the point where the sidewalk edge and the footway edge meet.

## Generic Nodes

The network graph representation GATIS uses requires nodes between edges for routability. See the Routability section for more information.

In many cases, there is not a specific piece of physical infrastructure at a point where two edges intersect. Imagine a cyclist making a right hand turn onto a new block, for example, or a point where two multi-use paths intersect. Generic nodes in GATIS help to fill this gap. These nodes generally don’t contain attributes or any other information, and they exist solely to help connect the network.

Generic nodes do carry an attribute when they are used to help mark a rail crossing. See the section on Rail Crossings for the specifics of how this works.

## Informal Paths

GATIS edges have the attribute “official” to indicate whether a trail or footway is designated by a government agency or other organization with authority. However, many connecting paths and trails exist that are not official. Consider, for example, a shortcut on a grassy median that pedestrians have used over time to get to a nearby sidewalk (a “desire line”), or trails on private or other types of property that connect to officially managed trails but are not the responsibility of the government agency that maintains the trail network. 

Data producers who are government agencies will need to decide for themselves if they can and will include unofficial trails in their datasets. If not included, researchers, nonprofits or other organizations may decide to map the unofficial trails, and GATIS enables easy merging of the data from different sources.

When mapping desire lines and unofficial trails and paths, use official=”no.” The trail edge type is most appropriate for dirt trails or other pathways that may not be accessible to a wide range of travelers. The footway edge type is most appropriate for flat, wider, smoother-surfaced paths that are easier for travelers with mobility devices.

## Integrating with Other Specifications

GATIS is meant to be interoperable with several other specifications for related or connected infrastructure. This section describes how to integrate with these specifications. For any specifications not covered here, GATIS’ edges and nodes contain a reference\_ids attribute that can be used to list IDs and specification references.

### Transit (GTFS)

GATIS integrates with the General Transit Feed Specification (GTFS) and the Transit Integrated Data Exchange Specification (TIDES). Both GTFS and TIDES require an agency\_id and stop\_id to correctly identify a stop. The stop\_id can refer to the entrance to a transit station where multiple routes are accessible.

In GATIS, use the transit\_stop point to integrate with GTFS and TIDES. This point feature has attributes for agency\_id and stop\_id, which should both be filled out.

### Micromobility (GBFS)

GATIS integrates with the General Bikeshare Feed Specification (GBFS), which identifies the locations of parking and docking stations for bikesharing and micromobility. Use the point type bike\_parking. The parking\_id can be the GBFS station\_id when the point being marked is within GBFS, the parking\_provider can be the service provider, and the parking\_data\_URL can link to the website or API where the GBFS data about the facility can be found. 

The bike\_parking point also contains a parking\_type attribute that defines the mode (“bicycle”, “shared scooter,” etc.). This point can also be used to map out other types of parking, such as city-managed bike racks or lots. The recommended values for this attribute contain the word “shared” to indicate rented or borrowed vehicles. 

GATIS does not integrate directly with the Mobility Data Specification, which maps out service areas (rather than parking or docking) for micromobility. GATIS does not have a comparable zone type or designation for MDS’ service areas. However, some vehicles and other data can be mapped between GBFS and MDS where users of both specifications choose to apply common IDs.

### Routable Road Network (GMNS)

GATIS integrates fairly easily with the General Modeling Network Specification (GMNS), since the two specifications both aim to create network graphs. The network graph within GMNS focuses on the roadway space.

GMNS contains a links table, made up of LineString features. Links in GMNS represent the roadway centerline, so a road edge in GATIS can be crosswalked to a link in GMNS. The reference\_ids attribute on GATIS edges can be used to map to the correct link in GMNS. Pedestrian- and bike-specific edges in GATIS can be mapped to the bike\_facility and ped\_facility attributes on GMNS links. Note that these attributes describe the infrastructure present, but they do not provide space for a GATIS ID. 

GMNS also contains a nodes table. Some node types within GMNS overlap with GATIS node or point types, such as transit\_stop. The node\_type attribute within GMNS is a string field and can accept GATIS node or point types. Note that within GMNS, nodes are placed at the endpoints of links and used in routing, so any GATIS points added to a GMNS table would be treated as nodes. GMNS does not have a separate points table as GATIS does, but it does contain a locations table, which is used to represent points along links. GATIS issue points and other GATIS nodes or points may map to locations in GMNS rather than nodes.  

GMNS also captures detail on signalization in its Advanced Data Elements. GMNS signalization attributes also capture how motor vehicles interact with or are affected by signals, while GATIS focuses on bicycle and pedestrian interactions with signals. Much of the detail within GATIS data can be mapped to GMNS, and GMNS can be used to supplement GATIS data with deeper information about signalization for other road users.

### Traveler Counts

There are many different data sources that provide counts of pedestrians and bicyclists associated with particular pieces of infrastructure. GATIS integrates with these data sources and specifications via a point feature named “counter.” Generally, the point of type “counter” indicates a location where a counter is located. However, some specifications use zone features rather than point features to share their location. The point for data from these specifications can be placed at the center of the zone. 

The “counter” point contains a few fields to share necessary information to integrate the data, including the site ID and name within the source data, the URL of the source data, and a counter\_comments field that can be used to convey other instructions. For example, some datasets assign a site ID to a specific area that may have multiple sensors counting traffic coming from different segments or directions; counter\_comments can be used to describe the location or convey any additional IDs.

### Curb Space (CDS)

The Curb Data Specification maps out use of the curb space, including parking, zoning and curb usage. CDS represents curbs using linear features and polygons. Some geospatial features within CDS align with GATIS features, but many do not. For features that have a similar representation – such as a row of street parking – the CDS curb\_zone\_id, curb\_space\_id, curb\_area\_id or other ID field can be added to GATIS using the reference\_ids attribute on edges and nodes. 

For CDS data that isn’t easily represented in GATIS geometry, see the [Location Reference](https://github.com/openmobilityfoundation/curb-data-specification/tree/main/curbs#location-reference) JSON object in CDS. This object provides mapping to a roadway centerline LRS. GATIS’ LRS Extension can be filled out to align data from CDS and GATIS using an LRS format.

### Trails

Most federal agencies that maintain data about trails use the [Federal Trail GIS Schema (FTGS)](https://www.usgs.gov/national-digital-trails/federal-trail-gis-schema-leveraging-a-unified-strategy). FTGS is utilized by the U.S. Geological Survey’s [TRAILS application](https://www.usgs.gov/national-digital-trails/trails-advancing-sustainable-and-user-focused-trail-planning), as well as a range of other maps and applications. Many state, local and regional agencies use FTGS to easily integrate with TRAILS and other data nationally.

The simplest way to align GATIS data with FTGS data is to map the GATIS edge\_id of a trail to its FTGS GEOMETRYID. There are some attributes that are in both GATIS and FTGS data, including attributes for the name of the trail, its surface material, what types of uses are allowed, and who manages and maintains the trail. FTGS contains additional attributes that are useful, including trail numbers and classes, historic significance, trail condition, and  designation as a National Historic, Scenic or Recreational Trail. While these attributes are not a part of the GATIS schema, they can be added into GATIS data, and the GATIS validator will not fail a dataset that includes them. 

### OpenStreetMap

OpenStreetMap data contains a wide range of features, many of which are in GATIS. The consistency and quality of data can vary based on how active local mappers are, and how vigilant about the OSM schema they decide to be. Best practices for mapping between OSM and GATIS could be its own playbook. 

Here are a couple common mappings between OSM and GATIS to help new users get started. With any OSM data, take the time to review the data and understand the conventions local mappers are using. These tags are recommended within OSM schemas but are not always applied consistently.

Table 2: Feature Mapping

| Feature | OSM Feature(s) | GATIS Feature(s) | Notes |
| :---- | :---- | :---- | :---- |
| Sidewalk (marked on a roadway centerline) Sidewalk | Roadway centerline tagged as highway=\*, with attribute sidewalk=\* Sidewalk centerline tagged as highway=footway, with attribute footway=sidewalk | Convert to a separate sidewalk edge that follows the related road edge Use sidewalk edge | The OSM Pedestrian Working Group has released a [schema](https://wiki.openstreetmap.org/wiki/Draft:Foundation/Local_Chapters/United_States/Pedestrian_Working_Group/Schema) for better mapping sidewalks as their own networks, from which GATIS has drawn inspiration. OSM data that predates the schema follows different conventions. Many accessibility and other attributes of sidewalks in OSM can be mapped into GATIS. |
| Crossing | highway=crossing | Use crossing edge |  |
| Bike lane (marked on a roadway centerline) Bike lane | Roadway centerline with attribute cycleway=\* Bike lane centerline tagged as highway=cycleway | Use road edge with bikeway\_type indicated Use bikeway edge | OSM contains tags for buffer space, separation and a number of other attributes also in GATIS |

### Overture Maps Foundation

Overture employs GERS IDs to identify specific roadway segments. Much of Overture’s data is based on OSM data. GERS IDs are meant to provide stable IDs for specific infrastructure over time, and they account for changes in OSM, where changes to mapping or attributes can generate segments and new object IDs. At the moment, Overture’s core specification focuses on mapping roadway segments, though it may evolve to include other infrastructure over time. 

Use the reference\_ids attribute to link Overture features to GATIS road edges. Future versions of GATIS may contain more explicit integration.

### Metadata Schemas

The metadata file in GATIS shares some attributes and commonalities with the [Data Catalog Application Profile for the USA (DCAT 3.0),](https://github.com/GSA/dcat-us) [Croissant Format Specification](https://docs.mlcommons.org/croissant/docs/croissant-spec.html), [The Data Cards Playbook](https://sites.research.google/datacardsplaybook/), [The Data Nutrition Project](https://datanutrition.org/) and [OpenSidewalks Data Schema](https://github.com/OpenSidewalks/OpenSidewalks-Schema). All of these projects were considered as models during GATIS v1.0 development.

DCAT 3.0 is now the [metadata standard](https://resources.data.gov/resources/dcat-us3/) for federal data catalogs. There are many attributes that are in both DCAT and GATIS, including dataset title, publisher, description, contact, URLs for access, which other specifications the data conforms to, which other datasets reference this dataset, and more. Within DCAT, a GATIS dataset will best align with a class of Dataset or a class of Distribution, which is used for specific versions of the same dataset.

## Issues and Impediments

There are two main structures for tracking issues and impediments within GATIS: as an attribute, and as a point.

There are three attributes within GATIS that appear on edges, nodes and points: impediment, surface\_issue and other\_issue. Impediment attributes aim to capture objects that can block or impede some travelers, while surface\_issue aims to capture information about surface quality problems, and other\_issue is a catch-all for construction, design and any other type of issue that does not fit elsewhere. In tier 3, it is recommended for data producers who are new to tracking issues within their data to start identifying issues using these attributes. The issue could lie in a single point, and its location does not need to be specified. For example, a sidewalk edge with an attribute of “surface\_issue=cracking” may only have cracking at one point. That point is not specified within the attribute.

In tier 4, issue points are recommended. An issue point is used to mark the location of a specific issue, such as the single point of cracking mentioned above. Issue points also have the impediment, surface\_issue and other\_issue attributes to capture detail about the issue. The issue point should be placed in the location of the issue. Points are not required to be built into the network graph, but they can be integrated into it using buffers or other techniques. Doing so enables midblock routing and makes it possible for a traveler who cannot easily pass by the issue to be given a different route by a routing engine. See the Routing section for more information on adding points to a network.

In tier 4, a sidewalk edge that has cracking over a substantial portion of its length should still use the surface\_issue=cracking attribute. Marking individual points of cracking is probably not a good use of time in this case. It is up to the data producer to decide when to use an issue point and when to use the attribute tag on the edge.

Some datasets have a sidewalk condition attribute with ratings, such as “good,” “fair” and “poor.” GATIS’ [Guiding Principles](https://github.com/dotbts/BPA/wiki/Guiding-Principles) specifically call for a focus on “objective qualities of infrastructure,” and GATIS does not contain an attribute for rating sidewalk quality. However, data producers may include as many additional attributes as they like within their datasets, and GATIS data can provide helpful underlying data for designating these ratings.

## Left, Right and Both Tags

In some situations, there is a need to indicate whether a piece of infrastructure is on the left side, the right side or both sides of an edge. This edge may be a road, a bikeway, a sidewalk or any other type. 

GATIS includes “left,” “right” and “both” tags for this purpose. These tags may be used in any attribute where it makes sense, such as “shoulder\_width\_in,” “curb\_height\_in” and “buffer\_width\_ft.” To employ the tags, append them before the attribute. Here are some examples:

- To mark the width of a shoulder on the right side of a road edge, use left:shoulder\_width\_in=X, where “left:shoulder\_width\_in” is the attribute name and “X” is the measured number of inches.  
- To mark curb height that is the same on both sides of a raised cycleway, use both:curb\_height\_in=X on an edge of type bikeway, where “both:curb\_height\_in” is the attribute name and “X” is the measured number of inches.   
- To mark the presence of a bikeway on the left side of a road when the bikeway centerline is not being separately mapped, use bikeway:left:presence=yes as an attribute on the road edge, where “bikeway:left:presence” is the attribute name and “yes” is the value. Optionally, include bikeway:right:presence=no to clarify that there is not a bikeway on the right. 

Note in the third example that the attribute name references another type of edge. This same approach can be used to indicate the presence of sidewalks, multi-use paths and other linear infrastructure that follow the length of the edge they are tagged on. Try to avoid this approach for infrastructure such as crosswalks that appear at one point along the length, since it is much less clear. See the section on LRS Crosswalking for another way of tracking this infrastructure if it is not separately mapped (as GATIS recommends).

The directions “left” and “right” are determined based on how the geospatial features points are organized and drawn. See the section on Directionality for more information.

## Level Changes

Some infrastructure moves travelers to or places them on a different level. Consider, for example, overpasses, escalators and ramps. 

GATIS has a few attributes that help to track levels and level changes. On GATIS edges, the attributes “bridge,” “underpass\_tunnel” and “overpass\_skywalk” help to track where pedestrian and bicycle ways pass over or under other infrastructure. GATIS also contains edges for elevators, escalators and steps that give an indication of a level change.

GATIS also has two attributes that help to identify edges that lie above or below the grade level, or the ground level. The attribute “above\_below\_grade\_ft” helps to identify infrastructure that is above ground level if the value is positive and below ground level if the value is negative. It can be related to other edges to identify which infrastructure is higher. An edge with overpass\_skywalk=yes and above\_below\_grade\_ft=20 would be 20 feet above a neighboring road with no above\_below\_grade\_ft attribute set (meaning it is at ground level). 

The attribute “building\_level” helps to clarify the location of outdoor infrastructure that is next to a building. The value should be the label that the similar floor within the building is given. For example, if a ramp leads up to a small landing area or sidewalk that is at the mezzanine level, the sidewalk edge would be labeled with building\_level=mezzanine. Use GATIS for outdoor infrastructure. See the section on Integrating with Other Specifications for information on integrating with GTFS, which has a Pathways extension for indoor transit station mapping.

In many cases a traveler can move from one level to another, but in some cases – such as a pedestrian overpass over a freeway – travelers are not able or allowed to change from one edge to the other. Information about levels and connectivity is important to routing. In GATIS, edges that connect are marked with a node at their intersection. Any two edges lacking a node to connect them are understood to not connect. In this case, there should not be a node between the edge representing the pedestrian overpass and the road edge representing the freeway.

## Level of Traffic Stress / Pedestrian Level of Traffic Stress

Some datasets have attributes for the Level of Traffic Stress (LTS) for bicyclists and/or pedestrians. GATIS’ [Guiding Principles](https://github.com/dotbts/BPA/wiki/Guiding-Principles) specifically call for a focus on “objective qualities of infrastructure,” and GATIS does not contain an attribute for LTS. However, data producers may include as many additional attributes as they like within their datasets, including LTS. Many supporters of LTS measures were involved in developing and reviewing GATIS, and the hope is that GATIS can help to surface more high quality data on network connectivity, buffering, separation space, accessibility and a range of other attributes that can increase the robustness of LTS measures.

## Linear Referencing System (LRS) Crosswalking

Many transportation datasets that are near to or directly involve the roadway space are in a linear referencing system (LRS). Linear referencing datasets provide tabular data about roadway segments, with the data organized based on milepoints along the segment. For example, an LRS segment may have data indicating that the sidewalk on the right side of the segment starts at milepoint X.X. 

GATIS provides an LRS Extension that can be used to synthesize and convert data between GATIS’ network graph representation and an LRS. The extension contains attributes for the gatis\_id, reference\_ids that list out the related segment or segments within the LRS, the LRS source URL, starting and ending milepoints, and the side of the roadway segment where the specific infrastructure lies. All of these attributes are optional and may be used as needed.

LRS systems can carry a range of attributes, such as sidewalk width or bike lane type. The LRS Extension does not explicitly map these attributes into their proper place within GATIS, but rather provides a simple crosswalk that can be used to associate GATIS objects with LRS objects to enable further mapping.

The LRS Extension is optional and provided for convenience where it is useful. It is not associated with GATIS’ tier structure.

## Measuring Infrastructure

### Buffer Widths

When reporting buffer\_width\_ft, measure from the outer edge of the paint or barrier on each side. In other words, the reported value should include the width of any paint or barrier marking the buffer, and not just the space between the paint or barriers.  

### Bike Facility Width

When reporting width\_in, measure from the outer edge of any paint or barrier on each side. In other words, the reported value should include the width of any paint or barrier marking the lane, and not just the space between the paint or barriers.

### Sidewalk Width

GATIS recommends using ADA and PROWAG guidance for measuring sidewalk width. This guidance is very specific and focuses on measuring the “clear width,” meaning the unobstructed, continuous passage space available to pedestrians, [exclusive of curb width](https://www.access-board.gov/prowag/technical.html#r3022-continuous-clear-width). 

Some data may be collected using satellite, lidar and other imagery, from which widths can be derived. With this new data, ADA and PROWAG guidance remain important, and data producers are encouraged to apply them to the greatest possible extent. GATIS does not require the measurement method or measurement considerations to be reported, but it does provide the attribute ada\_compliant\_with that can be used to track the specific ADA guidance followed during an ADA assessment where the infrastructure was found to be compliant.

### Incline

The ADA and PROWAG also specify how to measure incline for sidewalks, curb ramps and crossings. AASHTO and NACTO provide guidance on how to measure incline for bikeways. As with sidewalk and bike lane widths, it is possible to derive the incline of a piece of infrastructure using lidar, a digital elevation model (DEM) or other 3D data. For pedestrian infrastructure, use the ada\_compliant\_with attribute to track whether ADA compliance has been achieved and under what specific guidance. While ADA guidance is superior for providing incline measurements, in some cases it may be preferable to release DEM-derived data.

## Metadata Topics

### Geospatial Bounding

As artificial intelligence and machine learning grow, having more data about the geospatial area covered is useful for easy categorization and incorporation of the data by algorithms. GATIS provides the geo\_bounding\_area in the metadata file to help ML applications and human users alike to easily understand the geographical area of coverage.

The data in geo\_bounding\_area can either be a polygon or a bounding box that simply identifies maximum and minimum latitudes and longitudes. Polygons are preferable when multiple jurisdictions are near each other and infrastructure crosses jurisdictional lines, because they can help the user to more readily identify who the infrastructure owner is at any given point. 

For bounding boxes, it is valid within GeoJSON and GATIS to use the GeoJSON “bbox” format, which maps out \[ minimum\_longitude, minimum\_latitude, maximum\_longitude, maximum\_latitude\]; for example, “\[-77.05, 38.88, \-77.00, 38.91\]”. A box can also be represented in polygon format: 

{

  "type": "Polygon",

  "coordinates": \[\[

    \[-77.05, 38.88\], 

    \[-77.00, 38.88\], 

    \[-77.00, 38.91\],

    \[-77.05, 38.91\],

    \[-77.05, 38.88\]

  \]\]

}

Polygons can be created fairly easily by creating a small buffer around all of the geospatial objects within the dataset. Some government agencies may already have polygons of their service areas that can be used.

### Data Provenance

As data collection using satellite, lidar and remote sensing grows, being able to track the way the data was collected becomes increasingly important. GATIS includes several optional attributes that are useful for tracking how data was collected, including source\_dataset, collection\_method, collection\_period\_start, collection\_period\_end, collection\_notes and modification\_notes.

Tracking data provenance is a newer development that GATIS encourages. It enables algorithms and human users to understand the quality and currency of the data, better interpret inconsistencies they might see, learn about resolution of the underlying imagery and other technical specifications, and easily compare data sources of the same infrastructure to know which best fits their needs. 

## Missing Infrastructure

GATIS does not require the explicit identification of network gaps or missing infrastructure in any tier of the tier model. However, GATIS’ network graph structure should make these gaps easier to identify. Missing infrastructure can be included in GATIS files if desired. Edges and nodes have an attribute for presence, which can be set to presence=no. A data producer that wanted to map a missing sidewalk segment could create a sidewalk edge with presence=no to indicate that there is no sidewalk at this location. Similarly, a curb\_ramp node with presence=no would mean that there is no curb ramp at this location. 

It is not implied that there should be infrastructure at the location anytime presence=no. Use context to make this determination, such as if a data producer puts out a dataset named “Sidewalk Network Gaps for Project Prioritization.” Contact data producers directly to get clarity.

Points and zones do not have the presence attribute. Only include these geospatial features if they exist.

## Planned and Budgeted Infrastructure

Infrastructure that is planned or budgeted for but not yet built should be marked with presence=no while it is incomplete and non-operational. See the section on Missing Infrastructure. 

In addition to being marked with presence=no, edges and nodes have a status attribute with possible values “under construction,” “proposed and funded”, and “proposed \- not yet funded.” The status attribute should be filled out for planned infrastructure where possible. Other attributes such as lifecycle\_stage and planned\_work are optional and can help to convey information about future plans.

Also, the Events Extension can be used to capture key events in the construction and planning process, such as dates of project or budget approval and the beginning and ending of construction. See the Events Extension section in this Playbook for more information.

## Presence Attribute

Edges and zones contain an attribute named “presence,” which is meant to convey whether the infrastructure is physically present or not. If this attribute is left blank, the infrastructure is assumed to be present. 

There are a number of cases where explicitly indicating the presence of infrastructure is useful. See the sections on Missing Infrastructure, Planned and Budgeted Infrastructure, and Unmarked Crossings to learn more about a few examples.

## Polygons

The current version of GATIS supports two different types of polygons: open and traffic\_calming.

“Open” polygons are used to map out areas like parks and plazas where travelers can choose their paths through the space freely, and where multiple modes are often allowed. The polygon should correctly mark out the space that is filled by the open use area, excluding sidewalks and other nearby infrastructure, which should be mapped separately and fully connected to the network graph. If a polygon is intersected by an edge – for example, a park space with a multi-use path through the middle – map it as multiple separate polygons that capture each open space on either side of the multi-use path. Map the multi-use path as a separate edge. 

Routing through a polygon is difficult because a path must be selected, and making this choice can be complicated. Routing engines will likely prioritize them over routing through polygons due to ease of use. Where needed, routes through polygons could be chosen by snapping the route to the closest edge connection, such as nearby sidewalks or bike lanes. Routing engines may also choose to create pairwise edges between all nodes contained within the zone to effectively collapse zones into edges, or they may handle them at request time using another logic of their choice.

Polygons of type traffic\_calming are not meant to be connected to the network graph, and they are not meant to be routable. Rather, they are meant to show the area where traffic calming features lie. Map the routable space through traffic calming features using a separate edge. For example, if mapping a bulb-out as a traffic\_calming polygon, have the polygon take the shape of the bulb-out, and place it where the bulb-out lies. Create an edge of type sidewalk, footway or whatever is appropriate for the space that passes over the polygon, and fully connect it to the network graph on either side of the traffic\_calming polygon. Routing engines will use the edge to route along, rather than the polygon. 

## Rail Crossings

GATIS recommends mapping out rail crossings with the crossing edge, particularly in higher tiers. There are no dedicated nodes and edges in GATIS for rail crossings, but there are attributes on other node and edge types to enable mapping.

To map a rail crossing, segment the edge and place a crossing edge within the space where a traveler will be crossing the tracks. Place generic nodes to mark the transition points on each side of the crossing between the sidewalk or other edge space and the crossing area. Similar to the ramp\_to\_street\_transition node that is a part of curb ramp mapping in tiers 3-4, these generic nodes serve to identify when a traveler leaves protected or safe space and may be within traffic. 

Use the attribute rail\_crossing\_control on the generic nodes to describe what types of control and information infrastructure exist at the point, such as gates, flashing lights and tactile markings. On the crossing edge, use the attribute rail\_crossing=yes to indicate that this is a rail crossing.

Note that within the other\_issue attribute for edges, there is a value for “rail tracks.” This value is meant to be used in cases where the tracks are likely not in use and may pose an impediment to pedestrians and cyclists. For example, there may be old rail tracks embedded in the road or sidewalk that can be a traction hazard for bikes. To map active rail crossings that see train traffic, use the crossing and generic nodes as described here.

## Relation Tables

Relation tables exist in a GATIS extension to enable making an explicit connection between pieces of infrastructure that are not otherwise explicitly connected in an obvious way. In developing relation tables, two main uses were considered: connecting pushbuttons and detectors to the crossings they affect, and mapping out or giving details on turning movements that may be unclear. The relation tables may be used for any other purpose of relating two pieces of infrastructure. For V1.0 the attributes on the relation table have been kept simple and streamlined to these two use cases, but data producers may add other attributes locally and propose them for inclusion in future versions of GATIS.

To connect pushbuttons and detectors with crossings, the relation table contains attributes for signal\_id and crossing\_id. Both attributes can contain lists, and the relationship can be many to many. For example, if a crossing has pushbuttons on each end, the two pushbuttons can be indicated in a list in signal\_id. Similarly, if there is a median island, a signal\_id could affect two crossing edges, the one a pedestrian will encounter before the median island and the one they will encounter after it. If there is a pushbutton on the other side of the crossing, there would be two pushbuttons affecting the same two crossings. These could be placed in one line in the relation table, or the data producer could decide to put each signal\_id in a separate row with a list of the two crossings under crossing\_id. 

For turning relations, one useful example is bicycle two-stage left turns, where a cyclist proceeds through an intersection and then either waits in a bike box or near a pedestrian crossing until a traffic light changes, then proceeds with motor vehicle traffic in their new direction. Within the relation table, from\_id and to\_id attributes map out the infrastructure that are connected within the relation. For a two-stage left turn, the from\_id could be the edge the cyclist is arriving on, and the to\_id could either be the new edge they would be traveling on after their turn, or the crossing edge they might follow before merging back into motor vehicle traffic. The attribute turning\_treatment on the relation table gives space to provide more information on the turn and how it is executed.

## Routing

### Network Graphs

GATIS uses a network graph (or graph network) representation. A network graph is made up of edges (also called lines or links) that are linear features, and nodes (also called vertices) that are points. Within the GATIS network graph, linear geospatial features such as sidewalks, crossings and bike paths are edges. Point features such as curb ramps or other nodes in the curb ramp space are nodes. By default, nodes are part of the network graph. The GATIS Explorer lists which features are edges and which are nodes. 

Routes are created by traveling along the edges in a network graph. The nodes represent origins, destinations and points where a traveler could potentially change direction and travel along a different edge. Within a network graph, two or more edges that connect and are meant to be routable must have a node in between them. 

GATIS recommends at a minimum that each block of a sidewalk or bike facility be its own edge, with nodes at the intersections. Blocks can be segmented down further to show intersections with multi-use paths, driveways, alleys or other infrastructure.

### Routability in Each Tier

In tier 1, GATIS data does not need to be routable. Pedestrian and bike networks may be represented in this tier as attributes on a road edge, rather than as a separate network graph. They may also be represented with separate centerlines, or with a mix of the two.

In tier 2, a separate network graph and separate centerlines should be created for pedestrian networks. Bike features that are not a part of the roadway space should also have their own separate centerlines, and bike features that are on the roadway space should be mapped on roadway edges and connected to the separate bike features within the same network graph. These graphs do not need to be fully connected, perfectly cover all areas or fully capture all possible connections. Metadata routing may be useful to help connect the network where full spatial connectivity doesn’t yet exist in the data. Users of tier 2 data should expect to spend some time making corrections and adding connections to use the data for routing applications. 

In tiers 3 and 4, a fully connected graph network should exist for both pedestrian and bike networks. This network should be connected via spatial topology, and may also be connected via metadata. Throughout every tier of GATIS, bike networks should use roadway centerlines where bike facilities exist on the roadway space and are only separated by paint. See the section on Bike Networks for more details. 

In tier 4, more connections, side paths and other detailed mapping may be present. It is recommended that edges be created in this tier to fully connect transit\_stop and pushbutton points to the network graph when desired. Also, see the section on Curb Ramps for details on more granular curb ramp mapping in tier 4\.

### Spatial Topography Routing

Routing via spatial topology requires that the endpoints of geospatial features be touching within the data when the infrastructure they represent is connected for travelers. The connectedness of the data signals to routing engines that the connection can be made.

Within a network graph, there must be a node in between two edges that connect. Routing engines are able to fill in these nodes when they are missing and when features appear to be close enough to connect, but it is recommended for data producers to explicitly place nodes where connections exist, rather than allowing routing engines to fill them in. The lack of a travelable connection is signaled in GATIS by not placing nodes at these intersections. For example, where a pedestrian overpass goes over a freeway, no node would be placed where the overpass and the freeway share the exact same coordinates, because the pedestrian cannot change edges at this point.

### Metadata Routing

One way to represent the connectivity between edges and nodes in a network graph is to have attributes that lay out these connections. GATIS shows this connectivity using the from\_node and to\_node attributes on edges. For example, a sidewalk edge might have from\_node=1234 and to\_node=1235. Another sidewalk edge might have from\_node=1233 and to\_node=1235. These two edges would be connected at node 1235\. The directionality attribute on the sidewalk edges would help routing engines know if this is a route that a traveler can follow or if the direction of travel on one of the edges makes the route impossible. See Directionality to learn more about travel in forward, backward and both directions.

If metadata routing is being used, geospatial features do not need to be connected via spatial topography. Instead, the data in the from\_node and to\_node fields are used to construct the graph and show what routes are possible to travel.

Metadata routing works well within machine learning applications, but it makes some safety and geospatial analyses challenging because it requires data users to draw in connections themselves to fully connect the network within mapping applications. Examining an intersection layout or running calculations within ArcGIS on the number of miles of bike lanes become difficult tasks, and maps do not display properly. GATIS prefers spatial connectivity for this reason and encourages that metadata routing generally be in addition to a spatially connected network.

Within metadata routing, if two features are not explicitly connected using from\_node and to\_node, the infrastructure they represent is not connected. Data producers should be careful to ensure that connections exist in the data where and only where they exist in the real world.

### Adding Points to a Network Graph

There are several different point types within GATIS that can be the origins, destinations or side points of trips. Transit stops, bike parking, pushbuttons and some object types can all be useful for routing. These points are not included in the network graph by default to reduce complexity and speed up any computations made on the network. They are meant to be relatively easy to add into the network graph when desired.

If a point is already connected via spatial topology or by metadata to the network graph, it can simply be converted to a node and incorporated into the graph network. In tier 4, it is recommended for transit stops and pushbuttons to have edges connecting them to the network to make it easy to add them. 

If a point is not already connected to the network, these connections can be added, or a buffer can be created around these points and a node added to the network at the point where the buffer touches an edge. Points can also simply be “snapped” (or shifted) to their closest edge. The latter approaches can be particularly useful for objects such as parklets or benches, to bring a traveler near to the object. 

## Sidewalk Condition

Some datasets have a sidewalk condition attribute with ratings, such as “good,” “fair” and “poor.” GATIS’ [Guiding Principles](https://github.com/dotbts/BPA/wiki/Guiding-Principles) specifically call for a focus on “objective qualities of infrastructure,” and GATIS does not contain an attribute for rating sidewalk quality. However, data producers may include as many additional attributes as they like within their datasets, and GATIS data can provide helpful underlying data for designating these ratings.

## Signals

GATIS contains a point type of “pushbutton” that is used to mark the location of infrastructure that a pedestrian must or should interact with to trigger a crossing – typically, an accessible pedestrian signal or signal button. There is also a “detector” point that can be used to track automated pedestrian detection points.

The pushbutton point can track information about accessibility and features of the signal, including crossing time. Relation tables are used within GATIS to identify which crossings are affected by a push button. See the Relation Tables section for more information.

In tier 4, GATIS recommends exploring some level of routability for pushbutton and detector points. Making these points routable requires a high level of geospatial precision on the part of both the data and the traveler’s device. To connect a pushbutton or detector point to the network, a data producer could use footway edges to connect the point to the sidewalk network in a manner that provides an appropriate approach from both directions. Routing engines would convert the point to a node. If a data producer does not have time to do this for every pushbutton and detector, the pushbutton and detector points that are placed in unexpected or more distant locations and may be harder for blind or low vision travelers to find can be prioritized, since this is the case where routing to the point is most useful.

At this time, GATIS does not track signal heads. Future iterations of GATIS may add signal heads for asset management purposes.

## Spatial Tolerance

### Width Tolerance

In addition, the width\_tolerance\_in attribute exists to help convey spatial tolerance for the width\_in attribute on any edge. It’s meant to convey the number of inches the width might differ at any point along the edge. For example, say that there is a sidewalk edge for which width\_in=40, and say that width\_tolerance\_in=2. This means that the width of that sidewalk edge is no more than \+/- 2 inches at any point along its length. It will be no less than 38 inches wide, and no more than 42 inches wide.

## Unmarked Crossings

In many jurisdictions, every intersection is a legal crossing point for pedestrians, regardless of whether there are painted crosswalk markings. GATIS data produced by state and local agencies should include all legal crossings, to enable routing. 

Within GATIS, an unmarked crossing should be a crossing edge. It should indicate presence=yes. It should also indicate visual\_markings=unmarked. 

# Appendices

## Acknowledgments

The following organizations and people were essential in the creation of this draft:

* National Collaboration on Bicycle, Pedestrian and Accessibility Infrastructure Data leadership. The following people have served in leadership roles throughout the time the collaboration NC-BPAID has been active.

  * National Co-Chairs: 

    * Anat Caspi, Taskar Center for Accessible Technology, University of Washington  
    * Bahar Dadashova, Texas A\&M Transportation Institute  
    * Peter Furth, Northeastern University  
    * Geoffrey (Jeff) Whitfield, Physical Activity and Health Branch, Centers for Disease Control and Prevention

  * Leaders of NC-BPAID subgroups on Data Practices, Outreach, and Specification Development: 

    * Jonah Chiarenza, Kittelson & Associates, Inc.  
    * Bahar Dadashova, Texas A\&M Transportation Institute  
    * Ellwood Hanrahan, New York State Department of Transportation  
    * Jeff Maki, Public Works Office  
    * Paul Moser, Delaware Department of Transportation  
    * Krista Nordback, Highway Safety Research Center, University of North Carolina  
    * Josh Roll, Oregon State Department of Transportation  
    * Ryan Westrom, Citian  
    * Ximon Zhu, Numobility  
* Members of the NC-BPAID Specification Development Subgroup Task Forces on Intersections and Accessibility.

* Participants in field and usability testing during the fall of 2025, whose in-depth reviews played a huge role in shaping the final specification.

* Members of NC-BPAID who provided insights, ideas, and feedback on this specification.

* The Bureau of Transportation Statistics, U.S. Department of Transportation, which served as a convener and coordinator of this work. Key contributors to the specification from BTS: Cyrus Chimento, Jay Davis, Justyna Goworowska and Reid Passmore.

* Carl Fredlund and our peers at MobilityData, who provided guidance and strategic advice throughout the NC-BPAID collaboration’s lifecycle.

* Volpe Center, U.S. Department of Transportation, which provided strategic, logistical and other support to the Bureau of Transportation Statistics. 

* The following operating administrations and departments of the U.S. Department of Transportation, who provided expertise throughout the process:

  * Federal Highway Administration

  * Federal Transit Administration

  * Intelligent Transportation Systems Joint Program Office

  * National Highway Traffic Safety Administration

* Developers and maintainers of other specifications who provided advice along the way, including OpenStreetMap and the OSM US Pedestrian Working Group, OpenSidewalks, Open Mobility Foundation, Overture Maps Foundation, General Transit Feed Specification (GTFS) and Workzone Data Exchange (WZDx). 

* Last but not least, all of the individuals and organizations who took the time to review drafts and help improve the specification step by step. We appreciate you\!

## Guiding Principles

The following guiding principles shape the specification and its development. They were adopted in 2025 through a vote of the National Collaboration.

1. **The specification is owned and openly governed by the community.**  
   * This specification is created under the CC0 1.0 Universal Public Domain license.  
   * Any organization or body that takes over management of the specification should:  
     1. Provide open and transparent governance for a broad-based community of contributors and users across a range of geographies, areas of expertise and other domains. A variety of perspectives are needed to support innovation and access to data and tools that can benefit everyone.  
     2. Be independent, and not have business interests that could be impacted by the contents of the specification.  
   * The specification may or may not evolve into a standard. If it does become a standard, we encourage it to remain free and “open source.”  
2. **Data produced under the specification should be shared freely and openly with the community.**  
   * Data producers are encouraged to license data in a way that keeps it free and available for commercial and noncommercial use.  
   * All data producers and consumers, regardless of size, are encouraged to contribute data to public and open repositories and contribute to the growth of the ecosystem through data, code, tools and other means.  
3. **The specification is designed to be as simple as possible, yet provide the ability to capture precise detail when available. It aims to enable technical and non-technical experts to effectively produce high quality data.**  
   * The specification deliberately includes a minimal set of required fields, recognizing that data collection is time consuming and often requires expertise not available to resource-constrained organizations who are motivated to improve the data.  
   * Thorough, public, plain language documentation is provided for the entirety of the specification to drive data quality and support data producers and consumers with various skill levels and knowledge bases.  
   * The specification allows data producers, including those who are technically sophisticated, to add more detail where they are able to.  
   * The specification is specific and precise, and aims to be mutually exclusive and collectively exhaustive. For example, it specifies numerical values with explicit allowable ranges, and it enumerates categories and types rather than allowing open-ended text fields. This is intended to make it easier for applications to consume data, especially across a variety of producers, and easier for producers to create data others can consume.  
   * One official validator is used to ensure consistency, and a transparent process exists for continual improvement of the validator.  
4. **The specification prioritizes universal accessibility and the needs of all travelers, across a range of use cases.**  
   * It includes attributes that help travelers of varying abilities and needs know how to navigate in a way that matches how they move.  
   * Connections between various types of transportation infrastructure are positively identified to enable routing and other use cases.  
   * It is tested and optimized in rural, suburban and urban areas nationwide, and in areas with differing density and land use patterns.  
5. **The specification describes objective qualities of infrastructure.**  
   * Rather than, for example, describing a path as “accessible” (incorporating the values of the person who is assessing that quality), the specification describes the path objectively as being six feet wide or having a slope of 1:48.  
   * It relies on third-party applications to help travelers and other users interpret the data in accordance with their needs–i.e. determining what is “accessible” for them.  
6. **The specification includes context that is useful for travelers and for information systems.**  
   * The specification includes metadata such as data origin, date of collection or last update, refresh schedules, authority or confidence, tolerance and error levels, completeness, recency and collection method. This metadata enables users to make their own decisions about how to use the data.  
   * The specification is designed to allow for two-way data exchange so that users who identify errors may submit or suggest them for correction.  
7. **The specification is extensible, and designed to be interoperable or interchangeable with other trusted specifications to make maintenance and creation as easy as possible.**  
   * Where possible, the specification uses the same or similar data structures and conventions as other specifications and standards that have clear alignment. Creating data in this specification should be as straightforward as possible, leveraging existing databases and/or data collection efforts as much as possible when and where they exist.  
   * Extensions to the specification may be added over time to cover gaps identified in previous releases.  
   * Data producers may add their own columns or create their own extensions to fit their local needs. These ad-hoc changes may be adopted into the formal specification if shown to be widely adopted.

## Related Specifications

The following specifications have a relationship with bicycle, pedestrian, and accessibility infrastructure. This specification is designed to be easily interoperable with them, wherever possible.

| Specification | Description | Interoperability |
| :---- | :---- | :---- |
| [General Modeling Network Specification (GMNS)](http://zephyr-data-specs.github.io/GMNS/) | GMNS is an extensible specification aimed at describing the entire transportation space, including physical elements, traffic controls and time varying policy elements. It includes representations of the physical transportation space (e.g., links, lanes, intersections, sidewalks, points of interest along a link), traffic controls (including signals) and time-varying policy elements (e.g., part-time lanes, restrictions on link or lane usage). | Bicycle and pedestrian facilities may either be modeled as attributes of a road link or as their own links. Nodes and edges within this specification can be integrated and joined with GMNS data in many cases. |
| [Indoor Mapping Data Format (IMDF)](http://register.apple.com/resources/imdf/) | IMDF is primarily used to create accurate, geo-referenced digital maps of indoor spaces. It is often adopted for use in buildings like airports, malls, stadiums, arenas, and other complex indoor environments. | There are no explicit ties between IMDF and this specification, but IMDF could easily be used to continue to route through an indoor space. This specification can end a route at a transit stop (including station entrances and exits) or in front of other building types. |
| [OpenSidewalks](https://tcat.cs.washington.edu/opensidewalks/) | The OpenSidewalks schema is used to create an internationally distributed pedestrian/bike transport graph layer, including infrastructure data for accessibility, safety, and pedestrian preferences. It includes extended attributes for advanced accessibility and route planning features. It builds on OpenStreetMap's tagging schema and community mapper model. | Interoperability with this specification is high, and many of the same data structures are shared. |
| [OpenStreetMap (OSM)](http://openstreetmap.org/about) | OSM is a global, crowd-sourced database that includes data on infrastructure across transportation and within other domains. OSM covers bicycle, pedestrian, and accessibility aspects in depth. | OSM and this specification have many shared data structures, and data is highly interoperable. See the [OSM US Pedestrian Working Group’s schema](https://wiki.openstreetmap.org/wiki/Foundation/Local_Chapters/United_States/Pedestrian_Working_Group/Schema) to learn more about pedestrian features. |
| [Overture Maps](http://overturemaps.org) | Overture is creating global, interoperable, open spatial data that covers many aspects of the transportation system.  | Overture data draws from OSM and uses many of their data structures, as well as layering on its own. |
| [Curb Data Specification (CDS)](https://www.openmobilityfoundation.org/about-cds/) | CDS expresses “dynamic curb zones” to improve parking, especially for delivery vehicles and passenger loading. It includes both defining on and off street parking/stopping/travel facilities (for any type of vehicle, bike, bus, robot, etc), and tracking events and usage metrics at these locations. | CDS and this specification have some connections at the curb space and objects in the right of way. CDS is a good source for real-time policy rules and occupancy data related to curb management, and tracking activity and usage. Crosswalk to GATIS on street\_name or do an LRS match on “location\_references” optional in CDS zones.  |
| [General Bike Feed Specification (GBFS)](https://gbfs.org/) | GBFS represents the availability of docked and free-floating bikeshare, scootershare, and carshare. It connects data from bikeshare systems to consumer journey planning apps.  | This specification maps out public bicycle facilities. With a little effort, features such as bikeshare stations and parking can be integrated into a routable network created using this specification. |
| [General Transit Feed Specification (GTFS)](https://gtfs.org/)  (plus extensions including \-RT, \-Pathways, \-Flex, \-Fares) | GTFS relays data from public transit agencies globally to provide public transportation information including stations, stops, routes and arrival information. GTFS-Pathways data is available for a subset of those agencies and describes the layout and accessibility of transit stations. | This specification includes GTFS agency\_id and stop\_id that can be used to pull in transit data from any available GTFS feed. GATIS includes agency-id and stop-id to enable interoperability with GTFS.  |
| [National Bicycle Network (NBN)](https://data.transportation.gov/stories/s/National-Bicycle-Network/88zh-3rqb/) | NBN compiles bicycle route geospatial data for the U.S., based on data released by public agencies. It is managed by the Federal Highway Administration.  | Many of the data structures in this specification align with NBN data structures.  |


