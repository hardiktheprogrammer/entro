from typing import Any

from sqlalchemy import JSON, PrimaryKeyConstraint, Text
from sqlalchemy.orm import Mapped, mapped_column

from nethermind.entro.database.models.base import Base
from nethermind.entro.types.backfill import BackfillDataType, SupportedNetwork


class ContractABI(Base):
    """
    Table for storing contract ABIs to use for decoding events.
    """

    __tablename__ = "contract_abis"

    abi_name: Mapped[str]
    abi_json: Mapped[list[dict[str, Any]]] = mapped_column(JSON)
    priority: Mapped[int]
    os: Mapped[str]  # 'EVM' or 'Cairo'

    __table_args__ = (
        PrimaryKeyConstraint("abi_name"),
        {"schema": "internal"},
    )


class BackfilledRange(Base):
    """
    Table for storing backfill states.

    This table is used to track the ranges of blocks that have been backfilled for each data type.

    """

    __tablename__ = "backfilled_ranges"

    backfill_id: Mapped[int] = mapped_column(Text, nullable=False)
    data_type: Mapped[BackfillDataType] = mapped_column(Text, nullable=False)
    network: Mapped[SupportedNetwork] = mapped_column(Text, nullable=False)
    start_block: Mapped[int]
    end_block: Mapped[int]

    filter_data: Mapped[dict[str, str | int] | None] = mapped_column(JSON)
    metadata_dict: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    decoded_abis: Mapped[list[str] | None] = mapped_column(JSON)

    __table_args__ = (
        PrimaryKeyConstraint("data_type", "network", "start_block", "end_block"),
        {"schema": "internal"},
    )
