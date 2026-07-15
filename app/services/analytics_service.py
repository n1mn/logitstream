from sqlalchemy.orm import Session

from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:

    def __init__(self):
        self.repository = AnalyticsRepository()

    def process_event(
        self,
        db: Session,
        event: dict,
    ):
        event_type = event["event_type"]

        if event_type == "SHIPMENT_CREATED":
            self.repository.increment_metric(
                db=db,
                metric="total_shipments",
            )

        elif event_type == "SHIPMENT_STATUS_UPDATED":

            status = event["status"].upper()

            if status == "DELIVERED":
                self.repository.increment_metric(
                    db=db,
                    metric="delivered_shipments",
                )

            elif status == "IN_TRANSIT":
                self.repository.increment_metric(
                    db=db,
                    metric="in_transit_shipments",
                )
    def get_metrics(
            self,
            db: Session,
    ):
        return self.repository.get_all_metrics(db)