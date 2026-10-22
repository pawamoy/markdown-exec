import json

spec = {
    "$schema": "https://vega.github.io/schema/vega/v6.json",
    "width": 400,
    "height": 200,
    "padding": 5,
    "data": [{"name": "table", "values": [
        {"category": "a", "amount": 1},
        {"category": "b", "amount": 3},
        {"category": "c", "amount": 2},
    ]}],
    "scales": [
        {
            "name": "x",
            "type": "band",
            "domain": {"data": "table", "field": "category"},
            "range": "width",
            "padding": 0.1,
        },
        {
            "name": "y",
            "domain": {"data": "table", "field": "amount"},
            "range": "height",
            "nice": True,
            "zero": True,
        },
    ],
    "axes": [
        {"orient": "bottom", "scale": "x"},
        {"orient": "left", "scale": "y", "tickMinStep": 1},
    ],
    "marks": [{
        "type": "rect",
        "from": {"data": "table"},
        "encode": {
            "enter": {
                "x": {"scale": "x", "field": "category"},
                "width": {"scale": "x", "band": 1},
                "y": {"scale": "y", "field": "amount"},
                "y2": {"scale": "y", "value": 0},
            },
            "update": {"fill": {"value": "steelblue"}},
            "hover": {"fill": {"value": "orange"}},
        },
    }],
}

print(f"""
<div id="vega-chart"></div>
<script src="https://cdn.jsdelivr.net/npm/vega@6"></script>
<script>
new vega.View(vega.parse({json.dumps(spec)}), {{
    renderer: 'svg',
    container: '#vega-chart',
    hover: true
}}).runAsync();
</script>
""")
