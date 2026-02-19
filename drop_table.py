import sys
import os

# Update path to find backend modules
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from memory.db import engine
from sqlalchemy import text

print("Dropping workflows table...")
with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS workflows"))
    conn.commit()
print("Table dropped successfully.")
