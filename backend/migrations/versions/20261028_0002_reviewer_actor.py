"""Pseudonymous actor reference for authorized reviewer decisions.

Revision ID: 20261028_0002
Revises: 20261026_0001
"""
from alembic import op
import sqlalchemy as sa

revision = "20261028_0002"
down_revision = "20261026_0001"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("review_audit", sa.Column(
        "actor_ref", sa.String(length=64), nullable=False,
        server_default="legacy_unattributed"))
    # Backfill is deliberately explicit; old shared-key reviews are not real identities.

def downgrade():
    op.drop_column("review_audit", "actor_ref")
