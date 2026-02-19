# Eonix User Guide

## Installation

1.  **Prerequisites**:
    -   Install [Python 3.10+](https://www.python.org/)
    -   Install [Node.js 16+](https://nodejs.org/)
    -   Install [Ollama](https://ollama.com/)

2.  **Setup**:
    Double-click `scripts\install.bat`.
    This will set up the Python environment and install Node modules.

3.  **AI Models**:
    Pull the required models in Ollama:
    ```cmd
    ollama pull llama3
    ollama pull mistral
    ```

## Running Eonix

Double-click `run_eonix.bat`.

This launches:
1.  **Backend Console**: Shows server logs and AI thinking.
2.  **Frontend Window**: The JARVIS interface.

## Features

### Chat & Commands
-   **General**: "How are you?", "Explain quantum physics."
-   **System**: "What is my CPU usage?", "List running processes."
-   **Apps**: "Open Chrome", "Close Spotify".
-   **Files**: "List files in Downloads", "Search for 'resume.pdf'".

### Dashboard
Click the 📊 icon to view:
-   Real-time graphs for CPU, RAM, Disk.
-   List of active processes (coming soon).

### Settings
Configure your preferred Voice (TTS) and AI model in the Settings panel.
