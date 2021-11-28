from core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_hash_and_verify_password():
    res = hash_password("testpassword")
    res_1 = verify_password("testpassword", res)
    assert res_1 is True


def test_failed_hash_and_verify_password():
    res = hash_password("testpassword")
    res_1 = verify_password("failedpass", res)
    assert res_1 is False


def test_create_and_decode_token():
    res = create_access_token({"sub": "testtest@example.com"})
    res_1 = decode_access_token(res)
    assert res_1['sub'] == "testtest@example.com"
