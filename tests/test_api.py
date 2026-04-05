from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
JS_PATH = REPO_ROOT / "password.js"
HTML_PATH = REPO_ROOT / "password.html"
CSS_PATH = REPO_ROOT / "password.css"


@pytest.fixture(scope="module")
def js_text() -> str:
    return JS_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def html_text() -> str:
    return HTML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def css_text() -> str:
    return CSS_PATH.read_text(encoding="utf-8")


def test_api_file_exists_js():
    assert JS_PATH.exists()


def test_api_file_exists_html():
    assert HTML_PATH.exists()


def test_api_file_exists_css():
    assert CSS_PATH.exists()


def test_api_js_not_empty(js_text):
    assert js_text.strip()


def test_api_html_not_empty(html_text):
    assert html_text.strip()


def test_api_css_not_empty(css_text):
    assert css_text.strip()


def test_api_js_references_document(js_text):
    assert "document" in js_text


def test_api_js_registers_event_listener(js_text):
    assert "addEventListener" in js_text


def test_api_html_has_doctype(html_text):
    assert "<!DOCTYPE html>" in html_text or "<!doctype html>" in html_text.lower()


def test_api_html_has_html_tag(html_text):
    assert "<html" in html_text.lower()


def test_api_html_has_head_tag(html_text):
    assert "<head" in html_text.lower()


def test_api_html_has_body_tag(html_text):
    assert "<body" in html_text.lower()


def test_api_html_links_css(html_text):
    assert "password.css" in html_text


def test_api_html_links_js(html_text):
    assert "password.js" in html_text


def test_api_css_has_selector(css_text):
    assert "{" in css_text and "}" in css_text


def test_api_css_mentions_body(css_text):
    assert "body" in css_text.lower()


def test_api_css_contains_property_separator(css_text):
    assert ":" in css_text


def test_api_index_file_exists():
    assert (REPO_ROOT / "index.html").exists()


def test_api_index_is_html_document():
    content = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
    assert "<html" in content.lower()


def test_api_password_html_references_title(html_text):
    assert "<title" in html_text.lower()


def test_api_js_uses_query_selector_or_get_element(js_text):
    assert "querySelector" in js_text or "getElementById" in js_text


def test_api_js_mentions_password_keyword(js_text):
    assert "password" in js_text.lower()


def test_api_html_contains_form_or_input(html_text):
    assert "<form" in html_text.lower() or "<input" in html_text.lower()


def test_api_css_has_multiple_lines(css_text):
    assert len(css_text.splitlines()) >= 3


def test_api_js_has_multiple_lines(js_text):
    assert len(js_text.splitlines()) >= 3
