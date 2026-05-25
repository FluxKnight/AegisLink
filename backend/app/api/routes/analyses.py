from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.analysis import Analysis
from app.schemas.analysis import (
    AnalysisListResponse,
    AnalysisResponse,
    AnalyzeUrlRequest,
    RiskLevelEnum,
)
from app.services.analysis_workflow import (
    analysis_to_response,
    analyze_url_string,
    persist_analysis,
)
from app.utils.validators import validate_url_input

router = APIRouter(prefix="/api/v1/analyses", tags=["analyses"])


@router.post("", response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(
    payload: AnalyzeUrlRequest,
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    try:
        cleaned_url = validate_url_input(payload.url)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    parsed, findings, score, risk_level, explanation, recommendations = analyze_url_string(
        cleaned_url
    )
    record = persist_analysis(
        db,
        cleaned_url,
        parsed,
        findings,
        score,
        risk_level,
        explanation,
        recommendations,
    )
    return analysis_to_response(record)


@router.get("", response_model=AnalysisListResponse)
def list_analyses(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    risk_level: RiskLevelEnum | None = None,
    db: Session = Depends(get_db),
) -> AnalysisListResponse:
    query = select(Analysis)
    count_query = select(func.count()).select_from(Analysis)

    if risk_level is not None:
        query = query.where(Analysis.risk_level == risk_level.value)
        count_query = count_query.where(Analysis.risk_level == risk_level.value)

    total = db.scalar(count_query) or 0
    rows = (
        db.execute(
            query.order_by(Analysis.created_at.desc()).offset(offset).limit(limit)
        )
        .scalars()
        .all()
    )

    return AnalysisListResponse(
        items=[analysis_to_response(row) for row in rows],
        limit=limit,
        offset=offset,
        total=total,
    )


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
) -> AnalysisResponse:
    record = db.get(Analysis, analysis_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found.",
        )
    return analysis_to_response(record)
