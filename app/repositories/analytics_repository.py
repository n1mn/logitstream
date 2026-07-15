from sqlalchemy.orm import Session

from app.models.analytics import Analytics


class AnalyticsRepository:

    def get_metric(
        self,
        db: Session,
        metric: str,
    ):
        return (
            db.query(Analytics)
            .filter(Analytics.metric == metric)
            .first()
        )

    def increment_metric(
        self,
        db: Session,
        metric: str,
    ):
        analytics = self.get_metric(
            db=db,
            metric=metric,
        )

        if analytics is None:
            analytics = Analytics(
                metric=metric,
                value=1,
            )
            db.add(analytics)
        else:
            analytics.value += 1

        db.commit()
        db.refresh(analytics)

        return analytics
    
    def get_all_metrics(
        self,
        db: Session,
    ):
        return db.query(Analytics).all()