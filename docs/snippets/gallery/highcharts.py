import json

options = {
    "chart": {"type": "column"},
    "title": {"text": "Example bar chart"},
    "xAxis": {"categories": ["a", "b", "c"]},
    "yAxis": {"title": {"text": "Value"}},
    "series": [{"name": "Values", "data": [1, 3, 2]}],
}

print(f"""
<div id="highcharts-chart" style="width: 100%; height: 300px;"></div>
<script src="https://cdn.jsdelivr.net/npm/highcharts@12/highcharts.js"></script>
<script>
Highcharts.chart('highcharts-chart', {json.dumps(options)});
</script>
""")
