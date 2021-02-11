import pytest

from blog.models import Tag, Post
from users.models import CustomUser as User


@pytest.mark.django_db
def test_tag_create():
    tag = Tag.objects.create(
        name="John",
        description="Doe",
    )
    assert tag.name == "John"
    assert tag.description == "Doe"


@pytest.mark.django_db
def test_post_create():
    author = User.objects.create(email="test@test.com", is_writer=True)
    tag = Tag.objects.create(
        name="John",
        description="Doe",
    )
    post = Post.objects.create(
        author=author,
        title="Article test",
        content="Any possible content",
        description="Dans cet article, vous allez...",
    )
    post.tags.set([tag])
    assert post.author == author
    assert post.title == "Article test"
    assert post.content == "Any possible content"
    assert post.description == "Dans cet article, vous allez..."
    assert post.tags.count() == 1
