"""
Workflow Routes - API endpoints for managing and running workflows.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from memory.db import get_db, Workflow
from agent.workflow_engine import workflow_engine
import json

router = APIRouter()

class WorkflowCreate(BaseModel):
    name: str
    trigger_type: str = "manual"
    schedule: Optional[str] = None
    event_name: Optional[str] = None
    workflow_json: str # JSON string of nodes/edges
    active: bool = True

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    trigger_type: Optional[str] = None
    schedule: Optional[str] = None
    event_name: Optional[str] = None
    workflow_json: Optional[str] = None
    active: Optional[bool] = None

@router.get("/workflows")
async def list_workflows():
    """List all workflows."""
    db = get_db()
    try:
        workflows = db.query(Workflow).all()
        return workflows
    finally:
        db.close()

@router.post("/workflows")
async def create_workflow(workflow: WorkflowCreate):
    """Create a new workflow."""
    db = get_db()
    try:
        new_wf = Workflow(
            name=workflow.name,
            trigger_type=workflow.trigger_type,
            schedule=workflow.schedule,
            event_name=workflow.event_name,
            workflow_json=workflow.workflow_json,
            active=workflow.active
        )
        db.add(new_wf)
        db.commit()
        db.refresh(new_wf)
        
        # Reload engine to pick up new triggers (if we had a scheduler integration)
        workflow_engine.load_workflows()
        
        return new_wf
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/workflows/{workflow_id}")
async def get_workflow(workflow_id: int):
    """Get a specific workflow."""
    db = get_db()
    try:
        wf = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not wf:
            raise HTTPException(status_code=404, detail="Workflow not found")
        return wf
    finally:
        db.close()

@router.delete("/workflows/{workflow_id}")
async def delete_workflow(workflow_id: int):
    """Delete a workflow."""
    db = get_db()
    try:
        wf = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not wf:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        db.delete(wf)
        db.commit()
        workflow_engine.load_workflows()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.put("/workflows/{workflow_id}")
async def update_workflow(workflow_id: int, workflow: WorkflowUpdate):
    """Update a workflow."""
    db = get_db()
    try:
        wf = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not wf:
            raise HTTPException(status_code=404, detail="Workflow not found")
        
        if workflow.name is not None: wf.name = workflow.name
        if workflow.trigger_type is not None: wf.trigger_type = workflow.trigger_type
        if workflow.schedule is not None: wf.schedule = workflow.schedule
        if workflow.event_name is not None: wf.event_name = workflow.event_name
        if workflow.workflow_json is not None: wf.workflow_json = workflow.workflow_json
        if workflow.active is not None: wf.active = workflow.active
        
        db.commit()
        db.refresh(wf)
        workflow_engine.load_workflows()
        return wf
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/workflows/{workflow_id}/run")
async def run_workflow(workflow_id: int):
    """Manually trigger a workflow."""
    # We run this as a background task essentially, but for now we await it 
    # to return immediate feedback in this simple version
    try:
        await workflow_engine.run_workflow(workflow_id)
        
        # update run count
        db = get_db()
        wf = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if wf:
            wf.run_count += 1
            db.commit()
        db.close()
            
        return {"status": "executed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
