from __future__ import absolute_import

import pytest

import numpy as np

from nengo.utils.numpy import meshgrid_nd, array_hash


def test_meshgrid_nd():
    a = [0, 0, 1]
    b = [1, 2, 3]
    c = [23, 42]
    expected = [
        np.array([[[0, 0], [0, 0], [0, 0]],
                  [[0, 0], [0, 0], [0, 0]],
                  [[1, 1], [1, 1], [1, 1]]]),
        np.array([[[1, 1], [2, 2], [3, 3]],
                  [[1, 1], [2, 2], [3, 3]],
                  [[1, 1], [2, 2], [3, 3]]]),
        np.array([[[23, 42], [23, 42], [23, 42]],
                  [[23, 42], [23, 42], [23, 42]],
                  [[23, 42], [23, 42], [23, 42]]])]
    actual = meshgrid_nd(a, b, c)
    assert np.allclose(expected, actual)


@pytest.mark.parametrize("shape", [(50,), (500, 2)])
def test_array_hash(shape):
    flat = np.arange(np.prod(shape))
    a1 = flat.reshape(shape)
    a2 = np.array(a1)

    # (a1, a2) have same hash but copies of each other
    assert a1 is not a2
    assert np.all(a1 == a2)
    assert array_hash(a1) == array_hash(a2)
    assert not np.shares_memory(a1, a2)

    # (a1, a3) have different hashes but reversed view
    a3 = flat[::-1].reshape(shape)
    assert a1 is not a3
    assert not np.all(a1 == a3)
    assert array_hash(a1) != array_hash(a3)
    assert np.shares_memory(a1, a3)
