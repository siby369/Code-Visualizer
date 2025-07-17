import React, { useState, useRef, useEffect } from "react";
import MonacoEditor from "@monaco-editor/react";
import "./App.css";

function App() {
  const [code, setCode] = useState("# Write your Python code here\nprint('Hello, World!')");
  const [loading, setLoading] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1000);
  const [zoom, setZoom] = useState(1);
  const [highlightedLine, setHighlightedLine] = useState(2); // Default to line 2
  const editorRef = useRef(null);

  // Update highlightedLine when cursor position changes
  useEffect(() => {
    if (!editorRef.current) return;
    const editor = editorRef.current;
    const onCursorChange = () => {
      const pos = editor.getPosition();
      if (pos && pos.lineNumber !== highlightedLine) {
        setHighlightedLine(pos.lineNumber);
      }
    };
    editor.onDidChangeCursorPosition(onCursorChange);
    return () => {
      // No need to clean up in Monaco, but could add a dispose if needed
    };
  }, [highlightedLine]);

  useEffect(() => {
    const editor = editorRef.current;
    if (!editor) return;
    const model = editor.getModel && editor.getModel();
    if (!model) return;
    if (editor._currentDecorations) {
      editor.deltaDecorations(editor._currentDecorations, []);
    }
    const lineToHighlight = highlightedLine;
    const lineLength = model.getLineLength(lineToHighlight);
    const monaco = window.monaco || (window.require && window.require('monaco-editor'));
    if (!monaco || !monaco.Range) return;
    const decorations = editor.deltaDecorations(
      [],
      [
        {
          range: new monaco.Range(lineToHighlight, 1, lineToHighlight, lineLength + 1),
          options: {
            className: "monaco-execution-highlight"
          }
        }
      ]
    );
    editor._currentDecorations = decorations;
  }, [highlightedLine, zoom]);

  // Suppress ResizeObserver warning in development
  if (process.env.NODE_ENV === 'development') {
    const ignoreResizeObserverError = (err) => {
      if (
        err.message &&
        err.message.includes('ResizeObserver loop completed with undelivered notifications')
      ) {
        return;
      }
      throw err;
    };
    window.addEventListener('error', ignoreResizeObserverError);
  }

  // --- UI ---
  return (
    <div className="app">
      {/* Header */}
      {/* Main Split Area */}
      {/* Removed main-area and its contents */}
    </div>
  );
}

export default App;