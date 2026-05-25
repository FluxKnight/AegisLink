from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.analysis import Analysis
from app.schemas.analysis import ReportResponse
from app.services.report_builder import build_markdown_report

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])


@router.get("/analyses/{analysis_id}", response_model=ReportResponse)
def get_analysis_report(
    analysis_id: int,
    db: Session = Depends(get_db),
) -> ReportResponse:
    record = db.get(Analysis, analysis_id)
    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found.",
        )
    markdown = build_markdown_report(record)
    return ReportResponse(analysis_id=record.id, report_markdown=markdown)
