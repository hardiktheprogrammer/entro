from typing import Any

from sqlalchemy import JSON, BigInteger, Numeric, PrimaryKeyConstraint, Text
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import Mapped, mapped_column

from nethermind.entro.database.models.base import (
    AbstractBlock,
    AbstractERC20Transfer,
    AbstractEvent,
    AbstractTrace,
    AbstractTransaction,
    Address,
    CalldataBytes,
    Hash32,
    IndexedAddress,
    IndexedBlockNumber,
    IndexedNullableAddress,
)

# pylint: disable=missing-class-docstring


class Block(AbstractBlock):
    __tablename__ = "blocks"

    parent_hash: Mapped[Hash32]
    miner: Mapped[Address]
    difficulty: Mapped[int] = mapped_column(Numeric(32, 0), nullable=True)
    gas_limit: Mapped[int] = mapped_column(BigInteger, nullable=False)

    extra_data: Mapped[str] = mapped_column(Text().with_variant(BYTEA, "postgresql"), nullable=False)

    __table_args__ = {"schema": "ethereum_data"}


class DefaultEvent(AbstractEvent):
    __tablename__ = "default_events"

    event_name: Mapped[str | None] = mapped_column(Text, index=True)
    abi_name: Mapped[str | None] = mapped_column(Text, index=True)
    decoded_event: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint("block_number", "log_index"),
        {"schema": "ethereum_data"},
    )


class Transaction(AbstractTransaction):
    __tablename__ = "transactions"

    nonce: Mapped[int]
    from_address: Mapped[IndexedAddress]
    to_address: Mapped[IndexedNullableAddress]
    input: Mapped[CalldataBytes | None]

    value: Mapped[int] = mapped_column(Numeric(24, 0))

    gas_available: Mapped[int | None] = mapped_column(BigInteger)
    gas_price: Mapped[int] = mapped_column(Numeric(16, 0))
    gas_used: Mapped[int | None] = mapped_column(BigInteger)

    decoded_signature: Mapped[str | None]
    decoded_input: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    __table_args__ = {"schema": "ethereum_data"}


class Trace(AbstractTrace):
    __tablename__ = "traces"

    transaction_hash: Mapped[Hash32]
    block_number: Mapped[IndexedBlockNumber]
    # Trace addresses are converted to Text strings ie, [0,1,2,3,4]
    trace_address: Mapped[list[int]] = mapped_column(Text)

    from_address: Mapped[IndexedAddress]
    to_address: Mapped[IndexedNullableAddress | None]

    input: Mapped[CalldataBytes | None]
    output: Mapped[CalldataBytes | None]

    gas_used: Mapped[int] = mapped_column(BigInteger, nullable=False)
    decoded_function: Mapped[str | None] = mapped_column(Text, index=True)
    decoded_input: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    decoded_output: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    __table_args__ = (
        PrimaryKeyConstraint("transaction_hash", "trace_address"),
        {"schema": "ethereum_data"},
    )


class ERC20Transfer(AbstractERC20Transfer):
    __tablename__ = "erc20_transfers"

    __table_args__ = (PrimaryKeyConstraint("transaction_hash", "log_index"), {"schema": "ethereum_data"})
