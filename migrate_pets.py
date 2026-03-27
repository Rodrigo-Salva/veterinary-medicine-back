"""
Script para agregar los nuevos campos de ficha completa de mascota.
Ejecutar: python migrate_pets.py
"""
from sqlalchemy import create_engine, text
from app.infrastructure.config.settings import settings

engine = create_engine(settings.DATABASE_URL)


def migrate():
    with engine.begin() as conn:
        # 1. Agregar nuevos campos a pets (si no existen)
        new_columns = {
            'is_active': 'BOOLEAN DEFAULT TRUE',
            'photo_url': 'VARCHAR',
            'sex': 'VARCHAR(10)',
            'color': 'VARCHAR(50)',
            'weight': 'FLOAT',
            'allergies': 'TEXT',
            'is_neutered': 'BOOLEAN DEFAULT FALSE',
            'microchip': 'VARCHAR(50)',
            'birth_date': 'DATE',
            'notes': 'TEXT',
        }

        for col_name, col_type in new_columns.items():
            exists = conn.execute(text("""
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'pets' AND column_name = :col
            """), {"col": col_name}).fetchone()

            if not exists:
                conn.execute(text(f"ALTER TABLE pets ADD COLUMN {col_name} {col_type}"))
                print(f"  Columna 'pets.{col_name}' agregada.")
            else:
                print(f"  Columna 'pets.{col_name}' ya existe.")

        # Set default is_active = TRUE for existing pets
        conn.execute(text("UPDATE pets SET is_active = TRUE WHERE is_active IS NULL"))
        print("  Pets existentes marcados como activos.")

        # 2. Crear tabla weight_records
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS weight_records (
                id UUID PRIMARY KEY,
                pet_id UUID NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
                weight FLOAT NOT NULL,
                recorded_date DATE NOT NULL,
                notes VARCHAR(200)
            )
        """))
        print("  Tabla 'weight_records' creada.")

        # 3. Crear indice en weight_records.pet_id
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_weight_records_pet_id ON weight_records(pet_id)
        """))
        print("  Indice en weight_records.pet_id creado.")

    print("\nMigracion de mascotas completada!")


if __name__ == "__main__":
    migrate()
