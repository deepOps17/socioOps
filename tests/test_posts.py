import pytest

from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

# def test_get_one_post(authorized_client, test_posts):
#     res = authorized_client.get(f"/posts/{test_posts[0].id}")
#     # post = schemas.PostOut(**res.json())
#     # assert post.Post.id == test_posts[0].id
#     assert res.status_code == 200

@pytest.mark.parametrize("title, content, published",[
    ("awesome title", "awesome content", True),
    ("alkjlajslkjsa", "random post", False),
    ("random title", "random content", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_posts):
    res = client.post("/posts/", json={
        "title": "helloworld","content": "trying to get access"
    })
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
     res = client.delete(f"/posts/{test_posts[0].id}")
     assert res.status_code == 401
    
def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204