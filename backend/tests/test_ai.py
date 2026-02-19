from ai.intent_classifier import IntentClassifier
from ai.task_planner import TaskPlanner

def test_intent_classification(mocker):
    # Mock Ollama response
    mock_ollama = mocker.patch('ai.intent_classifier.OllamaClient.generate')
    mock_ollama.return_value = '{"intent": "app_control", "confidence": 0.95}'
    
    classifier = IntentClassifier()
    result = classifier.classify("Open Chrome")
    
    assert result["intent"] == "app_control"
    assert result["confidence"] > 0.9

def test_task_planning(mocker):
    # Mock Ollama response
    mock_ollama = mocker.patch('ai.task_planner.OllamaClient.generate')
    mock_ollama.return_value = '{"tasks": [{"action": "list_files", "params": {"path": "."}}]}'
    
    planner = TaskPlanner()
    plan = planner.plan_tasks("List all files here")
    
    assert len(plan) == 1
    assert plan[0]["action"] == "list_files"
