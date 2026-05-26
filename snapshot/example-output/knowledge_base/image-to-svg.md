---
tag: image-to-svg
memory_count: 5
date_range: 2026-03-26 to 2026-04-01
---

# image-to-svg

_5 memories from Muninn's past, primary tag `image-to-svg`._

## 2026-04-01 — procedure (b86b8d02)
_tags: warhol, svg, squirrel, animation, project_

WARHOL SQUIRREL SVG PROJECT — session findings (2026-03-31)

SOURCE: IMG_5015.jpeg — close-up squirrel photo, 4032x3024.
Downscaled to 400x300, then image-to-svg pipeline.

GRID SETUP (working):
- 2x2 grid, each cell 300x300
- Each image rotated 90° CW: transform="rotate(90, cx, cy)"
- Square crop from 400x300: clip to center 300px, crop_x=50
- Clip paths per quadrant to contain overflow

WHAT FAILED FOR COLOR CYCLING:
1. feColorMatrix hueRotate with continuous from/to animation: all 4 quadrants converge to same hue regularly, even with different speeds/offsets. Fundamental problem — adjacent hue ranges look similar.
2. Oscillating within 90° hue bands (bounded arcs): still converge because neighboring bands (green/cyan, blue/purple) are perceptually close. 3 of 4 were green simultaneously.
3. Discrete SMIL visibility cycling of 4 baked palettes: guarantees separation but feels like a slideshow (hard cuts every 2s). Mechanically correct but aesthetically dead.

WHAT WORKS:
- image_to_svg_batch() with shared K=16: generates structurally identical paths with different palette remaps. ~136KB per variant, 320 paths each. Same contours, different fills.
- 4 distinct palettes that read well: hot (#1a0a1a/#e8173e/#ff5c8a/#ffe14c), jungle (#0a1a0a/#1b7a2b/#5ce65c/#d4ff7a), ocean (#0a0a2e/#1444cc/#4c99ff/#b8e0ff), grape (#2a0a3a/#8b24aa/#cc66ff/#f0c0ff)
- <symbol> + <use> for deduplicating 4 copies per quadrant (16 total uses, 4 symbols)

NEXT APPROACH TO TRY:
- Smooth animated fill transitions on paths themselves (SMIL animate on fill attribute, cycling through 4 palette colors per path, offset per quadrant)
- Or: cross-fade between palette layers using animated opacity (0→1→0) with overlapping timing
- Key constraint: at any given frame, all 4 quadrants must show visually distinct color schemes

FILES: squirrel_small.jpg (400x300 source), sq_hot/jungle/ocean/grape.svg (4 palette variants)

---

## 2026-03-30 — analysis (d6d08d84)
_tags: quality-scaling, threshold-scaling, issue-502, experiment_

image-to-svg quality scaling investigation: threshold scaling recovers ~30-45% of upscale shape gain for sub-1000px sources.

FINDINGS:
- Area thresholds (MIN_AREA=40, isolation=500) operate in pixel² space — proportionally aggressive on small sources
- Scaling: area_scale=(source_w/1000)², MIN_AREA=max(1,int(40*area_scale)), ISO=max(10,int(500*area_scale))
- At 500px: 1031→2527 shapes (2.5x), at 250px: 228→766 (3.4x), at 1000px: identity (0 change)
- Adding morph iteration scaling + epsilon scaling: marginal (+9% more recovery)
- Removing dilation at low res: actually HURTS — dilation helps fragments coalesce into discoverable contours
- The remaining 55-70% gap comes from spatial merging: 3x3 morph kernels and 1px dilation are proportionally 2x larger at 500px vs 1000px. This is structural, not parametric.

CONCLUSION: Threshold scaling is a clean win (zero-risk at reference res, meaningful gain below). But for high-quality output from small sources, upscaling remains recommended. These are complementary — threshold scaling helps modest detail recovery, upscaling provides the real quality jump.

IMPLEMENTATION: 3-line change in preprocess() + extract_contours(). Ready to file as GitHub issue.

WHY (experience): The hypothesis was threshold scaling alone would get 80% of the upscale gain. Reality: 30%. The detail loss is dominated by morphological operations, not by area filtering. The kernel sizes are the bottleneck, not the threshold values. This is a useful insight about where the pipeline's resolution dependence actually lives.

---

## 2026-03-29 — procedure (b192b25b)
_tags: stash, active, issue-494_

STASH: image-to-svg #494 testing
STATUS: PR #496 merged (or merging). All 4 fixes implemented: mode→pipeline map, exposed stroke params, bezier curve fitting, group-level stroke styling. Plain painting-mode runs verified clean (no Hough strokes). Portrait mode runs verified. Oilpaint variants produced.
NEXT: Continue testing the merged code. Re-run the three paintings through plain image_to_svg to confirm classify_input no longer fires. Test mode="graphic" on actual line art to verify compositional still works. Test new stroke params (stroke_opacity, stroke_blur, stroke_merge, stroke_dasharray).
CONTEXT: Three test images in test_images.zip: starry_night.jpeg (Van Gogh, 500x396), mona_lisa.jpeg (da Vinci, 960x1431), el_greco.jpeg (Christ Driving the Money Changers, 1280x1280). The pre-merge runs showed classify_input misclassifying all three as graphic (Starry Night edge_density=0.34, Mona Lisa 9242 Hough lines from craquelure). Post-merge should route all to fill via MODE_PIPELINE.
ARTIFACTS: Upload test_images.zip to resume testing.

---

## 2026-03-29 — procedure (7620a92d)
_tags: container, network, image-sources, motif-finder_

IMAGE SOURCE DOMAINS FOR CONTAINER ENVIRONMENT

WORKING (tested 2026-03-29):
1. raw.githubusercontent.com — ML repos have sample images:
   - jcjohnson/fast-neural-style/master/images/styles/ → Starry Night, The Scream, The Muse (public domain art)
   - jcjohnson/fast-neural-style/master/images/content/ → Chicago cityscape photo
   - pytorch/hub/master/images/ → dog.jpg (661KB)
   - opencv/opencv/master/samples/data/ → lena.jpg, various test images
   - ultralytics/yolov5/master/data/images/ → zidane.jpg, bus.jpg
   - gradio-app/gradio/main/test/test_files/ → cheetah, various
2. storage.googleapis.com — Google ML samples:
   - /mediapipe-assets/ → portrait.jpg (820x1024), cat.jpg
   - /download.tensorflow.org/example_images/ → sunflower, flower_photos/
   - /tfds-data/visualization/ → dataset visualizations
3. scikit-image bundled: data.astronaut(), data.chelsea(), data.coffee() — already installed

BLOCKED:
- upload.wikimedia.org: proxy returns hostname_blocked despite being in network allowlist
- huggingface.co: redirects fail silently
- images.metmuseum.org: host_not_allowed (not in allowlist)
- cdn-lfs.huggingface.co: connection issues

CONTEXT: Needed for motif-finder/riso pipeline — downloading public domain art for SVG conversion.

---

## 2026-03-26 — decision (1fb5a3b0)
_tags: batch-api, shipped, 2026-03-26_

IMAGE-TO-SVG BATCH API shipped (PR #473, 2026-03-26). Two additions to pipeline.py:

1. _assemble_pure(shapes, svg_w, svg_h, bg_hex, palette, bg_color) — pure function, no global state, doesn't mutate shapes. Enables safe fan-out from shared contour extraction.

2. image_to_svg_batch(source_path, variants, svg_width) — groups variants by K, runs pipeline once per K group, fans out at assembly. Guarantees structural identity across palette variants (same K → identical paths). 3x speedup for 3 palette variants at same K (24s vs 72s measured).

Uses loosest dark-shape gating params across same-K group to ensure all plausible shapes are extracted for every variant.

The real gap wasn't code — it was that K-means is stochastic, so re-running at same K gives different clusters. Batch fixes both the performance AND correctness problem in one move.

---
