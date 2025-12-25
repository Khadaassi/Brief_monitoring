"""
Module de métriques Prometheus pour l'API Items
EXEMPLE DE CODE avec annotations pédagogiques
"""

from prometheus_client import Counter, Histogram, Gauge, Info
import time

# ℹ️ INFO : Informations statiques sur l'application
app_info = Info(
    'fastapi_app_info',
    'Information about the FastAPI application'
)

# 📊 COUNTER : Compteurs pour les opérations CRUD
items_created_total = Counter(
    'items_created_total',
    'Nombre total d\'items créés depuis le démarrage'
)

items_read_total = Counter(
    'items_read_total',
    'Nombre total de lectures d\'items'
)

items_updated_total = Counter(
    'items_updated_total',
    'Nombre total d\'items mis à jour'
)

items_deleted_total = Counter(
    'items_deleted_total',
    'Nombre total d\'items supprimés'
)

# 📈 GAUGE : Valeur instantanée
db_connection_pool_size = Gauge(
    'db_connection_pool_size',
    'Taille actuelle du pool de connexions DB'
)

# ⏱️ HISTOGRAM : Distribution de valeurs avec buckets
db_query_duration_seconds = Histogram(
    'db_query_duration_seconds',
    'Durée des requêtes base de données (secondes)',
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0]
)

# 🎯 Context Manager pour mesurer automatiquement les durées
class DatabaseQueryTimer:
    """Context manager pour mesurer le temps d'exécution d'une requête DB."""

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        db_query_duration_seconds.observe(duration)