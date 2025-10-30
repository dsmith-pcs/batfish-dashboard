// SVG Export functionality for Cytoscape
// This function generates SVG from the current graph state, preserving all node positions

function generateCytoscapeSVG(cy) {
    if (!cy) {
        console.error('Cytoscape instance not provided');
        return null;
    }

    // Get the bounding box to center the SVG properly
    var bb = cy.elements().boundingBox();
    var width = bb.w + 200;  // Add padding
    var height = bb.h + 200;
    var offsetX = -bb.x1 + 100;
    var offsetY = -bb.y1 + 100;

    // Start SVG with proper namespace and viewBox
    var svg = '<?xml version="1.0" encoding="UTF-8"?>\n';
    svg += '<svg xmlns="http://www.w3.org/2000/svg" ';
    svg += 'width="' + width + '" height="' + height + '" ';
    svg += 'viewBox="0 0 ' + width + ' ' + height + '">\n';

    // Add background
    svg += '<rect width="100%" height="100%" fill="white"/>\n';

    // Create group for graph elements
    svg += '<g id="graph">\n';

    // Draw edges first (so they appear behind nodes)
    cy.edges().forEach(function(edge) {
        var source = edge.source().position();
        var target = edge.target().position();
        var sourceLabel = edge.data('source_label') || '';
        var targetLabel = edge.data('target_label') || '';

        // Draw edge line
        svg += '<line ';
        svg += 'x1="' + (source.x + offsetX) + '" ';
        svg += 'y1="' + (source.y + offsetY) + '" ';
        svg += 'x2="' + (target.x + offsetX) + '" ';
        svg += 'y2="' + (target.y + offsetY) + '" ';
        svg += 'stroke="#666" stroke-width="2" />\n';

        // Add source label if present
        if (sourceLabel) {
            var midX1 = source.x + (target.x - source.x) * 0.25 + offsetX;
            var midY1 = source.y + (target.y - source.y) * 0.25 + offsetY;
            svg += '<text x="' + midX1 + '" y="' + midY1 + '" ';
            svg += 'font-size="10" fill="#000" ';
            svg += 'text-anchor="middle" ';
            svg += 'style="background: white; padding: 2px;">';
            svg += sourceLabel + '</text>\n';
        }

        // Add target label if present
        if (targetLabel) {
            var midX2 = source.x + (target.x - source.x) * 0.75 + offsetX;
            var midY2 = source.y + (target.y - source.y) * 0.75 + offsetY;
            svg += '<text x="' + midX2 + '" y="' + midY2 + '" ';
            svg += 'font-size="10" fill="#000" ';
            svg += 'text-anchor="middle" ';
            svg += 'style="background: white; padding: 2px;">';
            svg += targetLabel + '</text>\n';
        }
    });

    // Draw nodes
    cy.nodes().forEach(function(node) {
        var pos = node.position();
        var label = node.data('label') || node.data('id');
        var width = parseFloat(node.style('width')) || 100;
        var height = parseFloat(node.style('height')) || 100;
        var x = pos.x + offsetX;
        var y = pos.y + offsetY;

        // Check if this is a parent node (AS group)
        var isParent = node.hasClass('parent');

        svg += '<g transform="translate(' + x + ',' + y + ')">\n';

        if (isParent) {
            // Draw AS group as rectangle
            svg += '<rect ';
            svg += 'x="' + (-width/2) + '" y="' + (-height/2) + '" ';
            svg += 'width="' + width + '" height="' + height + '" ';
            svg += 'fill="ghostwhite" stroke="#555" stroke-width="2" />\n';
        } else {
            // Draw regular node as circle
            svg += '<circle r="' + (width/2) + '" ';
            svg += 'fill="#f0f0f0" stroke="#333" stroke-width="2" />\n';
        }

        // Add node label with background
        svg += '<text text-anchor="middle" dy=".3em" ';
        svg += 'font-size="12" font-weight="bold" fill="#000">';
        svg += label + '</text>\n';

        svg += '</g>\n';
    });

    svg += '</g>\n';
    svg += '</svg>';

    return svg;
}

// Initialize and store cytoscape instance globally
window.addEventListener('load', function() {
    console.log('Initializing Cytoscape SVG export functionality...');

    // Function to find and store cytoscape instance
    function findCytoscapeInstance() {
        var el = document.getElementById("cytoscape");
        if (el && el._cyreg && el._cyreg.cy) {
            window.cy = el._cyreg.cy;
            console.log('✓ Cytoscape instance found and stored globally');
            return true;
        }
        return false;
    }

    // Try immediately
    if (!findCytoscapeInstance()) {
        // Try again after delays
        setTimeout(findCytoscapeInstance, 500);
        setTimeout(findCytoscapeInstance, 1000);
        setTimeout(findCytoscapeInstance, 2000);
    }
});

// Also try to find instance when tab changes
if (typeof MutationObserver !== 'undefined') {
    var observer = new MutationObserver(function(mutations) {
        if (!window.cy) {
            var el = document.getElementById("cytoscape");
            if (el && el._cyreg && el._cyreg.cy) {
                window.cy = el._cyreg.cy;
                console.log('✓ Cytoscape instance found via mutation observer');
            }
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}
