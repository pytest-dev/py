import pytest
pytest.register_assert_rewrite(
    __name__ + '.common',
    __name__ + '.svntestbase',
)
