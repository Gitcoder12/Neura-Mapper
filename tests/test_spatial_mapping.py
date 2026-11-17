"""Tests for validated 3D spatial classification and routing."""

from __future__ import annotations

import pytest

from neuro_router import NeuroMapper
from pathfinder import AStarRouter


@pytest.mark.parametrize("router_factory", [lambda: NeuroMapper(), lambda: AStarRouter((10, 10, 10))])
def test_invalid_start_and_goal_are_rejected(router_factory):
    router = router_factory()
    if isinstance(router, NeuroMapper):
        assert router.find_safest_path((-1, 0, 0), (2, 2, 2)) is None
        assert router.find_safest_path((0, 0, 0), (10, 0, 0)) is None
    else:
        assert router.find_path((-1, 0, 0), (2, 2, 2)) == []
        assert router.find_path((0, 0, 0), (10, 0, 0)) == []


@pytest.mark.parametrize("router_factory", [lambda: NeuroMapper(), lambda: AStarRouter((10, 10, 10))])
def test_classification_rejects_invalid_coordinates_and_values(router_factory):
    router = router_factory()
    with pytest.raises(ValueError, match="coordinate"):
        router.classify_region((1, 2), 1)
    with pytest.raises(ValueError, match="classification"):
        router.classify_region((1, 2, 3), 9)


@pytest.mark.parametrize("router_factory", [lambda: NeuroMapper(), lambda: AStarRouter((10, 10, 10))])
def test_classification_rejects_out_of_bounds_coordinate(router_factory):
    router = router_factory()
    with pytest.raises(ValueError, match="coordinate"):
        router.classify_region((10, 0, 0), 1)


def test_neuro_mapper_avoids_critical_voxels():
    mapper = NeuroMapper(grid_size=(3, 3, 1))
    mapper.classify_region((1, 0, 0), 2)
    path = mapper.find_safest_path((0, 0, 0), (2, 0, 0))

    assert path is not None
    assert (1, 0, 0) not in path


def test_astar_avoids_critical_voxels_and_warning_penalty():
    router = AStarRouter((3, 3, 1))
    router.classify_region((1, 0, 0), 2)
    router.classify_region((1, 1, 0), 1)
    path = router.find_path((0, 0, 0), (2, 0, 0))

    assert path
    assert (1, 0, 0) not in path
    assert (1, 1, 0) not in path


def test_router_rejects_invalid_grid_dimensions():
    with pytest.raises(ValueError, match="grid_size"):
        NeuroMapper((10, 0, 10))
    with pytest.raises(ValueError, match="grid_size"):
        AStarRouter((10, 10))
