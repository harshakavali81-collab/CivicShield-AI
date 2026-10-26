"""Initial schema for EMPTY local demonstration databases.
Revision ID: 20261026_0001
Revises:
"""
from alembic import op
import sqlalchemy as sa

revision = "20261026_0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "incidents",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=30), nullable=False),
        sa.Column("city", sa.String(length=80), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("language", sa.String(length=5), nullable=False),
        sa.Column("priority_hint", sa.String(length=16), nullable=False),
        sa.Column("duplicate_of", sa.String(length=36), nullable=True),
        sa.Column("dedup_hash", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("reviewer_note", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_incidents_dedup_hash", "incidents", ["dedup_hash"])
    op.create_table(
        "review_audit",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("incident_id", sa.String(length=36), nullable=False),
        sa.Column("previous_status", sa.String(length=20), nullable=False),
        sa.Column("new_status", sa.String(length=20), nullable=False),
        sa.Column("reviewer_note", sa.Text(), nullable=False),
        sa.Column("changed_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_review_audit_incident_id", "review_audit", ["incident_id"])

def downgrade():
    op.drop_index("ix_review_audit_incident_id", table_name="review_audit")
    op.drop_table("review_audit")
    op.drop_index("ix_incidents_dedup_hash", table_name="incidents")
    op.drop_table("incidents")
