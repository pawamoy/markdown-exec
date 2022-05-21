from base64 import b64encode
from contextlib import suppress

from diagrams import Diagram
from diagrams.k8s.clusterconfig import HPA
from diagrams.k8s.compute import Deployment, Pod, ReplicaSet
from diagrams.k8s.network import Ingress, Service

with suppress(FileNotFoundError):
    with Diagram("Exposed Pod with 3 Replicas", show=False) as diagram:
        diagram.render = lambda: None
        net = Ingress("domain.com") >> Service("svc")
        net >> [Pod("pod1"), Pod("pod2"), Pod("pod3")] << ReplicaSet("rs") << Deployment("dp") << HPA("hpa")
        png = b64encode(diagram.dot.pipe(format="png")).decode()

print(f'<img src="data:image/png;base64, {png}"/>')
