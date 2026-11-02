#!/usr/bin/env python3
"""
Build unified, enum-keyed data dictionaries from the four language copies
of each Saves/<...>.xml file.

Usage:
    python build_item_data.py /path/to/data_root
"""

import argparse
import csv
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

LANGUAGE_FOLDERS = {
    "ja": "Saves",
    "en": "Saves_EN",
    "sc": "Saves_SC",
    "tc": "Saves_TC",
}

_CODEC_CANDIDATES = {
    "ja": ["utf-8-sig", "cp932", "shift_jis"],
    "en": ["utf-8-sig", "cp1252"],
    "sc": ["utf-8-sig", "gbk", "gb18030"],
    "tc": ["utf-8-sig", "cp950", "big5"],
}

_XML_DECL_RE = re.compile(r'^\s*<\?xml[^>]*\?>\s*', re.IGNORECASE)

SCRIPT_DIR = Path(__file__).resolve().parent

DATASETS = {
    "itemData": {
        "xml_relative_path": Path("item") / "itemData.xml",
        "enum_path": SCRIPT_DIR / "enums" / "enums_items.txt",
        "tag": "itemData",
        "name_attr": "ItemName",
        "remove_keys": {"元効力値", "効力基準", "元レベル", "レベル", "元属性値", "属性数", "attribute", "補正値"},
    },
    "item_effect": {
        "xml_relative_path": Path("item") / "item_effect.xml",
        "tag": "item_effect",
        "name_attr": "ItemEffectName",
        "remove_keys": {"Lv想定", "効果アイテム", "コスト", "レシピ使用", "属性補正"},
    },
    "item_mat_pot": {
        "xml_relative_path": Path("item") / "item_mat_pot.xml",
        "enum_path": SCRIPT_DIR / "enums" / "enums_traits.txt",
        "tag": "item_mat_pot",
        "name_attr": "EspName",
        "remove_keys": {},
    },
    "item_potential": {
        "xml_relative_path": Path("item") / "item_potential.xml",
        "enum_path": SCRIPT_DIR / "enums" / "enums_properties.txt",
        "tag": "item_potential",
        "name_attr": "PotName",
        "remove_keys": {},
    },
    "item_book": {
        "xml_relative_path": Path("item") / "item_book.xml",
        "tag": "item_book",
        "name_attr": "BookName",
        "remove_keys": {"修得レシピ"},
    },
    "item_analyze": {
        "xml_relative_path": Path("item") / "item_analyze.xml",
        "tag": "item_analyze",
        "name_attr": "ItemName",
        "remove_keys": {"レベル", "分解専用アイテム案"},
    },
    "ShopData": {
        "xml_relative_path": Path("shop") / "ShopData.xml",
        "tag": "ShopData",
        "name_attr": "ShopName",
        "remove_keys": {"itemName", "ShopTag"},
    },
    "HomData": {
        "xml_relative_path": Path("hom") / "HomData.xml",
        "tag": "HomData",
        "remove_keys": {"cost"},
    },
    "item_status": {
        "xml_relative_path": Path("item") / "item_status.xml",
        "tag": "item_status",
        "remove_keys": {},
    },
}


def _decode_bytes(raw: bytes, xml_path: Path, lang: str) -> str:
    candidates = _CODEC_CANDIDATES.get(lang, ["utf-8-sig"])
    for codec in candidates:
        try:
            return raw.decode(codec)
        except UnicodeDecodeError:
            continue

    exc_info = None
    try:
        raw.decode(candidates[0])
    except UnicodeDecodeError as exc:
        exc_info = exc

    if exc_info:
        context = raw[max(0, exc_info.start - 20): exc_info.start + 20]
        print(
            f"[warn] {xml_path}: none of {candidates} decoded cleanly. "
            f"First failure at byte {exc_info.start} "
            f"(0x{raw[exc_info.start]:02x}). Context: {context!r}",
            file=sys.stderr,
        )
    print(f"[warn] {xml_path}: falling back to utf-8 with replacement characters.", file=sys.stderr)
    return raw.decode("utf-8", errors="replace")


def _read_xml_text(xml_path: Path, lang: str) -> str:
    raw = xml_path.read_bytes()
    text = _decode_bytes(raw, xml_path, lang)
    text = _XML_DECL_RE.sub("", text, count=1)
    return text


def _coerce(value: str):
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


def _load_enum_list(enum_path: Path) -> list[str]:
    with enum_path.open("r", encoding="utf-8-sig") as f:
        return [line.strip() for line in f if line.strip()]


def _parse_language_file(xml_path: Path, lang: str, tag: str, name_attr: str | None) -> list[dict]:
    """Parse one language's XML file into an ORDERED list of records
    (document order preserved, no filtering, no keying by any attribute)."""
    text = _read_xml_text(xml_path, lang)
    root = ET.fromstring(text)

    elements = root.findall(f".//{tag}")
    if not elements and root.tag == tag:
        elements = [root]

    records = []
    for elem in elements:
        attrs = dict(elem.attrib)
        name_val = attrs.pop(name_attr, None) if name_attr is not None else None
        records.append({"_name": name_val, "_attrs": attrs})
    return records


def build_dataset(data_root: Path, dataset_key: str) -> dict:
    """Build one enum-keyed dataset dict, e.g. data['itemData']."""
    config = DATASETS[dataset_key]
    xml_relative_path = config["xml_relative_path"]
    enum_path = config.get("enum_path")
    tag = config["tag"]
    name_attr = config.get("name_attr")
    remove_keys = config.get("remove_keys", set())

    per_lang_records: dict[str, list[dict]] = {}

    for lang, folder in LANGUAGE_FOLDERS.items():
        xml_path = data_root / folder / xml_relative_path
        if not xml_path.is_file():
            print(f"Warning: missing file for '{lang}': {xml_path}", file=sys.stderr)
            continue
        per_lang_records[lang] = _parse_language_file(xml_path, lang, tag, name_attr)

    if not per_lang_records:
        print(f"Warning: no language files found for '{dataset_key}'.", file=sys.stderr)
        return {}

    lengths = {lang: len(recs) for lang, recs in per_lang_records.items()}
    if len(set(lengths.values())) > 1:
        canonical_count = lengths.get("ja", max(lengths.values()))
        print(
            f"[warn] {dataset_key}: language files have mismatched entry counts: {lengths}. "
            f"Using {canonical_count} records from Japanese when available; "
            "check for missing/extra rows.",
            file=sys.stderr,
        )
    merge_len = lengths.get("ja", max(lengths.values()))

    # Merge languages together purely by POSITION - ImageNo (or lack of it)
    # plays no role here.
    merged: list[dict] = []
    for i in range(merge_len):
        entry: dict = {}
        for lang, recs in per_lang_records.items():
            if i >= len(recs):
                continue
            record = recs[i]
            if name_attr is not None:
                entry[f"name_{lang}"] = record["_name"]
            for key, val in record["_attrs"].items():
                if key in remove_keys:
                    continue
                entry.setdefault(key, _coerce(val))
        merged.append(entry)

    if enum_path is None:
        return {i: entry for i, entry in enumerate(merged)}

    if not enum_path.is_file():
        print(f"Warning: enum file not found: {enum_path}. Returning a plain list instead.", file=sys.stderr)
        return {i: entry for i, entry in enumerate(merged)}

    enum_list = _load_enum_list(enum_path)

    if len(enum_list) != len(merged):
        print(
            f"[warn] {dataset_key}: enum count ({len(enum_list)}) does not match "
            f"merged entry count ({len(merged)}). Zipping to the shorter of the two; "
            f"check enums/{enum_path.name} against the XML for a mismatch.",
            file=sys.stderr,
        )

    final: dict = {}
    for i, entry in enumerate(merged):
        if i >= len(enum_list):
            final[i] = entry
            continue

        enum_name = enum_list[i]
        entry["enum"] = enum_name
        key = enum_name
        if key in final:
            print(f"[warn] {dataset_key}: duplicate enum {enum_name!r} at record {i}.", file=sys.stderr)
            key = i
        final[key] = entry

    return final


def write_tsv(dataset: dict, out_path: Path) -> None:
    preferred = ["enum", "name_ja", "name_en", "name_sc", "name_tc"]
    available = {key for entry in dataset.values() for key in entry}
    fieldnames = [key for key in preferred if key in available]
    seen = set(fieldnames)
    for entry in dataset.values():
        for key in entry.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        for entry in dataset.values():
            writer.writerow(entry)


def main():
    parser = argparse.ArgumentParser(description="Build enum-keyed data dicts from language XML files.")
    parser.add_argument("data_root", type=Path, help="Root directory containing the Saves* folders")
    args = parser.parse_args()

    data = {}
    for dataset_key in DATASETS:
        data[dataset_key] = build_dataset(args.data_root, dataset_key)

    item_entries = list(data["itemData"].values())
    status_entries = list(data["item_status"].values())
    if len(item_entries) != len(status_entries):
        print(
            f"[warn] itemData and item_status have different entry counts "
            f"({len(item_entries)} and {len(status_entries)}); merging by position "
            f"up to the shorter dataset.",
            file=sys.stderr,
        )
    for item_entry, status_entry in zip(item_entries, status_entries):
        for key, value in status_entry.items():
            item_entry.setdefault(key, value)

    out = 'output'
    for dataset_key, dataset in data.items():
        if dataset_key == "item_status":
            continue
        write_tsv(dataset, Path(out) / f"{dataset_key}.tsv")


if __name__ == "__main__":
    main()
