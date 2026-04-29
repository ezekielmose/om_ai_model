from ai_vision.quality_rules import HOTEL_VIDEO_RULES

def evaluate_video(scene_results):

    score = 100
    flags = []

    full_text = " ".join([str(s) for s in scene_results]).lower()

    # -----------------------------
    # CHECK: MUST HAVE CONTENT
    # -----------------------------
    must_hits = sum(
        1 for kw in HOTEL_VIDEO_RULES["must_have"]
        if kw in full_text
    )

    if must_hits == 0:
        score -= 40
        flags.append("No hotel experience content detected")

    elif must_hits < 2:
        score -= 20
        flags.append("Weak hotel experience coverage")

    # -----------------------------
    # CHECK: AVOID CONTENT
    # -----------------------------
    avoid_hits = sum(
        1 for kw in HOTEL_VIDEO_RULES["avoid"]
        if kw in full_text
    )

    if avoid_hits > 0:
        score -= avoid_hits * 15
        flags.append("Contains low-quality or irrelevant scenes")

    # -----------------------------
    # HOOK CHECK (FIRST SCENE)
    # -----------------------------
    first_scene = str(scene_results[0]).lower()

    if "fade" in first_scene:
        score -= 25
        flags.append("Weak hook (fade-in detected)")

    if "random" in first_scene:
        score -= 20
        flags.append("Weak opening scene")

    # -----------------------------
    # FINAL DECISION
    # -----------------------------
    passed = score >= 70

    return {
        "score": max(score, 0),
        "passed": passed,
        "flags": flags
    }