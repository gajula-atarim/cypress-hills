"""Media library attachments uploaded to cypress-hills.wsdfy.com (IDs from the upload)."""
BASE = "https://cypress-hills.wsdfy.com/wp-content/uploads/2026/10/"


def _m(i, f, alt):
    return {"id": i, "url": BASE + f, "alt": alt}


LOGO = _m(55, "cypress-hills-logo.png", "Cypress Hills Landscaping")
AWARDS = _m(56, "awards-of-excellence.png", "50 Years Awards of Excellence, 1973–2023")
POOL = _m(57, "pool.jpg", "Backyard pool with stone terraces and evening lighting")
STONE = _m(58, "armour-stone.jpg", "Armour stone retaining walls and steps")
GREEN = _m(59, "putting-green.jpg", "Backyard putting green")
KITCHEN = _m(60, "outdoor-kitchen.jpg", "Outdoor kitchen and cabana")
AERIAL = _m(61, "aerial-estate.jpg", "Aerial view of a landscaped estate")
CREW = _m(62, "crew.jpg", "Cypress Hills crew at work")
NIGHT = _m(63, "night-lighting.jpg", "Landscape lighting at night")
COURSE = _m(64, "golf-course.jpg", "Golf course shaping")
FALLS = _m(65, "waterfall-pool.jpg", "Pool with waterfall feature")
SKETCH = _m(66, "design-sketch.jpg", "Landscape design sketch")
FINISHED = _m(67, "finished-yard.jpg", "The finished backyard")
STEP_WALK = _m(68, "process-site-walk.jpg", "Site walk")
STEP_DESIGN = _m(69, "process-design.jpg", "Design")
STEP_BUILD = _m(70, "process-build.jpg", "Build")
STEP_HANDOVER = _m(71, "process-handover.jpg", "Handover")

# Brand-kit inner-page photos (uploaded 2026-10-06).
FIBERGLASS_CRANE = _m(108, "fiberglass-pool-craning.jpg", "Crane lowering a fiberglass pool shell into place")
TURF_CREW = _m(109, "turf-installation-crew.jpg", "Crew rolling out and compacting artificial turf")
FREEFORM_POOL = _m(110, "freeform-pool-dusk.jpg", "Freeform pool with stone deck at dusk")
PET_TURF = _m(111, "pet-friendly-turf.jpg", "Dog resting on artificial grass beside a stone border")
POOL_CABANA = _m(112, "pool-cabana-terrace.jpg", "Rectangular pool with cabana and stone terrace")
STONE_SETTING = _m(113, "armour-stone-setting.jpg", "Crew setting armour stone with an excavator")
POOL_HILLS = _m(114, "pool-hillside-view.jpg", "Pool overlooking rolling hills at sunset")
GOLF_AERIAL = _m(115, "golf-course-aerial.jpg", "Aerial view of a shaped golf hole with bunkers")
STONE_TERRACES = _m(116, "armour-stone-terraces.jpg", "Terraced armour stone walls with steps and planting")
GRASS_LAWN = _m(117, "artificial-grass-lawn.jpg", "Artificial grass lawn in a modern backyard")
POOL_STEPS = _m(118, "fiberglass-pool-steps.jpg", "Fiberglass pool steps with stone coping")
BUNKER = _m(119, "bunker-shaping.jpg", "Excavator shaping a golf course bunker")
TURF_PATIO = _m(120, "synthetic-turf-patio.jpg", "Synthetic turf lawn beside a stone patio")

# Client photos (already in the media library), used on the Home page.
P_POOL_CABANA = _m(9, "mike-1.jpeg", "Pool with stone deck and cabana")
P_STONE_HOUSE = _m(10, "mike-2.jpeg", "Stone house with terraced steps and planting")
P_PUTTING = _m(13, "mike-golf.jpeg", "Backyard putting green")
P_KITCHEN = _m(17, "mike3.jpeg", "Stone outdoor kitchen with built-in grill")
P_CABANA = _m(28, "mike15.jpeg", "Cabana and patio beside the pool")
P_POOL_TURF = _m(30, "mike17-rotated.jpeg", "Pool with turf and stone deck")
P_ARMOUR = _m(31, "mike18.jpeg", "Armour stone terraces being set")
P_STEPS = _m(32, "mike19-rotated.jpeg", "Armour stone steps and wall")
P_STEPS_BUILD = _m(37, "mike24-rotated.jpeg", "Crew building stone steps")
P_LOUNGE = _m(40, "mike27.jpeg", "Pool lounge with turf and loungers")
P_TIMBER = _m(41, "mike28.jpeg", "Timber garden building")
P_GREEN_BUNKER = _m(48, "mike36.jpeg", "Shaped green with bunker")
P_GREEN_MOUNTAINS = _m(49, "mike37.jpeg", "Green and bunker with mountains behind")

# Brand-kit image ids (atarim S3 "generations/<id>.jpg") -> media library attachments.
KIT = {
    "6b71663b-b520-44a7-94bb-a5c470c68ce1": POOL,
    "3ba47ee2-7f56-4aaf-9d34-bd3844bda08e": STONE,
    "8f31a0ce-dd1b-43c0-a698-6acdfd047caa": GREEN,
    "b77c3889-6717-4556-8bb0-b9d812545c75": KITCHEN,
    "a7606c2d-5fc9-4d4e-9486-757d5101e8ac": AERIAL,
    "e39ef06c-0b14-4e6f-88cc-7956c6082637": CREW,
    "e2ed4fb5-6ace-4fbf-beed-eeaee18f7f69": NIGHT,
    "79017ad2-7cdf-45a0-9659-e4b04f8f0cd2": COURSE,
    "e60daa01-e579-4885-b3b2-9a3ea46940b9": FALLS,
    "d29796c7-7bdc-420d-98be-42877f39f314": SKETCH,
    "8c87c463-0e87-4f1f-8397-fec0efcba075": FINISHED,
    "3a95cf80-6eb0-412c-8a10-7a4d7dd828a6": STEP_WALK,
    "f1023ca8-3f28-4151-9bb7-78c9632e54a2": STEP_DESIGN,
    "47905afa-a719-4571-8892-7caabdd348c3": STEP_BUILD,
    "2b23aed4-6e35-4fb2-9a86-0c73cf8f0b40": STEP_HANDOVER,
    "1e28f731-a945-416c-92b6-5a6e95975e8a": FIBERGLASS_CRANE,
    "1eb81543-abd2-4b8e-a8b2-372d731c5862": TURF_CREW,
    "23a5229f-f69d-41ed-95c4-83191817eb5f": FREEFORM_POOL,
    "3d31ce2b-8dba-470f-9eda-df410c8f5af6": PET_TURF,
    "67b2e1f0-4a59-4908-ab1e-375c2268aebc": POOL_CABANA,
    "9a73a302-1532-486c-a6e8-0067b959b93d": STONE_SETTING,
    "9b015868-fec8-4725-be40-efc5ab5512e6": POOL_HILLS,
    "a4e25fb7-3d81-4ec0-b002-b4fd803cce0d": GOLF_AERIAL,
    "b7f06178-3de9-47c4-b5c8-61ff00d91ab1": STONE_TERRACES,
    "d1c0ca16-ea3a-4da7-b24c-3e26c6ef7a63": GRASS_LAWN,
    "dcd86a37-e03c-48cb-af7f-9ecadc50c33c": POOL_STEPS,
    "ece444b3-20c7-4cd0-9e95-d2d216875970": BUNKER,
    "edbd01f9-b228-4a27-a809-fc960d3775ef": TURF_PATIO,
}

# Projects page gallery, in the kit's order.
GALLERY = [KIT[k] for k in (
    "67b2e1f0-4a59-4908-ab1e-375c2268aebc", "3ba47ee2-7f56-4aaf-9d34-bd3844bda08e",
    "a7606c2d-5fc9-4d4e-9486-757d5101e8ac", "9b015868-fec8-4725-be40-efc5ab5512e6",
    "b7f06178-3de9-47c4-b5c8-61ff00d91ab1", "e60daa01-e579-4885-b3b2-9a3ea46940b9",
    "8f31a0ce-dd1b-43c0-a698-6acdfd047caa", "b77c3889-6717-4556-8bb0-b9d812545c75",
    "23a5229f-f69d-41ed-95c4-83191817eb5f", "e2ed4fb5-6ace-4fbf-beed-eeaee18f7f69",
    "a4e25fb7-3d81-4ec0-b002-b4fd803cce0d", "edbd01f9-b228-4a27-a809-fc960d3775ef",
    "6b71663b-b520-44a7-94bb-a5c470c68ce1", "e39ef06c-0b14-4e6f-88cc-7956c6082637",
    "d1c0ca16-ea3a-4da7-b24c-3e26c6ef7a63", "9a73a302-1532-486c-a6e8-0067b959b93d",
    "8c87c463-0e87-4f1f-8397-fec0efcba075", "79017ad2-7cdf-45a0-9659-e4b04f8f0cd2",
    "dcd86a37-e03c-48cb-af7f-9ecadc50c33c", "ece444b3-20c7-4cd0-9e95-d2d216875970",
    "1e28f731-a945-416c-92b6-5a6e95975e8a", "3d31ce2b-8dba-470f-9eda-df410c8f5af6",
    "1eb81543-abd2-4b8e-a8b2-372d731c5862")]
