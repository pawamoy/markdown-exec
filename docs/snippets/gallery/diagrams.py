from base64 import b64encode
from contextlib import suppress

from diagrams import Diagram
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service

# By default, Diagrams tries to write the result on disk, so we prevent that by patching its `render` method,
# and by ignoring the `FileNotFoundError` that ensues.
#
# Then we use its internal `dot` object and its `pipe` method to store the diagram in a variable,
# as base64 encoded PNG data.
#
# Finally we output an HTML image with the base64 data.
# Using SVG is not possible here since Diagrams embeds actual, smaller PNG files in the result,
# files which are not automatically added to the final site.
with suppress(FileNotFoundError):
    with Diagram("Exposed Pod with 3 Replicas", show=False) as diagram:
        diagram.render = lambda: None
        net = Ingress("domain.com") >> Service("svc")
        net >> [Pod("pod1"), Pod("pod2"), Pod("pod3")] << ReplicaSet("rs") << Deployment("dp") << HPA("hpa")
        png = b64encode(diagram.dot.pipe(format="png")).decode()

# Wrapping the image in a div prevents it from being wrapped in a paragraph,
# which would add unnecessary space around it.
print(f'<div><img src="data:image/png;base64, {png}"/></div>')
