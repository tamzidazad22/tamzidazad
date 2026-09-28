# Media & Photo Carousel System

This directory houses the media stories and photo carousels for `tamzidazad.com`.

## Directory Structure

```
media/
├── carousels/
│   ├── inbox/           # Raw photo drop folder for unreviewed images
│   ├── registry.json    # Structured metadata catalog for all curated carousels
│   └── README.md        # This workflow guide
├── ventures/            # Venture ecosystem photography & event captures
├── teaching/            # Classroom, workshop, and lecture captures
├── doodlepad/           # Product screenshots, team, and accelerator moments
```

## Scalable Workflow: From Inbox to Deployed Carousel

To keep the site editorial, performant, and clutter-free, images dropped into `media/carousels/inbox/` are not automatically published. Follow this 4-step curation pipeline:

### 1. Drop Raw Photos
Place raw photographs into `media/carousels/inbox/`. Accepted formats: JPG, PNG, WEBP, HEIC.

### 2. Curate & Optimize
1. Select the strongest editorial or action photographs (prefer action photography over stiff poses).
2. Resize to web dimensions (e.g. max width 1600px, aspect ratio 4:3 or 16:9).
3. Convert to web-ready JPEG or WEBP.
4. Move the optimized file from `inbox/` into its target folder:
   - `media/ventures/` for venture programs, Schulich Startups, Telenor, Digital Main Street
   - `media/teaching/` for Schulich classrooms, workshops, executive sessions
   - `media/doodlepad/` for founder milestones, YSpace, team, product showcases

### 3. Register Metadata in `registry.json`
Add an entry under the corresponding carousel key in `media/carousels/registry.json` with the required fields:
- `id`: Unique kebab-case identifier
- `src`: Absolute web path (e.g. `/media/ventures/photo.jpeg`)
- `alt`: Descriptive accessibility text for screen readers
- `caption`: Editorial caption displayed beneath the image
- `year`: Year of the event/project
- `event`: Event or milestone name
- `project`: Associated organization or project
- `order`: Display order integer (1, 2, 3...)
- `relatedPage`: Target page (`ventures`, `teaching`, `home`, `product`)

### 4. Embed in Web Pages
Use the standard semantic, accessible carousel markup:

```html
<div class="carousel-container" data-carousel-id="schulich-startup-night-2021" role="region" aria-roledescription="carousel" aria-label="Schulich Startup Night 2021 Photo Archive">
  <div class="carousel-track">
    <!-- Slide 1 -->
    <figure class="carousel-slide" aria-roledescription="slide" aria-label="1 of 2">
      <img src="/media/ventures/schulich-startup-night-2021-speaking.jpeg" alt="..." loading="lazy" width="1600" height="1067">
      <figcaption>
        <span class="carousel-tag">2021 · Schulich Startup Night</span>
        <p>Tamzid Azad speaking at Schulich Startup Night 2021 · Toronto</p>
      </figcaption>
    </figure>
    <!-- Slide 2 -->
    ...
  </div>
  <div class="carousel-controls">
    <button type="button" class="carousel-btn prev" aria-label="Previous slide" disabled>←</button>
    <span class="carousel-counter" aria-live="polite">1 / 2</span>
    <button type="button" class="carousel-btn next" aria-label="Next slide">→</button>
  </div>
</div>
```
