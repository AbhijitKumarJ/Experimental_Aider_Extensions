(function() {
    // Get context data from hidden script tag
    const contextData = JSON.parse(document.getElementById('context-data').textContent);
    
    // Add selection functions to window scope
    window.selectAll = function() {
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = true;
        });
    };

    window.deselectAll = function() {
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            checkbox.checked = false;
        });
    };

    window.exportSelected = function() {
        const exportData = {
            timestamp: contextData.timestamp,
            model: contextData.model_info.name,
            files: [],
            messages: []
        };
        
        // Get selected files (only paths)
        contextData.files.forEach((file, index) => {
            if (document.getElementById(`file_${index+1}_check`).checked) {
                exportData.files.push(file.name);
            }
        });
        
        // Get selected messages
        contextData.messages.forEach((msg, index) => {
            if (document.getElementById(`message_${index+1}_check`).checked) {
                exportData.messages.push({
                    role: msg.role,
                    content: msg.content
                });
            }
        });
        
        // Download as JSON file
        const blob = new Blob([JSON.stringify(exportData, null, 2)], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `aider_context_${exportData.timestamp.replace(/[: ]/g, '_')}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    };
})();