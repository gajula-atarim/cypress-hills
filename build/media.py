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
