from common import category_from_text, parse_frontmatter, slugify


def test_slugify():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("Навык для YouTube") == "навык-для-youtube"


def test_parse_frontmatter():
    metadata, body = parse_frontmatter(
        "---\nname: test\ndescription: demo\n---\n\n# Hello"
    )
    assert metadata["name"] == "test"
    assert body.strip() == "# Hello"


def test_category_detection_devops():
    category = category_from_text("A practical Docker and GitHub Actions CI/CD workflow")
    assert category == "devops"


def test_category_detection_networking():
    category = category_from_text("A guide for configuring VPN and proxy privacy tools")
    assert category == "networking"
