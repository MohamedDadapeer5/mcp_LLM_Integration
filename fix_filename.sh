#!/bin/bash
# Fix Healthcare Knowledge Base Filename
# Run this in HAWCC if you have healthcare.kb.yaml instead of healthcare-kb.yaml

echo "Checking for incorrectly named file..."

if [ -f "knowledge/healthcare.kb.yaml" ]; then
    echo "Found: knowledge/healthcare.kb.yaml (INCORRECT - has dot instead of dash)"
    echo "Renaming to: knowledge/healthcare-kb.yaml"
    mv knowledge/healthcare.kb.yaml knowledge/healthcare-kb.yaml
    echo "✅ Fixed!"
else
    echo "File not found: knowledge/healthcare.kb.yaml"
fi

if [ -f "knowledge/healthcare-kb.yaml" ]; then
    echo "✅ Correct file exists: knowledge/healthcare-kb.yaml"
else
    echo "❌ Missing: knowledge/healthcare-kb.yaml"
    echo "Please ensure this file exists"
fi

echo ""
echo "Listing all knowledge base files:"
ls -la knowledge/
