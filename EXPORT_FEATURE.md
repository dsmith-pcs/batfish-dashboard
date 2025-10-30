# Network Topology Export Feature

## Overview
The Batfish Dashboard now includes the ability to export network topology graphs to SVG (Scalable Vector Graphics) format. This feature preserves the exact positioning of all nodes, including any manual adjustments you make to the layout.

## Features

### ✅ **Vector Format (SVG)**
- High-quality, scalable graphics
- Can be opened in any modern browser or vector graphics editor
- Maintains quality at any zoom level
- Editable in tools like Inkscape, Adobe Illustrator, or any SVG editor

### ✅ **Preserves Manual Positioning**
- **Drag and arrange nodes** to your preferred layout
- **Export captures the current state** - exactly as you see it
- All node labels, edge labels, and interface names are included
- Network topology structure is preserved

### ✅ **Automatic Timestamping**
- Files are named with timestamps: `network-topology-2025-10-17T18-30-45.svg`
- Prevents accidental overwrites
- Easy to track different versions of your network documentation

## How to Use

### Step 1: Load Your Network
1. Connect to Batfish service
2. Select your network and snapshot
3. Navigate to the **Layer 3**, **OSPF**, or **BGP** tab

### Step 2: Arrange Your Topology (Optional)
- **Click and drag** any node to reposition it
- Arrange nodes to match your physical topology
- Group related devices together
- Create a clear, logical layout

### Step 3: Export
1. Click the **"Export to SVG"** button at the top of the graph
2. The file will automatically download to your default downloads folder
3. Open with any SVG-compatible application

## Supported Graph Types

The export feature works with all network topology visualizations:

- ✅ **Layer 3 Topology** - Physical network connections
- ✅ **OSPF Topology** - OSPF neighbor relationships
- ✅ **BGP Topology** - BGP peering relationships (with AS grouping)

## SVG File Contents

The exported SVG includes:
- **All network nodes** (routers, switches, devices)
- **All connections** (interfaces, links)
- **Interface labels** (source and target interfaces)
- **Node labels** (device names)
- **AS groupings** (for BGP topologies)
- **Current positions** (preserving your manual layout)

## Use Cases

### 📊 **Network Documentation**
- Create professional network diagrams for documentation
- Generate topology diagrams for change requests
- Document network architecture

### 🎨 **Further Editing**
- Import into vector graphics editors
- Add annotations, highlights, or additional information
- Customize colors and styling
- Create presentation-ready diagrams

### 📋 **Compliance and Auditing**
- Export topology snapshots for compliance records
- Document network state at specific points in time
- Create audit trail of network changes

### 👥 **Collaboration**
- Share network topology with team members
- Include in technical documentation
- Attach to incident reports or RFCs

## Technical Details

### File Format
- **Format**: SVG (Scalable Vector Graphics)
- **Standard**: W3C SVG 1.1
- **Compatibility**: All modern browsers, vector editors

### Export Method
- **Client-side export**: Processing happens in your browser
- **No server processing**: Fast and secure
- **Real-time capture**: Exports current viewport state

### Browser Compatibility
- ✅ Chrome/Chromium (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

## Tips and Best Practices

### 🎯 **For Best Results:**
1. **Arrange your topology first** before exporting
2. **Zoom to fit** the entire topology in view
3. **Check labels** are visible and not overlapping
4. **Use consistent naming** for your files

### 🔧 **Troubleshooting:**

**Export button doesn't work?**
- Refresh the page and wait for the graph to fully load
- Make sure you're on a graph tab (Layer 3, OSPF, or BGP)

**File not downloading?**
- Check your browser's download permissions
- Verify downloads folder is accessible
- Try a different browser

**Positions reset after export?**
- This is normal - export doesn't change the graph
- Your manual positions are captured in the export
- Re-arrange if needed and export again

## Example Workflow

```
1. Connect to Batfish
   └─> Enter Batfish host IP
   └─> Select network
   └─> Select snapshot

2. View Topology
   └─> Click "Layer 3" tab
   └─> Wait for graph to render

3. Customize Layout (Optional)
   └─> Drag nodes to desired positions
   └─> Arrange for clarity

4. Export
   └─> Click "Export to SVG"
   └─> File downloads automatically
   └─> Open in SVG viewer or editor

5. Use Exported File
   └─> Include in documentation
   └─> Edit in vector editor
   └─> Share with team
```

## Future Enhancements

Potential future additions:
- PNG/PDF export options
- Custom styling before export
- Batch export of multiple topologies
- Export with embedded metadata

## Support

For issues or feature requests related to the export functionality, please refer to the main project documentation or submit an issue on the project repository.

---

**Happy network diagramming!** 🚀