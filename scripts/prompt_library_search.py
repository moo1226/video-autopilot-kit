"""Search the local awesome-opus5-5-videos clone without loading its 800 KB index into context."""
import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("category", choices=["all", "motion", "explainer", "3d", "interactive"])
    parser.add_argument("keywords", nargs="*", help="any-match, case-insensitive")
    parser.add_argument("--root", default="_scratch_prompts")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()
    keywords = [k.lower() for k in args.keywords]
    videos = json.loads(Path(args.root, "data", "videos.json").read_text(encoding="utf-8"))
    hits = []
    for video in videos:
        if args.category not in ("all", video["category"]) or video["prompt_partial"]:
            continue
        text = (video.get("title", "") + " " + video["prompt"]).lower()
        score = sum(k in text for k in keywords)
        if keywords and not score:
            continue
        hits.append((not video["has_remake"], -score, video))
    hits.sort(key=lambda h: h[:2])
    for _, _, video in hits[: args.limit]:
        label = (video.get("title") or video["prompt"])[:70].replace("\n", " ")
        print(f"prompts/{video['slug']}.md | {label} | {video['post_url']}")
    print(f"{len(hits)} matches")


if __name__ == "__main__":
    main()
