#!/usr/bin/env python3
"""Validate rendered figures for one media-object cache audit.

The audit pipeline publishes SVGs directly, so a file can be well-formed yet
still be unusable (for example, an accessible wrapper containing only the
primary graph polyline).  These checks describe the structural contract the
page builder and staging pass require.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET


AUDIT_PLATE_STEM = "earth-ck-44-22.gray-water242-landwhite"
XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
GE_1080P_UNAVAILABLE_MARKER = (
    "UNAVAILABLE — no collection members at 1080p or 2160 resolution.")
WIKIPEDIA_UNAVAILABLE_MARKER = (
    "UNAVAILABLE — no English Wikipedia page exists")


class FigureValidationError(ValueError):
    """A rendered figure is syntactically valid but structurally incomplete."""


def _tag(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def _parse(path: pathlib.Path) -> ET.Element:
    try:
        return ET.parse(path).getroot()
    except (ET.ParseError, OSError) as error:
        raise FigureValidationError(f"{path}: invalid SVG: {error}") from error


def _require(condition: bool, path: pathlib.Path, message: str) -> None:
    if not condition:
        raise FigureValidationError(f"{path}: {message}")


def _group(root: ET.Element, identifier: str) -> ET.Element | None:
    return next(
        (element for element in root.iter()
         if _tag(element) == "g" and element.get("id") == identifier),
        None,
    )


def _groups_with_prefix(root: ET.Element, prefix: str) -> list[ET.Element]:
    return [
        element for element in root.iter()
        if _tag(element) == "g" and element.get("id", "").startswith(prefix)
    ]


def _children(element: ET.Element | None, tag: str) -> list[ET.Element]:
    if element is None:
        return []
    return [child for child in element.iter() if _tag(child) == tag]


def _text_values(root: ET.Element) -> list[str]:
    return [
        " ".join("".join(element.itertext()).split())
        for element in root.iter()
        if _tag(element) == "text"
    ]


def _load_document(path: pathlib.Path | None) -> dict:
    if path is None:
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise FigureValidationError(
            f"{path}: invalid visualization document: {error}") from error
    return value if isinstance(value, dict) else {}


def validate_histogram(path: pathlib.Path,
                       document_path: pathlib.Path | None = None) -> dict:
    """Validate bars, titles, axes, and the four-or-more x-tick contract."""
    root = _parse(path)
    document = _load_document(document_path)
    texts = _text_values(root)
    expected_x = str(document.get("x_label") or "SIZE IN GB")
    expected_y = str(document.get("y_label") or "MEDIA OBJECTS")
    expected_title = str(document.get("title") or "")

    bars = _group(root, "histogram-bars")
    axes = _group(root, "axes-lines")
    x_ticks = _group(root, "tic-x-labels")
    y_ticks = _group(root, "tic-y-labels")
    bar_count = len(_children(bars, "rect"))
    x_tick_mark_count = len(_children(x_ticks, "line"))
    x_tick_label_count = len(_children(x_ticks, "text"))
    x_tick_values = [" ".join("".join(element.itertext()).split())
                     for element in _children(x_ticks, "text")]

    _require(bar_count > 0, path, "histogram-bars has no rendered bars")
    _require(len(_children(axes, "line")) >= 2, path,
             "axes-lines does not contain both axes")
    _require(expected_x in texts, path,
             f"missing exact x-axis title {expected_x!r}")
    _require(expected_y in texts, path,
             f"missing exact y-axis title {expected_y!r}")
    if expected_title:
        _require(expected_title in texts, path,
                 f"missing visible graph title {expected_title!r}")
    else:
        annotation_nodes = {
            id(element)
            for group in (axes, x_ticks, y_ticks)
            for element in _children(group, "text")
        }
        visible_titles = [
            " ".join("".join(element.itertext()).split())
            for element in root.iter()
            if _tag(element) == "text" and id(element) not in annotation_nodes
        ]
        _require(any(visible_titles), path, "missing visible graph title")
    _require(x_tick_mark_count >= 4, path,
             "fewer than four x-axis tick marks")
    _require(x_tick_label_count >= 4, path,
             "fewer than four x-axis tick labels")
    _require(x_tick_mark_count == x_tick_label_count, path,
             "x-axis tick marks and labels do not pair one-to-one")
    _require(len(set(x_tick_values)) == x_tick_label_count, path,
             "x-axis tick labels are not distinct")
    _require(len(_children(y_ticks, "line")) > 0
             and len(_children(y_ticks, "text")) > 0,
             path, "missing y-axis ticks or labels")

    return {
        "role": "histogram",
        "status": "passed",
        "bars": bar_count,
        "x_tick_marks": x_tick_mark_count,
        "x_tick_labels": x_tick_label_count,
        "x_label": expected_x,
        "y_label": expected_y,
    }


def validate_line_graph(path: pathlib.Path,
                        document_path: pathlib.Path | None = None,
                        period: str | None = None) -> dict:
    """Validate the complete annotation and dual-series line-graph surface."""
    root = _parse(path)
    document = _load_document(document_path)
    period = period or str(document.get("x_label") or "").lower()
    if period not in ("week", "day"):
        period = "day" if "by-day" in path.name else "week"
    expected_x = str(document.get("x_label") or period).upper()
    expected_y = str(document.get("y_label") or "downloaders").upper()
    expected_title = str(document.get("title") or "")
    texts = _text_values(root)

    axes = _group(root, "axes-lines")
    x_ticks = _group(root, "tic-x-labels")
    y_ticks = _group(root, "tic-y-labels")
    polylines = [element for element in root.iter()
                 if _tag(element) == "polyline"]
    primary_groups = [
        group for group in _groups_with_prefix(root, "polyline-")
        if "uploaders" not in group.get("id", "")
    ]
    secondary_groups = [
        group for group in _groups_with_prefix(root, "polyline-")
        if "uploaders" in group.get("id", "")
    ]

    axis_titles = _text_values(axes) if axes is not None else []
    _require(expected_x in axis_titles and expected_y in axis_titles, path,
             "axes-lines does not contain both axes with exact titles")
    if expected_title:
        _require(expected_title in texts, path,
                 f"missing visible graph title {expected_title!r}")
    else:
        _require(any(f"downloads by {period}" in text.lower()
                     for text in texts),
                 path, f"missing visible downloads-by-{period} title")
    _require(len(_children(x_ticks, "text")) > 0,
             path, "missing x-axis tick labels")
    _require(len(_children(y_ticks, "text")) > 0,
             path, "missing y-axis tick labels")
    _require(len(polylines) >= 2 and primary_groups and secondary_groups,
             path, "missing primary or uploader polyline series")

    if period == "week":
        marker_groups = _groups_with_prefix(root, "markers-")
        marker_circles = [
            circle for group in marker_groups
            for circle in _children(group, "circle")
        ]
        _require(marker_groups and marker_circles,
                 path, "week graph is missing marker/tool-tip circles")
        _require(all(_children(circle, "title")
                     for circle in marker_circles),
                 path, "week graph marker circle is missing its title "
                       "tool-tip")
    else:
        ranges = document.get("weekend_x_ranges", [])
        # Weekend bands are required only when the day document proves the
        # sample contains a weekend.  Callers without the document (figure
        # revalidation) defer to the document-aware generation pass; a short
        # working-week sample legitimately has no bands to draw.
        if ranges:
            weekend_groups = _groups_with_prefix(root, "weekend-bands-")
            _require(weekend_groups
                     and any(_children(group, "rect")
                             for group in weekend_groups),
                     path, "day graph is missing weekend bands")

    return {
        "role": f"{period}-graph",
        "status": "passed",
        "polylines": len(polylines),
        "x_tick_labels": len(_children(x_ticks, "text")),
        "y_tick_labels": len(_children(y_ticks, "text")),
    }


def validate_plate_reference(path: pathlib.Path,
                             plate_stem: str = AUDIT_PLATE_STEM) -> dict:
    root = _parse(path)
    expected = f"{plate_stem}.png"
    references = [
        element.get("href") or element.get(XLINK_HREF) or ""
        for element in root.iter()
        if _tag(element) == "image"
    ]
    _require(any(reference.endswith(expected) for reference in references),
             path, f"does not reference shared audit plate {expected}")
    return {
        "status": "passed",
        "plate": plate_stem,
        "image_references": references,
    }


def validate_cumulative_data_map(path: pathlib.Path,
                                 plate_stem: str = AUDIT_PLATE_STEM,
                                 topn: int = 10,
                                 allow_equal_sizes: bool = False) -> dict:
    result = validate_plate_reference(path, plate_stem)
    root = _parse(path)
    layer = _group(root, "text-geolocation-text")
    labels = _children(layer, "text")
    _require(layer is not None, path,
             "missing text-geolocation-text layer")
    _require(0 < len(labels) <= topn, path,
             f"expected 1..{topn} top-location labels, found {len(labels)}")

    top_level = list(root)
    layer_index = next(
        (index for index, element in enumerate(top_level)
         if element is layer), -1)
    vector_indices = [
        index for index, element in enumerate(top_level)
        if (_tag(element) == "g"
            and element.get("id", "").startswith("vector-peer-clouds"))
    ]
    _require(vector_indices and layer_index > max(vector_indices), path,
             "top-location labels are not above the vector glyph layer")

    sizes: list[float] = []
    label_values: list[str] = []
    for label in labels:
        style = re.sub(r"\s+", "", label.get("style", "")).lower()
        fill = re.sub(r"\s+", "", label.get("fill", "")).lower()
        _require("fill:rgb(0,0,0)" in style
                 or fill in ("rgb(0,0,0)", "#000", "#000000", "black"),
                 path, "top-location label is not black")
        size = label.get("font-size", "").removesuffix("pt")
        try:
            sizes.append(float(size))
        except ValueError as error:
            raise FigureValidationError(
                f"{path}: top-location label has no numeric font size") \
                from error
        label_values.append(" ".join("".join(label.itertext()).split()))

    _require(allow_equal_sizes or len(labels) < topn
             or len({round(size, 6) for size in sizes}) > 1, path,
             "top-location labels are present but not visibly sized")

    result.update({
        "role": "cumulative-data-map",
        "labels": label_values,
        "label_count": len(labels),
        "font_sizes": sizes,
    })
    return result


def validate_audit_bundle(audit_dir: pathlib.Path, key: str,
                          require_render_receipt: bool = True) -> dict:
    """Validate copied page figures and the upstream render receipt."""
    manifest_path = audit_dir / "figure-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise FigureValidationError(
            f"{manifest_path}: missing or invalid figure manifest") from error
    figures = manifest.get("figures", {})
    _require(isinstance(figures, dict), manifest_path,
             "figures is not an object")

    def figure(role: str) -> pathlib.Path:
        entry = figures.get(role, {})
        relative = entry.get("file") if isinstance(entry, dict) else None
        _require(isinstance(relative, str), manifest_path,
                 f"missing {role} figure entry")
        path = audit_dir / relative
        _require(path.is_file(), manifest_path,
                 f"missing {role} figure {path}")
        return path

    checks = {
        "histogram": validate_histogram(figure("histogram")),
        "week": validate_line_graph(figure("week"), period="week"),
        "day": validate_line_graph(figure("day"), period="day"),
    }
    receipt = manifest.get("render_receipt", {})
    if require_render_receipt:
        _require(isinstance(receipt, dict)
                 and receipt.get("status") == "passed",
                 manifest_path, "render receipt is absent or not passed")
        validations = receipt.get("validations", {})
        required_roles = []
        if "carto-map" in figures:
            required_roles.append("network-map")
        if "data-map-data-ge-1080p" in figures:
            required_roles.append("data-map-ge-1080p")
        if "data-map-data-lt-1080p" in figures:
            required_roles.append("data-map-lt-1080p")
        for role in required_roles:
            _require(isinstance(validations.get(role), dict)
                     and validations[role].get("status") == "passed",
                     manifest_path,
                     f"render receipt has no passed {role} validation")

    return {
        "schema": "alpha60-media-object-audit-validation/1",
        "media_object": key,
        "status": "passed",
        "checks": checks,
    }


def validate_country_map(path: pathlib.Path, receipt: dict, variant: dict) -> dict:
    """Require vector-only country geometry and contained, weighted glyphs."""
    root = _parse(path)
    _require(not _children(root, "image"), path, "country plate contains an image")
    ids = [e.get("id") for e in root.iter() if e.get("id")]
    _require(len(ids) == len(set(ids)), path, "duplicate SVG IDs")
    width, height = receipt["page"]
    _require(list(map(float, root.get("viewBox").split())) == [0,0,width,height],
             path, "country viewBox disagrees with receipt")
    groups = [e for e in root.iter() if e.get("data-country")]
    _require(len(groups) == len(receipt["panels"]), path, "missing country panels")
    circles = 0
    area_weight = 0.0
    for group, panel in zip(groups, receipt["panels"]):
        _require(group.get("data-country") == receipt["country"] and
                 group.get("data-group") == variant["group"] and
                 group.get("data-panel") == panel["id"], path, "wrong country panel")
        x,y,w,h = panel["rect"]
        for circle in _children(group, "circle"):
            cx,cy,r = (float(circle.get(k)) for k in ("cx","cy","r"))
            _require(r >= 0 and cx-r >= x-.01 and cy-r >= y-.01 and
                     cx+r <= x+w+.01 and cy+r <= y+h+.01,
                     path, "country bubble is outside its panel")
            area_weight += (r/receipt["radius_base"])**2
            circles += 1
    _require(circles > 0, path, "no downloader bubbles")
    # izzi serializes radii to a finite precision; tolerate that rounding only.
    _require(abs(area_weight-variant["downloaders"]) <= max(1,variant["downloaders"]*2e-6),
             path, "bubble areas do not conserve downloader weight")
    _require(bool(_children(root,"path")) and bool(_children(root,"text")),
             path, "missing vector outlines or labels")
    # Current detail maps reuse the cumulative-audit text layer unchanged.
    # Older receipts without positions remain readable as historical evidence.
    labels = [v for v in variant["labels"] if v.get("position")]
    if labels:
        layer = next((e for e in root.iter() if e.get("id") == "text-geolocation-text"), None)
        _require(layer is not None, path, "missing audit location text layer")
        texts = _children(layer, "text")
        _require(len(texts) == len(labels), path, "audit location label count differs")
        remaining = list(texts)
        for label in labels:
            text = next((e for e in remaining if "".join(e.itertext()).strip() == label["city"]), None)
            _require(text is not None, path, "location name differs from accounting")
            remaining.remove(text)
            _require(all(abs(float(text.get(a))-p) < .01 for a,p in zip(("x","y"), label["position"])),
                     path, "location label is offset from its mapped position")
            style = re.sub(r"\s+", "", text.get("style", ""))
            _require(text.get("text-anchor") == "middle" and text.get("font-family") == "Apercu",
                     path, "location text differs from audit typography")
            _require("fill:rgb(0,0,0)" in style and "stroke:rgb(255,255,255)" in style
                     and "stroke-width:0.3" in style, path, "location outline style differs from audit")
        _require(not _children(layer,"path") and not _children(layer,"rect"),
                 path, "location text layer contains callouts")
    return {"file":path.name,"status":"passed","circles":circles,
            "area_weight":area_weight,"vector_only":True,"glyph_containment":True,
            "audit_location_labels_checked":len(labels)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--audit-dir", type=pathlib.Path, required=True)
    parser.add_argument("--media-object", required=True)
    parser.add_argument("--allow-missing-render-receipt", action="store_true")
    args = parser.parse_args()
    try:
        result = validate_audit_bundle(
            args.audit_dir, args.media_object,
            require_render_receipt=not args.allow_missing_render_receipt)
    except FigureValidationError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
