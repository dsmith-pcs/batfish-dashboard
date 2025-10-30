// Store cytoscape instance globally for SVG export
window.addEventListener('load', function() {
    // Wait for cytoscape to be initialized
    setTimeout(function() {
        var el = document.getElementById("cytoscape");
        if (el && el._cyreg && el._cyreg.cy) {
            window.cy = el._cyreg.cy;
            console.log("Cytoscape instance stored globally for export functionality");

            // Add SVG export extension to cytoscape
            if (window.cy && !window.cy.svg) {
                // Simple SVG export function if library not available
                window.cy.svg = function(options) {
                    var cy = this;
                    var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + cy.width() + '" height="' + cy.height() + '">';

                    // Add nodes
                    cy.nodes().forEach(function(node) {
                        var pos = node.position();
                        var label = node.data('label') || node.data('id');
                        var width = node.style('width');
                        var height = node.style('height');

                        // Draw node as circle/rectangle
                        svg += '<g transform="translate(' + pos.x + ',' + pos.y + ')">';
                        svg += '<circle r="' + (width/2) + '" fill="#f0f0f0" stroke="#333" stroke-width="2"/>';
                        svg += '<text text-anchor="middle" dy=".3em" font-size="12" font-weight="bold">' + label + '</text>';
                        svg += '</g>';
                    });

                    // Add edges
                    cy.edges().forEach(function(edge) {
                        var source = edge.source().position();
                        var target = edge.target().position();
                        var sourceLabel = edge.data('source_label') || '';
                        var targetLabel = edge.data('target_label') || '';

                        svg += '<line x1="' + source.x + '" y1="' + source.y + '" x2="' + target.x + '" y2="' + target.y + '" stroke="#333" stroke-width="2"/>';

                        // Add labels if present
                        if (sourceLabel) {
                            var midX1 = source.x + (target.x - source.x) * 0.25;
                            var midY1 = source.y + (target.y - source.y) * 0.25;
                            svg += '<text x="' + midX1 + '" y="' + midY1 + '" font-size="10" fill="#000">' + sourceLabel + '</text>';
                        }
                        if (targetLabel) {
                            var midX2 = source.x + (target.x - source.x) * 0.75;
                            var midY2 = source.y + (target.y - source.y) * 0.75;
                            svg += '<text x="' + midX2 + '" y="' + midY2 + '" font-size="10" fill="#000">' + targetLabel + '</text>';
                        }
                    });

                    svg += '</svg>';
                    return svg;
                };
            }
        }
    }, 1000);
});
