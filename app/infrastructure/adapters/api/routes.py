from fastapi import APIRouter
from app.infrastructure.adapters.api.routes_pets import router as pet_router
from app.infrastructure.adapters.api.routes_owners import router as owner_router
from app.infrastructure.adapters.api.routes_appointments import router as appointment_router
from app.infrastructure.adapters.api.routes_stats import router as stats_router
from app.infrastructure.adapters.api.routes_medical import router as medical_router
from app.infrastructure.adapters.api.routes_hospital import router as hospital_router
from app.infrastructure.adapters.api.routes_inventory import router as inventory_router
from app.infrastructure.adapters.api.routes_prescription import router as prescription_router
from app.infrastructure.adapters.api.routes_vaccines import router as vaccines_router
from app.infrastructure.adapters.api.routes_attachments import router as attachments_router
from app.infrastructure.adapters.api.routes_user import router as user_router
from app.infrastructure.adapters.api.routes_billing import router as billing_router
from app.infrastructure.adapters.api.routes_search import router as search_router

router = APIRouter()
router.include_router(pet_router)
router.include_router(owner_router)
router.include_router(appointment_router)
router.include_router(stats_router)
router.include_router(medical_router)
router.include_router(hospital_router)
router.include_router(inventory_router)
router.include_router(prescription_router)
router.include_router(vaccines_router)
router.include_router(attachments_router)
router.include_router(user_router)
router.include_router(billing_router)
router.include_router(search_router)
