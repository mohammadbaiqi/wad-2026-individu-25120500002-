from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request, Response, status

from app.schemas.ticket import TiketCreate, TiketOut

router = APIRouter(prefix="/api/tiket", tags=["tiket"])

# Penyimpanan sementara di memori (in-memory).
# id dibuat oleh server, bukan oleh klien -> memenuhi "Skema Input != Skema Output".
_DB: dict[int, TiketOut] = {}
_NEXT_ID = 1


@router.post("", response_model=TiketOut, status_code=status.HTTP_201_CREATED)
def buat_tiket(payload: TiketCreate, request: Request, response: Response) -> TiketOut:
    global _NEXT_ID

    # Cegah kode_tiket duplikat (validasi bisnis tambahan yang wajar untuk sebuah "kode unik")
    for tiket in _DB.values():
        if tiket.kode_tiket == payload.kode_tiket:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"kode_tiket '{payload.kode_tiket}' sudah dipakai",
            )

    tiket = TiketOut(id=_NEXT_ID, **payload.model_dump())
    _DB[_NEXT_ID] = tiket
    _NEXT_ID += 1

    # Header Location menunjuk ke resource yang baru dibuat, wajib untuk 201 Created.
    response.headers["Location"] = f"{request.url.path}/{tiket.id}"
    return tiket


@router.get("", response_model=list[TiketOut], status_code=status.HTTP_200_OK)
def daftar_tiket(skip: int = 0, limit: int = 10, search: str | None = None) -> list[TiketOut]:
    hasil = list(_DB.values())

    if search:
        s = search.lower()
        hasil = [
            t for t in hasil
            if s in t.kode_tiket.lower() or s in t.nama_event.lower()
        ]

    return hasil[skip: skip + limit]


@router.get("/{tiket_id}", response_model=TiketOut, status_code=status.HTTP_200_OK)
def detail_tiket(tiket_id: int) -> TiketOut:
    tiket = _DB.get(tiket_id)
    if tiket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tiket dengan id={tiket_id} tidak ditemukan",
        )
    return tiket