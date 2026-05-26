---
tag: focus-zones
memory_count: 3
date_range: 2026-03-27 to 2026-03-27
---

# focus-zones

_3 memories from Muninn's past, primary tag `focus-zones`._

## 2026-03-27 — procedure (df874f11)
_tags: image-processing, seeing-images, precision-workflow, luminance-thresholding_

FOCUS ZONE REFINED WORKFLOW — zoom-first precision (vintage B&W test case, 2026-03-27):

PROBLEM: My raw vision coordinates are terrible. Face ellipse covered the hat band, beard polygon was wrong shape, hands were in wrong location.

SOLUTION PIPELINE (tested on HipsterElf.jpg where MP face detection fails):
1. grid(photo, rows=5, cols=4) → orient spatially
2. crop() into each semantic area I identified (face+hat, hands+stick)
3. sample() horizontal and vertical scan lines through each area to find luminance transitions:
   - Hat band: L=89 at y≈120 (darkest feature in face region)
   - Eyes: L=112 and L=144 at y=158 (dark spots in skin-toned band)
   - Face skin: L=130-200 range
   - Beard: L>200 (bright white)
   - Jacket: L<100 (dark)
   - Walking stick: L=31-54 (very dark, thin diagonal)
4. Create binary masks via luminance thresholding within semantic regions:
   - face = skin_toned (L=120-195) & person_mask & y∈[125,195] & x∈[215,300]
   - beard = bright (L=185-245) & person_mask & y∈[170,290]
   - hat = dark (L<100) & person_mask & y∈[95,138]
   - hands = skin_toned & person_mask & hand_region
   - stick = dark & person_mask & stick_region
5. Clean with morphological opening/closing, keep largest connected component
6. Layer into zone map: person→periphery, beard/hat/hands/stick→focus edge, face→focus target

KEY INSIGHT: My vision provides the WHAT (semantic labels) and rough WHERE. Zoom (crop) + luminance sampling provides PRECISE boundaries. MP provides the person silhouette constraint. The three work together — none alone is sufficient.

The luminance thresholding works because in B&W photos, different semantic regions map to distinct luminance bands. This wouldn't work as cleanly in color photos (use LAB channels, or per-channel thresholds instead).

---

## 2026-03-27 — procedure (6b6da1df)
_tags: image-processing, mediapipe, technical-reference, face-landmarks_

FOCUS ZONE DETECTION — TECHNICAL DETAILS:

MEDIAPIPE MODELS USED:
- selfie_segmenter.tflite (person/bg segmentation, confidence mask)
- blaze_face_short_range.tflite (face bounding box + keypoints)
- face_landmarker.task (478 face landmarks for face oval + feature polygons)
Download from storage.googleapis.com/mediapipe-models/...

FACE LANDMARK INDICES:
- Face oval: [10,338,297,332,284,251,389,356,454,323,361,288,397,365,379,378,400,377,152,148,176,149,150,136,172,58,132,93,234,127,162,21,54,103,67,109]
- Left eye: [33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]
- Right eye: [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]
- Left brow: [70,63,105,66,107,55,65,52,53,46]
- Right brow: [300,293,334,296,336,285,295,282,283,276]
- Outer mouth: [61,146,91,181,84,17,314,405,321,375,291,409,270,269,267,0,37,39,40,185]
- Nose bridge: [168,6,197,195,5,4,1,2]

IM SALIENCY MAPS (cheap): edge detection (-edge 2), color saliency (difference from blur), multiscale edge
IM SALIENCY MAPS (expensive): local variance (-statistic StandardDeviation 11x11 takes ~2.5s alone)

SEGMENTATION CONFIDENCE: Use confidence_masks[0] (not category_mask). Threshold at 0.5 for binary.

MULTI-PASS: Generate IM transforms (auto-level, equalize, contrast-stretch, brightness/darkness, saturate/desat, grayscale, invert, sharpen, blur, R/G/B channels, LAB channels, gamma). Run MP on each. Stack masks → agreement map. Boundary gradient of agreement = transition zones. Landmark median across passes = robust positions.

FAILURE MODES: Inverted images break face detection. LAB-A channel breaks segmentation entirely. Saturation channel breaks face detection. These are useful perturbation probes.

---

## 2026-03-27 — analysis (273c99ce)
_tags: image-processing, mediapipe, imagemagick, saliency, seeing-images, pipeline-architecture_

FOCUS ZONE DETECTION: Three-image experiment (Mona Lisa, modern portrait, vintage B&W photo).

PIPELINE ARCHITECTURE (emerged from testing):
1. Claude vision → semantic skeleton (face location, important objects, compositional hierarchy). Irreplaceable — works on paintings, modern photos, vintage B&W. Neither MP nor saliency can replace semantic understanding.
2. MediaPipe → pixel-precise boundaries. Person silhouette always works. Face landmarks when detectable (failed on vintage B&W: 0/22 passes found landmarks). Cheap enough for multi-pass (22 passes × 3 models = ~1.2-1.5s total, 53-67ms/pass).
3. ImageMagick saliency → texture-level refinement. MUST be gated to within-person regions. Never leads, only promotes within MP person mask.

ZONE HIERARCHY: Focus Target (eyes/nose/mouth) → Focus Edge (face boundary, hands, distinctive features) → Periphery (body/clothing) → Background.

KEY FINDINGS:
- MP overhead vs IM saliency is effectively zero (53ms vs 12.3s for IM statistical filters)
- Multi-pass MP (22 IM transforms fed through MP) gives soft segmentation boundaries via agreement map. Landmarks are rock-stable (1-2px jitter). Main value is boundary softness, not feature detection.
- Saliency-first ordering fails on textured clothing (gingham shirt registered hotter than face) and architectural backgrounds (wood siding > face in B&W photo)
- MP-first fails when face detection fails (vintage/unusual images)
- Vision-first with MP+saliency refinement is the robust universal approach

OPTIMAL WORKFLOW: grid() to orient → crop()/zoom into areas of interest → sample() boundary transitions → draw masks with verified coordinates → MP for silhouette → saliency for within-person promotion only.

FOUR APPROACHES TESTED: MP Only, MP→Saliency refine, Saliency→MP constrain, Weighted Fusion. No single ordering wins across all images. Vision-led is the answer.

---
