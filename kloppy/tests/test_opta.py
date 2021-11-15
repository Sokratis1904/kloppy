import os

import pytest

from kloppy.domain import (
    AttackingDirection,
    Period,
    Orientation,
    Provider,
    Ground,
    Point,
    BodyPart,
    SetPieceType,
    PassType,
    DatasetType,
)

from kloppy import opta


class TestOpta:
    """"""

    @pytest.fixture
    def f24_data(self) -> str:
        base_dir = os.path.dirname(__file__)
        return f"{base_dir}/files/opta_f24.xml"

    @pytest.fixture
    def f7_data(self) -> str:
        base_dir = os.path.dirname(__file__)
        return f"{base_dir}/files/opta_f7.xml"

    def test_correct_deserialization(self, f7_data: str, f24_data: str):
        dataset = opta.load(
            f24_data=f24_data, f7_data=f7_data, coordinates="opta"
        )

        assert dataset.metadata.provider == Provider.OPTA
        assert dataset.dataset_type == DatasetType.EVENT
        assert len(dataset.events) == 17
        assert len(dataset.metadata.periods) == 2
        assert dataset.events[10].ball_owning_team == dataset.metadata.teams[1]
        assert dataset.events[15].ball_owning_team == dataset.metadata.teams[0]
        assert (
            dataset.metadata.orientation == Orientation.ACTION_EXECUTING_TEAM
        )
        assert dataset.metadata.teams[0].name == "FC København"
        assert dataset.metadata.teams[0].ground == Ground.HOME
        assert dataset.metadata.teams[1].name == "FC Nordsjælland"
        assert dataset.metadata.teams[1].ground == Ground.AWAY

        player = dataset.metadata.teams[0].players[0]
        assert player.player_id == "111319"
        assert player.jersey_no == 21
        assert str(player) == "Jesse Joronen"
        assert player.position.position_id == "1"
        assert player.position.name == "Goalkeeper"

        assert dataset.metadata.periods[0] == Period(
            id=1,
            start_timestamp=1537714933.608,
            end_timestamp=1537717701.222,
            attacking_direction=AttackingDirection.NOT_SET,
        )
        assert dataset.metadata.periods[1] == Period(
            id=2,
            start_timestamp=1537718728.873,
            end_timestamp=1537721737.788,
            attacking_direction=AttackingDirection.NOT_SET,
        )

        assert dataset.events[0].coordinates == Point(50.1, 49.4)

        # Check the qualifiers
        assert dataset.events[0].qualifiers[0].value == SetPieceType.KICK_OFF
        assert dataset.events[6].qualifiers[0].value == BodyPart.HEAD
        assert dataset.events[5].qualifiers[0].value == PassType.CHIPPED_PASS

    def test_correct_normalized_deserialization(
        self, f7_data: str, f24_data: str
    ):
        dataset = opta.load(
            f24_data=f24_data,
            f7_data=f7_data,
        )
        assert dataset.events[0].coordinates == Point(0.501, 0.506)
