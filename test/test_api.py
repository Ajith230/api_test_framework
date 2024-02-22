def test_get_post_1(simple_api_driver):
    simple_api_driver.get('/posts/1')
    simple_api_driver.response.assert_status_code_200()
    simple_api_driver.response.assert_json_contains(key='userId', value=1)


def test_post(simple_api_driver):
    simple_api_driver.post('posts', json={'title': 'foo', 'body': 'bar', 'userId': 1})
    simple_api_driver.response.assert_is_success_status_codes()
    simple_api_driver.response.assert_json_equals(dict(id=101, title='foo', body='bar', userId=1))


def test_put(simple_api_driver):
    user_id = 1
    simple_api_driver.put(f'posts/{user_id}', json={'title': 'foo', 'body': 'bar', 'userId': 1})
    simple_api_driver.response.assert_status_code_200()
    simple_api_driver.response.assert_json_equals(dict(id=1, title='foo', body='bar', userId=1))


def test_patch(simple_api_driver):
    simple_api_driver.put('posts/1', json={'title': 'foo'})
    simple_api_driver.response.assert_status_code_200()
    simple_api_driver.response.assert_json_equals(dict(id=1, title='foo'))


def test_delete(simple_api_driver):
    simple_api_driver.delete('posts/1')
    simple_api_driver.response.assert_status_code_200()
