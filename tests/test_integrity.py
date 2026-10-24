from __future__ import annotations

from integrity import (
    check_bundle,
    detect_promo,
    extract_references,
    fit_score,
    missing_references,
    precheck,
    similarity,
)

PROFILE = {
    "enabled": True,
    "domains": [
        {"name": "network-vpn", "keywords": ["vpn", "xray", "proxy", "tunnel", "ssh"]},
        {"name": "media", "keywords": ["video", "audio", "ffmpeg", "transcript"]},
    ],
}


def test_extract_references_ignores_urls():
    text = (
        "Run `scripts/setup.sh` and read references/guide.md.\n"
        "Source: https://github.com/owner/repo/blob/main/scripts/setup.sh\n"
        "Also see scripts/beats.py.\n"
    )
    assert extract_references(text) == ["references/guide.md", "scripts/beats.py", "scripts/setup.sh"]


def test_missing_references_counts_globs_as_covered():
    refs = ["references/*.md", "scripts/run.py"]
    files = {"references/intro.md", "SKILL.md"}
    assert missing_references(refs, files) == ["scripts/run.py"]


def test_check_bundle_marks_incomplete(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "run.py").write_text("print(1)", encoding="utf-8")
    text = "Запусти scripts/run.py и посмотри references/missing.md."
    result = check_bundle(text, tmp_path)
    assert result["complete"] is False
    assert result["missing"] == ["references/missing.md"]
    assert result["file_count"] == 1


def test_check_bundle_complete_when_no_references(tmp_path):
    result = check_bundle("Просто инструкция без файлов рядом.", tmp_path)
    assert result["complete"] is True
    assert result["references"] == []


def test_detect_promo_flags_monetization():
    text = "Great skill. Full version: https://rafaamaral.gumroad.com/l/x — one-time $29. Buy now!"
    result = detect_promo(text)
    assert result["promotional"] is True
    assert "gumroad" in result["hits"]
    assert result["count"] >= 2


def test_detect_promo_clean_text():
    text = "Настройка xray: создай inbound, проверь логи, перезапусти сервис."
    assert detect_promo(text)["promotional"] is False


def test_fit_score_rewards_on_profile():
    on_profile = "Настройка VPN через xray, proxy и tunnel, проверка ssh."
    off_profile = "How to fold origami cranes for a wedding decoration."
    assert fit_score(on_profile, PROFILE)["score"] >= 60
    assert fit_score(off_profile, PROFILE)["score"] == 0


def test_similarity_is_stable_for_near_duplicates():
    left = "Humanize text: remove AI writing patterns from prose, rewrite sentences."
    right = "Humanize: remove AI writing patterns from prose and rewrite each sentence."
    other = "Setup xray inbound with reality and check server logs."
    assert similarity(left, right) > 0.5
    assert similarity(left, other) < 0.1


def test_precheck_collects_all_reasons(tmp_path):
    text = (
        "Запусти scripts/missing.py.\n"
        "Купить полную версию: https://example.gumroad.com/x — one-time $49.\n"
        "Рецепт борща и советы по даче."
    )
    result = precheck(
        text,
        tmp_path,
        profile=PROFILE,
        require_complete_bundle=True,
        min_fit=35,
        max_promo_hits=0,
    )
    assert result["passed"] is False
    assert set(result["reasons"]) == {"incomplete_bundle", "promotional", "off_profile"}


def test_precheck_passes_good_bundle(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "scripts" / "run.py").write_text("print(1)", encoding="utf-8")
    text = "Навык: настройка xray и vpn. Запусти scripts/run.py, проверь логи ssh."
    result = precheck(text, tmp_path, profile=PROFILE, min_fit=35)
    assert result["passed"] is True
    assert result["reasons"] == []
