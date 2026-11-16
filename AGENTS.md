# Working on this drawing

## Scope

Use Python vector drawing. Keep each visual element in its own script under
`yueyue/elements/`; keep paint order in `yueyue/composition.py`. Implement the user's
current art request without adding an editor, animation system or general framework.
Judge the rendered image, not only the source. Aesthetics take priority over showing
every profile detail. The tail, teeth and ribbon cross are intentionally absent.

## Frozen horns — explicit user instruction

The viewer-left and viewer-right horns are independent and frozen until the user
explicitly unfreezes the relevant horn. Do not alter either horn's geometry,
placement, size, angle, shading, ridges, grain, random seed, colors or outlines.
`horn_left.py`, `horn_right.py` and `_horn_surface.py` own these frozen properties.
Shared canvas or dependency changes must preserve their rendered appearance too.
Do not update the expected hashes in `tests/test_frozen_horns.py` merely because a
change fails. Hair root tufts are a separate hair layer; do not merge them into a horn.

## Element ownership

`head.py` owns the complete skull and neck. `hair.py` covers that skull in the same
local coordinate frame, with natural volume; keep the ears and cheek sides covered.
`face.py` owns the expression. `ribbon.py` owns the bow/rose; additional ribbon detail
is deferred. `clothing.py` owns fabric and collar, not skin. Keep the cross removed.

## Verify

Run `python draw_yueyue.py` and inspect the PNG after visual edits. Render affected
parts with `--element` when useful. Run `python -m unittest discover -s tests -v`
after refactoring, changing dependencies or changing shared drawing helpers.
Keep `docs/preview.png` consistent with the final portrait. Do not introduce unrelated
checks or use a changed baseline to conceal an unapproved horn modification.
