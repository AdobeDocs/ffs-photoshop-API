#!/usr/bin/env python3
"""
figma_full_extract_and_combine.py

Single-script workflow:
 - Fetch a frame node (FRAME_NODE_ID) from a Figma file (FILE_KEY)
 - Traverse frame children and collect node IDs + metadata
 - Fetch absoluteBoundingBox for each node
 - Use /v1/images to render each node as PNG and download to exports/
 - Save exports/node_meta.json with metadata & filenames
 - Combine downloaded PNGs into one composite using document absolute coordinates

Usage example:
  export FIGMA_TOKEN="..."
  python figma_full_extract_and_combine.py \
    --file_key <FILE_KEY> \
    --frame_node_id 12:345 \
    --token $FIGMA_TOKEN \
    --exports_dir exports \
    --out composite.png \
    --scale 2 \
    --batch_size 40 \
    --force_resize

Notes:
 - FRAME_NODE_ID is required. Convert from Figma URL node-id format (12-345 -> 12:345).
 - Token must have access to the file.
"""

import os
import re
import sys
import json
import time
import argparse
from math import ceil
from tqdm import tqdm
import requests
from PIL import Image
from dotenv import load_dotenv
import boto3
import uuid

load_dotenv()

access_key = os.getenv("AWS_S3_ACCESS_KEY")
secret_key = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
region = os.getenv("AWS_S3_REGION")
# ---------------- Helpers -----------------
def safe_filename(name: str, node_id: str, ext="png"):
    name = (name or "unnamed").strip()
    name = re.sub(r'[\\/:"*?<>|]+', "_", name)
    name = re.sub(r"\s+", "_", name)
    short_id = node_id.replace(":", "-")
    maxlen = 80
    if len(name) > maxlen:
        name = name[:maxlen]
    return f"{name}__{short_id}.{ext}"

def mkdir_p(p):
    os.makedirs(p, exist_ok=True)

# -------------- Figma API helpers --------------
def figma_get_file(file_key, token):
    url = f"https://api.figma.com/v1/files/{file_key}"
    headers = {"X-Figma-Token": token}
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def figma_get_nodes(file_key, ids, token):
    url = f"https://api.figma.com/v1/files/{file_key}/nodes"
    headers = {"X-Figma-Token": token}
    params = {"ids": ",".join(ids)}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json().get("nodes", {})

def figma_request_images(file_key, ids, token, fmt="png", scale=2):
    url = f"https://api.figma.com/v1/images/{file_key}"
    headers = {"X-Figma-Token": token}
    params = {"ids": ",".join(ids), "format": fmt, "scale": str(scale)}
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json()

def check_text_node(node):
    for c in node.get("children", []):
        if c.get("type") == "TEXT":
            return True
        else:
            return False

# --------------- Node traversal ---------------
def traverse_collect(node, parent_path=""):
    out = []
    nid = node.get("id")
    name = node.get("name", "")
    typ = node.get("type", "UNKNOWN")
    path = f"{parent_path}/{name}" if name else parent_path
    # if typ != "GROUP":
        # out.append({"id": nid, "name": name, "type": typ, "path": path})
    # out.append({"id": nid, "name": name, "type": typ, "path": path})
    check_text = check_text_node(node)
    if check_text:
        for c in node.get("children", []):
            out.extend(traverse_collect(c, parent_path=path))
    else:
        out.append({"id": nid, "name": name, "type": typ, "path": path})
    return out

# --------------- Combining utilities ---------------
def compute_document_canvas(metadata):
    xs, ys, xs_w, ys_h = [], [], [], []
    for m in metadata:
        b = m.get("absoluteBoundingBox")
        if not b:
            continue
        xs.append(b["x"])
        ys.append(b["y"])
        xs_w.append(b["x"] + b["width"])
        ys_h.append(b["y"] + b["height"])
    if not xs:
        raise RuntimeError("No bounding boxes found to compute document canvas.")
    left = min(xs)
    top = min(ys)
    right = max(xs_w)
    bottom = max(ys_h)
    width = max(1, int(ceil(right - left)))
    height = max(1, int(ceil(bottom - top)))
    return {"left": left, "top": top, "width": width, "height": height}

def open_image_rgba(path):
    return Image.open(path).convert("RGBA")

def layers_placement(canvas_size=(1200, 1200)):
    with open("./exports/node_meta.json", "r") as f:
        nodes = json.load(f)
    for i in nodes:
        canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        filename = i.get("filename")
        component_path = f"./exports/{filename}"
        if not os.path.exists(component_path):
            continue

        bbox = i.get("absoluteBoundingBox")
        if bbox['width'] == 1200 and bbox['height'] == 1200:
            continue
        render_box = i.get("absoluteRenderBounds")
        if render_box is None:
            x_coord = bbox['x']
            y_coord = bbox['y']
        elif (bbox["x"]< 0 and render_box['x']>0) or (bbox["x"]>0 and render_box['x']<0):
            x_coord = render_box['x']
            y_coord = render_box['y']
        else:
            x_coord_abs = abs(render_box['x'])
            x_coord_abs_bbox = abs(bbox['x'])
            if x_coord_abs > x_coord_abs_bbox:
                x_coord = render_box['x']
                y_coord = render_box['y'] 
            else:
                x_coord = bbox['x']
                y_coord = bbox['y']
        frame_x = 0
        frame_y = 0

        # Compute placement coordinates
        x = round(x_coord - frame_x)
        y = round(y_coord - frame_y)
        component = Image.open(component_path).convert("RGBA")
        canvas.paste(component, (x, y), component)
        # Save final output
        canvas.save(component_path)
        print(f"💾 Saved to: {component_path}")


# --------------- Main flow ---------------
def run_all(file_key, frame_node_id, token, exports_dir="exports", meta_out="exports/node_meta.json",
            batch_size=50, scale=1, image_format="png", out_composite="composite.png", force_resize=False, debug_outline=False):

    mkdir_p(exports_dir)

    # 1) fetch the frame node document
    print("Fetching frame node document for:", frame_node_id)
    nodes_resp = figma_get_nodes(file_key, [frame_node_id], token)
    frame_entry = nodes_resp.get(frame_node_id)
    if not frame_entry:
        raise SystemExit(f"Could not fetch frame node {frame_node_id}. Check file_key, node id and token permissions.")
    frame_doc = frame_entry.get("document") or frame_entry.get("components") or frame_entry
    # find name and type and children
    frame_name = frame_doc.get("name", "FRAME")
    frame_type = frame_doc.get("type", "FRAME")

    print(f"Frame: {frame_name} ({frame_type})")

    # 2) collect nodes under the frame children (only children of frame, not whole file)
    children = frame_doc.get("children", [])

    bbox = frame_doc["absoluteBoundingBox"]

    width = bbox["width"]
    height = bbox["height"]

    if not children:
        print("Warning: frame has no children. Exiting.")
        return

    collected = []
    for child in children:
        collected.extend(traverse_collect(child, parent_path=frame_doc.get("name","/ROOT")))

    # de-duplicate by id preserving order
    seen = set()
    unique_nodes = []
    for n in collected:
        if n["id"] in seen:
            continue
        seen.add(n["id"])
        unique_nodes.append(n)

    print(f"Collected {len(unique_nodes)} unique nodes under the frame (including nested).")

    # 3) fetch absoluteBoundingBox for all nodes via nodes endpoint
    node_ids = [n["id"] for n in unique_nodes]
    # chunk requests if large
    nodes_docs = {}
    chunk_size = 100  # Figma nodes endpoint allows many ids; keep chunks
    for i in range(0, len(node_ids), chunk_size):
        batch = node_ids[i:i+chunk_size]
        print(f"Fetching node doc batch {i//chunk_size + 1} / {ceil(len(node_ids)/chunk_size)} ...")
        docs = figma_get_nodes(file_key, batch, token)
        for nid, obj in docs.items():
            nodes_docs[nid] = obj.get("document", obj)

    # 4) build metadata objects with bounding boxes
    metadata = []
    for n in unique_nodes:
        nid = n["id"]
        doc = nodes_docs.get(nid, {})
        # if doc["type"] != "TEXT":
        #     continue
        bbox = doc.get("absoluteBoundingBox")
        rbound = doc.get("absoluteRenderBounds")
        style = doc.get("style", {}),
        constraints = doc.get("constraints", {})
        characters = doc.get("characters", "")
        strokealign = doc.get("strokeAlign", "")
        strokeweight = doc.get("strokeWeight", 0)
        fills = doc.get("fills", [])
        meta = {
            "id": nid,
            "name": n.get("name"),
            "type": n.get("type"),
            "path": n.get("path"),
            "absoluteBoundingBox": bbox,
            "absoluteRenderBounds": rbound,
            "frame_node_id": frame_node_id,
            "frame_name": frame_name,
            "style": style,
            "constraints": constraints,
            "characters": characters,
            "strokeAlign": strokealign,
            "strokeWeight": strokeweight,
            "fills": fills
        }
        metadata.append(meta)

    # 5) Request images (images endpoint) in batches and download
    print(f"Requesting images for {len(node_ids)} nodes (format={image_format}, scale={scale}) ...")
    failed = []
    images_map = {}
    for i in range(0, len(node_ids), batch_size):
        batch = node_ids[i:i+batch_size]
        try:
            resp = figma_request_images(file_key, batch, token, fmt=image_format, scale=scale)
        except Exception as e:
            print(f"Images request failed for batch starting at {i}: {e}")
            # mark these as failed and continue
            for nid in batch:
                failed.append({"id": nid, "error": str(e)})
            time.sleep(1)
            continue
        images = resp.get("images", {})
        # Download images that returned URLs
        for nid in batch:
            url = images.get(nid)
            if not url:
                failed.append({"id": nid, "error": "No URL returned"})
                continue
            filename = safe_filename(next((m["name"] for m in metadata if m["id"]==nid), "unnamed"), nid, ext=image_format)
            dest = os.path.join(exports_dir, filename)
            try:
                # stream download
                dl = requests.get(url, stream=True)
                dl.raise_for_status()
                with open(dest, "wb") as fh:
                    for chunk in dl.iter_content(1024*32):
                        if chunk:
                            fh.write(chunk)
                images_map[nid] = filename
            except Exception as e:
                failed.append({"id": nid, "error": str(e)})
        time.sleep(0.12)

    # attach filenames to metadata
    for m in metadata:
        m["filename"] = images_map.get(m["id"])

    # persist node_meta.json
    mkdir_p(os.path.dirname(meta_out))
    with open(meta_out, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"Saved metadata to {meta_out}. {len([m for m in metadata if m.get('filename')])} images downloaded, {len(failed)} failures.")
    layers_placement((int(width), int(height)))

# -------------- CLI --------------
if __name__ == "__main__":
    file_key = "DHQ3LE7GcwSAIGUSlj3U9x"
    frame_node_id = '19:209'
    token = os.getenv("figma_token")
    exports_dir = "exports"
    meta_out = "exports/node_meta.json"
    out = "composite.png"
    batch_size = 40
    scale = 1
    image_format = "png"  # or "svg"
    force_resize = True
    debug_outline = True

    try:
        run_all(file_key=file_key,
                frame_node_id=frame_node_id,
                token=token,
                exports_dir=exports_dir,
                meta_out=meta_out,
                batch_size=batch_size,
                scale=scale,
                image_format=image_format,
                out_composite=out,
                force_resize=force_resize,
                debug_outline=debug_outline)
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
