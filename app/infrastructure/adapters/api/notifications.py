from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta
import json
import asyncio

from app.infrastructure.adapters.db.database import get_db, SessionLocal
from app.infrastructure.adapters.db.models import AppointmentModel, PetModel, OwnerModel
from app.infrastructure.adapters.db.models_medical import MedicalRecordModel
from app.infrastructure.adapters.db.models_inventory import ProductModel

router = APIRouter(prefix="/notifications", tags=["notifications"])


class ConnectionManager:
    """Gestiona las conexiones WebSocket activas."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)
        for conn in disconnected:
            self.disconnect(conn)


manager = ConnectionManager()


def get_pending_notifications(db: Session) -> List[dict]:
    """Genera notificaciones basadas en el estado actual del sistema."""
    notifications = []
    now = datetime.utcnow()
    today = now.date()

    # 1. Citas de hoy pendientes
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    today_appointments = (
        db.query(AppointmentModel, PetModel.name.label("pet_name"))
        .join(PetModel, PetModel.id == AppointmentModel.pet_id)
        .filter(
            AppointmentModel.date >= today_start,
            AppointmentModel.date <= today_end,
            AppointmentModel.status == "Pending",
        )
        .all()
    )
    for appt, pet_name in today_appointments:
        hour = appt.date.strftime("%H:%M")
        notifications.append({
            "id": str(appt.id),
            "type": "appointment_today",
            "title": "Cita pendiente hoy",
            "message": f"{pet_name} tiene cita a las {hour} - {appt.reason}",
            "priority": "high",
            "timestamp": now.isoformat(),
        })

    # 2. Citas proximas (mañana)
    tomorrow = today + timedelta(days=1)
    tomorrow_start = datetime.combine(tomorrow, datetime.min.time())
    tomorrow_end = datetime.combine(tomorrow, datetime.max.time())
    tomorrow_appointments = (
        db.query(AppointmentModel, PetModel.name.label("pet_name"))
        .join(PetModel, PetModel.id == AppointmentModel.pet_id)
        .filter(
            AppointmentModel.date >= tomorrow_start,
            AppointmentModel.date <= tomorrow_end,
            AppointmentModel.status == "Pending",
        )
        .all()
    )
    for appt, pet_name in tomorrow_appointments:
        notifications.append({
            "id": f"tomorrow-{appt.id}",
            "type": "appointment_tomorrow",
            "title": "Cita programada mañana",
            "message": f"{pet_name} - {appt.reason}",
            "priority": "medium",
            "timestamp": now.isoformat(),
        })

    # 3. Vacunas/controles proximos (próximos 7 días)
    next_week = now + timedelta(days=7)
    upcoming_records = (
        db.query(MedicalRecordModel, PetModel.name.label("pet_name"))
        .join(PetModel, PetModel.id == MedicalRecordModel.pet_id)
        .filter(
            MedicalRecordModel.next_date != None,
            MedicalRecordModel.next_date >= today,
            MedicalRecordModel.next_date <= next_week.date(),
        )
        .all()
    )
    for record, pet_name in upcoming_records:
        days_left = (record.next_date - today).days
        urgency = "hoy" if days_left == 0 else f"en {days_left} día{'s' if days_left > 1 else ''}"
        notifications.append({
            "id": f"vaccine-{record.id}",
            "type": "vaccine_reminder",
            "title": f"Control/vacuna {urgency}",
            "message": f"{pet_name} - {record.record_type}: {record.description[:50]}",
            "priority": "high" if days_left <= 1 else "medium",
            "timestamp": now.isoformat(),
        })

    # 4. Stock bajo (productos con stock < 5)
    low_stock = db.query(ProductModel).filter(ProductModel.stock < 5).all()
    for product in low_stock:
        notifications.append({
            "id": f"stock-{product.id}",
            "type": "low_stock",
            "title": "Stock bajo",
            "message": f"{product.name} - Solo quedan {product.stock} unidades",
            "priority": "high" if product.stock == 0 else "low",
            "timestamp": now.isoformat(),
        })

    return notifications


@router.get("/")
def get_notifications(db: Session = Depends(get_db)):
    """Endpoint REST para obtener notificaciones actuales."""
    return get_pending_notifications(db)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para notificaciones en tiempo real."""
    await manager.connect(websocket)
    try:
        # Enviar notificaciones iniciales
        db = SessionLocal()
        try:
            notifications = get_pending_notifications(db)
            await websocket.send_json({"type": "initial", "notifications": notifications})
        finally:
            db.close()

        # Mantener conexion abierta y enviar actualizaciones periodicas
        while True:
            try:
                # Esperar mensajes del cliente o timeout para refresh
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                # Si el cliente pide refresh
                if data == "refresh":
                    db = SessionLocal()
                    try:
                        notifications = get_pending_notifications(db)
                        await websocket.send_json({"type": "update", "notifications": notifications})
                    finally:
                        db.close()
            except asyncio.TimeoutError:
                # Enviar actualizacion periodica cada 30 segundos
                db = SessionLocal()
                try:
                    notifications = get_pending_notifications(db)
                    await websocket.send_json({"type": "update", "notifications": notifications})
                finally:
                    db.close()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def broadcast_notification(notification: dict):
    """Función utilitaria para emitir una notificación a todos los clientes conectados."""
    await manager.broadcast({"type": "new", "notification": notification})
