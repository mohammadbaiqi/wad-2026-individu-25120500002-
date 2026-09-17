from __future__ import annotations

import re
from pydantic import BaseModel, Field, field_validator

KODE_TIKET_PATTERN = re.compile(r"^EVT-\d{4}$")


class TiketCreate(BaseModel):
    """Skema INPUT — dipakai di body POST /api/tiket. Tidak punya field id."""

    kode_tiket: str = Field(
        ...,
        description="Kode tiket dengan pola EVT-XXXX, contoh: EVT-0001",
        examples=["EVT-0001"],
    )
    nama_event: str = Field(..., min_length=1, max_length=200)
    kuota: int = Field(..., gt=0, description="Kuota harus lebih besar dari 0")

    @field_validator("kode_tiket")
    @classmethod
    def validasi_kode_tiket(cls, v: str) -> str:
        if not KODE_TIKET_PATTERN.match(v):
            raise ValueError("kode_tiket harus mengikuti pola EVT-XXXX (contoh: EVT-0001)")
        return v


class TiketOut(BaseModel):
    """Skema OUTPUT — dikembalikan di response. id dibuat oleh server, bukan dari input."""

    id: int
    kode_tiket: str
    nama_event: str
    kuota: int

    class Config:
        from_attributes = True